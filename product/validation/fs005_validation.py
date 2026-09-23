from __future__ import annotations

import importlib.util
import json
import re
import tempfile
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
REQS = ROOT / "product" / "specs" / "FS-005-requirements.md"
MANIFEST = ROOT / "product" / "validation" / "requirement-evaluation.json"
DESIGN_REVISION = "21e017572c31f0aa9b95b9de0785f557511949b1"


def check(condition: bool, message: str) -> bool:
    if not condition:
        print(f"FAIL product-validation: {message}")
        return False
    return True


def _load_runtime():
    path = ROOT / "product" / "src" / "authoring_runtime.py"
    spec = importlib.util.spec_from_file_location("fs005_authoring_runtime", path)
    if spec is None or spec.loader is None:
        raise ValueError("cannot load FS-005 authoring runtime")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def _fixture(root: Path) -> None:
    d = root / "dataset"
    _write_json(d / "instance.json", {"id": "fs005-authoring-fixture"})
    _write_json(d / "story.json", {"application": "adr-story-writer", "dataset_role": "story", "title": "FS-005 Workshop Fixture", "status": "active"})
    _write_json(d / "canon/character.json", {})
    _write_json(d / "canon/setting.json", {})
    _write_json(d / "canon/events.json", [])
    _write_json(d / "plot/synopsis.json", {})
    _write_json(d / "plot/outline.json", [])
    _write_json(d / "plot/sequence.json", [])
    _write_json(d / "prose/beats.json", {})
    _write_json(d / "prose/modes.json", {})
    _write_json(d / "prose/pseudo-prose.json", {})
    _write_json(d / "chapters/manifest.json", {"format": "markdown", "files": []})


def _develop(rt, root: Path):
    s = rt.open_authoring_session(root, authorize_transition=True)
    s.accept_artifact(s.propose_artifact("canon.character", {"id": "character-mara", "name": "Mara", "traits": ["methodical"]})["id"])
    s.accept_artifact(s.propose_artifact("canon.setting", {"id": "setting-red-hollow", "name": "Red Hollow"})["id"])
    s.accept_artifact(s.propose_artifact("canon.events", {"id": "event-storm", "summary": "A storm damages the west telegraph span."}, dependencies=["setting-red-hollow"])["id"])
    s.accept_artifact(s.propose_artifact("plot.synopsis", {"id": "plot-synopsis", "summary": "Mara arrives to restore telegraph service after the storm."}, dependencies=["character-mara", "event-storm"])["id"])
    s.accept_artifact(s.propose_artifact("plot.sequence", {
        "id": "scene-001", "ordinal": 1, "viewpoint": "character-mara",
        "entry": "Mara enters the signal shed.",
        "required_movements": ["Mara tests the relay."],
        "exit": "Mara decides to inspect the west span.",
        "reader_information": {"may_reveal": ["The relay works locally."]},
    }, dependencies=["character-mara", "event-storm", "setting-red-hollow"])["id"])
    return s


def task_planning_binding():
    for rel in (
        "product/planning/FS-005-governed-author-workshop-and-progressive-story-development/functional-set.md",
        "product/planning/FS-005-governed-author-workshop-and-progressive-story-development/plan.md",
    ):
        text = (ROOT / rel).read_text(encoding="utf-8")
        if not check(f"design_revision: {DESIGN_REVISION}" in text, f"{rel}: missing exact FS-005 Design binding"):
            return False
    return check(REQS.is_file(), "FS-005 normative requirements missing")


