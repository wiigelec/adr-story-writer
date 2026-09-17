#!/usr/bin/env python3
from __future__ import annotations

import argparse
import copy
import json
import os
import tempfile
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CONTRACT = ROOT / "ruleset" / "compatibility.json"


class CompatibilityError(ValueError):
    pass


class TransitionError(CompatibilityError):
    pass


def load_contract(path: Path = DEFAULT_CONTRACT) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise CompatibilityError("compatibility contract root must be an object")
    return data


def _get_path(data: dict[str, Any], dotted: str) -> Any:
    current: Any = data
    for part in dotted.split("."):
        if not isinstance(current, dict) or part not in current:
            return None
        current = current[part]
    return current


def _legacy_matches(dataset: dict[str, Any], transition: dict[str, Any]) -> bool:
    source = transition["source"]

    exact_top_level = source.get("exact_top_level")
    if not isinstance(exact_top_level, list) or set(dataset) != set(exact_top_level):
        return False

    for path, expected in source.get("required_literals", {}).items():
        if _get_path(dataset, path) != expected:
            return False

    for path, required_keys in source.get("required_object_keys", {}).items():
        value = _get_path(dataset, path)
        if not isinstance(value, dict) or set(value) != set(required_keys):
            return False

    for path in source.get("required_array_fields", []):
        if not isinstance(_get_path(dataset, path), list):
            return False

    return True


def _legacy_shaped(dataset: dict[str, Any]) -> bool:
    if "schema" in dataset or "ruleset_binding" in dataset:
        return False
    historical = {"instance", "story", "canon", "plot", "prose", "chapters"}
    return bool(historical & set(dataset))


def _binding_key(binding: Any) -> tuple[Any, Any, Any] | None:
    if not isinstance(binding, dict):
        return None
    return (
        binding.get("application"),
        binding.get("component"),
        binding.get("version"),
    )


def _schema_key(schema: Any) -> tuple[Any, Any] | None:
    if not isinstance(schema, dict):
        return None
    return (schema.get("id"), schema.get("version"))


def classify(
    dataset: dict[str, Any],
    requested_operation: str = "ordinary",
    contract: dict[str, Any] | None = None,
) -> dict[str, Any]:
    contract = contract or load_contract()
    schema = dataset.get("schema")
    binding = dataset.get("ruleset_binding")
    current_schema = contract["dataset_schema"]["current"]
    current_binding = contract["ruleset_binding"]["current"]

    result: dict[str, Any]

    if _schema_key(schema) == _schema_key(current_schema):
        if _binding_key(binding) == _binding_key(current_binding):
            result = {"state": "directly_compatible", "permitted": [requested_operation]}
        else:
            supported_rebind = None
            for transition in contract["rebinding"].get("supported_transitions", []):
                if (
                    _schema_key(schema) == _schema_key(transition.get("schema"))
                    and _binding_key(binding) == _binding_key(transition.get("source"))
                    and _binding_key(current_binding) == _binding_key(transition.get("target"))
                ):
                    supported_rebind = transition
                    break
            if supported_rebind:
                result = {
                    "state": "rebinding_required",
                    "transition": supported_rebind["id"],
                    "permitted": ["rebind", "inspect", "export", "diagnose"],
                }
            else:
                result = {
                    "state": "indeterminate",
                    "reason": "ruleset binding is absent or not explicitly compatible",
                    "permitted": ["inspect", "export", "diagnose"],
                }
    elif schema is None and binding is None:
        supported_migration = None
        for transition in contract["migration"].get("supported_transitions", []):
            if _legacy_matches(dataset, transition):
                supported_migration = transition
                break
        if supported_migration:
            result = {
                "state": "migration_required",
                "transition": supported_migration["id"],
                "permitted": ["migrate", "inspect", "export", "diagnose"],
            }
        else:
            ambiguous = contract["migration"].get("ambiguous_source_behavior", {})
            result = {
                "state": "indeterminate",
                "reason": "unversioned Dataset cannot be identified as the exact supported legacy realization",
                "permitted": ["inspect", "export", "diagnose"],
                "semantic_author_decision_required": bool(
                    ambiguous.get("semantic_author_decision_required")
                ) if _legacy_shaped(dataset) else False,
                "unresolved_decisions": (
                    [ambiguous.get("unresolved_decision")]
                    if _legacy_shaped(dataset) and ambiguous.get("unresolved_decision")
                    else []
                ),
            }
    else:
        result = {
            "state": "unsupported",
            "reason": "Dataset schema realization is not explicitly supported",
            "permitted": ["inspect", "export", "diagnose"],
        }

    restricted = set(contract["compatibility"].get("restricted_operations", []))
    if requested_operation in restricted and result["state"] in {"unsupported", "indeterminate"}:
        return {
            "state": "restricted_operation",
            "underlying_state": result["state"],
            "reason": result.get("reason"),
            "permitted": sorted(restricted),
        }
    return result


