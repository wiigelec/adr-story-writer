#!/usr/bin/env python3
from __future__ import annotations

import argparse
import importlib.util
import json
import re
import sys

sys.dont_write_bytecode = True
import tempfile
from pathlib import Path
from typing import Callable

ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "product" / "validation" / "requirement-evaluation.json"
REQS = ROOT / "product" / "specs" / "FS-001-requirements.md"
FS002_REQS = ROOT / "product" / "specs" / "FS-002-requirements.md"
DESIGN_REVISION = "3ba9e3f600adf2a5ccae8db8aca00ebbbb9c17c9"
FS002_DESIGN_REVISION = "325c7f22cd140dee43c01dbf7f93500325585ce9"
TASKS: dict[str, Callable[[], bool | None]] = {}


def fail(message: str) -> int:
    print(f"FAIL product-validation: {message}", file=sys.stderr)
    return 1


def load_json(path: str) -> dict:
    p = ROOT / path
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"{path}: {exc}") from exc
    if not isinstance(data, dict):
        raise ValueError(f"{path}: root must be an object")
    return data


def check(condition: bool, message: str) -> bool:
    if not condition:
        print(f"FAIL product-validation: {message}", file=sys.stderr)
        return False
    return True


def task_planning_binding() -> bool:
    for rel in (
        "product/planning/FS-001-governed-prose-production-and-acceptance/functional-set.md",
        "product/planning/FS-001-governed-prose-production-and-acceptance/plan.md",
    ):
        text = (ROOT / rel).read_text(encoding="utf-8")
        if not check(f"design_revision: {DESIGN_REVISION}" in text, f"{rel}: missing exact Design binding"):
            return False
    return check(REQS.is_file(), "FS-001 normative requirements missing")


def task_governed_state_contract() -> bool:
    data = load_json("ruleset/governed-state.json")
    model = data.get("artifact_model", {})
    required = {"id", "surface", "authority_class", "revision"}
    classes = {
        "accepted_semantic", "candidate_semantic", "production_candidate",
        "production_approved", "candidate_manuscript", "accepted_manuscript",
    }
    dep = data.get("dependency_model", {})
    persistence = data.get("persistence", {})
    return (
        check(required <= set(model.get("required_fields", [])), "governed-state: missing required artifact fields")
        and check(classes == set(model.get("authority_classes", [])), "governed-state: authority classes differ from FS-001")
        and check(dep.get("material_candidate_dependencies_block_acceptance") is True, "governed-state: candidate dependency gate missing")
        and check(persistence.get("persisted_candidate_remains_candidate") is True, "governed-state: persisted candidates must remain candidate")
    )


def task_production_contract() -> bool:
    data = load_json("ruleset/production.json")
    caps = set(data.get("production_contract", {}).get("capabilities", []))
    required = {
        "target_scope", "stop_boundary", "narrative_movement",
        "local_realization_units", "viewpoint_access", "reveal_concealment",
        "entry_exit_conditions", "prose_guidance", "style_voice",
        "protected_material", "creative_allowance",
        "prohibited_consequential_invention", "accepted_dependencies",
        "candidate_dependencies",
    }
    return (
        check(required <= caps, "production: production contract lacks FS-001 capabilities")
        and check(data.get("production_contract", {}).get("must_be_bounded_before_generation") is True, "production: bounded-generation gate missing")
    )


def task_generation_package() -> bool:
    data = load_json("ruleset/production.json")
    package = data.get("generation_package", {})
    required = {
        "id", "contract_id", "target_scope", "stop_boundary",
        "selected_revisions", "creative_allowance",
        "prohibited_invention", "provenance",
    }
    access = data.get("information_access", {})
    generation = data.get("generation", {})
    return (
        check(required <= set(package.get("required_fields", [])), "production: generation package missing required fields")
        and check(package.get("stable_after_use") is True, "production: generation package must be stable after use")
        and check(package.get("overflow_remains_candidate") is True, "production: generation overflow must remain candidate")
        and check(access.get("supports_generator_visible_context") is True and access.get("supports_reviewer_only_constraints") is True, "production: information-access separation missing")
        and check(generation.get("output_authority_class") == "candidate_manuscript", "production: generated prose must be candidate_manuscript")
    )


