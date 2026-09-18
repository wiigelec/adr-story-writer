from __future__ import annotations

import copy
import importlib.util
import json
import re
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
            ],
            "does_not_know": [
                "Eli concealed a sealed railway dispatch satchel beneath the signal-shed floor."
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
            "ordinal": 2,
            "viewpoint": "character-mara-venn",
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
            "units": [
                "The relay test succeeds.",
                "Mara notices the floorboard.",
                "They leave for the west span.",
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

        generator_payload = json.dumps(context["generator_visible"], ensure_ascii=False).lower()
        reviewer_payload = json.dumps(context["reviewer_only"], ensure_ascii=False).lower()
        if not check("dispatch satchel" not in generator_payload, "FS-003: concealed fact leaked into generator context"):
            return False
        if not check("does_not_know" not in generator_payload, "FS-003: negative viewpoint knowledge leaked into generator context"):
            return False
        if not check("dispatch satchel" in reviewer_payload, "FS-003: reviewer-only concealed fact missing"):
            return False
        if not check(contract["stop_boundary"] == "Mara decides to inspect the west span.", "FS-003: explicit stop boundary missing"):
            return False
        if not check(package["target_scope"] == "scene-002-signal-shed", "FS-003: package target incorrect"):
            return False
        if not check(
            package == rt.build_generation_package(copy.deepcopy(contract)),
            "FS-003: generation package is not stable for identical governing state",
        ):
            return False

        broken = copy.deepcopy(env["session"].dataset)
        broken["canon"]["events"] = [
            event for event in broken["canon"]["events"]
            if event.get("id") != "event-storm"
        ]
        try:
            rt.project_scene_context(broken, "scene-002-signal-shed")
        except rt.SceneNotReadyError:
            pass
        else:
            return check(False, "FS-003: missing material context was guessed instead of refused")

        bad = rt.create_candidate(
            package,
            "Mara saw the loose board and somehow understood that Eli had hidden a sealed railway dispatch satchel beneath it.",
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
        if not check(review["outcome"] == "non_conforming", "FS-003: violating candidate not rejected"):
            return False
        if not check(bad["authority_class"] == "candidate_manuscript", "FS-003: rejected candidate authority changed"):
            return False
        try:
            rt.accept_candidate(bad, package)
        except rt.AcceptanceError:
            pass
        else:
            return check(False, "FS-003: non-conforming candidate was accepted")

        indeterminate = rt.create_candidate(package, "Mara tests the relay.", 2)
        rt.review_candidate(indeterminate, package, indeterminate=True)
        try:
            rt.accept_candidate(indeterminate, package)
        except rt.AcceptanceError:
            pass
        else:
            return check(False, "FS-003: indeterminate candidate was accepted")

        good = rt.create_candidate(
            package,
            "Mara tested the relay until its armature clicked cleanly. The fault lay farther west. "
            "When she shifted her knee she noticed one floorboard had cleaner edges than its neighbors, "
            "an oddity she filed away while Eli pointed toward the storm-hit span. "
            "The line fault was the stronger lead, so she packed her meter and followed him outside.",
            3,
        )
        rt.review_candidate(good, package)
        accepted = rt.accept_candidate(good, package)
        if not check(accepted["authority_class"] == "accepted_manuscript", "FS-003: conforming candidate not accepted"):
            return False
        if not check(
            not (env["root"] / "dataset" / "chapters" / "002-scene-002-signal-shed.md").exists(),
            "FS-003: acceptance incorrectly implied persistence",
        ):
            return False
        env["accepted"] = accepted
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
            "Mara proved the relay worked locally, noticed the clean edge of one floorboard, "
            "and chose to inspect the west span because the diagnostic evidence pointed there.",
            2,
        )
        rt.review_candidate(good, package)
        accepted = rt.accept_candidate(good, package)
        session.persist_accepted(accepted)

        chapter_path = env["root"] / "dataset" / "chapters" / "002-scene-002-signal-shed.md"
        if not check(chapter_path.is_file(), "FS-003: accepted Manuscript was not persisted"):
            return False
        if not check((env["root"] / "dataset" / "schema.json").is_file(), "FS-003: migrated schema identity was not persisted"):
            return False
        if not check((env["root"] / "dataset" / "ruleset-binding.json").is_file(), "FS-003: migrated Ruleset binding was not persisted"):
            return False

        # Fresh runtime: no object/session state is reused.
        fresh = rt.open_scene_session(env["root"])
        accepted_entries = [
            entry for entry in fresh.dataset["chapters"]["files"]
            if entry.get("plot_scope") == "scene-002-signal-shed"
        ]
        if not check(len(accepted_entries) == 1, "FS-003: fresh session did not reconstruct accepted scene"):
            return False
        entry = accepted_entries[0]
        if not check(entry.get("authority_class") == "accepted_manuscript", "FS-003: Manuscript acceptance lost after restart"):
            return False
        if not check(entry.get("generation_package_id") == package["id"], "FS-003: generation provenance lost after restart"):
            return False
        next_scene = fresh.next_scene("scene-002-signal-shed")
        if not check(next_scene and next_scene.get("id") == "scene-003-first-message", "FS-003: next scene continuation failed"):
            return False
        next_context = fresh.context("scene-003-first-message")
        return check(next_context["target_scope"] == "scene-003-first-message", "FS-003: next scene could not be prepared")
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
