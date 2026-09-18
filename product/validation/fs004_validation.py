#!/usr/bin/env python3
from __future__ import annotations

import copy
import importlib.util
import json
import re
import tempfile
from pathlib import Path
from typing import Any, Callable


ROOT = Path(__file__).resolve().parents[2]
REQS = ROOT / "product" / "specs" / "FS-004-requirements.md"
MANIFEST = ROOT / "product" / "validation" / "requirement-evaluation.json"
DESIGN_REVISION = "0ab706c19fcca4f133188393529e386662d1126e"


def check(condition: bool, message: str) -> bool:
    if condition:
        return True
    print(f"FAIL {message}")
    return False


def _load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ValueError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _runtime():
    return _load(ROOT / "product" / "src" / "revision_runtime.py", "fs004_revision_runtime")


def _fs003_validation():
    return _load(ROOT / "product" / "validation" / "fs003_validation.py", "fs003_fixture_source")


def _json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def _write(path: Path, value: Any):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def _fixture(root: Path):
    fs003 = _fs003_validation()
    fs003._fixture(root)
    d = root / "dataset"

    sequence = _json(d / "plot" / "sequence.json")
    for scene in sequence:
        if scene["id"] == "scene-001-arrival":
            scene["dependency_relations"] = [{
                "target_id": "event-storm",
                "target_revision": "canon-event-storm-r1",
                "authority_basis": "accepted",
                "material": False,
            }]
        elif scene["id"] == "scene-002-signal-shed":
            scene["dependency_relations"] = [{
                "target_id": "event-storm",
                "target_revision": "canon-event-storm-r1",
                "authority_basis": "accepted",
                "material": True,
            }]
        elif scene["id"] == "scene-003-first-message":
            scene["dependency_relations"] = [
                {
                    "target_id": "event-storm",
                    "target_revision": "canon-event-storm-r1",
                    "authority_basis": "accepted",
                    "material": False,
                },
                {
                    "target_id": "scene-002-signal-shed",
                    "target_revision": "plot-scene-002-r1",
                    "authority_basis": "accepted",
                    "material": True,
                },
            ]
    _write(d / "plot" / "sequence.json", sequence)

    beats = _json(d / "prose" / "beats.json")
    beats["scene-002-signal-shed"]["dependency_relations"] = [{
        "target_id": "scene-002-signal-shed",
        "target_revision": "plot-scene-002-r1",
        "authority_basis": "accepted",
        "material": True,
    }]
    _write(d / "prose" / "beats.json", beats)

    pseudo = _json(d / "prose" / "pseudo-prose.json")
    pseudo["scene-002-signal-shed"]["dependency_relations"] = [{
        "target_id": "scene-002-signal-shed",
        "target_revision": "plot-scene-002-r1",
        "authority_basis": "accepted",
        "material": True,
    }]
    _write(d / "prose" / "pseudo-prose.json", pseudo)

    manifest = _json(d / "chapters" / "manifest.json")
    manifest["files"].append({
        "id": "manuscript-scene-002",
        "surface": "manuscript",
        "authority_class": "accepted_manuscript",
        "revision": "manuscript-scene-002-r1",
        "ordinal": 2,
        "plot_scope": "scene-002-signal-shed",
        "path": "chapters/002-scene-002-signal-shed.md",
        "generation_package_id": "historical-package-scene-002",
        "generation_provenance": {
            "package_id": "historical-package-scene-002",
            "selected_revisions": {"scene": "plot-scene-002-r1"},
        },
        "dependency_relations": [{
            "target_id": "scene-002-signal-shed",
            "target_revision": "plot-scene-002-r1",
            "authority_basis": "accepted",
            "material": True,
        }],
    })
    _write(d / "chapters" / "manifest.json", manifest)
    (d / "chapters" / "002-scene-002-signal-shed.md").write_text(
        "# Chapter 2\n\nMara verifies the relay and follows the line fault west.\n",
        encoding="utf-8",
    )


def _exercise():
    rt = _runtime()
    temp = tempfile.TemporaryDirectory()
    root = Path(temp.name)
    _fixture(root)
    session = rt.open_revision_session(root, authorize_transition=True)
    package_before = session.package("scene-002-signal-shed")
    return temp, rt, root, session, package_before


