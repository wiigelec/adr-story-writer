from __future__ import annotations

import copy
import importlib.util
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any, Callable

ROOT = Path(__file__).resolve().parents[2]
REQS = ROOT / "product" / "specs" / "FS-003-requirements.md"
MANIFEST = ROOT / "product" / "validation" / "requirement-evaluation.json"
DESIGN_REVISION = "58ebbd0c90060c1fce9da6ac4e18835032ed2336"


def check(condition: bool, message: str) -> bool:
    if not condition:
        print(f"FAIL product-validation: {message}")
        return False
    return True


def _load_runtime():
    path = ROOT / "product" / "src" / "scene_runtime.py"
    spec = importlib.util.spec_from_file_location("fs003_scene_runtime", path)
    if spec is None or spec.loader is None:
        raise ValueError("cannot load FS-003 scene runtime")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def _fixture(root: Path) -> None:
    d = root / "dataset"
    _write_json(d / "instance.json", {"id": "sw-test-story"})
    _write_json(d / "story.json", {
        "application": "adr-story-writer",
        "dataset_role": "story",
        "title": "The Lantern at Red Hollow",
        "status": "active",
    })
    _write_json(d / "canon/character.json", {
        "mara-venn": {
            "id": "character-mara-venn",
            "surface": "canon.character",
            "authority_class": "accepted_semantic",
            "revision": "canon-mara-r1",
            "name": "Mara Venn",
            "knowledge": [
                "A lightning storm damaged the west telegraph span before her arrival.",
                "Eli Rusk is the caretaker at Red Hollow.",
                "A sealed railway dispatch satchel is hidden beneath the signal-shed floor.",
            ],
            "does_not_know": [
                "Why Eli concealed the dispatch satchel."
            ],
        },
        "eli-rusk": {
            "id": "character-eli-rusk",
            "surface": "canon.character",
            "authority_class": "accepted_semantic",
            "revision": "canon-eli-r1",
            "name": "Eli Rusk",
            "knowledge": [
                "A sealed railway dispatch satchel is hidden beneath the signal-shed floor."
            ],
        },
    })
    _write_json(d / "canon/setting.json", {
        "red-hollow": {
            "id": "setting-red-hollow",
            "surface": "canon.setting",
            "authority_class": "accepted_semantic",
            "revision": "canon-setting-r1",
            "name": "Red Hollow Relay Station",
        }
    })
    _write_json(d / "canon/events.json", [
        {
            "id": "event-storm",
            "surface": "canon.events",
            "authority_class": "accepted_semantic",
            "revision": "canon-event-storm-r1",
            "summary": "A lightning storm damages the west telegraph span.",
        },
        {
            "id": "event-satchel-hidden",
            "surface": "canon.events",
            "authority_class": "accepted_semantic",
            "revision": "canon-event-satchel-r1",
            "summary": "Eli conceals a sealed railway dispatch satchel beneath the signal-shed floor.",
            "known_by": ["character-eli-rusk"],
            "concealed_from": [
                "character-mara-venn",
                "reader-through-scene-002-signal-shed",
            ],
        },
        {
            "id": "event-mara-arrives",
            "surface": "canon.events",
            "authority_class": "accepted_semantic",
            "revision": "canon-event-arrival-r1",
            "summary": "Mara arrives at Red Hollow to restore telegraph service.",
        },
    ])
    _write_json(d / "plot/synopsis.json", {
        "id": "plot-synopsis",
        "surface": "plot.synopsis",
        "authority_class": "accepted_semantic",
        "revision": "plot-synopsis-r1",
        "summary": "Mara investigates storm damage while Eli withholds a consequential fact.",
    })
    _write_json(d / "plot/outline.json", [{
        "id": "outline-opening",
        "surface": "plot.outline",
        "authority_class": "accepted_semantic",
        "revision": "plot-outline-r1",
        "scene_ids": [
            "scene-001-arrival",
            "scene-002-signal-shed",
            "scene-003-first-message",
        ],
    }])
    _write_json(d / "plot/sequence.json", [
        {
            "id": "scene-001-arrival",
            "surface": "plot.sequence",
            "authority_class": "accepted_semantic",
            "revision": "plot-scene-001-r1",
            "ordinal": 1,
            "viewpoint": "character-mara-venn",
            "entry": "Mara approaches the station.",
            "exit": "Eli says the relay is dead.",
            "dependencies": ["event-storm", "event-mara-arrives", "setting-red-hollow"],
        },
        {
            "id": "scene-002-signal-shed",
            "surface": "plot.sequence",
            "authority_class": "accepted_semantic",
            "revision": "plot-scene-002-r1",
            "title": "The Signal Shed",
            "ordinal": 2,
            "viewpoint": "character-mara-venn",
            "setting": "the signal shed at Red Hollow Relay Station",
            "purpose": "Diagnose the relay without revealing Eli's hidden satchel.",
            "entry": "Mara and Eli enter the signal shed.",
            "required_movements": [
                "Mara verifies that the relay is intact.",
                "Mara notices a recently disturbed floorboard.",
                "Eli redirects attention toward the west span.",
            ],
            "exit": "Mara decides to inspect the west span.",
            "dependencies": [
                "character-mara-venn",
                "character-eli-rusk",
                "setting-red-hollow",
                "event-storm",
                "event-satchel-hidden",
            ],
            "reader_information": {
                "may_reveal": [
                    "The relay is not the primary fault.",
                    "A floorboard appears disturbed.",
                ],
                "must_conceal": [
                    "event-satchel-hidden",
                    "The existence of the dispatch satchel.",
                ],
            },
        },
        {
            "id": "scene-003-first-message",
            "surface": "plot.sequence",
            "authority_class": "accepted_semantic",
            "revision": "plot-scene-003-r1",
            "ordinal": 3,
            "viewpoint": "character-mara-venn",
            "purpose": "Mara sends the first restored message.",
            "entry": "Mara returns after repairing the span.",
            "exit": "She records a traffic-log discrepancy.",
            "dependencies": [
                "scene-002-signal-shed",
                "event-storm",
                "character-mara-venn",
            ],
        },
    ])
    _write_json(d / "prose/beats.json", {
        "scene-002-signal-shed": {
            "id": "beats-scene-002",
            "surface": "prose.beats",
            "authority_class": "production_approved",
            "revision": "prose-beats-002-r1",
            "target_scope": "scene-002-signal-shed",
            "beats": [
                "Mara tests the relay.",
                "The local test succeeds.",
                "Mara notices the disturbed floorboard.",
                "They leave for the west span.",
            ],
            "protected_meaning": [
                "Mara must not discover the satchel in this scene.",
                "The reader must not be told that a satchel exists.",
            ],
        },
        "scene-003-first-message": {
            "id": "beats-scene-003",
            "surface": "prose.beats",
            "authority_class": "production_approved",
            "revision": "prose-beats-003-r1",
            "target_scope": "scene-003-first-message",
            "beats": ["Mara sends a message.", "Mara notices a log discrepancy."],
        },
    })
    _write_json(d / "prose/modes.json", {
        "default-scene-mode": {
            "id": "mode-close-third-mara",
            "surface": "prose.modes",
            "authority_class": "production_approved",
            "revision": "prose-mode-r1",
            "viewpoint": "close third person through Mara",
            "style": [
                "concrete physical observation",
                "no omniscient explanation of concealed facts",
            ],
        }
    })
    _write_json(d / "prose/pseudo-prose.json", {
        "scene-002-signal-shed": {
            "id": "pseudo-scene-002",
            "surface": "prose.pseudo_prose",
            "authority_class": "production_approved",
            "revision": "prose-pseudo-002-r1",
            "target_scope": "scene-002-signal-shed",
            "opening_shape": "enter through practical diagnosis rather than exposition",
            "closing_shape": "leave on the stronger west-span lead",
            "units": [
                {
                    "unit_id": "unit-relay",
                    "primary_mode": "action",
                    "content_movement": "The relay test succeeds.",
                },
                {
                    "unit_id": "unit-floorboard",
                    "primary_mode": "internal",
                    "content_movement": "Mara notices the floorboard.",
                },
                {
                    "unit_id": "unit-exit",
                    "primary_mode": "action",
                    "content_movement": "They leave for the west span.",
                },
            ],
        },
        "scene-003-first-message": {
            "id": "pseudo-scene-003",
            "surface": "prose.pseudo_prose",
            "authority_class": "production_approved",
            "revision": "prose-pseudo-003-r1",
            "target_scope": "scene-003-first-message",
            "units": ["Mara sends the message.", "The log entry troubles her."],
        },
    })
    _write_json(d / "chapters/manifest.json", {
        "format": "markdown",
        "files": [{
            "id": "manuscript-scene-001",
            "surface": "manuscript",
            "authority_class": "accepted_manuscript",
            "revision": "manuscript-scene-001-r1",
            "ordinal": 1,
            "plot_scope": "scene-001-arrival",
            "path": "chapters/001.md",
        }],
    })
    (d / "chapters/001.md").write_text(
        "# Chapter 1\n\nMara arrives at Red Hollow and asks to inspect the dead relay.\n",
        encoding="utf-8",
    )


