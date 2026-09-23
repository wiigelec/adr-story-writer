#!/usr/bin/env python3
from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
from pathlib import Path
from typing import Any


class RevisionRuntimeError(ValueError):
    pass


def _load_scene_runtime():
    path = Path(__file__).resolve().with_name("scene_runtime.py")
    spec = importlib.util.spec_from_file_location("story_writer_scene_runtime_fs004", path)
    if spec is None or spec.loader is None:
        raise RevisionRuntimeError("cannot load scene runtime")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


SCENE = _load_scene_runtime()


def _canonical(value: Any) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")


def _stable_id(prefix: str, value: Any) -> str:
    return f"{prefix}-{hashlib.sha256(_canonical(value)).hexdigest()[:20]}"


def _location(dataset: dict[str, Any], artifact_id: str):
    canon = dataset.get("canon", {})
    for collection in ("character", "setting"):
        value = canon.get(collection, {})
        if isinstance(value, dict):
            for key, artifact in value.items():
                if isinstance(artifact, dict) and artifact.get("id") == artifact_id:
                    return value, key
    events = canon.get("events", [])
    if isinstance(events, list):
        for index, artifact in enumerate(events):
            if isinstance(artifact, dict) and artifact.get("id") == artifact_id:
                return events, index

    plot = dataset.get("plot", {})
    synopsis = plot.get("synopsis")
    if isinstance(synopsis, dict) and synopsis.get("id") == artifact_id:
        return plot, "synopsis"
    for collection in ("outline", "sequence"):
        value = plot.get(collection, [])
        if isinstance(value, list):
            for index, artifact in enumerate(value):
                if isinstance(artifact, dict) and artifact.get("id") == artifact_id:
                    return value, index

    prose = dataset.get("prose", {})
    for collection in ("beats", "modes", "pseudo_prose"):
        value = prose.get(collection, {})
        if isinstance(value, dict):
            for key, artifact in value.items():
                if isinstance(artifact, dict) and artifact.get("id") == artifact_id:
                    return value, key

    files = dataset.get("chapters", {}).get("files", [])
    if isinstance(files, list):
        for index, artifact in enumerate(files):
            if isinstance(artifact, dict) and artifact.get("id") == artifact_id:
                return files, index

    raise RevisionRuntimeError(f"unknown governed artifact: {artifact_id}")


def _artifact(dataset: dict[str, Any], artifact_id: str) -> dict[str, Any]:
    container, key = _location(dataset, artifact_id)
    artifact = container[key]
    if not isinstance(artifact, dict):
        raise RevisionRuntimeError(f"invalid governed artifact: {artifact_id}")
    return artifact


def _surface_owner(artifact: dict[str, Any]) -> str:
    surface = artifact.get("surface")
    if not isinstance(surface, str) or not surface:
        raise RevisionRuntimeError("governed artifact has no surface")
    return surface.split(".", 1)[0]


def _history_snapshot(artifact: dict[str, Any]) -> dict[str, Any]:
    value = copy.deepcopy(artifact)
    value.pop("revision_candidates", None)
    value.pop("revision_history", None)
    value.pop("reconciliation", None)
    value.pop("reconciliation_history", None)
    return value


def _relations(artifact: dict[str, Any]) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    explicit_targets: set[str] = set()
    explicit = artifact.get("dependency_relations")
    if isinstance(explicit, list):
        for relation in explicit:
            if not isinstance(relation, dict):
                continue
            target_id = relation.get("target_id")
            if not isinstance(target_id, str) or not target_id:
                continue
            result.append(copy.deepcopy(relation))
            explicit_targets.add(target_id)

    dependencies = artifact.get("dependencies", [])
    if isinstance(dependencies, list):
        for target in dependencies:
            if (
                isinstance(target, str)
                and target
                and target not in explicit_targets
            ):
                result.append({
                    "target_id": target,
                    "authority_basis": "accepted",
                    "material": True,
                })
    return result

def _matching_relation(
    artifact: dict[str, Any],
    target_id: str,
    target_revision: str | None,
) -> dict[str, Any] | None:
    for relation in _relations(artifact):
        if relation.get("target_id") != target_id:
            continue
        revision = relation.get("target_revision")
        if revision is None or target_revision is None or revision == target_revision:
            return relation
        return None
    return None

def _ensure_explicit_relation(
    artifact: dict[str, Any],
    target_id: str,
    *,
    material: bool,
) -> dict[str, Any]:
    relations = artifact.setdefault("dependency_relations", [])
    if not isinstance(relations, list):
        raise RevisionRuntimeError("dependency_relations must be an array")
    for relation in relations:
        if isinstance(relation, dict) and relation.get("target_id") == target_id:
            relation.setdefault("material", material)
            return relation
    relation = {
        "target_id": target_id,
        "authority_basis": "accepted",
        "material": material,
    }
    relations.append(relation)
    return relation


def _blocked(artifact: dict[str, Any]) -> bool:
    reconciliation = artifact.get("reconciliation")
    return (
        isinstance(reconciliation, dict)
        and reconciliation.get("state")
        in {"review_required", "stale", "unresolved", "superseded"}
    )