def task_planning_binding() -> bool:
    for rel in (
        "product/planning/FS-004-governed-upstream-revision-impact-and-reconciliation/functional-set.md",
        "product/planning/FS-004-governed-upstream-revision-impact-and-reconciliation/plan.md",
    ):
        text = (ROOT / rel).read_text(encoding="utf-8")
        if not check(
            f"design_revision: {DESIGN_REVISION}" in text,
            f"{rel}: missing exact FS-004 Design binding",
        ):
            return False
    return check(REQS.is_file(), "FS-004 normative requirements missing")


def task_reconciliation_contract() -> bool:
    data = _json(ROOT / "ruleset" / "reconciliation.json")
    return (
        check(data["revision"]["candidate_does_not_change_accepted_meaning"] is True, "FS-004: candidate/accepted revision boundary missing")
        and check(data["impact"]["material_dependency_distinct_from_historical_derivation"] is True, "FS-004: material/historical distinction missing")
        and check("unresolved" in data["impact"]["outcomes"], "FS-004: unresolved impact outcome missing")
        and check(data["freshness"]["is_not_authority_class"] is True, "FS-004: freshness incorrectly modeled as authority")
        and check(data["generation_package"]["used_package_immutable"] is True, "FS-004: package immutability missing")
        and check(data["reconciliation"]["accepted_manuscript_not_directly_rewritten"] is True, "FS-004: Manuscript revision boundary missing")
    )


def task_revision_runtime() -> bool:
    temp, rt, root, session, package_before = _exercise()
    try:
        event = rt._artifact(session.dataset, "event-storm")
        accepted_before = copy.deepcopy(event)
        candidate = session.propose_revision(
            "event-storm",
            {
                "summary": (
                    "A rockslide severed the west telegraph span; the storm exposed "
                    "damage but was not the primary cause."
                )
            },
        )
        if not check(event["revision"] == accepted_before["revision"], "FS-004: candidate revision changed accepted revision"):
            return False
        if not check(event["summary"] == accepted_before["summary"], "FS-004: candidate revision changed accepted meaning"):
            return False
        if not check(candidate["authority_class"] == "candidate_semantic", "FS-004: upstream proposal is not candidate semantic state"):
            return False

        ambiguous = session.propose_revision(
            "event-storm",
            {"summary": "Ambiguous identity proposal."},
            identity_operation="unresolved",
        )
        try:
            session.accept_revision(ambiguous["id"])
        except rt.SCENE.AcceptanceError:
            pass
        else:
            return check(False, "FS-004: ambiguous semantic identity was silently accepted")

        change = session.accept_revision(candidate["id"])
        event_after = rt._artifact(session.dataset, "event-storm")
        return (
            check(event_after["id"] == "event-storm", "FS-004: ordinary revision changed stable semantic identity")
            and check(event_after["revision"] != accepted_before["revision"], "FS-004: accepted revision did not establish new revision identity")
            and check(event_after["authority_class"] == "accepted_semantic", "FS-004: revision changed authority class")
            and check(bool(event_after.get("revision_history")), "FS-004: prior accepted revision provenance missing")
            and check(change["from_revision"] == accepted_before["revision"], "FS-004: revision change provenance missing source revision")
        )
    finally:
        temp.cleanup()