def task_planning_binding() -> bool:
    for rel in (
        "product/planning/FS-003-governed-scene-production-and-session-reconstruction/functional-set.md",
        "product/planning/FS-003-governed-scene-production-and-session-reconstruction/plan.md",
    ):
        text = (ROOT / rel).read_text(encoding="utf-8")
        if not check(
            f"design_revision: {DESIGN_REVISION}" in text,
            f"{rel}: missing exact FS-003 Design binding",
        ):
            return False
    return check(REQS.is_file(), "FS-003 normative requirements missing")


def _exercise() -> tuple[Any, dict[str, Any]]:
    rt = _load_runtime()
    temp = tempfile.TemporaryDirectory()
    root = Path(temp.name)
    _fixture(root)

    try:
        rt.open_scene_session(root)
    except rt.CompatibilityGateError as exc:
        if not check(exc.status.get("state") == "migration_required", "FS-003: legacy Dataset bypassed compatibility gate"):
            temp.cleanup()
            raise AssertionError("compatibility gate failed")
    else:
        temp.cleanup()
        raise AssertionError("FS-003: legacy Dataset unexpectedly admitted")

    session = rt.open_scene_session(root, authorize_transition=True)
    context = session.context("scene-002-signal-shed")
    contract = session.contract("scene-002-signal-shed")
    package = rt.build_generation_package(contract)
    return (temp, {
        "rt": rt,
        "root": root,
        "session": session,
        "context": context,
        "contract": contract,
        "package": package,
    })