def _normalize_candidate_dependencies(
    material_dependencies: list[dict[str, Any]] | None,
) -> list[dict[str, Any]]:
    if material_dependencies is None:
        return []
    if not isinstance(material_dependencies, list):
        raise RevisionRuntimeError("material_dependencies must be an array")
    normalized: list[dict[str, Any]] = []
    for relation in material_dependencies:
        if not isinstance(relation, dict):
            raise RevisionRuntimeError("candidate dependency must be an object")
        target_id = relation.get("target_id")
        if not isinstance(target_id, str) or not target_id:
            raise RevisionRuntimeError("candidate dependency requires target_id")
        value = copy.deepcopy(relation)
        value["material"] = True
        value.setdefault("authority_basis", "accepted")
        normalized.append(value)
    return normalized


def _promote_candidate_material_dependencies(
    artifact: dict[str, Any],
    candidate: dict[str, Any],
) -> None:
    declared = candidate.get("material_dependencies", [])
    if not isinstance(declared, list):
        raise RevisionRuntimeError("candidate material_dependencies must be an array")
    if not declared:
        return

    relations = artifact.setdefault("dependency_relations", [])
    if not isinstance(relations, list):
        raise RevisionRuntimeError("dependency_relations must be an array")

    for declared_relation in declared:
        if not isinstance(declared_relation, dict):
            raise RevisionRuntimeError("candidate dependency must be an object")
        target_id = declared_relation.get("target_id")
        if not isinstance(target_id, str) or not target_id:
            raise RevisionRuntimeError("candidate dependency requires target_id")

        promoted = copy.deepcopy(declared_relation)
        promoted["material"] = True
        promoted["authority_basis"] = "accepted"

        matches = [
            index
            for index, relation in enumerate(relations)
            if isinstance(relation, dict) and relation.get("target_id") == target_id
        ]
        if matches:
            relations[matches[0]] = promoted
            for index in reversed(matches[1:]):
                del relations[index]
        else:
            relations.append(promoted)


def _normalize_candidate_assumptions(
    assumptions: list[str] | None,
) -> list[str]:
    if assumptions is None:
        return []
    if not isinstance(assumptions, list) or any(
        not isinstance(item, str) or not item for item in assumptions
    ):
        raise RevisionRuntimeError(
            "candidate assumptions must be an array of non-empty strings"
        )
    return list(assumptions)


def propose_revision(
    dataset: dict[str, Any],
    target_id: str,
    proposed_changes: dict[str, Any],
    *,
    identity_operation: str = "revision",
    replacement_id: str | None = None,
    material_dependencies: list[dict[str, Any]] | None = None,
    assumptions: list[str] | None = None,
) -> dict[str, Any]:
    target = _artifact(dataset, target_id)
    owner = _surface_owner(target)
    if owner not in {"canon", "plot"}:
        raise RevisionRuntimeError("upstream semantic revision target must be Canon or Plot")
    if target.get("authority_class") != "accepted_semantic":
        raise RevisionRuntimeError("upstream revision requires accepted semantic target")
    if identity_operation not in {"revision", "replacement", "unresolved"}:
        raise RevisionRuntimeError("unsupported identity operation")
    if not isinstance(proposed_changes, dict) or not proposed_changes:
        raise RevisionRuntimeError("revision requires proposed semantic changes")
    protected = {"id", "surface", "authority_class", "revision"}
    if protected & set(proposed_changes):
        raise RevisionRuntimeError("proposed changes cannot replace governed identity fields")
    if identity_operation == "replacement" and not replacement_id:
        raise RevisionRuntimeError("replacement requires replacement_id")

    base_revision = target.get("revision")
    if not isinstance(base_revision, str) or not base_revision:
        raise RevisionRuntimeError("target has no durable revision")
    candidate_dependencies = _normalize_candidate_dependencies(material_dependencies)
    candidate_assumptions = _normalize_candidate_assumptions(assumptions)
    seed = {
        "target_id": target_id,
        "base_revision": base_revision,
        "proposed_changes": proposed_changes,
        "identity_operation": identity_operation,
        "replacement_id": replacement_id,
        "material_dependencies": candidate_dependencies,
        "assumptions": candidate_assumptions,
    }
    candidate = {
        "id": _stable_id("semantic-revision-candidate", seed),
        "surface": target["surface"],
        "authority_class": "candidate_semantic",
        "revision": _stable_id("semantic-candidate-revision", seed),
        "target_id": target_id,
        "base_revision": base_revision,
        "proposed_changes": copy.deepcopy(proposed_changes),
        "identity_operation": identity_operation,
        "replacement_id": replacement_id,
        "material_dependencies": candidate_dependencies,
        "assumptions": candidate_assumptions,
        "status": "candidate",
    }
    candidates = target.setdefault("revision_candidates", [])
    if not isinstance(candidates, list):
        raise RevisionRuntimeError("revision_candidates must be an array")
    candidates.append(copy.deepcopy(candidate))
    return candidate


def _candidate_for(dataset: dict[str, Any], candidate_id: str):
    for artifact in SCENE._iter_artifacts(dataset):
        candidates = artifact.get("revision_candidates", [])
        if not isinstance(candidates, list):
            continue
        for candidate in candidates:
            if isinstance(candidate, dict) and candidate.get("id") == candidate_id:
                return artifact, candidate
    raise RevisionRuntimeError(f"unknown revision candidate: {candidate_id}")