def task_review_contract() -> bool:
    data = load_json("ruleset/review.json")
    outcomes = {"conforming", "non_conforming", "indeterminate"}
    invention = data.get("consequential_invention", {})
    return (
        check(outcomes == set(data.get("outcomes", [])), "review: required outcomes missing")
        and check(len(data.get("indeterminate_when", [])) >= 3, "review: indeterminate-context conditions missing")
        and check(invention.get("becomes_candidate_at_owning_surface") is True, "review: consequential invention candidate handling missing")
        and check(invention.get("never_silently_promoted") is True, "review: silent promotion prohibition missing")
    )


def task_authority_operations() -> bool:
    data = load_json("ruleset/authority.json")
    required = {
        "semantic_acceptance", "production_approval", "manuscript_acceptance",
        "revision_acceptance", "coordinated_acceptance",
        "persistence_authorization",
    }
    return (
        check(required == set(data.get("acceptance_operations", [])), "authority: acceptance operations incomplete")
        and check(data.get("persistence_preserves_authority_class") is True, "authority: persistence must preserve authority class")
        and check(data.get("acceptance_closure_required") is True, "authority: acceptance closure must be required")
    )


def task_dataset_boundary() -> bool:
    return (
        check(not (ROOT / "dataset").exists(), "story Dataset instance must not be stored in ruleset repository")
        and check((ROOT / "ruleset" / "governed-state.json").is_file(), "ruleset must define Dataset interpretation semantics")
    )


def task_manifest_bindings() -> bool:
    text = REQS.read_text(encoding="utf-8")
    pattern = re.compile(r"^### (FS-001-NR-\d{3}).*?\n\*\*Classification: ([MSB])\*\*", re.M | re.S)
    required = {rid for rid, cls in pattern.findall(text) if cls in {"M", "B"}}
    manifest = load_manifest()
    bound = {b.get("requirement") for b in manifest["bindings"] if isinstance(b, dict)}
    return check(required <= bound, f"manifest missing FS-001 mechanical bindings: {sorted(required - bound)}")


TASKS.update({
    "fs001-planning-binding": task_planning_binding,
    "fs001-governed-state-contract": task_governed_state_contract,
    "fs001-production-contract": task_production_contract,
    "fs001-generation-package": task_generation_package,
    "fs001-review-contract": task_review_contract,
    "fs001-authority-operations": task_authority_operations,
    "fs001-dataset-boundary": task_dataset_boundary,
    "fs001-manifest-bindings": task_manifest_bindings,
})


def load_fs002_runtime():
    path = ROOT / "product" / "src" / "compatibility.py"
    spec = importlib.util.spec_from_file_location("fs002_compatibility", path)
    if spec is None or spec.loader is None:
        raise ValueError("cannot load FS-002 compatibility runtime")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def task_fs002_planning_binding() -> bool:
    for rel in (
        "product/planning/FS-002-ruleset-dataset-compatibility-migration-and-rebinding/functional-set.md",
        "product/planning/FS-002-ruleset-dataset-compatibility-migration-and-rebinding/plan.md",
    ):
        text = (ROOT / rel).read_text(encoding="utf-8")
        if not check(f"design_revision: {FS002_DESIGN_REVISION}" in text, f"{rel}: missing exact Design binding"):
            return False
    return check(FS002_REQS.is_file(), "FS-002 normative requirements missing")