def task_scene_runtime() -> bool:
    temp, env = _exercise()
    try:
        rt = env["rt"]
        context = env["context"]
        contract = env["contract"]
        package = env["package"]

        production_rules = json.loads(
            (ROOT / "ruleset/production.json").read_text(encoding="utf-8")
        )
        if not check(
            "generator_payload"
            in production_rules["generation_package"]["required_fields"]
            and production_rules["information_access"][
                "supports_generator_visible_context"
            ]
            is False
            and production_rules["information_access"][
                "supports_compiled_generator_payload"
            ]
            is True,
            "FS-003: production Ruleset still advertises the retired broad generator context",
        ):
            return False

        compiler_payload = json.dumps(
            context["generator_visible"],
            ensure_ascii=False,
        ).lower()
        reviewer_payload = json.dumps(
            context["reviewer_only"],
            ensure_ascii=False,
        ).lower()
        if not check(
            "does_not_know" not in compiler_payload,
            "FS-003: negative viewpoint knowledge leaked into compiler projection",
        ):
            return False
        if not check(
            "dispatch satchel" in reviewer_payload,
            "FS-003: reviewer-only concealed fact missing",
        ):
            return False
        if not check(
            contract["stop_boundary"] == "Mara decides to inspect the west span.",
            "FS-003: explicit stop boundary missing",
        ):
            return False
        if not check(
            contract["reveal_concealment"]["reviewer_only"],
            "FS-003: contract omitted reviewer-only concealment constraints",
        ):
            return False
        if not check(
            package["target_scope"] == "scene-002-signal-shed",
            "FS-003: package target incorrect",
        ):
            return False
        if not check(
            "generator_visible_context" not in package,
            "FS-003: package still exposes broad upstream generator context",
        ):
            return False
        generation = package.get("generator_payload")
        if not check(
            isinstance(generation, dict)
            and set(generation)
            == {"scene_contract", "style_projection", "pseudo_prose"},
            "FS-003: package generator payload is not the compiled scene/style/pseudo-prose interface",
        ):
            return False
        scene_contract = generation["scene_contract"]
        if not check(
            scene_contract["identity"]["title"] == "The Signal Shed"
            and scene_contract["setting"]
            == "the signal shed at Red Hollow Relay Station"
            and scene_contract["opening_state"]
            == "Mara and Eli enter the signal shed."
            and scene_contract["stop_condition"]
            == "Mara decides to inspect the west span."
            and scene_contract["narrative_movement"]
            == [
                "Mara verifies that the relay is intact.",
                "Mara notices a recently disturbed floorboard.",
                "Eli redirects attention toward the west span.",
            ]
            and scene_contract["realization_shape"]
            == {
                "opening": [
                    "enter through practical diagnosis rather than exposition"
                ],
                "closing": ["leave on the stronger west-span lead"],
            },
            "FS-003: compiled scene contract lost governed scene movement or shape",
        ):
            return False
        prior = scene_contract["continuity"]["immediate_prior_scene"]
        if not check(
            isinstance(prior, dict)
            and prior["id"] == "scene-001-arrival"
            and prior["exit"] == "Eli says the relay is dead."
            and "content" not in prior,
            "FS-003: immediate same-viewpoint Plot state was not compiled safely",
        ):
            return False
        if not check(
            generation["pseudo_prose"]
            == [
                {
                    "unit_id": "unit-relay",
                    "primary_mode": "action",
                    "content_movement": "The relay test succeeds.",
                },
                {
                    "unit_id": "unit-floorboard",
                    "primary_mode": "internal",
                    "content_movement": "Mara notices the floorboard.",
                },
                {
                    "unit_id": "unit-exit",
                    "primary_mode": "action",
                    "content_movement": "They leave for the west span.",
                },
            ],
            "FS-003: structured production-approved pseudo-prose was not preserved in order",
        ):
            return False
        compiled_payload = json.dumps(generation, ensure_ascii=False).lower()
        if not check(
            "dispatch satchel" not in compiled_payload,
            "FS-003: viewpoint knowledge or concealed Plot material leaked into compiled generator payload",
        ):
            return False
        if not check(
            "knowledge" not in generation["scene_contract"]["viewpoint"],
            "FS-003: raw viewpoint knowledge remained generator-visible without Plot reveal authorization",
        ):
            return False
        if not check(
            "accepted_dependencies" not in generation
            and "accepted_prior_manuscript" not in generation,
            "FS-003: raw upstream artifacts remain routine generator inputs",
        ):
            return False
        if not check(
            package == rt.build_generation_package(copy.deepcopy(contract)),
            "FS-003: generation package is not stable for identical governing state",
        ):
            return False

        selected = package["selected_revisions"]
        if not check(
            selected["prose_controls"]["beats"].get("beats-scene-002")
            == "prose-beats-002-r1",
            "FS-003: Beat revision missing from package provenance",
        ):
            return False
        if not check(
            selected["prose_controls"]["modes"].get("mode-close-third-mara")
            == "prose-mode-r1",
            "FS-003: Mode revision missing from package provenance",
        ):
            return False
        if not check(
            selected["prior_scene"].get("scene-001-arrival")
            == "plot-scene-001-r1",
            "FS-003: compiled prior Plot revision missing from package provenance",
        ):
            return False
        if not check(
            selected["prior_manuscript"].get("manuscript-scene-001")
            == "manuscript-scene-001-r1",
            "FS-003: prior Manuscript revision missing from package provenance",
        ):
            return False

        candidate_prior = copy.deepcopy(env["session"].dataset)
        for prior_scene in candidate_prior["plot"]["sequence"]:
            if prior_scene.get("id") == "scene-001-arrival":
                prior_scene["authority_class"] = "candidate_semantic"
        candidate_prior_package = rt.build_generation_package(
            rt.build_production_contract(
                candidate_prior,
                "scene-002-signal-shed",
            )
        )
        if not check(
            candidate_prior_package["generator_payload"]["scene_contract"][
                "continuity"
            ]["immediate_prior_scene"]
            is None
            and candidate_prior_package["selected_revisions"]["prior_scene"]
            == {},
            "FS-003: candidate prior Plot state silently governed continuity",
        ):
            return False

        no_movement = copy.deepcopy(env["session"].dataset)
        for target_scene in no_movement["plot"]["sequence"]:
            if target_scene.get("id") == "scene-002-signal-shed":
                target_scene.pop("required_movements", None)
        no_movement_contract = rt.build_production_contract(
            no_movement,
            "scene-002-signal-shed",
        )
        no_movement_scene = no_movement_contract["scene_contract"]
        if not check(
            no_movement_scene["narrative_movement"] == []
            and no_movement_scene["information_access"]["may_reveal"]
            == [
                "The relay is not the primary fault.",
                "A floorboard appears disturbed.",
            ],
            "FS-003: reveal permission was promoted into narrative movement",
        ):
            return False

        broken = copy.deepcopy(env["session"].dataset)
        broken["canon"]["events"] = [
            event
            for event in broken["canon"]["events"]
            if event.get("id") != "event-storm"
        ]
        try:
            rt.project_scene_context(broken, "scene-002-signal-shed")
        except rt.SceneNotReadyError:
            pass
        else:
            return check(
                False,
                "FS-003: missing material context was guessed instead of refused",
            )

        unknown_authority = copy.deepcopy(env["session"].dataset)
        for event in unknown_authority["canon"]["events"]:
            if event.get("id") == "event-storm":
                event.pop("authority_class", None)
        try:
            rt.project_scene_context(
                unknown_authority,
                "scene-002-signal-shed",
            )
        except rt.SceneNotReadyError:
            pass
        else:
            return check(
                False,
                "FS-003: missing authority was inferred as accepted",
            )

        unapproved_prose = copy.deepcopy(env["session"].dataset)
        unapproved_prose["prose"]["beats"]["scene-002-signal-shed"][
            "authority_class"
        ] = "production_candidate"
        try:
            rt.project_scene_context(
                unapproved_prose,
                "scene-002-signal-shed",
            )
        except rt.SceneNotReadyError:
            pass
        else:
            return check(
                False,
                "FS-003: non-approved Prose control governed generation",
            )

        candidate_dependency = copy.deepcopy(env["session"].dataset)
        for event in candidate_dependency["canon"]["events"]:
            if event.get("id") == "event-storm":
                event["authority_class"] = "candidate_semantic"
        candidate_contract = rt.build_production_contract(
            candidate_dependency,
            "scene-002-signal-shed",
        )
        candidate_package = rt.build_generation_package(candidate_contract)
        candidate_text = rt.create_candidate(
            candidate_package,
            "Mara tests the relay and follows the evidence west.",
            40,
        )
        rt.review_candidate(candidate_text, candidate_package)
        try:
            rt.accept_candidate(candidate_text, candidate_package)
        except rt.AcceptanceError:
            pass
        else:
            return check(
                False,
                "FS-003: candidate semantic dependency bypassed acceptance closure",
            )

        candidate_target = copy.deepcopy(env["session"].dataset)
        for scene in candidate_target["plot"]["sequence"]:
            if scene.get("id") == "scene-002-signal-shed":
                scene["authority_class"] = "candidate_semantic"
        candidate_target_package = rt.build_generation_package(
            rt.build_production_contract(
                candidate_target,
                "scene-002-signal-shed",
            )
        )
        target_attempt = rt.create_candidate(
            candidate_target_package,
            "Mara tests the relay and follows the evidence west.",
            41,
        )
        rt.review_candidate(target_attempt, candidate_target_package)
        try:
            rt.accept_candidate(target_attempt, candidate_target_package)
        except rt.AcceptanceError:
            pass
        else:
            return check(
                False,
                "FS-003: candidate target Plot scope bypassed acceptance closure",
            )

        bad = rt.create_candidate(
            package,
            "Mara saw the loose board and somehow understood that Eli had hidden "
            "a sealed railway dispatch satchel beneath it.",
            1,
        )
        review = rt.review_candidate(
            bad,
            package,
            [{
                "dimension": "reveal_concealment",
                "material": True,
                "detail": "Candidate reveals reviewer-only dispatch satchel.",
            }],
        )
        if not check(
            review["outcome"] == "non_conforming",
            "FS-003: violating candidate not rejected",
        ):
            return False
        if not check(
            bad["authority_class"] == "candidate_manuscript",
            "FS-003: rejected candidate authority changed",
        ):
            return False
        try:
            rt.accept_candidate(bad, package)
        except rt.AcceptanceError:
            pass
        else:
            return check(False, "FS-003: non-conforming candidate was accepted")

        indeterminate = rt.create_candidate(
            package,
            "Mara tests the relay.",
            2,
        )
        rt.review_candidate(indeterminate, package, indeterminate=True)
        try:
            rt.accept_candidate(indeterminate, package)
        except rt.AcceptanceError:
            pass
        else:
            return check(False, "FS-003: indeterminate candidate was accepted")

        unresolved = rt.create_candidate(
            package,
            "Mara tests the relay and makes a new consequential inference.",
            3,
        )
        rt.review_candidate(
            unresolved,
            package,
            unresolved_consequential_dependencies=[{
                "id": "candidate-new-motive",
                "owning_surface": "canon",
                "material": True,
            }],
        )
        try:
            rt.accept_candidate(unresolved, package)
        except rt.AcceptanceError:
            pass
        else:
            return check(
                False,
                "FS-003: unresolved consequential invention bypassed acceptance closure",
            )

        tampered = copy.deepcopy(package)
        tampered["stop_boundary"] = "A different stopping boundary."
        try:
            rt.create_candidate(
                tampered,
                "Mara tests the relay.",
                4,
            )
        except rt.SceneRuntimeError:
            pass
        else:
            return check(
                False,
                "FS-003: mutated frozen package governed a generation attempt",
            )

        good = rt.create_candidate(
            package,
            "Mara tested the relay until its armature clicked cleanly. "
            "The fault lay farther west. When she shifted her knee she noticed "
            "one floorboard had cleaner edges than its neighbors, an oddity she "
            "filed away while Eli pointed toward the storm-hit span. The line "
            "fault was the stronger lead, so she packed her meter and followed "
            "him outside.",
            5,
        )
        rt.review_candidate(good, package)
        accepted = rt.accept_candidate(good, package)
        if not check(
            accepted["authority_class"] == "accepted_manuscript",
            "FS-003: conforming candidate not accepted",
        ):
            return False
        if not check(
            accepted["generation_provenance"]["package_snapshot"] == package,
            "FS-003: accepted candidate lost frozen package provenance",
        ):
            return False
        if not check(
            not (
                env["root"]
                / "dataset"
                / "chapters"
                / "002-scene-002-signal-shed.md"
            ).exists(),
            "FS-003: acceptance incorrectly implied persistence",
        ):
            return False
        return True
    finally:
        temp.cleanup()