def inspect_revision_candidate(
    dataset: dict[str, Any],
    candidate_id: str,
) -> dict[str, Any]:
    target, candidate = _candidate_for(dataset, candidate_id)
    result = copy.deepcopy(candidate)
    result["target_current_revision"] = target.get("revision")
    result["target_authority_class"] = target.get("authority_class")
    return result


def reject_revision(
    dataset: dict[str, Any],
    candidate_id: str,
    *,
    reason: str | None = None,
) -> dict[str, Any]:
    target, candidate = _candidate_for(dataset, candidate_id)
    if candidate.get("status") != "candidate":
        raise SCENE.AcceptanceError("revision candidate is not pending")
    candidate["status"] = "rejected"
    if reason:
        candidate["resolution_reason"] = reason
    return copy.deepcopy(candidate)


def withdraw_revision(
    dataset: dict[str, Any],
    candidate_id: str,
    *,
    reason: str | None = None,
) -> dict[str, Any]:
    target, candidate = _candidate_for(dataset, candidate_id)
    if candidate.get("status") != "candidate":
        raise SCENE.AcceptanceError("revision candidate is not pending")
    candidate["status"] = "withdrawn"
    if reason:
        candidate["resolution_reason"] = reason
    return copy.deepcopy(candidate)


def _reconciliation_record(
    artifact: dict[str, Any],
    current: dict[str, Any],
    *,
    action: str,
    before_revision: str | None,
    dependent_id: str,
) -> dict[str, Any]:
    return {
        "impact_id": current["id"],
        "upstream_id": current["upstream_id"],
        "upstream_result_id": current["upstream_result_id"],
        "from_revision": current["from_revision"],
        "to_revision": current["to_revision"],
        "action": action,
        "dependent_id": dependent_id,
        "result_dependent_id": artifact.get("id"),
        "dependent_revision_before": before_revision,
        "dependent_revision_after": artifact.get("revision"),
        "authority_class_after": artifact.get("authority_class"),
        "state": "reconciled",
    }


def _finish_reconciliation(
    artifact: dict[str, Any],
    current: dict[str, Any],
    *,
    action: str,
    before_revision: str | None,
    dependent_id: str,
) -> dict[str, Any]:
    _update_relation_to_current(artifact, current)
    record = _reconciliation_record(
        artifact,
        current,
        action=action,
        before_revision=before_revision,
        dependent_id=dependent_id,
    )
    history = artifact.setdefault("reconciliation_history", [])
    if not isinstance(history, list):
        raise RevisionRuntimeError("reconciliation_history must be an array")
    history.append(copy.deepcopy(record))
    artifact["reconciliation"] = {
        **copy.deepcopy(current),
        "state": "reconciled",
        "action": action,
    }
    return record


def _accept_revision_in_place(
    dataset: dict[str, Any],
    candidate_id: str,
) -> dict[str, Any]:
    target, candidate = _candidate_for(dataset, candidate_id)
    if candidate.get("status") != "candidate":
        raise SCENE.AcceptanceError("revision candidate is not pending")
    if candidate.get("identity_operation") == "unresolved":
        raise SCENE.AcceptanceError(
            "identity continuity is unresolved; revision acceptance cannot guess"
        )
    if target.get("revision") != candidate.get("base_revision"):
        raise SCENE.AcceptanceError("revision candidate is stale against current target")

    old_id = target["id"]
    old_revision = target["revision"]
    old_snapshot = _history_snapshot(target)
    new_revision = _stable_id(
        "semantic-revision",
        {
            "candidate": candidate["revision"],
            "target": old_id,
            "base_revision": old_revision,
        },
    )

    history = copy.deepcopy(target.get("revision_history", []))
    if not isinstance(history, list):
        raise RevisionRuntimeError("revision_history must be an array")
    history.append(old_snapshot)

    operation = candidate["identity_operation"]
    candidate_snapshot = copy.deepcopy(candidate)
    if operation == "replacement":
        replacement_id = candidate.get("replacement_id")
        if not isinstance(replacement_id, str) or not replacement_id:
            raise SCENE.AcceptanceError("replacement candidate lacks replacement identity")
        container, key = _location(dataset, old_id)
        new_target = copy.deepcopy(target)
        new_target["id"] = replacement_id
        new_target["supersedes"] = old_id
        new_target["revision_history"] = history
        new_target.pop("revision_candidates", None)
        for field, value in candidate["proposed_changes"].items():
            new_target[field] = copy.deepcopy(value)
        new_target["revision"] = new_revision
        container[key] = new_target
        result_target = new_target
        result_id = replacement_id
    else:
        target["revision_history"] = history
        for field, value in candidate["proposed_changes"].items():
            target[field] = copy.deepcopy(value)
        target["revision"] = new_revision
        result_target = target
        result_id = old_id

    candidate["status"] = "accepted"
    candidate_snapshot["status"] = "accepted"
    acceptance = {
        "candidate_id": candidate_id,
        "candidate_revision": candidate_snapshot["revision"],
        "candidate_snapshot": candidate_snapshot,
        "from_revision": old_revision,
        "to_revision": new_revision,
        "identity_operation": operation,
        "target_id": old_id,
        "result_target_id": result_id,
    }
    acceptance_history = result_target.setdefault("revision_acceptance_history", [])
    if not isinstance(acceptance_history, list):
        raise RevisionRuntimeError("revision_acceptance_history must be an array")
    acceptance_history.append(copy.deepcopy(acceptance))
    result_target["last_revision_acceptance"] = copy.deepcopy(acceptance)

    reconciliation_context = candidate_snapshot.get("reconciliation_context")
    if isinstance(reconciliation_context, dict):
        current = result_target.get("reconciliation")
        if (
            not isinstance(current, dict)
            or current.get("id") != reconciliation_context.get("impact_id")
        ):
            raise SCENE.AcceptanceError(
                "accepted reconciliation candidate no longer matches current impact"
            )
        _finish_reconciliation(
            result_target,
            current,
            action=operation,
            before_revision=old_revision,
            dependent_id=old_id,
        )

    _promote_candidate_material_dependencies(result_target, candidate_snapshot)

    return {
        "id": _stable_id(
            "accepted-revision-change",
            {
                "candidate_id": candidate_id,
                "target_id": old_id,
                "result_target_id": result_id,
                "from_revision": old_revision,
                "to_revision": new_revision,
            },
        ),
        "target_id": old_id,
        "result_target_id": result_id,
        "surface": candidate_snapshot["surface"],
        "from_revision": old_revision,
        "to_revision": new_revision,
        "identity_operation": operation,
        "candidate_id": candidate_id,
    }