def task_fs002_compatibility_contract() -> bool:
    data = load_json("ruleset/compatibility.json")
    schema = data.get("dataset_schema", {})
    binding = data.get("ruleset_binding", {})
    comp = data.get("compatibility", {})
    migration = data.get("migration", {})
    rebinding = data.get("rebinding", {})
    identity = load_json("ruleset/identity.json")
    template = load_json("init-config/dataset.json")
    states = {
        "directly_compatible", "restricted_operation", "migration_required",
        "rebinding_required", "unsupported", "indeterminate",
    }
    forbidden_inference = {
        "filename_match", "version_ordering", "semantic_version_syntax",
        "parser_success", "field_presence", "apparent_partial_operation",
    }
    migration_ids = {t.get("id") for t in migration.get("supported_transitions", []) if isinstance(t, dict)}
    rebind_ids = {t.get("id") for t in rebinding.get("supported_transitions", []) if isinstance(t, dict)}
    return (
        check(schema.get("current") == template.get("schema"), "FS-002: Dataset schema identity mismatch")
        and check(binding.get("current") == template.get("ruleset_binding"), "FS-002: template Ruleset binding mismatch")
        and check(binding.get("current") == identity, "FS-002: current Ruleset identity mismatch")
        and check(schema.get("binding_is_not_schema_identity") is True, "FS-002: schema and binding axes collapsed")
        and check(states == set(comp.get("states", [])), "FS-002: compatibility states incomplete")
        and check(forbidden_inference <= set(comp.get("no_inference_from", [])), "FS-002: compatibility inference prohibitions incomplete")
        and check(comp.get("ordinary_operation_requires_established_compatibility") is True, "FS-002: ordinary-operation gate missing")
        and check("legacy-unversioned-v0-to-dataset-v1" in migration_ids, "FS-002: supported migration missing")
        and check(
            set(migration.get("supported_transitions", [])[0].get("source", {}).get("exact_top_level", []))
            == {"instance", "story", "canon", "plot", "prose", "chapters"},
            "FS-002: legacy migration must use an exact historical realization signature",
        )
        and check(
            migration.get("ambiguous_source_behavior", {}).get("semantic_author_decision_required") is True,
            "FS-002: ambiguous legacy source must surface author decision",
        )
        and check("ruleset-0.1.0-to-0.2.0" in rebind_ids, "FS-002: supported rebinding missing")
    )


def _story_payload(dataset: dict) -> dict:
    ignored = {"schema", "ruleset_binding", "compatibility_history"}
    return {k: v for k, v in dataset.items() if k not in ignored}