def task_persistence_reconstruction() -> bool:
    temp, env = _exercise()
    try:
        rt = env["rt"]
        session = env["session"]
        package = env["package"]
        good = rt.create_candidate(
            package,
            "Mara proved the relay worked locally, noticed the clean edge of one "
            "floorboard, and chose to inspect the west span because the "
            "diagnostic evidence pointed there.",
            20,
        )
        rt.review_candidate(good, package)
        accepted = rt.accept_candidate(good, package)
        session.persist_accepted(accepted)

        chapter_path = (
            env["root"]
            / "dataset"
            / "chapters"
            / "002-scene-002-signal-shed.md"
        )
        if not check(
            chapter_path.is_file(),
            "FS-003: accepted Manuscript was not persisted",
        ):
            return False
        if not check(
            (env["root"] / "dataset" / "schema.json").is_file(),
            "FS-003: migrated schema identity was not persisted",
        ):
            return False
        if not check(
            (env["root"] / "dataset" / "ruleset-binding.json").is_file(),
            "FS-003: migrated Ruleset binding was not persisted",
        ):
            return False

        child_code = r"""
import importlib.util
import json
import sys
from pathlib import Path

runtime_path = Path(sys.argv[1])
root = Path(sys.argv[2])
spec = importlib.util.spec_from_file_location("fs003_child_runtime", runtime_path)
if spec is None or spec.loader is None:
    raise SystemExit("cannot load runtime")
rt = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rt)

session = rt.open_scene_session(root)
entries = [
    entry
    for entry in session.dataset["chapters"]["files"]
    if entry.get("plot_scope") == "scene-002-signal-shed"
]
context = session.context("scene-002-signal-shed")
next_scene = session.next_scene("scene-002-signal-shed")
next_context = session.context("scene-003-first-message")
next_package = session.package("scene-003-first-message")
entry = entries[0] if len(entries) == 1 else {}
print(json.dumps({
    "accepted_count": len(entries),
    "authority_class": entry.get("authority_class"),
    "generation_package_id": entry.get("generation_package_id"),
    "package_digest": (
        entry.get("generation_provenance", {}).get("package_digest")
    ),
    "selected_revisions": (
        entry.get("generation_provenance", {}).get("selected_revisions")
    ),
    "package_snapshot_target": (
        entry.get("generation_provenance", {})
        .get("package_snapshot", {})
        .get("target_scope")
    ),
    "current_target_count": len(
        context["generator_visible"]["current_target_manuscript"]
    ),
    "current_target_has_provenance": (
        bool(context["generator_visible"]["current_target_manuscript"])
        and "generation_provenance"
        in context["generator_visible"]["current_target_manuscript"][0]
    ),
    "next_scene": next_scene.get("id") if next_scene else None,
    "next_context": next_context.get("target_scope"),
    "next_generator_contains_satchel": (
        "dispatch satchel"
        in json.dumps(
            next_package["generator_payload"],
            ensure_ascii=False,
        ).lower()
    ),
    "next_prior_manuscript_contains_provenance": any(
        "generation_provenance" in item or "review" in item
        for item in next_context["generator_visible"]["accepted_prior_manuscript"]
    ),
    "next_prior_plot_dependency_contains_purpose": any(
        item.get("surface") == "plot.sequence" and "purpose" in item
        for item in next_context["generator_visible"]["accepted_dependencies"]
    ),
}))
"""
        completed = subprocess.run(
            [
                sys.executable,
                "-c",
                child_code,
                str(ROOT / "product" / "src" / "scene_runtime.py"),
                str(env["root"]),
            ],
            check=False,
            capture_output=True,
            text=True,
        )
        if not check(
            completed.returncode == 0,
            f"FS-003: fresh-process reconstruction failed: {completed.stderr}",
        ):
            return False
        reconstructed = json.loads(completed.stdout)
        if not check(
            reconstructed["accepted_count"] == 1,
            "FS-003: fresh process did not reconstruct accepted scene",
        ):
            return False
        if not check(
            reconstructed["authority_class"] == "accepted_manuscript",
            "FS-003: Manuscript acceptance lost after process restart",
        ):
            return False
        if not check(
            reconstructed["generation_package_id"] == package["id"],
            "FS-003: generation package identity lost after process restart",
        ):
            return False
        if not check(
            reconstructed["package_digest"]
            == package["provenance"]["package_digest"],
            "FS-003: generation package digest lost after process restart",
        ):
            return False
        if not check(
            reconstructed["selected_revisions"] == package["selected_revisions"],
            "FS-003: selected revision provenance lost after process restart",
        ):
            return False
        if not check(
            reconstructed["package_snapshot_target"]
            == "scene-002-signal-shed",
            "FS-003: frozen package context was not durably reconstructable",
        ):
            return False
        if not check(
            reconstructed["current_target_count"] == 1,
            "FS-003: current target Manuscript missing from reconstructed projection",
        ):
            return False
        if not check(
            reconstructed["current_target_has_provenance"] is False,
            "FS-003: Manuscript provenance leaked reviewer-only state into generator context",
        ):
            return False
        if not check(
            reconstructed["next_generator_contains_satchel"] is False,
            "FS-003: prior governed context leaked concealed Canon into next scene",
        ):
            return False
        if not check(
            reconstructed["next_prior_manuscript_contains_provenance"] is False,
            "FS-003: prior Manuscript exposed review/provenance to generation",
        ):
            return False
        if not check(
            reconstructed["next_prior_plot_dependency_contains_purpose"] is False,
            "FS-003: prior Plot dependency exposed reviewer-facing purpose text",
        ):
            return False
        if not check(
            reconstructed["next_scene"] == "scene-003-first-message",
            "FS-003: next scene continuation failed after process restart",
        ):
            return False
        if not check(
            reconstructed["next_context"] == "scene-003-first-message",
            "FS-003: next scene could not be prepared after process restart",
        ):
            return False

        # After a successful save the session has a new baseline. A later
        # external change must make the next save fail rather than overwrite it.
        story_path = env["root"] / "dataset" / "story.json"
        story = json.loads(story_path.read_text(encoding="utf-8"))
        story["external_change_marker"] = True
        _write_json(story_path, story)
        try:
            session.persist_accepted(accepted)
        except rt.PersistenceConflictError:
            pass
        else:
            return check(
                False,
                "FS-003: stale session overwrote newer persisted Dataset state",
            )

        return True
    finally:
        temp.cleanup()