def accept_revision(
    dataset: dict[str, Any],
    candidate_id: str,
) -> dict[str, Any]:
    before = copy.deepcopy(dataset)
    try:
        return _accept_revision_in_place(dataset, candidate_id)
    except Exception:
        dataset.clear()
        dataset.update(before)
        raise

def analyze_impact(
    dataset: dict[str, Any],
    accepted_change: dict[str, Any],
) -> list[dict[str, Any]]:
    target_id = accepted_change["target_id"]
    from_revision = accepted_change["from_revision"]
    to_target_id = accepted_change["result_target_id"]
    to_revision = accepted_change["to_revision"]
    replacement = accepted_change.get("identity_operation") == "replacement"
    impacts: list[dict[str, Any]] = []

    for dependent in SCENE._iter_artifacts(dataset):
        if dependent.get("id") in {target_id, to_target_id}:
            continue
        relation = _matching_relation(dependent, target_id, from_revision)
        if relation is None:
            continue

        if "material" not in relation:
            material: bool | None = None
            state = "unresolved"
        else:
            material = bool(relation["material"])
            if not material:
                state = "still_valid"
            elif replacement:
                state = "superseded"
            else:
                state = "review_required"

        impact = {
            "id": _stable_id(
                "impact",
                {
                    "dependent": dependent.get("id"),
                    "target": target_id,
                    "from_revision": from_revision,
                    "to_revision": to_revision,
                    "state": state,
                },
            ),
            "dependent_id": dependent.get("id"),
            "upstream_id": target_id,
            "upstream_result_id": to_target_id,
            "from_revision": from_revision,
            "to_revision": to_revision,
            "material": material,
            "state": state,
        }
        dependent["reconciliation"] = copy.deepcopy(impact)
        impacts.append(impact)
    return impacts

def _update_relation_to_current(
    artifact: dict[str, Any],
    reconciliation: dict[str, Any],
    *,
    material: bool | None = None,
) -> None:
    old_id = reconciliation["upstream_id"]
    new_id = reconciliation["upstream_result_id"]
    relation = _ensure_explicit_relation(
        artifact,
        old_id,
        material=bool(reconciliation.get("material", True)),
    )
    legacy_revision_pin = "target_revision" in relation
    relation["target_id"] = new_id
    if legacy_revision_pin:
        relation["target_revision"] = reconciliation["to_revision"]
    relation["authority_basis"] = "accepted"
    if material is not None:
        relation["material"] = material

    alignment = artifact.setdefault("alignment", {})
    if not isinstance(alignment, dict):
        raise RevisionRuntimeError("alignment must be an object")
    dependency_alignment = alignment.setdefault("dependencies", {})
    if not isinstance(dependency_alignment, dict):
        raise RevisionRuntimeError("alignment.dependencies must be an object")
    if old_id != new_id:
        dependency_alignment.pop(old_id, None)
    dependency_alignment[new_id] = reconciliation["to_revision"]


