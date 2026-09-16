#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Callable

ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "product" / "validation" / "requirement-evaluation.json"
REQS = ROOT / "product" / "specs" / "FS-001-requirements.md"
DESIGN_REVISION = "3ba9e3f600adf2a5ccae8db8aca00ebbbb9c17c9"
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
        "product/specs/FS-001-governed-prose-production-and-acceptance.md",
        "product/specs/FS-001-plan.md",
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