def task_dataset_boundary() -> bool:
    return (
        check(not (ROOT / "dataset").exists(), "FS-003: story Dataset instance stored in Ruleset repository")
        and check(not (ROOT / "sw-test-story").exists(), "FS-003: reference story copied into Ruleset repository")
    )


def task_manifest_bindings() -> bool:
    text = REQS.read_text(encoding="utf-8")
    pattern = re.compile(
        r"^### (FS-003-NR-\d{3}).*?\n\*\*Classification: ([MSB])\*\*(?:\n\*\*State: (Inactive)\*\*)?",
        re.M | re.S,
    )
    parsed = pattern.findall(text)
    required = {rid for rid, cls, state in parsed if cls in {"M", "B"} and state != "Inactive"}
    forbidden = {rid for rid, cls, state in parsed if cls == "S" or state == "Inactive"}
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    bound = {b.get("requirement") for b in data["bindings"] if isinstance(b, dict)}
    return (
        check(required <= bound, f"manifest missing FS-003 mechanical bindings: {sorted(required - bound)}")
        and check(not (forbidden & bound), f"manifest binds FS-003 semantic/inactive requirements: {sorted(forbidden & bound)}")
    )


TASKS: dict[str, Callable[[], bool | None]] = {
    "fs003-planning-binding": task_planning_binding,
    "fs003-scene-runtime": task_scene_runtime,
    "fs003-persistence-reconstruction": task_persistence_reconstruction,
    "fs003-dataset-boundary": task_dataset_boundary,
    "fs003-manifest-bindings": task_manifest_bindings,
}