def reconcile(
    dataset: dict[str, Any],
    dependent_id: str,
    impact_id: str,
    action: str,
    *,
    proposed_changes: dict[str, Any] | None = None,
    replacement_id: str | None = None,
) -> dict[str, Any]:
    artifact = _artifact(dataset, dependent_id)
    current = artifact.get("reconciliation")
    if not isinstance(current, dict) or current.get("id") != impact_id:
        raise RevisionRuntimeError("reconciliation target does not match current impact")

    allowed = {
        "preserve",
        "revise",
        "rebuild",
        "narrow",
        "withdraw",
        "supersede",
        "unresolved",
    }
    if action not in allowed:
        raise RevisionRuntimeError(f"unsupported reconciliation action: {action}")

    before_revision = artifact.get("revision")
    authority_before = artifact.get("authority_class")
    owner = _surface_owner(artifact)

    if action == "unresolved":
        artifact["reconciliation"] = {**copy.deepcopy(current), "state": "unresolved"}
        return copy.deepcopy(artifact["reconciliation"])

    if action in {"revise", "supersede"} and owner in {"canon", "plot"}:
        if artifact.get("authority_class") != "accepted_semantic":
            raise RevisionRuntimeError(
                "semantic reconciliation revision requires accepted semantic target"
            )
        if not isinstance(proposed_changes, dict) or not proposed_changes:
            raise RevisionRuntimeError(
                "semantic reconciliation revision requires proposed_changes"
            )
        identity_operation = "replacement" if action == "supersede" else "revision"
        candidate = propose_revision(
            dataset,
            dependent_id,
            proposed_changes,
            identity_operation=identity_operation,
            replacement_id=replacement_id,
            material_dependencies=[{
                "target_id": current["upstream_result_id"],
                "authority_basis": "accepted",
                "material": True,
            }],
        )
        stored_target, stored_candidate = _candidate_for(dataset, candidate["id"])
        stored_candidate["reconciliation_context"] = {
            "impact_id": impact_id,
            "upstream_id": current["upstream_id"],
            "upstream_result_id": current["upstream_result_id"],
            "from_revision": current["from_revision"],
            "to_revision": current["to_revision"],
            "action": action,
        }
        return {
            "impact_id": impact_id,
            "action": action,
            "dependent_id": dependent_id,
            "candidate_id": candidate["id"],
            "state": "candidate_pending_acceptance",
        }

    if action == "withdraw":
        if authority_before not in {
            "candidate_semantic",
            "candidate_manuscript",
            "production_candidate",
        }:
            raise RevisionRuntimeError("only candidate state may be withdrawn")
        artifact["withdrawn"] = True
        return _finish_reconciliation(
            artifact,
            current,
            action=action,
            before_revision=before_revision,
            dependent_id=dependent_id,
        )

    if action == "narrow":
        _update_relation_to_current(artifact, current, material=False)
    elif action == "preserve":
        _update_relation_to_current(artifact, current)
    elif action == "rebuild":
        if authority_before != "production_approved":
            raise RevisionRuntimeError("rebuild applies to production-approved control")
        _update_relation_to_current(artifact, current)
        artifact["revision"] = _stable_id(
            "production-revision",
            {
                "artifact": dependent_id,
                "from_revision": before_revision,
                "impact": impact_id,
            },
        )
    elif action == "revise":
        if authority_before == "accepted_manuscript":
            raise SCENE.AcceptanceError(
                "accepted Manuscript cannot be rewritten by upstream reconciliation"
            )
        if not isinstance(proposed_changes, dict) or not proposed_changes:
            raise RevisionRuntimeError("revision reconciliation requires proposed_changes")
        protected = {"id", "surface", "authority_class", "revision"}
        if protected & set(proposed_changes):
            raise RevisionRuntimeError("reconciliation cannot replace governed identity fields")
        history = artifact.setdefault("revision_history", [])
        if not isinstance(history, list):
            raise RevisionRuntimeError("revision_history must be an array")
        history.append(_history_snapshot(artifact))
        _update_relation_to_current(artifact, current)
        for field, value in proposed_changes.items():
            artifact[field] = copy.deepcopy(value)
        artifact["revision"] = _stable_id(
            "reconciled-revision",
            {
                "artifact": dependent_id,
                "from_revision": before_revision,
                "impact": impact_id,
                "changes": proposed_changes,
            },
        )
    else:  # non-semantic supersede
        if not isinstance(replacement_id, str) or not replacement_id:
            raise RevisionRuntimeError("supersede requires replacement_id")
        container, key = _location(dataset, dependent_id)
        replacement = copy.deepcopy(artifact)
        replacement["id"] = replacement_id
        replacement["supersedes"] = dependent_id
        if isinstance(proposed_changes, dict):
            for field, value in proposed_changes.items():
                replacement[field] = copy.deepcopy(value)
        _update_relation_to_current(replacement, current)
        replacement["revision"] = _stable_id(
            "replacement-revision",
            {
                "artifact": dependent_id,
                "replacement": replacement_id,
                "impact": impact_id,
            },
        )
        container[key] = replacement
        artifact = replacement

    record = _reconciliation_record(
        artifact,
        current,
        action=action,
        before_revision=before_revision,
        dependent_id=dependent_id,
    )
    history = artifact.setdefault("reconciliation_history", [])
    if not isinstance(history, list):
        raise RevisionRuntimeError("reconciliation_history must be an array")
    history.append(copy.deepcopy(record))
    artifact["reconciliation"] = {
        **copy.deepcopy(current),
        "state": "reconciled",
        "action": action,
    }
    return record