def task_authoring_runtime():
    rt = _load_runtime()
    with tempfile.TemporaryDirectory() as temp:
        root = Path(temp)
        _fixture(root)
        s = rt.open_authoring_session(root, authorize_transition=True)
        c = s.propose_artifact("canon.character", {"id": "character-one", "name": "One"})
        if not check(c["authority_class"] == "candidate_semantic", "new Canon proposal was not candidate"):
            return False
        r = s.revise_candidate("character-one", {"traits": ["careful"]})
        if not check(r["id"] == c["id"] and r["revision"] != c["revision"], "candidate refinement identity/revision failure"):
            return False
        if not check(len(r.get("candidate_revision_history", [])) == 1, "candidate revision history missing"):
            return False
        a = s.accept_artifact("character-one")
        if not check(a["authority_class"] == "accepted_semantic", "semantic candidate not accepted"):
            return False

        dep = s.propose_artifact("canon.character", {"id": "candidate-dependency", "name": "Candidate Dependency"})
        dependent = s.propose_artifact("plot.sequence", {
            "id": "dependent-scene", "ordinal": 2, "viewpoint": "character-one",
            "entry": "Start.", "exit": "Stop.",
        }, dependencies=[dep["id"]])
        try:
            s.accept_artifact(dependent["id"])
        except rt.SCENE.AcceptanceError:
            pass
        else:
            return check(False, "candidate dependency bypassed closure")
        # Reverse dependency order deliberately: coordinated acceptance must be
        # atomic/order-independent and rebase the relation to the accepted revision.
        both = s.accept_artifacts([dependent["id"], dep["id"]])
        if not check(all(x["authority_class"] == "accepted_semantic" for x in both), "coordinated acceptance failed"):
            return False
        coordination = [x.get("acceptance", {}).get("coordination") for x in both]
        if not check(
            all(isinstance(x, dict) for x in coordination)
            and len({x["decision_id"] for x in coordination}) == 1
            and all(x.get("operation") == "coordinated_acceptance" for x in coordination)
            and all(x.get("related_scopes") == sorted([dep["id"], dependent["id"]]) for x in coordination),
            "coordinated acceptance did not retain one durable explicit author decision",
        ):
            return False
        dep_current = rt.REV._artifact(s.dataset, dep["id"])
        dependent_current = rt.REV._artifact(s.dataset, dependent["id"])
        relation = dependent_current["dependency_relations"][0]
        if not check(
            "target_revision" not in relation
            and relation["authority_basis"] == "accepted"
            and dependent_current["alignment"]["dependencies"][dep["id"]]
            == dep_current["revision"],
            "coordinated acceptance did not preserve live identity plus accepted alignment",
        ):
            return False
        try:
            rt.REV.ensure_artifact_current(s.dataset, dependent_current)
        except rt.SCENE.SceneNotReadyError:
            return check(False, "coordinated acceptance produced immediately stale dependent")

        # A dependent candidate must not silently rebase onto an upstream revision
        # accepted after the dependent candidate was proposed.
        upstream = s.propose_artifact("canon.character", {
            "id": "revision-upstream", "name": "Before",
        })
        s.accept_artifact(upstream["id"])
        stale_dependent = s.propose_artifact("plot.sequence", {
            "id": "stale-dependent", "ordinal": 3, "viewpoint": "character-one",
            "entry": "Start.", "exit": "Stop.",
        }, dependencies=[upstream["id"]])
        revision = s.propose_revision(upstream["id"], {"name": "After"})
        s.accept_revision(revision["id"])
        try:
            s.accept_artifact(stale_dependent["id"])
        except rt.SCENE.AcceptanceError:
            pass
        else:
            return check(False, "dependent candidate silently rebased onto changed upstream revision")

        # Prove transitive closure through the FS-004 lifecycle:
        # A changes, impact analysis marks accepted B review_required, and a
        # candidate C that materially depends on B must be refused even though
        # B's own revision did not change.
        transitive_a = s.propose_artifact("canon.character", {
            "id": "transitive-a", "name": "A",
        })
        s.accept_artifact(transitive_a["id"])
        transitive_b = s.propose_artifact("plot.sequence", {
            "id": "transitive-b", "ordinal": 4, "viewpoint": "character-one",
            "entry": "Start.", "exit": "Stop.",
        }, dependencies=[transitive_a["id"]])
        s.accept_artifact(transitive_b["id"])
        transitive_c = s.propose_artifact("plot.sequence", {
            "id": "transitive-c", "ordinal": 5, "viewpoint": "character-one",
            "entry": "Start.", "exit": "Stop.",
        }, dependencies=[transitive_b["id"]])

        upstream_revision = s.propose_revision(transitive_a["id"], {"name": "A2"})
        accepted_change = s.accept_revision(upstream_revision["id"])
        impacts = s.analyze_impact(accepted_change)
        if not check(
            any(
                impact.get("dependent_id") == transitive_b["id"]
                and impact.get("state") == "review_required"
                for impact in impacts
            ),
            "FS-004 impact analysis did not mark transitive middle dependency review_required",
        ):
            return False

        try:
            s.accept_artifact(transitive_c["id"])
        except rt.SCENE.AcceptanceError:
            return True
        return check(False, "transitive stale dependency did not block candidate acceptance")