def _append_provenance(
    dataset: dict[str, Any],
    *,
    operation: str,
    source_realization: dict[str, Any],
    target_realization: dict[str, Any],
    semantic_author_decision_required: bool,
    unresolved: list[Any] | None = None,
) -> None:
    history = dataset.setdefault("compatibility_history", [])
    if not isinstance(history, list):
        raise TransitionError("compatibility_history must be a list")
    history.append(
        {
            "source_realization": source_realization,
            "target_realization": target_realization,
            "operation": operation,
            "unresolved_decisions_or_losses": unresolved or [],
            "semantic_author_decision_required": semantic_author_decision_required,
        }
    )


def migrate(
    dataset: dict[str, Any],
    transition_id: str,
    *,
    authorized: bool,
    contract: dict[str, Any] | None = None,
) -> dict[str, Any]:
    if not authorized:
        raise TransitionError("migration requires explicit authorization")
    contract = contract or load_contract()
    transition = next(
        (t for t in contract["migration"].get("supported_transitions", []) if t.get("id") == transition_id),
        None,
    )
    if transition is None:
        raise TransitionError(f"unsupported migration transition: {transition_id}")
    status = classify(dataset, contract=contract)
    if status.get("state") != "migration_required" or status.get("transition") != transition_id:
        raise TransitionError("Dataset does not match the requested supported migration")

    migrated = copy.deepcopy(dataset)
    migrated["schema"] = copy.deepcopy(transition["target"]["schema"])
    migrated["ruleset_binding"] = copy.deepcopy(transition["target"]["ruleset_binding"])
    _append_provenance(
        migrated,
        operation=f"migration:{transition_id}",
        source_realization={"schema": "legacy_unversioned_v0", "ruleset_binding": "absent"},
        target_realization=copy.deepcopy(transition["target"]),
        semantic_author_decision_required=bool(transition.get("semantic_author_decision_required")),
    )
    return migrated


def rebind(
    dataset: dict[str, Any],
    transition_id: str,
    *,
    authorized: bool,
    contract: dict[str, Any] | None = None,
) -> dict[str, Any]:
    if not authorized:
        raise TransitionError("rebinding requires explicit authorization")
    contract = contract or load_contract()
    transition = next(
        (t for t in contract["rebinding"].get("supported_transitions", []) if t.get("id") == transition_id),
        None,
    )
    if transition is None:
        raise TransitionError(f"unsupported rebinding transition: {transition_id}")
    status = classify(dataset, contract=contract)
    if status.get("state") != "rebinding_required" or status.get("transition") != transition_id:
        raise TransitionError("Dataset does not match the requested supported rebinding")

    rebound = copy.deepcopy(dataset)
    old_binding = copy.deepcopy(rebound.get("ruleset_binding"))
    rebound["ruleset_binding"] = copy.deepcopy(transition["target"])
    _append_provenance(
        rebound,
        operation=f"rebinding:{transition_id}",
        source_realization={"schema": copy.deepcopy(rebound.get("schema")), "ruleset_binding": old_binding},
        target_realization={"schema": copy.deepcopy(rebound.get("schema")), "ruleset_binding": copy.deepcopy(transition["target"])},
        semantic_author_decision_required=bool(transition.get("semantic_revision_required")),
    )
    return rebound


def atomic_save(path: Path, dataset: dict[str, Any]) -> None:
    path = path.resolve()
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(prefix=path.name + ".", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(dataset, handle, indent=2)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp_name, path)
    except Exception:
        try:
            os.unlink(tmp_name)
        except FileNotFoundError:
            pass
        raise


def load_dataset(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise CompatibilityError("Dataset root must be an object")
    return data


def load_and_classify(path: Path, requested_operation: str = "ordinary") -> tuple[dict[str, Any], dict[str, Any]]:
    dataset = load_dataset(path)
    return dataset, classify(dataset, requested_operation=requested_operation)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=["status", "migrate", "rebind"])
    parser.add_argument("dataset")
    parser.add_argument("--operation", default="ordinary")
    parser.add_argument("--transition")
    parser.add_argument("--authorize", action="store_true")
    parser.add_argument("--output")
    args = parser.parse_args(argv)

    source = Path(args.dataset)
    dataset = load_dataset(source)

    if args.action == "status":
        print(json.dumps(classify(dataset, requested_operation=args.operation), indent=2))
        return 0

    if not args.transition:
        raise SystemExit("--transition is required")
    if not args.output:
        raise SystemExit("--output is required for mutating transitions")

    if args.action == "migrate":
        result = migrate(dataset, args.transition, authorized=args.authorize)
    else:
        result = rebind(dataset, args.transition, authorized=args.authorize)

    atomic_save(Path(args.output), result)
    print(json.dumps(classify(result, requested_operation=args.operation), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