def ensure_artifact_current(dataset: dict[str, Any], artifact: dict[str, Any]) -> None:
    if _blocked(artifact):
        raise SCENE.SceneNotReadyError(
            f"{artifact.get('id')}: material reconciliation is unresolved"
        )

    index = SCENE.artifact_index(dataset)
    for relation in _relations(artifact):
        if "material" not in relation:
            raise SCENE.SceneNotReadyError(
                f"{artifact.get('id')}: dependency materiality is unresolved"
            )
        if not bool(relation["material"]):
            continue
        target_id = relation.get("target_id")
        if not isinstance(target_id, str) or target_id not in index:
            raise SCENE.SceneNotReadyError(
                f"{artifact.get('id')}: unresolved dependency {target_id}"
            )
        target_revision = relation.get("target_revision")
        if (
            isinstance(target_revision, str)
            and target_revision
            and index[target_id].get("revision") != target_revision
        ):
            raise SCENE.SceneNotReadyError(
                f"{artifact.get('id')}: dependency {target_id} is stale"
            )
        if not isinstance(target_revision, str) or not target_revision:
            alignment = artifact.get("alignment", {})
            dependency_alignment = (
                alignment.get("dependencies", {})
                if isinstance(alignment, dict)
                else {}
            )
            aligned_revision = dependency_alignment.get(target_id)
            if (
                isinstance(aligned_revision, str)
                and aligned_revision
                and index[target_id].get("revision") != aligned_revision
            ):
                raise SCENE.SceneNotReadyError(
                    f"{artifact.get('id')}: dependency {target_id} alignment is stale"
                )


def ensure_scene_ready(dataset: dict[str, Any], scene_id: str) -> None:
    scene = SCENE._scene_by_id(dataset, scene_id)
    ensure_artifact_current(dataset, scene)

    prose = dataset.get("prose", {})
    for collection in ("beats", "modes", "pseudo_prose"):
        values = prose.get(collection, {})
        if not isinstance(values, dict):
            continue
        for artifact in values.values():
            if not isinstance(artifact, dict):
                continue
            target = artifact.get("target_scope")
            if target == scene_id or (collection == "modes" and target is None):
                ensure_artifact_current(dataset, artifact)

    files = dataset.get("chapters", {}).get("files", [])
    if isinstance(files, list):
        for artifact in files:
            if isinstance(artifact, dict) and artifact.get("plot_scope") == scene_id:
                ensure_artifact_current(dataset, artifact)


def _target_manuscript(
    dataset: dict[str, Any],
    scene_id: str,
) -> dict[str, Any] | None:
    files = dataset.get("chapters", {}).get("files", [])
    if not isinstance(files, list):
        return None
    for artifact in files:
        if isinstance(artifact, dict) and artifact.get("plot_scope") == scene_id:
            return artifact
    return None


def _ensure_scene_inputs_for_manuscript_repair(
    dataset: dict[str, Any],
    scene_id: str,
) -> None:
    scene = SCENE._scene_by_id(dataset, scene_id)
    ensure_artifact_current(dataset, scene)

    prose = dataset.get("prose", {})
    for collection in ("beats", "modes", "pseudo_prose"):
        values = prose.get(collection, {})
        if not isinstance(values, dict):
            continue
        for artifact in values.values():
            if not isinstance(artifact, dict):
                continue
            target = artifact.get("target_scope")
            if target == scene_id or (collection == "modes" and target is None):
                ensure_artifact_current(dataset, artifact)


def build_manuscript_repair_package(
    dataset: dict[str, Any],
    scene_id: str,
) -> dict[str, Any]:
    _ensure_scene_inputs_for_manuscript_repair(dataset, scene_id)
    current = _target_manuscript(dataset, scene_id)
    if current is None or current.get("authority_class") != "accepted_manuscript":
        raise SCENE.SceneNotReadyError(
            "Manuscript repair requires an accepted current target Manuscript"
        )
    reconciliation = current.get("reconciliation")
    if (
        not isinstance(reconciliation, dict)
        or reconciliation.get("state") not in {"review_required", "stale", "superseded"}
    ):
        raise SCENE.SceneNotReadyError(
            "Manuscript repair requires a materially stale or superseded target"
        )

    contract = SCENE.build_production_contract(dataset, scene_id)
    package = SCENE.build_generation_package(contract)
    package["purpose"] = "manuscript_reconciliation"
    package["replaces_manuscript"] = {
        "id": current.get("id"),
        "revision": current.get("revision"),
        "reconciliation": copy.deepcopy(reconciliation),
    }
    package["provenance"]["package_digest"] = None
    package["provenance"]["package_digest"] = hashlib.sha256(
        _canonical(package)
    ).hexdigest()
    return package