def task_progressive_refinement():
    rt = _load_runtime()
    with tempfile.TemporaryDirectory() as temp:
        root = Path(temp)
        _fixture(root)
        s = _develop(rt, root)
        if not check(s.readiness("scene-001")["ready"] is False, "scene ready without production controls"):
            return False
        s.accept_artifact(s.propose_artifact("prose.beats", {
            "id": "beats-scene-001", "target_scope": "scene-001",
            "beats": ["Mara tests the relay.", "She chooses the west span."],
        }, dependencies=["scene-001"])["id"])
        s.accept_artifact(s.propose_artifact("prose.modes", {
            "id": "mode-mara-close-third", "viewpoint": "close third through Mara", "tense": "past",
        }, dependencies=["character-mara"])["id"])
        s.accept_artifact(s.propose_artifact("prose.pseudo_prose", {
            "id": "pseudo-scene-001", "target_scope": "scene-001",
            "units": ["The relay test succeeds.", "Mara heads west."],
        }, dependencies=["scene-001"])["id"])
        after = s.readiness("scene-001")
        if not check(after["ready"] is True, f"refined scene not ready: {after.get('blockers')}"):
            return False
        package = s.package("scene-001")
        return check(package["target_scope"] == "scene-001", "ready scene did not hand off to FS-003")


def task_views():
    rt = _load_runtime()
    with tempfile.TemporaryDirectory() as temp:
        root = Path(temp)
        _fixture(root)
        s = _develop(rt, root)
        c = s.propose_artifact("canon.character", {"id": "character-pending", "name": "Pending"})
        story = s.overview()
        candidates = s.overview("candidates")
        return (
            check(story.get("derived") is True, "story view not derived")
            and check(c["id"] in story.get("pending_candidates", []), "story view omitted pending candidate")
            and check(any(x.get("id") == c["id"] for x in candidates["candidates"]), "candidate view omitted pending candidate")
        )


def task_revision_integration():
    rt = _load_runtime()
    with tempfile.TemporaryDirectory() as temp:
        root = Path(temp)
        _fixture(root)
        s = _develop(rt, root)
        before = rt.REV._artifact(s.dataset, "character-mara")["revision"]
        p = s.propose_revision("character-mara", {"traits": ["methodical", "skeptical"]})
        if not check(rt.REV._artifact(s.dataset, "character-mara")["revision"] == before, "revision proposal changed accepted state"):
            return False
        accepted = s.accept_revision(p["id"])
        return check(accepted["from_revision"] == before, "FS-004 revision semantics not preserved")