def task_fs002_runtime_transitions() -> bool:
    rt = load_fs002_runtime()
    contract = rt.load_contract()

    legacy = {
        "instance": {"id": "story-1"},
        "story": {
            "application": "adr-story-writer",
            "dataset_role": "story",
            "title": "Continuity Fixture",
            "status": "active",
        },
        "canon": {
            "character": {
                "c1": {
                    "id": "character-1",
                    "surface": "canon.character",
                    "authority_class": "accepted_semantic",
                    "revision": "r7",
                    "temporal_state": {"as_of": "event-3"},
                    "ambiguity": {"eye_color": "unknown"},
                }
            },
            "setting": {},
            "events": [
                {
                    "id": "event-3",
                    "surface": "canon.events",
                    "authority_class": "accepted_semantic",
                    "revision": "r2",
                }
            ],
        },
        "plot": {
            "synopsis": {},
            "outline": [],
            "sequence": [
                {
                    "id": "sequence-9",
                    "surface": "plot.sequence",
                    "authority_class": "candidate_semantic",
                    "revision": "r3",
                    "dependencies": ["character-1", "event-3"],
                    "candidate_assumptions": ["assumption-weather"],
                }
            ],
        },
        "prose": {
            "beats": {
                "beat-4": {
                    "id": "beat-4",
                    "surface": "prose.beats",
                    "authority_class": "production_approved",
                    "revision": "r5",
                    "protected_material": ["exact-line-1"],
                    "generation_provenance": {
                        "generation_package_id": "gp-12",
                        "selected_revisions": ["r7", "r2", "r3"],
                    },
                }
            },
            "modes": {},
            "pseudo_prose": {},
        },
        "chapters": {
            "format": "markdown",
            "files": [
                {
                    "id": "chapter-1",
                    "authority_class": "accepted_manuscript",
                    "ordinal": 1,
                    "path": "chapters/001.md",
                }
            ],
        },
    }

    pre_story = json.loads(json.dumps(legacy))
    status = rt.classify(legacy, contract=contract)
    if not check(status.get("state") == "migration_required", "FS-002: exact legacy Dataset not classified migration_required"):
        return False

    migrated = rt.migrate(legacy, status["transition"], authorized=True, contract=contract)
    if not check(_story_payload(migrated) == pre_story, "FS-002: migration changed governed story payload"):
        return False
    if not check(rt.classify(migrated, contract=contract).get("state") == "directly_compatible", "FS-002: migrated Dataset not directly compatible"):
        return False

    ambiguous_legacy = json.loads(json.dumps(legacy))
    ambiguous_legacy["story"]["legacy_extra"] = "unrecognized"
    ambiguous = rt.classify(ambiguous_legacy, contract=contract)
    if not check(ambiguous.get("state") == "indeterminate", "FS-002: ambiguous legacy source not indeterminate"):
        return False
    if not check(ambiguous.get("semantic_author_decision_required") is True, "FS-002: ambiguous legacy source did not surface author decision"):
        return False
    if not check("legacy_realization_identity" in ambiguous.get("unresolved_decisions", []), "FS-002: unresolved legacy identity decision missing"):
        return False
    try:
        rt.migrate(ambiguous_legacy, "legacy-unversioned-v0-to-dataset-v1", authorized=True, contract=contract)
        return check(False, "FS-002: ambiguous legacy Dataset was migrated")
    except rt.TransitionError:
        pass

    field_presence_only = {
        "instance": {},
        "story": {},
        "canon": {},
        "plot": {},
        "prose": {},
        "chapters": {},
    }
    field_only_status = rt.classify(field_presence_only, contract=contract)
    if not check(field_only_status.get("state") == "indeterminate", "FS-002: field-presence-only Dataset was treated as compatible"):
        return False

    old_binding = json.loads(json.dumps(migrated))
    old_binding["ruleset_binding"]["version"] = "0.1.0"
    before_rebind = _story_payload(old_binding)
    status = rt.classify(old_binding, contract=contract)
    if not check(status.get("state") == "rebinding_required", "FS-002: known compatible old binding not classified rebinding_required"):
        return False

    rebound = rt.rebind(old_binding, status["transition"], authorized=True, contract=contract)
    if not check(_story_payload(rebound) == before_rebind, "FS-002: rebinding changed governed story payload"):
        return False
    if not check(rt.classify(rebound, contract=contract).get("state") == "directly_compatible", "FS-002: rebound Dataset not directly compatible"):
        return False

    unknown = json.loads(json.dumps(rebound))
    unknown["schema"] = {"id": "adr-story-writer.dataset", "version": 999}
    ordinary = rt.classify(unknown, contract=contract)
    inspect = rt.classify(unknown, requested_operation="inspect", contract=contract)
    if not check(ordinary.get("state") == "unsupported", "FS-002: unknown schema did not fail safe"):
        return False
    if not check(inspect.get("state") == "restricted_operation", "FS-002: safe restricted inspection unavailable"):
        return False

    try:
        rt.migrate(unknown, "legacy-unversioned-v0-to-dataset-v1", authorized=True, contract=contract)
        return check(False, "FS-002: unsupported Dataset was migrated")
    except rt.TransitionError:
        pass

    try:
        rt.rebind(old_binding, "ruleset-0.1.0-to-0.2.0", authorized=False, contract=contract)
        return check(False, "FS-002: rebinding proceeded without authorization")
    except rt.TransitionError:
        pass

    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "dataset.json"
        rt.atomic_save(path, rebound)
        loaded, reloaded_status = rt.load_and_classify(path)

        if not check(loaded == rebound, "FS-002: coherent persistence did not round-trip"):
            return False
        if not check(reloaded_status.get("state") == "directly_compatible", "FS-002: fresh-session reload not directly compatible"):
            return False

        # Fresh-session reconstruction must preserve governed interpretation,
        # not merely parse the JSON.
        character = loaded["canon"]["character"]["c1"]
        sequence = loaded["plot"]["sequence"][0]
        beat = loaded["prose"]["beats"]["beat-4"]
        chapter = loaded["chapters"]["files"][0]
        if not check(character["authority_class"] == "accepted_semantic", "FS-002: accepted Canon authority lost on reconstruction"):
            return False
        if not check(sequence["authority_class"] == "candidate_semantic", "FS-002: candidate Plot authority lost on reconstruction"):
            return False
        if not check(sequence["dependencies"] == ["character-1", "event-3"], "FS-002: material dependencies lost on reconstruction"):
            return False
        if not check(beat["authority_class"] == "production_approved", "FS-002: production approval lost on reconstruction"):
            return False
        if not check(beat["generation_provenance"]["generation_package_id"] == "gp-12", "FS-002: generation provenance lost on reconstruction"):
            return False
        if not check(character["ambiguity"]["eye_color"] == "unknown", "FS-002: preserved ambiguity lost on reconstruction"):
            return False
        if not check(chapter["authority_class"] == "accepted_manuscript", "FS-002: Manuscript acceptance lost on reconstruction"):
            return False

    return True