def assert_manuscript_repair_package_current(
    dataset: dict[str, Any],
    package: dict[str, Any],
) -> None:
    SCENE._verify_package_digest(package)
    if package.get("purpose") != "manuscript_reconciliation":
        raise SCENE.SceneNotReadyError("package is not a Manuscript-repair package")
    scene_id = package.get("target_scope")
    if not isinstance(scene_id, str):
        raise SCENE.SceneNotReadyError("Manuscript-repair package has no target scope")

    _ensure_scene_inputs_for_manuscript_repair(dataset, scene_id)
    current = _target_manuscript(dataset, scene_id)
    replaced = package.get("replaces_manuscript")
    if current is None or not isinstance(replaced, dict):
        raise SCENE.SceneNotReadyError("Manuscript-repair target is missing")
    if (
        replaced.get("id") != current.get("id")
        or replaced.get("revision") != current.get("revision")
    ):
        raise SCENE.SceneNotReadyError("Manuscript-repair target changed after packaging")

    reconciliation = current.get("reconciliation")
    if (
        not isinstance(reconciliation, dict)
        or reconciliation.get("state") not in {"review_required", "stale", "superseded"}
    ):
        raise SCENE.SceneNotReadyError("Manuscript-repair target is no longer stale")

    selected = package.get("selected_revisions", {})
    scene = SCENE._scene_by_id(dataset, scene_id)
    if selected.get("scene") != scene.get("revision"):
        raise SCENE.SceneNotReadyError("Manuscript-repair Plot revision is stale")

    index = SCENE.artifact_index(dataset)
    for artifact_id, revision in selected.get("dependencies", {}).items():
        artifact = index.get(artifact_id)
        if artifact is None or artifact.get("revision") != revision:
            raise SCENE.SceneNotReadyError(
                f"Manuscript-repair dependency {artifact_id} is stale"
            )
    controls = selected.get("prose_controls", {})
    for mapping in controls.values() if isinstance(controls, dict) else []:
        if not isinstance(mapping, dict):
            continue
        for artifact_id, revision in mapping.items():
            artifact = index.get(artifact_id)
            if artifact is None or artifact.get("revision") != revision:
                raise SCENE.SceneNotReadyError(
                    f"Manuscript-repair control {artifact_id} is stale"
                )


def create_manuscript_replacement_candidate(
    dataset: dict[str, Any],
    package: dict[str, Any],
    text: str,
    attempt: int,
) -> dict[str, Any]:
    assert_manuscript_repair_package_current(dataset, package)
    return SCENE.create_candidate(package, text, attempt)


def assert_package_current(dataset: dict[str, Any], package: dict[str, Any]) -> None:
    SCENE._verify_package_digest(package)
    scene_id = package.get("target_scope")
    if not isinstance(scene_id, str):
        raise SCENE.SceneNotReadyError("generation package has no target scope")
    ensure_scene_ready(dataset, scene_id)

    selected = package.get("selected_revisions", {})
    scene = SCENE._scene_by_id(dataset, scene_id)
    if selected.get("scene") != scene.get("revision"):
        raise SCENE.SceneNotReadyError("generation package target revision is stale")

    index = SCENE.artifact_index(dataset)
    for artifact_id, revision in selected.get("dependencies", {}).items():
        current = index.get(artifact_id)
        if current is None or current.get("revision") != revision:
            raise SCENE.SceneNotReadyError(
                f"generation package dependency {artifact_id} is stale"
            )

    controls = selected.get("prose_controls", {})
    for mapping in controls.values() if isinstance(controls, dict) else []:
        if not isinstance(mapping, dict):
            continue
        for artifact_id, revision in mapping.items():
            current = index.get(artifact_id)
            if current is None or current.get("revision") != revision:
                raise SCENE.SceneNotReadyError(
                    f"generation package control {artifact_id} is stale"
                )

    for key in ("prior_manuscript", "current_target_manuscript"):
        mapping = selected.get(key, {})
        if not isinstance(mapping, dict):
            continue
        for artifact_id, revision in mapping.items():
            current = index.get(artifact_id)
            if current is None or current.get("revision") != revision:
                raise SCENE.SceneNotReadyError(
                    f"generation package Manuscript {artifact_id} is stale"
                )


