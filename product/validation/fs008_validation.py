from __future__ import annotations

import copy
import importlib.util
import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
REQS = ROOT / "product" / "specs" / "FS-008-requirements.md"
MANIFEST = ROOT / "product" / "validation" / "requirement-evaluation.json"
DESIGN_REVISION = "7867554b02d39a55b7171c992a61196a87863552"


def check(condition: bool, message: str) -> bool:
    if not condition:
        print(f"FAIL product-validation: {message}")
        return False
    return True


def _load(name: str, rel: str):
    path = ROOT / rel
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ValueError(f"cannot load {rel}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


AUTH = _load("fs008_authoring_runtime", "product/src/authoring_runtime.py")
COMPAT = _load("fs008_compatibility", "product/src/compatibility.py")
SCENE = AUTH.SCENE
REV = AUTH.REV


def _dataset() -> dict[str, Any]:
    return {
        "schema": {"id": "adr-story-writer.dataset", "version": 1},
        "ruleset_binding": {
            "application": "adr-story-writer",
            "component": "ruleset",
            "version": "0.5.0",
        },
        "compatibility_history": [],
        "instance": {"id": "fs008-fixture"},
        "story": {
            "application": "adr-story-writer",
            "dataset_role": "story",
            "title": "FS-008 Fixture",
            "status": "active",
        },
        "canon": {
            "character": {
                "character-mara": {
                    "id": "character-mara",
                    "surface": "canon.character",
                    "authority_class": "accepted_semantic",
                    "revision": "character-mara-r1",
                    "name": "Mara",
                }
            },
            "setting": {},
            "events": [
                {
                    "id": "event-bridge",
                    "surface": "canon.events",
                    "authority_class": "accepted_semantic",
                    "revision": "event-bridge-r1",
                    "summary": "The bridge is broken before the later scene begins.",
                }
            ],
        },
        "plot": {"synopsis": {}, "outline": [], "sequence": []},
        "prose": {"beats": {}, "modes": {}, "pseudo_prose": {}},
        "chapters": {"format": "markdown", "files": []},
    }


def _accepted_scene(dataset: dict[str, Any]) -> dict[str, Any]:
    candidate = AUTH.propose_artifact(
        dataset,
        "plot.sequence",
        {
            "id": "scene-013",
            "ordinal": 13,
            "viewpoint": "character-mara",
            "entry": "Mara reaches the river.",
            "required_movements": ["Mara works around the broken bridge."],
            "exit": "Mara reaches the far bank.",
        },
        dependencies=["character-mara", "event-bridge"],
    )
    scene = AUTH.accept_artifacts(dataset, [candidate["id"]])[0]
    dataset["prose"]["beats"]["scene-013"] = {
        "id": "beats-scene-013",
        "surface": "prose.beats",
        "authority_class": "production_approved",
        "revision": "beats-scene-013-r1",
        "target_scope": "scene-013",
        "beats": ["Mara evaluates the break.", "Mara finds another crossing."],
    }
    dataset["prose"]["modes"]["default"] = {
        "id": "mode-default",
        "surface": "prose.modes",
        "authority_class": "production_approved",
        "revision": "mode-default-r1",
        "viewpoint": "close third through Mara",
    }
    return scene


def task_planning_binding() -> bool:
    for rel in (
        "product/planning/FS-008-live-dependency-semantic-alignment/functional-set.md",
        "product/planning/FS-008-live-dependency-semantic-alignment/plan.md",
    ):
        text = (ROOT / rel).read_text(encoding="utf-8")
        if not check(
            f"design_revision: {DESIGN_REVISION}" in text,
            f"{rel}: missing exact FS-008 Design binding",
        ):
            return False
    return check(REQS.is_file(), "FS-008 normative requirements missing")


def task_ruleset_contract() -> bool:
    governed = json.loads((ROOT / "ruleset/governed-state.json").read_text(encoding="utf-8"))
    reconciliation = json.loads((ROOT / "ruleset/reconciliation.json").read_text(encoding="utf-8"))
    compatibility = json.loads((ROOT / "ruleset/compatibility.json").read_text(encoding="utf-8"))
    dep = governed["dependency_model"]
    transition_ids = {
        item.get("id")
        for item in compatibility["migration"]["supported_transitions"]
        if isinstance(item, dict)
    }
    rebind_ids = {
        item.get("id")
        for item in compatibility["rebinding"]["supported_transitions"]
        if isinstance(item, dict)
    }
    return (
        check(
            dep["required_fields"] == ["target_id", "authority_basis", "material"],
            "FS-008: governed live dependency still requires target_revision",
        )
        and check(
            dep.get("live_relation_uses_stable_target_identity") is True
            and dep.get("alignment_evidence_is_revision_specific") is True,
            "FS-008: governed-state separation flags missing",
        )
        and check(
            reconciliation["reconciliation"].get(
                "successful_reconciliation_advances_alignment_evidence"
            )
            is True,
            "FS-008: reconciliation alignment rule missing",
        )
        and check(
            "dependency-relations-v1-to-live-alignment-v1" in transition_ids,
            "FS-008: governed legacy dependency migration missing",
        )
        and check(
            compatibility["ruleset_binding"]["current"]["version"] == "0.5.0"
            and "ruleset-0.4.0-to-0.5.0" in rebind_ids,
            "FS-008: changed Ruleset realization is not distinctly identified and rebound",
        )
    )


def task_live_dependency_alignment() -> bool:
    dataset = _dataset()
    scene = _accepted_scene(dataset)
    relation = scene["dependency_relations"][1]
    if not check(
        relation["target_id"] == "event-bridge"
        and "target_revision" not in relation,
        "FS-008: new live dependency is revision-pinned",
    ):
        return False

    old_event_revision = REV._artifact(dataset, "event-bridge")["revision"]
    old_package = SCENE.build_generation_package(
        SCENE.build_production_contract(dataset, "scene-013")
    )
    candidate = REV.propose_revision(
        dataset,
        "event-bridge",
        {"summary": "The bridge is broken and the ford is flooded."},
    )
    change = REV.accept_revision(dataset, candidate["id"])
    impact = next(
        item
        for item in REV.analyze_impact(dataset, change)
        if item["dependent_id"] == "scene-013"
    )
    scene = REV._artifact(dataset, "scene-013")
    if not check(
        impact["state"] == "review_required"
        and scene["dependency_relations"][1]["target_id"] == "event-bridge"
        and "target_revision" not in scene["dependency_relations"][1]
        and scene["alignment"]["dependencies"]["event-bridge"] == old_event_revision,
        "FS-008: upstream revision changed live identity or failed to stale alignment",
    ):
        return False

    REV.reconcile(dataset, "scene-013", impact["id"], "preserve")
    scene = REV._artifact(dataset, "scene-013")
    current_event_revision = REV._artifact(dataset, "event-bridge")["revision"]
    if not check(
        scene["dependency_relations"][1]["target_id"] == "event-bridge"
        and "target_revision" not in scene["dependency_relations"][1]
        and scene["alignment"]["dependencies"]["event-bridge"]
        == current_event_revision,
        "FS-008: reconciliation did not advance alignment while preserving identity",
    ):
        return False

    REV.ensure_artifact_current(dataset, scene)
    new_package = SCENE.build_generation_package(
        SCENE.build_production_contract(dataset, "scene-013")
    )
    return (
        check(
            old_package["selected_revisions"]["dependencies"]["event-bridge"]
            == old_event_revision,
            "FS-008: frozen old package provenance changed",
        )
        and check(
            new_package["selected_revisions"]["dependencies"]["event-bridge"]
            == current_event_revision,
            "FS-008: new package did not select current dependency revision",
        )
    )


def task_generation_independence() -> bool:
    dataset = _dataset()
    _accepted_scene(dataset)

    # Establish the one bounded automatic Plot convenience that the current
    # compiler may select: the immediate prior scene. Capture the target package
    # after that local context exists, then grow the rest of the novel around it.
    prior = {
        "id": "scene-scale-012",
        "surface": "plot.sequence",
        "authority_class": "accepted_semantic",
        "revision": "scene-scale-012-r1",
        "ordinal": 12,
        "viewpoint": "character-mara",
        "entry": "Mara approaches the river.",
        "required_movements": ["Mara sees the river ahead."],
        "exit": "Mara reaches the riverbank.",
        "dependencies": ["character-mara"],
        "dependency_relations": [{
            "target_id": "character-mara",
            "authority_basis": "accepted",
            "material": True,
        }],
        "alignment": {
            "dependencies": {
                "character-mara": "character-mara-r1",
            }
        },
    }
    dataset["plot"]["sequence"].append(prior)

    before = SCENE.build_generation_package(
        SCENE.build_production_contract(dataset, "scene-013")
    )
    before_payload_size = len(
        json.dumps(before["generator_payload"], sort_keys=True)
    )

    # Grow the Dataset to a 100-scene novel-shaped dependency graph. The target
    # remains scene-013 and scene-scale-012 remains its immediate prior Plot
    # context. The other 98 scenes, their Canon dependencies, Prose controls,
    # and accepted Manuscript are deliberately unrelated to the target.
    for event_number in range(1, 31):
        dataset["canon"]["events"].append({
            "id": f"event-scale-{event_number:03d}",
            "surface": "canon.events",
            "authority_class": "accepted_semantic",
            "revision": f"event-scale-{event_number:03d}-r1",
            "summary": f"Synthetic novel-scale continuity event {event_number}.",
        })

    other_ordinals = [
        ordinal
        for ordinal in range(1, 101)
        if ordinal not in {12, 13}
    ]
    for ordinal in other_ordinals:
        first_event = (ordinal % 30) + 1
        second_event = ((ordinal + 11) % 30) + 1
        dependencies = [
            "character-mara",
            f"event-scale-{first_event:03d}",
            f"event-scale-{second_event:03d}",
        ]
        alignment = {
            target_id: (
                "character-mara-r1"
                if target_id == "character-mara"
                else f"{target_id}-r1"
            )
            for target_id in dependencies
        }
        scene_id = f"scene-scale-{ordinal:03d}"
        dataset["plot"]["sequence"].append({
            "id": scene_id,
            "surface": "plot.sequence",
            "authority_class": "accepted_semantic",
            "revision": f"{scene_id}-r1",
            "ordinal": ordinal,
            "viewpoint": "character-mara",
            "entry": f"Synthetic entry for scene {ordinal}.",
            "required_movements": [
                f"Synthetic governed movement for scene {ordinal}."
            ],
            "exit": f"Synthetic exit for scene {ordinal}.",
            "dependencies": dependencies,
            "dependency_relations": [
                {
                    "target_id": target_id,
                    "authority_basis": "accepted",
                    "material": True,
                }
                for target_id in dependencies
            ],
            "alignment": {"dependencies": alignment},
        })
        dataset["prose"]["beats"][scene_id] = {
            "id": f"beats-{scene_id}",
            "surface": "prose.beats",
            "authority_class": "production_approved",
            "revision": f"beats-{scene_id}-r1",
            "target_scope": scene_id,
            "beats": [f"Synthetic beat for scene {ordinal}."],
        }
        dataset["chapters"]["files"].append({
            "id": f"manuscript-{scene_id}",
            "surface": "manuscript",
            "authority_class": "accepted_manuscript",
            "revision": f"manuscript-{scene_id}-r1",
            "ordinal": ordinal,
            "plot_scope": scene_id,
            "path": f"chapters/scale-{ordinal:03d}.md",
            "content": (
                f"Synthetic accepted prose for unrelated scene {ordinal}. " * 20
            ),
        })

    # Add accepted Manuscript for the one immediate-prior scene only after the
    # baseline package was captured. Its appearance must not alter target-scene
    # continuity, because prior Manuscript is not a routine continuity source.
    dataset["chapters"]["files"].append({
        "id": "manuscript-scene-scale-012",
        "surface": "manuscript",
        "authority_class": "accepted_manuscript",
        "revision": "manuscript-scene-scale-012-r1",
        "ordinal": 12,
        "plot_scope": "scene-scale-012",
        "path": "chapters/scale-012.md",
        "content": "Immediate-prior prose that must not enter target context. " * 20,
    })

    after = SCENE.build_generation_package(
        SCENE.build_production_contract(dataset, "scene-013")
    )
    after_payload_size = len(
        json.dumps(after["generator_payload"], sort_keys=True)
    )
    payload_text = json.dumps(after["generator_payload"], sort_keys=True)
    total_dependency_edges = sum(
        len(scene.get("dependency_relations", []))
        for scene in dataset["plot"]["sequence"]
        if isinstance(scene, dict)
    )

    return (
        check(
            len(dataset["plot"]["sequence"]) == 100,
            "FS-008: novel-scale fixture did not contain exactly 100 scenes",
        )
        and check(
            total_dependency_edges >= 250,
            "FS-008: novel-scale fixture did not exercise a material dependency graph",
        )
        and check(
            len(dataset["chapters"]["files"]) == 99,
            "FS-008: novel-scale fixture did not exercise accepted Manuscript growth",
        )
        and check(
            "prior_manuscript" not in after["selected_revisions"],
            "FS-008: package still records routine prior Manuscript revisions",
        )
        and check(
            "accepted_prior_manuscript"
            not in after["generator_payload"]["scene_contract"],
            "FS-008: generator payload exposes routine prior Manuscript",
        )
        and check(
            before["generator_payload"] == after["generator_payload"],
            "FS-008: generator payload changed when unrelated novel-scale state was added",
        )
        and check(
            before_payload_size == after_payload_size,
            "FS-008: generator payload size grew with total story size",
        )
        and check(
            before["id"] == after["id"],
            "FS-008: package identity changed from unrelated novel-scale state",
        )
        and check(
            "event-scale-" not in payload_text,
            "FS-008: unrelated Canon leaked into the target generation package",
        )
        and check(
            "Synthetic accepted prose" not in payload_text
            and "Immediate-prior prose" not in payload_text,
            "FS-008: unrelated or prior Manuscript leaked into target generation context",
        )
        and check(
            "The bridge is broken before the later scene begins." in payload_text,
            "FS-008: required Canon continuity was not compiled into target package",
        )
    )

def task_compatibility_migration() -> bool:
    dataset = _dataset()
    _accepted_scene(dataset)
    scene = REV._artifact(dataset, "scene-013")
    relation = scene["dependency_relations"][1]
    aligned = scene["alignment"]["dependencies"]["event-bridge"]
    relation["target_revision"] = aligned
    scene.pop("alignment", None)
    scene["generation_provenance"] = {
        "package_snapshot": {
            "historical_relation": {
                "target_id": "event-bridge",
                "target_revision": "historical-package-r7",
            }
        }
    }
    historical = copy.deepcopy(scene["generation_provenance"])

    status = COMPAT.classify(dataset)
    if not check(
        status.get("state") == "migration_required"
        and status.get("transition")
        == "dependency-relations-v1-to-live-alignment-v1",
        "FS-008: legacy pinned relation did not require governed migration",
    ):
        return False

    migrated = COMPAT.migrate(
        dataset,
        status["transition"],
        authorized=True,
    )
    migrated_scene = REV._artifact(migrated, "scene-013")
    migrated_relation = migrated_scene["dependency_relations"][1]
    return (
        check(
            "target_revision" not in migrated_relation
            and migrated_relation["target_id"] == "event-bridge",
            "FS-008: migration did not produce stable live dependency identity",
        )
        and check(
            migrated_scene["alignment"]["dependencies"]["event-bridge"] == aligned,
            "FS-008: migration lost historical alignment revision",
        )
        and check(
            migrated_scene["generation_provenance"] == historical,
            "FS-008: migration rewrote historical generation provenance",
        )
        and check(
            COMPAT.classify(migrated).get("state") == "directly_compatible",
            "FS-008: migrated Dataset is not directly compatible",
        )
    )


def task_dataset_boundary() -> bool:
    return check(
        not (ROOT / "dataset").exists(),
        "FS-008: story Dataset instance must remain external",
    )


def task_manifest_bindings() -> bool:
    text = REQS.read_text(encoding="utf-8")
    parsed = re.findall(
        r"^### (FS-008-NR-\\d{3}).*?\\n\\*\\*Classification: ([MSB])\\*\\*",
        text,
        re.M | re.S,
    )
    required = {rid for rid, cls in parsed if cls in {"M", "B"}}
    forbidden = {rid for rid, cls in parsed if cls == "S"}
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    bound = {
        item.get("requirement")
        for item in manifest["bindings"]
        if isinstance(item, dict)
    }
    return (
        check(
            required <= bound,
            f"manifest missing FS-008 bindings: {sorted(required - bound)}",
        )
        and check(
            not (forbidden & bound),
            f"manifest binds semantic-only FS-008 requirements: {sorted(forbidden & bound)}",
        )
    )


TASKS = {
    "fs008-planning-binding": task_planning_binding,
    "fs008-ruleset-contract": task_ruleset_contract,
    "fs008-live-dependency-alignment": task_live_dependency_alignment,
    "fs008-generation-independence": task_generation_independence,
    "fs008-compatibility-migration": task_compatibility_migration,
    "fs008-dataset-boundary": task_dataset_boundary,
    "fs008-manifest-bindings": task_manifest_bindings,
}