def task_persistence_reconstruction():
    rt = _load_runtime()
    with tempfile.TemporaryDirectory() as temp:
        root = Path(temp)
        _fixture(root)
        first = _develop(rt, root)
        pending = first.propose_artifact("canon.character", {"id": "character-persisted-candidate", "name": "Persisted Candidate"})
        coordinated_semantic = first.propose_artifact("canon.character", {
            "id": "coordinated-persisted-semantic", "name": "Coordinated",
        })
        coordinated_production = first.propose_artifact("prose.modes", {
            "id": "coordinated-persisted-production",
            "viewpoint": "close third through Coordinated",
        }, dependencies=[coordinated_semantic["id"]])
        accepted_pair = first.accept_artifacts([
            coordinated_production["id"],
            coordinated_semantic["id"],
        ])
        coordination_id = accepted_pair[0]["acceptance"]["coordination"]["decision_id"]
        if not check(
            accepted_pair[0]["acceptance"]["operation"] == "production_approval"
            and accepted_pair[1]["acceptance"]["operation"] == "semantic_acceptance"
            and accepted_pair[1]["acceptance"]["coordination"]["decision_id"] == coordination_id,
            "coordinated acceptance lost distinct acceptance purposes",
        ):
            return False
        first.persist()

        fresh = rt.open_authoring_session(root)
        if not check(any(x.get("id") == pending["id"] and x.get("authority_class") == "candidate_semantic" for x in fresh.overview("candidates")["candidates"]), "fresh session lost persisted candidate"):
            return False
        fresh_semantic = rt.REV._artifact(fresh.dataset, coordinated_semantic["id"])
        fresh_production = rt.REV._artifact(fresh.dataset, coordinated_production["id"])
        if not check(
            fresh_semantic.get("acceptance", {}).get("coordination", {}).get("decision_id") == coordination_id
            and fresh_production.get("acceptance", {}).get("coordination", {}).get("decision_id") == coordination_id
            and fresh_semantic["acceptance"]["coordination"].get("related_scopes")
                == sorted([coordinated_semantic["id"], coordinated_production["id"]]),
            "fresh session lost coordinated-acceptance provenance",
        ):
            return False

        stale = rt.open_authoring_session(root)
        fresh.propose_artifact("canon.character", {"id": "character-newer", "name": "Newer"})
        fresh.persist()
        stale.propose_artifact("canon.character", {"id": "character-stale", "name": "Stale"})
        try:
            stale.persist()
        except rt.SCENE.PersistenceConflictError:
            return True
        return check(False, "stale session overwrote newer Dataset")


def task_candidate_withdrawal():
    rt = _load_runtime()
    with tempfile.TemporaryDirectory() as temp:
        root = Path(temp)
        _fixture(root)
        s = rt.open_authoring_session(root, authorize_transition=True)
        a = s.propose_artifact("canon.character", {"id": "accepted-sibling", "name": "Accepted"})
        s.accept_artifact(a["id"])
        c = s.propose_artifact("canon.character", {"id": "withdraw-me", "name": "Withdraw"})
        w = s.withdraw_artifact(c["id"], reason="author changed direction")
        ids = {x.get("id") for x in rt.SCENE._iter_artifacts(s.dataset) if isinstance(x, dict)}
        return (
            check(w.get("candidate_status") == "withdrawn", "withdrawal status missing")
            and check("withdraw-me" not in ids, "withdrawn candidate still governs Dataset")
            and check("accepted-sibling" in ids, "withdrawal changed accepted sibling")
        )


def task_dataset_boundary():
    return check(not (ROOT / "dataset").exists(), "story Dataset instance must remain external")


def task_manifest_bindings():
    text = REQS.read_text(encoding="utf-8")
    parsed = re.findall(r"^### (FS-005-NR-\\d{3}).*?\\n\\*\\*Classification: ([MSB])\\*\\*", text, re.M | re.S)
    required = {rid for rid, cls in parsed if cls in {"M", "B"}}
    forbidden = {rid for rid, cls in parsed if cls == "S"}
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    bound = {x.get("requirement") for x in manifest["bindings"] if isinstance(x, dict)}
    return (
        check(required <= bound, f"manifest missing FS-005 bindings: {sorted(required - bound)}")
        and check(not (forbidden & bound), f"manifest binds semantic-only FS-005 requirements: {sorted(forbidden & bound)}")
    )


TASKS = {
    "fs005-planning-binding": task_planning_binding,
    "fs005-authoring-runtime": task_authoring_runtime,
    "fs005-progressive-refinement": task_progressive_refinement,
    "fs005-author-views": task_views,
    "fs005-revision-integration": task_revision_integration,
    "fs005-persistence-reconstruction": task_persistence_reconstruction,
    "fs005-candidate-withdrawal": task_candidate_withdrawal,
    "fs005-dataset-boundary": task_dataset_boundary,
    "fs005-manifest-bindings": task_manifest_bindings,
}