class RevisionSession(SCENE.SceneSession):
    def context(self, scene_id: str) -> dict[str, Any]:
        ensure_scene_ready(self.dataset, scene_id)
        return super().context(scene_id)

    def contract(self, scene_id: str) -> dict[str, Any]:
        ensure_scene_ready(self.dataset, scene_id)
        return super().contract(scene_id)

    def package(self, scene_id: str) -> dict[str, Any]:
        ensure_scene_ready(self.dataset, scene_id)
        return super().package(scene_id)

    def propose_revision(
        self,
        target_id: str,
        proposed_changes: dict[str, Any],
        *,
        identity_operation: str = "revision",
        replacement_id: str | None = None,
        material_dependencies: list[dict[str, Any]] | None = None,
        assumptions: list[str] | None = None,
    ) -> dict[str, Any]:
        return propose_revision(
            self.dataset,
            target_id,
            proposed_changes,
            identity_operation=identity_operation,
            replacement_id=replacement_id,
            material_dependencies=material_dependencies,
            assumptions=assumptions,
        )

    def inspect_revision_candidate(self, candidate_id: str) -> dict[str, Any]:
        return inspect_revision_candidate(self.dataset, candidate_id)

    def accept_revision(self, candidate_id: str) -> dict[str, Any]:
        return accept_revision(self.dataset, candidate_id)

    def reject_revision(
        self,
        candidate_id: str,
        *,
        reason: str | None = None,
    ) -> dict[str, Any]:
        return reject_revision(self.dataset, candidate_id, reason=reason)

    def withdraw_revision(
        self,
        candidate_id: str,
        *,
        reason: str | None = None,
    ) -> dict[str, Any]:
        return withdraw_revision(self.dataset, candidate_id, reason=reason)

    def analyze_impact(self, accepted_change: dict[str, Any]) -> list[dict[str, Any]]:
        return analyze_impact(self.dataset, accepted_change)

    def reconcile(
        self,
        dependent_id: str,
        impact_id: str,
        action: str,
        **kwargs,
    ) -> dict[str, Any]:
        return reconcile(self.dataset, dependent_id, impact_id, action, **kwargs)

    def manuscript_repair_package(self, scene_id: str) -> dict[str, Any]:
        return build_manuscript_repair_package(self.dataset, scene_id)

    def create_manuscript_replacement_candidate(
        self,
        package: dict[str, Any],
        text: str,
        attempt: int,
    ) -> dict[str, Any]:
        return create_manuscript_replacement_candidate(
            self.dataset,
            package,
            text,
            attempt,
        )

    def persist_manuscript_replacement(
        self,
        accepted: dict[str, Any],
    ) -> None:
        if accepted.get("authority_class") != "accepted_manuscript":
            raise SCENE.AcceptanceError(
                "Manuscript replacement requires accepted Manuscript state"
            )
        provenance = accepted.get("generation_provenance", {})
        package = provenance.get("package_snapshot")
        if not isinstance(package, dict):
            raise SCENE.AcceptanceError(
                "Manuscript replacement lacks generation package provenance"
            )
        assert_manuscript_repair_package_current(self.dataset, package)

        scene_id = accepted.get("target_scope")
        if not isinstance(scene_id, str):
            raise SCENE.AcceptanceError("Manuscript replacement has no target scope")
        scene = SCENE._scene_by_id(self.dataset, scene_id)
        ordinal = scene.get("ordinal")
        if not isinstance(ordinal, int):
            raise SCENE.SceneRuntimeError(
                "target scene requires ordinal for Manuscript persistence"
            )

        current = _target_manuscript(self.dataset, scene_id)
        if current is None:
            raise SCENE.AcceptanceError("Manuscript replacement target disappeared")

        previous = copy.deepcopy(current)
        updated = copy.deepcopy(self.dataset)
        files = updated["chapters"]["files"]
        existing = next(
            (
                entry
                for entry in files
                if isinstance(entry, dict) and entry.get("plot_scope") == scene_id
            ),
            None,
        )
        if existing is None:
            raise SCENE.AcceptanceError("Manuscript replacement target disappeared")

        prior_history = copy.deepcopy(existing.get("manuscript_revision_history", []))
        if not isinstance(prior_history, list):
            raise RevisionRuntimeError("manuscript_revision_history must be an array")
        prior_history.append(previous)

        reconciliation_history = copy.deepcopy(
            existing.get("reconciliation_history", [])
        )
        if not isinstance(reconciliation_history, list):
            raise RevisionRuntimeError("reconciliation_history must be an array")
        reconciliation_history.append({
            "action": "replace_manuscript",
            "dependent_id": existing.get("id"),
            "dependent_revision_before": existing.get("revision"),
            "dependent_revision_after": accepted.get("revision"),
            "upstream_id": scene_id,
            "to_revision": scene.get("revision"),
            "state": "reconciled",
        })

        record = {
            "id": existing.get("id") or f"manuscript-{scene_id}",
            "surface": "manuscript",
            "authority_class": "accepted_manuscript",
            "revision": accepted["revision"],
            "ordinal": ordinal,
            "plot_scope": scene_id,
            "path": f"chapters/{ordinal:03d}-{scene_id}.md",
            "generation_package_id": accepted["generation_package_id"],
            "generation_provenance": copy.deepcopy(
                accepted["generation_provenance"]
            ),
            "review": copy.deepcopy(accepted["review"]),
            "accepted_from_candidate": accepted["accepted_from_candidate"],
            "content": accepted["text"],
            "dependency_relations": [{
                "target_id": scene_id,
                "target_revision": scene.get("revision"),
                "authority_basis": "accepted",
                "material": True,
            }],
            "replaces_revision": previous.get("revision"),
            "manuscript_revision_history": prior_history,
            "reconciliation_history": reconciliation_history,
            "reconciliation": {
                "state": "reconciled",
                "action": "replace_manuscript",
                "upstream_id": scene_id,
                "to_revision": scene.get("revision"),
            },
        }
        files[files.index(existing)] = record
        files.sort(key=lambda entry: entry.get("ordinal", 0))

        self.baseline_digest = self.backend.save(
            updated,
            expected_digest=self.baseline_digest,
        )
        self.dataset = updated

    def create_candidate(
        self,
        package: dict[str, Any],
        text: str,
        attempt: int,
    ) -> dict[str, Any]:
        assert_package_current(self.dataset, package)
        return SCENE.create_candidate(package, text, attempt)

    def persist(self) -> None:
        self.baseline_digest = self.backend.save(
            self.dataset,
            expected_digest=self.baseline_digest,
        )


def open_revision_session(
    repository_root: Path,
    *,
    authorize_transition: bool = False,
) -> RevisionSession:
    base = SCENE.open_scene_session(
        repository_root,
        authorize_transition=authorize_transition,
    )
    return RevisionSession(
        base.backend,
        base.dataset,
        base.compatibility_status,
        base.baseline_digest,
    )