def _perform_reconciliation():
    temp, rt, root, session, package_before = _exercise()
    event_candidate = session.propose_revision(
        "event-storm",
        {
            "summary": (
                "A rockslide severed the west telegraph span; the storm exposed "
                "damage but was not the primary cause."
            )
        },
    )
    event_change = session.accept_revision(event_candidate["id"])
    impacts = session.analyze_impact(event_change)
    by_dependent = {impact["dependent_id"]: impact for impact in impacts}

    scene2_impact = by_dependent["scene-002-signal-shed"]
    scene1_impact = by_dependent["scene-001-arrival"]

    scene2_before = copy.deepcopy(rt._artifact(session.dataset, "scene-002-signal-shed"))
    scene1_before = copy.deepcopy(rt._artifact(session.dataset, "scene-001-arrival"))

    scene2_record = session.reconcile(
        "scene-002-signal-shed",
        scene2_impact["id"],
        "revise",
        proposed_changes={
            "purpose": (
                "Diagnose the relay and distinguish storm exposure from the "
                "actual line break without revealing Eli's hidden satchel."
            )
        },
    )
    scene2_after = rt._artifact(session.dataset, "scene-002-signal-shed")
    scene_change = {
        "id": "scene2-reconciliation-change",
        "target_id": "scene-002-signal-shed",
        "result_target_id": "scene-002-signal-shed",
        "surface": scene2_after["surface"],
        "from_revision": scene2_before["revision"],
        "to_revision": scene2_after["revision"],
        "identity_operation": "revision",
        "candidate_id": None,
    }
    downstream = session.analyze_impact(scene_change)
    downstream_by_id = {impact["dependent_id"]: impact for impact in downstream}

    for dependent_id in ("beats-scene-002", "pseudo-scene-002"):
        session.reconcile(
            dependent_id,
            downstream_by_id[dependent_id]["id"],
            "rebuild",
        )
    session.reconcile(
        "manuscript-scene-002",
        downstream_by_id["manuscript-scene-002"]["id"],
        "preserve",
    )
    session.reconcile(
        "scene-003-first-message",
        downstream_by_id["scene-003-first-message"]["id"],
        "preserve",
    )

    return {
        "temp": temp,
        "rt": rt,
        "root": root,
        "session": session,
        "package_before": package_before,
        "event_change": event_change,
        "impacts": by_dependent,
        "scene1_before": scene1_before,
        "scene2_before": scene2_before,
        "scene2_record": scene2_record,
        "downstream": downstream_by_id,
    }


def task_impact_reconciliation() -> bool:
    env = _perform_reconciliation()
    try:
        rt = env["rt"]
        session = env["session"]
        impacts = env["impacts"]
        scene1 = rt._artifact(session.dataset, "scene-001-arrival")
        scene2 = rt._artifact(session.dataset, "scene-002-signal-shed")
        manuscript = rt._artifact(session.dataset, "manuscript-scene-002")

        if not check(impacts["scene-002-signal-shed"]["state"] == "review_required", "FS-004: material dependent was not marked review-required"):
            return False
        if not check(impacts["scene-001-arrival"]["state"] == "still_valid", "FS-004: historical/non-material dependent was broadly invalidated"):
            return False
        if not check(scene1["revision"] == env["scene1_before"]["revision"], "FS-004: unrelated scene was artificially revised"):
            return False
        if not check(scene2["authority_class"] == env["scene2_before"]["authority_class"], "FS-004: staleness changed Plot authority"):
            return False
        if not check(manuscript["revision"] == "manuscript-scene-002-r1", "FS-004: upstream change directly rewrote accepted Manuscript"):
            return False
        if not check(manuscript["authority_class"] == "accepted_manuscript", "FS-004: Manuscript historical acceptance was revoked"):
            return False
        if not check(manuscript["generation_package_id"] == "historical-package-scene-002", "FS-004: historical generation provenance was replaced"):
            return False
        return check(
            manuscript.get("reconciliation", {}).get("state") == "reconciled",
            "FS-004: explicit Manuscript preserve reconciliation missing",
        )
    finally:
        env["temp"].cleanup()


def task_package_readiness() -> bool:
    env = _perform_reconciliation()
    try:
        rt = env["rt"]
        session = env["session"]
        old_package = env["package_before"]
        try:
            session.create_candidate(
                old_package,
                "This attempt must not be permitted under stale governing state.",
                1,
            )
        except rt.SCENE.SceneNotReadyError:
            pass
        else:
            return check(False, "FS-004: stale generation package governed a new attempt")

        new_package = session.package("scene-002-signal-shed")
        if not check(new_package["id"] != old_package["id"], "FS-004: reconciled state reused stale package identity"):
            return False
        if not check(
            new_package["selected_revisions"]["scene"]
            == rt._artifact(session.dataset, "scene-002-signal-shed")["revision"],
            "FS-004: new package did not select current Plot revision",
        ):
            return False
        attempt = session.create_candidate(
            new_package,
            "Mara verifies the relay, separates storm exposure from the actual break, and follows the line west.",
            2,
        )
        return check(
            attempt["generation_provenance"]["package_id"] == new_package["id"],
            "FS-004: current attempt lost generation package provenance",
        )
    finally:
        env["temp"].cleanup()


