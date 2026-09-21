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

    events = _json(d / "canon" / "events.json")
    for event in events:
        if event.get("id") == "event-storm":
            event["dependency_relations"] = [{
                "target_id": "setting-red-hollow",
                "target_revision": "canon-setting-r1",
                "authority_basis": "accepted",
                "material": False,
            }]
    _write(d / "canon" / "events.json", events)

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

    outline = _json(d / "plot" / "outline.json")
    for item in outline:
        if item.get("id") == "outline-opening":
            item["dependency_relations"] = [{
                "target_id": "event-storm",
                "target_revision": "canon-event-storm-r1",
                "authority_basis": "accepted",
            }]
    _write(d / "plot" / "outline.json", outline)

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

        rejected = session.propose_revision(
            "event-storm",
            {"summary": "Rejected alternate cause."},
        )
        session.reject_revision(rejected["id"], reason="author rejected")
        if not check(
            rt._artifact(session.dataset, "event-storm")["revision"]
            == accepted_before["revision"],
            "FS-004: rejecting a candidate changed accepted state",
        ):
            return False

        withdrawn = session.propose_revision(
            "event-storm",
            {"summary": "Withdrawn alternate cause."},
        )
        session.withdraw_revision(withdrawn["id"], reason="proposal withdrawn")
        if not check(
            rt._artifact(session.dataset, "event-storm")["revision"]
            == accepted_before["revision"],
            "FS-004: withdrawing a candidate changed accepted state",
        ):
            return False

        candidate = session.propose_revision(
            "event-storm",
            {
                "summary": (
                    "A rockslide severed the west telegraph span; the storm exposed "
                    "damage but was not the primary cause."
                )
            },
            material_dependencies=[{
                "target_id": "setting-red-hollow",
                "target_revision": "canon-setting-r1",
                "authority_basis": "accepted",
            }],
            assumptions=[
                "The proposed cause still concerns the Red Hollow telegraph span."
            ],
        )
        inspected = session.inspect_revision_candidate(candidate["id"])
        if not check(event["revision"] == accepted_before["revision"], "FS-004: candidate revision changed accepted revision"):
            return False
        if not check(event["summary"] == accepted_before["summary"], "FS-004: candidate revision changed accepted meaning"):
            return False
        if not check(candidate["authority_class"] == "candidate_semantic", "FS-004: upstream proposal is not candidate semantic state"):
            return False
        if not check(
            inspected.get("material_dependencies", [{}])[0].get("target_id")
            == "setting-red-hollow",
            "FS-004: candidate material dependencies are not inspectable",
        ):
            return False
        if not check(
            inspected.get("assumptions")
            == ["The proposed cause still concerns the Red Hollow telegraph span."],
            "FS-004: candidate assumptions are not inspectable",
        ):
            return False
        if not check(
            inspected.get("target_current_revision") == accepted_before["revision"],
            "FS-004: candidate inspection lost affected current scope",
        ):
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
        promoted = [
            relation
            for relation in event_after.get("dependency_relations", [])
            if isinstance(relation, dict)
            and relation.get("target_id") == "setting-red-hollow"
        ]
        if not (
            check(event_after["id"] == "event-storm", "FS-004: ordinary revision changed stable semantic identity")
            and check(event_after["revision"] != accepted_before["revision"], "FS-004: accepted revision did not establish new revision identity")
            and check(event_after["authority_class"] == "accepted_semantic", "FS-004: revision changed authority class")
            and check(bool(event_after.get("revision_history")), "FS-004: prior accepted revision provenance missing")
            and check(bool(event_after.get("revision_acceptance_history")), "FS-004: revision acceptance provenance missing")
            and check(change["from_revision"] == accepted_before["revision"], "FS-004: revision change provenance missing source revision")
            and check(len(promoted) == 1, "FS-004: accepted candidate dependency was duplicated instead of replaced")
            and check(promoted[0].get("material") is True, "FS-004: accepted candidate material dependency did not become current")
            and check(promoted[0].get("target_revision") == "canon-setting-r1", "FS-004: promoted dependency lost accepted target revision")
            and check(promoted[0].get("authority_basis") == "accepted", "FS-004: promoted dependency retained candidate authority basis")
        ):
            return False

        session.persist()
        fresh = rt.open_revision_session(root)
        reconstructed_event = rt._artifact(fresh.dataset, "event-storm")
        reconstructed_relations = [
            relation
            for relation in reconstructed_event.get("dependency_relations", [])
            if isinstance(relation, dict)
            and relation.get("target_id") == "setting-red-hollow"
        ]
        if not check(
            len(reconstructed_relations) == 1
            and reconstructed_relations[0].get("material") is True,
            "FS-004: promoted accepted dependency did not survive reconstruction",
        ):
            return False

        setting_candidate = fresh.propose_revision(
            "setting-red-hollow",
            {"name": "Red Hollow Relay Station and West Span"},
        )
        setting_change = fresh.accept_revision(setting_candidate["id"])
        setting_impacts = {
            impact["dependent_id"]: impact
            for impact in fresh.analyze_impact(setting_change)
        }
        return check(
            setting_impacts.get("event-storm", {}).get("state") == "review_required",
            "FS-004: later upstream revision could not discover the newly accepted dependency",
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
    scene2_before = copy.deepcopy(rt._artifact(session.dataset, "scene-002-signal-shed"))
    scene1_before = copy.deepcopy(rt._artifact(session.dataset, "scene-001-arrival"))

    pending = session.reconcile(
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
    scene2_candidate_state = copy.deepcopy(
        rt._artifact(session.dataset, "scene-002-signal-shed")
    )
    pending_candidate = session.inspect_revision_candidate(pending["candidate_id"])
    plot_change = session.accept_revision(pending["candidate_id"])

    downstream = session.analyze_impact(plot_change)
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
        "scene2_candidate_state": scene2_candidate_state,
        "pending_plot_revision": pending,
        "pending_plot_candidate": pending_candidate,
        "plot_change": plot_change,
        "downstream": downstream_by_id,
    }

def task_revision_failure_atomicity() -> bool:
    temp, rt, root, session, package_before = _exercise()
    try:
        candidate = session.propose_revision(
            "event-storm",
            {"summary": "Atomicity regression candidate."},
        )
        target = rt._artifact(session.dataset, "event-storm")
        stored = next(
            item
            for item in target.get("revision_candidates", [])
            if isinstance(item, dict) and item.get("id") == candidate["id"]
        )
        stored["reconciliation_context"] = {
            "impact_id": "impact-expected-by-candidate",
        }
        target["reconciliation"] = {
            "id": "impact-current-and-different",
            "state": "review_required",
        }
        before = copy.deepcopy(session.dataset)

        try:
            session.accept_revision(candidate["id"])
        except rt.SCENE.AcceptanceError:
            pass
        else:
            return check(
                False,
                "FS-004: invalid reconciliation context was silently accepted",
            )

        return check(
            session.dataset == before,
            "FS-004: failed revision acceptance partially mutated working Dataset",
        )
    finally:
        temp.cleanup()

def task_impact_reconciliation() -> bool:
    env = _perform_reconciliation()
    try:
        rt = env["rt"]
        session = env["session"]
        impacts = env["impacts"]
        scene1 = rt._artifact(session.dataset, "scene-001-arrival")
        scene2 = rt._artifact(session.dataset, "scene-002-signal-shed")
        manuscript = rt._artifact(session.dataset, "manuscript-scene-002")
        outline = rt._artifact(session.dataset, "outline-opening")

        if not check(impacts["scene-002-signal-shed"]["state"] == "review_required", "FS-004: material dependent was not marked review-required"):
            return False
        if not check(impacts["scene-001-arrival"]["state"] == "still_valid", "FS-004: historical/non-material dependent was broadly invalidated"):
            return False
        if not check(impacts["outline-opening"]["state"] == "unresolved", "FS-004: indeterminate materiality was guessed current"):
            return False
        if not check(scene1["revision"] == env["scene1_before"]["revision"], "FS-004: unrelated scene was artificially revised"):
            return False
        if not check(
            env["scene2_candidate_state"]["revision"] == env["scene2_before"]["revision"],
            "FS-004: candidate Plot reconciliation silently changed accepted revision",
        ):
            return False
        if not check(
            env["scene2_candidate_state"]["purpose"] == env["scene2_before"]["purpose"],
            "FS-004: candidate Plot reconciliation silently changed accepted meaning",
        ):
            return False
        if not check(
            env["pending_plot_revision"]["state"] == "candidate_pending_acceptance",
            "FS-004: Plot reconciliation did not create an explicit candidate",
        ):
            return False
        if not check(
            env["pending_plot_candidate"].get("material_dependencies", [{}])[0].get(
                "target_id"
            )
            == env["event_change"]["result_target_id"],
            "FS-004: Plot reconciliation candidate lost its accepted upstream dependency",
        ):
            return False
        if not check(scene2["revision"] == env["plot_change"]["to_revision"], "FS-004: accepted Plot revision not established after explicit acceptance"):
            return False
        if not check(scene2["authority_class"] == env["scene2_before"]["authority_class"], "FS-004: Plot reconciliation changed authority class"):
            return False
        if not check(manuscript["revision"] == "manuscript-scene-002-r1", "FS-004: upstream change directly rewrote accepted Manuscript"):
            return False
        if not check(manuscript["authority_class"] == "accepted_manuscript", "FS-004: Manuscript historical acceptance was revoked"):
            return False
        if not check(manuscript["generation_package_id"] == "historical-package-scene-002", "FS-004: historical generation provenance was replaced"):
            return False
        return (
            check(
                manuscript.get("reconciliation", {}).get("state") == "reconciled",
                "FS-004: explicit Manuscript preserve reconciliation missing",
            )
            and check(
                outline.get("reconciliation", {}).get("state") == "unresolved",
                "FS-004: unresolved impact state not retained",
            )
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
        outline = rt._artifact(fresh.dataset, "outline-opening")

        if not check(event["revision"] == env["event_change"]["to_revision"], "FS-004: accepted upstream revision not reconstructed"):
            return False
        if not check(bool(event.get("revision_history")), "FS-004: prior revision history not durable"):
            return False
        if not check(bool(event.get("revision_acceptance_history")), "FS-004: accepted upstream revision provenance not durable"):
            return False
        if not check(scene2.get("reconciliation", {}).get("state") == "reconciled", "FS-004: reconciliation state not durable"):
            return False
        if not check(outline.get("reconciliation", {}).get("state") == "unresolved", "FS-004: unresolved downstream state not reconstructed"):
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


def task_replacement_reconstruction() -> bool:
    rt = _runtime()
    temp = tempfile.TemporaryDirectory()
    try:
        root = Path(temp.name)
        _fixture(root)
        session = rt.open_revision_session(root, authorize_transition=True)
        candidate = session.propose_revision(
            "event-storm",
            {"summary": "A landslide, not a storm, severs the west telegraph span."},
            identity_operation="replacement",
            replacement_id="event-landslide-break",
        )
        change = session.accept_revision(candidate["id"])
        impacts = {
            item["dependent_id"]: item
            for item in session.analyze_impact(change)
        }
        if not check(
            impacts["scene-002-signal-shed"]["state"] == "superseded",
            "FS-004: known replacement path did not classify dependency as superseded",
        ):
            return False
        if not check(
            impacts["scene-001-arrival"]["state"] == "still_valid",
            "FS-004: non-material dependent was incorrectly invalidated by upstream replacement",
        ):
            return False
        rt.ensure_artifact_current(
            session.dataset,
            rt._artifact(session.dataset, "scene-001-arrival"),
        )

        pending = session.reconcile(
            "scene-002-signal-shed",
            impacts["scene-002-signal-shed"]["id"],
            "supersede",
            proposed_changes={
                "purpose": (
                    "Diagnose the relay and follow evidence of the landslide while "
                    "preserving the concealed satchel boundary."
                )
            },
            replacement_id="scene-002-landslide-shed",
        )
        if not check(
            pending.get("state") == "candidate_pending_acceptance",
            "FS-004: downstream semantic replacement did not remain candidate",
        ):
            return False
        plot_candidate = session.inspect_revision_candidate(pending["candidate_id"])
        if not check(
            plot_candidate.get("identity_operation") == "replacement",
            "FS-004: downstream replacement candidate lost replacement identity",
        ):
            return False
        plot_change = session.accept_revision(pending["candidate_id"])

        replacement = rt._artifact(session.dataset, "event-landslide-break")
        replaced_scene = rt._artifact(session.dataset, "scene-002-landslide-shed")
        if not check(
            replacement.get("supersedes") == "event-storm",
            "FS-004: replacement identity did not preserve supersession provenance",
        ):
            return False
        if not check(
            bool(replacement.get("revision_acceptance_history")),
            "FS-004: replacement acceptance provenance missing",
        ):
            return False
        if not check(
            replaced_scene.get("supersedes") == "scene-002-signal-shed",
            "FS-004: dependent replacement did not preserve superseded identity",
        ):
            return False
        if not check(
            replaced_scene.get("reconciliation", {}).get("state") == "reconciled",
            "FS-004: dependent replacement reconciliation did not close after acceptance",
        ):
            return False
        if not check(
            plot_change.get("result_target_id") == "scene-002-landslide-shed",
            "FS-004: accepted downstream replacement did not expose resulting identity",
        ):
            return False

        session.persist()
        fresh = rt.open_revision_session(root)
        replacement = rt._artifact(fresh.dataset, "event-landslide-break")
        replaced_scene = rt._artifact(fresh.dataset, "scene-002-landslide-shed")
        return (
            check(
                replacement.get("supersedes") == "event-storm",
                "FS-004: replacement provenance not reconstructed",
            )
            and check(
                bool(replacement.get("revision_acceptance_history")),
                "FS-004: replacement acceptance history not reconstructed",
            )
            and check(
                replaced_scene.get("supersedes") == "scene-002-signal-shed",
                "FS-004: replaced downstream identity not reconstructed",
            )
            and check(
                replaced_scene.get("reconciliation", {}).get("state") == "reconciled",
                "FS-004: replaced downstream reconciliation state not reconstructed",
            )
        )
    finally:
        temp.cleanup()


def task_manuscript_repair() -> bool:
    rt = _runtime()
    temp = tempfile.TemporaryDirectory()
    try:
        root = Path(temp.name)
        _fixture(root)
        session = rt.open_revision_session(root, authorize_transition=True)

        event_candidate = session.propose_revision(
            "event-storm",
            {"summary": "A rockslide, rather than lightning alone, broke the west span."},
        )
        event_change = session.accept_revision(event_candidate["id"])
        impacts = {
            item["dependent_id"]: item
            for item in session.analyze_impact(event_change)
        }
        pending_plot = session.reconcile(
            "scene-002-signal-shed",
            impacts["scene-002-signal-shed"]["id"],
            "revise",
            proposed_changes={
                "purpose": (
                    "Diagnose the relay and follow evidence of the rockslide without "
                    "revealing Eli's hidden satchel."
                )
            },
        )
        plot_change = session.accept_revision(pending_plot["candidate_id"])
        downstream = {
            item["dependent_id"]: item
            for item in session.analyze_impact(plot_change)
        }

        for dependent_id in ("beats-scene-002", "pseudo-scene-002"):
            session.reconcile(
                dependent_id,
                downstream[dependent_id]["id"],
                "rebuild",
            )
        session.reconcile(
            "scene-003-first-message",
            downstream["scene-003-first-message"]["id"],
            "preserve",
        )

        old_manuscript = copy.deepcopy(
            rt._artifact(session.dataset, "manuscript-scene-002")
        )
        if not check(
            old_manuscript.get("reconciliation", {}).get("state")
            == "review_required",
            "FS-004: changed Manuscript was not left review-required",
        ):
            return False

        try:
            session.package("scene-002-signal-shed")
        except rt.SCENE.SceneNotReadyError:
            pass
        else:
            return check(
                False,
                "FS-004: stale Manuscript incorrectly allowed ordinary generation",
            )

        repair_package = session.manuscript_repair_package(
            "scene-002-signal-shed"
        )
        if not check(
            repair_package.get("purpose") == "manuscript_reconciliation",
            "FS-004: Manuscript repair package is not explicitly scoped",
        ):
            return False
        if not check(
            repair_package.get("replaces_manuscript", {}).get("revision")
            == old_manuscript.get("revision"),
            "FS-004: repair package lost stale Manuscript provenance",
        ):
            return False

        candidate = session.create_manuscript_replacement_candidate(
            repair_package,
            (
                "Mara verifies the relay, recognizes that the storm exposed rather "
                "than caused the break, and follows the rockslide evidence west."
            ),
            70,
        )
        rt.SCENE.review_candidate(candidate, repair_package)
        accepted = rt.SCENE.accept_candidate(candidate, repair_package)

        # The previously accepted text remains current until explicit acceptance
        # and persistence of the replacement.
        if not check(
            rt._artifact(session.dataset, "manuscript-scene-002")["revision"]
            == old_manuscript["revision"],
            "FS-004: replacement candidate overwrote accepted Manuscript early",
        ):
            return False

        session.persist_manuscript_replacement(accepted)
        current = rt._artifact(session.dataset, "manuscript-scene-002")
        if not check(
            current["revision"] != old_manuscript["revision"],
            "FS-004: accepted Manuscript replacement did not establish a new revision",
        ):
            return False
        if not check(
            current.get("replaces_revision") == old_manuscript["revision"],
            "FS-004: Manuscript replacement lost prior revision provenance",
        ):
            return False
        if not check(
            bool(current.get("manuscript_revision_history")),
            "FS-004: prior accepted Manuscript was not retained historically",
        ):
            return False

        fresh = rt.open_revision_session(root)
        rebuilt = rt._artifact(fresh.dataset, "manuscript-scene-002")
        if not check(
            rebuilt["revision"] == current["revision"],
            "FS-004: replacement Manuscript revision not reconstructed",
        ):
            return False
        if not check(
            rebuilt.get("replaces_revision") == old_manuscript["revision"],
            "FS-004: replacement chain not reconstructed",
        ):
            return False

        # Once repaired, ordinary production may resume with the new current text.
        package = fresh.package("scene-002-signal-shed")
        return check(
            package["selected_revisions"]["current_target_manuscript"].get(
                "manuscript-scene-002"
            )
            == rebuilt["revision"],
            "FS-004: repaired Manuscript did not restore ordinary readiness",
        )
    finally:
        temp.cleanup()


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


def task_ruleset_compatibility() -> bool:
    identity = _json(ROOT / "ruleset" / "identity.json")
    contract = _json(ROOT / "ruleset" / "compatibility.json")
    current = contract["ruleset_binding"]["current"]
    migration_target = contract["migration"]["supported_transitions"][0]["target"][
        "ruleset_binding"
    ]
    return (
        check(
            current == identity,
            "FS-004: compatibility current binding differs from Ruleset identity",
        )
        and check(
            migration_target == current,
            "FS-004: supported legacy migration does not land on current Ruleset",
        )
    )


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
    "fs004-revision-failure-atomicity": task_revision_failure_atomicity,
    "fs004-impact-reconciliation": task_impact_reconciliation,
    "fs004-package-readiness": task_package_readiness,
    "fs004-persistence-reconstruction": task_persistence_reconstruction,
    "fs004-replacement-reconstruction": task_replacement_reconstruction,
    "fs004-manuscript-repair": task_manuscript_repair,
    "fs004-persistence-conflict": task_persistence_conflict,
    "fs004-ruleset-compatibility": task_ruleset_compatibility,
    "fs004-dataset-boundary": task_dataset_boundary,
    "fs004-manifest-bindings": task_manifest_bindings,
}