def task_fs002_transition_provenance() -> bool:
    rt = load_fs002_runtime()
    contract = rt.load_contract()
    legacy = {
        "instance": {"id": "story-2"},
        "story": {
            "application": "adr-story-writer",
            "dataset_role": "story",
            "title": None,
            "status": "active",
        },
        "canon": {"character": {}, "setting": {}, "events": []},
        "plot": {"synopsis": {}, "outline": [], "sequence": []},
        "prose": {"beats": {}, "modes": {}, "pseudo_prose": {}},
        "chapters": {"format": "markdown", "files": []},
    }
    migrated = rt.migrate(legacy, "legacy-unversioned-v0-to-dataset-v1", authorized=True, contract=contract)
    required = set(contract["transition_provenance"]["required_fields"])
    history = migrated.get(contract["transition_provenance"]["dataset_field"], [])
    return (
        check(len(history) == 1, "FS-002: migration provenance entry missing")
        and check(required <= set(history[0]), "FS-002: migration provenance fields incomplete")
        and check(history[0]["source_realization"]["schema"] == "legacy_unversioned_v0", "FS-002: migration source realization not exact")
        and check(history[0]["semantic_author_decision_required"] is False, "FS-002: supported migration unexpectedly requires semantic invention")
    )


def task_fs002_dataset_boundary() -> bool:
    data = load_json("ruleset/compatibility.json")
    boundary = data.get("dataset_boundary", {})
    return (
        check(not (ROOT / "dataset").exists(), "FS-002: story Dataset instance stored in Ruleset repository")
        and check(boundary.get("story_instance_state_external_to_ruleset_repository") is True, "FS-002: external Dataset boundary missing")
        and check(boundary.get("reverse_ruleset_to_dataset_instance_binding_forbidden") is True, "FS-002: reverse Dataset binding prohibition missing")
    )


def task_fs002_manifest_bindings() -> bool:
    text = FS002_REQS.read_text(encoding="utf-8")
    pattern = re.compile(
        r"^### (FS-002-NR-\d{3}).*?\n\*\*Classification: ([MSB])\*\*(?:\n\*\*State: (Inactive)\*\*)?",
        re.M | re.S,
    )
    parsed = pattern.findall(text)
    required = {rid for rid, cls, state in parsed if cls in {"M", "B"} and state != "Inactive"}
    forbidden = {rid for rid, cls, state in parsed if cls == "S" or state == "Inactive"}
    manifest = load_manifest()
    bound = {b.get("requirement") for b in manifest["bindings"] if isinstance(b, dict)}
    return (
        check(required <= bound, f"manifest missing FS-002 mechanical bindings: {sorted(required - bound)}")
        and check(not (forbidden & bound), f"manifest binds FS-002 semantic/inactive requirements: {sorted(forbidden & bound)}")
    )