def task_persistence_reconstruction() -> bool:
    env = _perform_reconciliation()
    try:
        rt = env["rt"]
        session = env["session"]
        current_package = session.package("scene-002-signal-shed")
        session.persist()

        fresh = rt.open_revision_session(env["root"])
        event = rt._artifact(fresh.dataset, "event-storm")
        scene2 = rt._artifact(fresh.dataset, "scene-002-signal-shed")
        manuscript = rt._artifact(fresh.dataset, "manuscript-scene-002")

        if not check(event["revision"] == env["event_change"]["to_revision"], "FS-004: accepted upstream revision not reconstructed"):
            return False
        if not check(bool(event.get("revision_history")), "FS-004: prior revision history not durable"):
            return False
        if not check(scene2.get("reconciliation", {}).get("state") == "reconciled", "FS-004: reconciliation state not durable"):
            return False
        if not check(manuscript["generation_package_id"] == "historical-package-scene-002", "FS-004: historical package provenance not durable"):
            return False
        rebuilt = fresh.package("scene-002-signal-shed")
        return (
            check(rebuilt["selected_revisions"]["scene"] == scene2["revision"], "FS-004: fresh-session package did not use current Plot revision")
            and check(current_package["selected_revisions"] == rebuilt["selected_revisions"], "FS-004: fresh-session readiness differs from persisted reconciled state")
        )
    finally:
        env["temp"].cleanup()


def task_persistence_conflict() -> bool:
    rt = _runtime()
    temp = tempfile.TemporaryDirectory()
    try:
        root = Path(temp.name)
        _fixture(root)
        first = rt.open_revision_session(root, authorize_transition=True)
        # Persist the migration before starting concurrent current-schema sessions.
        first.persist()

        a = rt.open_revision_session(root)
        b = rt.open_revision_session(root)
        candidate_a = a.propose_revision(
            "event-storm",
            {"summary": "Concurrent revision A."},
        )
        a.accept_revision(candidate_a["id"])
        a.persist()

        candidate_b = b.propose_revision(
            "event-storm",
            {"summary": "Concurrent revision B."},
        )
        b.accept_revision(candidate_b["id"])
        try:
            b.persist()
        except rt.SCENE.PersistenceConflictError:
            return True
        return check(False, "FS-004: stale session overwrote newer persisted Dataset state")
    finally:
        temp.cleanup()


def task_dataset_boundary() -> bool:
    return (
        check(not (ROOT / "dataset").exists(), "FS-004: story Dataset instance stored in Ruleset repository")
        and check(not (ROOT / "sw-test-story").exists(), "FS-004: external fixture copied into Ruleset repository")
    )


def task_manifest_bindings() -> bool:
    text = REQS.read_text(encoding="utf-8")
    pattern = re.compile(
        r"^### (FS-004-NR-\d{3}).*?\n\*\*Classification: ([MSB])\*\*(?:\n\*\*State: (Inactive)\*\*)?",
        re.M | re.S,
    )
    parsed = pattern.findall(text)
    required = {rid for rid, cls, state in parsed if cls in {"M", "B"} and state != "Inactive"}
    forbidden = {rid for rid, cls, state in parsed if cls == "S" or state == "Inactive"}
    manifest = _json(MANIFEST)
    bound = {b.get("requirement") for b in manifest["bindings"] if isinstance(b, dict)}
    return (
        check(required <= bound, f"manifest missing FS-004 mechanical bindings: {sorted(required - bound)}")
        and check(not (forbidden & bound), f"manifest binds FS-004 semantic/inactive requirements: {sorted(forbidden & bound)}")
    )


TASKS: dict[str, Callable[[], bool | None]] = {
    "fs004-planning-binding": task_planning_binding,
    "fs004-reconciliation-contract": task_reconciliation_contract,
    "fs004-revision-runtime": task_revision_runtime,
    "fs004-impact-reconciliation": task_impact_reconciliation,
    "fs004-package-readiness": task_package_readiness,
    "fs004-persistence-reconstruction": task_persistence_reconstruction,
    "fs004-persistence-conflict": task_persistence_conflict,
    "fs004-dataset-boundary": task_dataset_boundary,
    "fs004-manifest-bindings": task_manifest_bindings,
}