TASKS.update({
    "fs002-planning-binding": task_fs002_planning_binding,
    "fs002-compatibility-contract": task_fs002_compatibility_contract,
    "fs002-runtime-transitions": task_fs002_runtime_transitions,
    "fs002-transition-provenance": task_fs002_transition_provenance,
    "fs002-dataset-boundary": task_fs002_dataset_boundary,
    "fs002-manifest-bindings": task_fs002_manifest_bindings,
})


def load_fs003_validation():
    path = ROOT / "product" / "validation" / "fs003_validation.py"
    spec = importlib.util.spec_from_file_location("fs003_validation", path)
    if spec is None or spec.loader is None:
        raise ValueError("cannot load FS-003 Validation")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


TASKS.update(load_fs003_validation().TASKS)


def load_fs004_validation():
    path = ROOT / "product" / "validation" / "fs004_validation.py"
    spec = importlib.util.spec_from_file_location("fs004_validation", path)
    if spec is None or spec.loader is None:
        raise ValueError("cannot load FS-004 Validation")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


TASKS.update(load_fs004_validation().TASKS)

def load_fs005_validation():
    path = ROOT / "product" / "validation" / "fs005_validation.py"
    spec = importlib.util.spec_from_file_location("fs005_validation", path)
    if spec is None or spec.loader is None:
        raise ValueError("cannot load FS-005 Validation")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

TASKS.update(load_fs005_validation().TASKS)

def load_fs006_validation():
    path = ROOT / "product" / "validation" / "fs006_validation.py"
    spec = importlib.util.spec_from_file_location("fs006_validation", path)
    if spec is None or spec.loader is None:
        raise ValueError("cannot load FS-006 Validation")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

TASKS.update(load_fs006_validation().TASKS)

def load_fs007_validation():
    path = ROOT / "product" / "validation" / "fs007_validation.py"
    spec = importlib.util.spec_from_file_location("fs007_validation", path)
    if spec is None or spec.loader is None:
        raise ValueError("cannot load FS-007 Validation")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

TASKS.update(load_fs007_validation().TASKS)

def load_manifest() -> dict:
    try:
        data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot load product Requirement Evaluation Manifest: {exc}") from exc
    if data.get("version") != 1 or not isinstance(data.get("bindings"), list):
        raise ValueError("invalid product Requirement Evaluation Manifest structure")
    return data


def manifest_tasks() -> list[str]:
    data = load_manifest()
    ordered: list[str] = []
    for binding in data["bindings"]:
        if not isinstance(binding, dict):
            raise ValueError("product manifest binding must be an object")
        tasks = binding.get("tasks")
        if not isinstance(tasks, list) or not tasks:
            raise ValueError("product manifest binding requires a non-empty tasks list")
        for task in tasks:
            if not isinstance(task, str) or not task:
                raise ValueError("product validation task identity must be a non-empty string")
            if task not in TASKS:
                raise ValueError(f"product manifest references unknown task: {task}")
            if task not in ordered:
                ordered.append(task)
    return ordered


def execute(task: str) -> int:
    fn = TASKS.get(task)
    if fn is None:
        return fail(f"unknown product Validation task: {task}")
    try:
        result = fn()
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        return fail(f"{task}: {exc}")
    return 1 if result is False else 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--list-tasks", action="store_true")
    parser.add_argument("--task")
    args = parser.parse_args(argv)

    if args.list_tasks and args.task:
        return fail("--list-tasks and --task are mutually exclusive")
    if args.list_tasks:
        for task in sorted(TASKS):
            print(task)
        return 0
    if args.task:
        return execute(args.task)

    try:
        tasks = manifest_tasks()
    except ValueError as exc:
        return fail(str(exc))
    for task in tasks:
        result = execute(task)
        if result:
            return result
    print("Product Validation: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
