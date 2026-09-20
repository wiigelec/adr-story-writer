from __future__ import annotations

import copy
import importlib.util
import json
import re
import tempfile
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
REQS = ROOT / "product" / "specs" / "FS-006-requirements.md"
MANIFEST = ROOT / "product" / "validation" / "requirement-evaluation.json"
DESIGN_REVISION = "22b8f2dcb3ff22b1ff1613fb965353dd2917d443"


def check(condition: bool, message: str) -> bool:
    if not condition:
        print(f"FAIL product-validation: {message}")
        return False
    return True


def _load_runtime():
    path = ROOT / "product" / "src" / "authoring_runtime.py"
    spec = importlib.util.spec_from_file_location("fs006_authoring_runtime", path)
    if spec is None or spec.loader is None:
        raise ValueError("cannot load FS-006 authoring runtime")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def _fixture(root: Path) -> None:
    d = root / "dataset"
    _write_json(d / "instance.json", {"id": "fs006-generated-view-fixture"})
    _write_json(d / "story.json", {
        "application": "adr-story-writer",
        "dataset_role": "story",
        "title": "FS-006 Generated View Fixture",
        "status": "active",
    })
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
    s.accept_artifact(s.propose_artifact(
        "canon.character",
        {
            "id": "character-mara",
            "name": "Mara",
            "traits": ["methodical"],
            "knowledge": ["The local relay can be tested from the shed."],
        },
    )["id"])
    s.accept_artifact(s.propose_artifact(
        "canon.events",
        {
            "id": "event-storm",
            "summary": "A storm damages the west telegraph span.",
        },
        dependencies=["character-mara"],
    )["id"])
    s.accept_artifact(s.propose_artifact(
        "plot.synopsis",
        {
            "id": "plot-synopsis",
            "summary": "Mara restores service after the storm.",
        },
        dependencies=["character-mara", "event-storm"],
    )["id"])
    return s


def task_planning_binding():
    for rel in (
        "product/planning/FS-006-governed-editable-generated-author-views/functional-set.md",
        "product/planning/FS-006-governed-editable-generated-author-views/plan.md",
    ):
        text = (ROOT / rel).read_text(encoding="utf-8")
        if not check(
            f"design_revision: {DESIGN_REVISION}" in text,
            f"{rel}: missing exact FS-006 Design binding",
        ):
            return False
    return check(REQS.is_file(), "FS-006 normative requirements missing")


def task_generated_views():
    rt = _load_runtime()
    with tempfile.TemporaryDirectory() as temp:
        root = Path(temp)
        _fixture(root)

        # FS-002 compatibility must gate ordinary FS-006 use before a supported
        # migration/rebinding transition is explicitly authorized.
        try:
            rt.open_authoring_session(root)
        except rt.SCENE.CompatibilityGateError:
            pass
        else:
            return check(False, "FS-006 ordinary session bypassed compatibility gate")

        s = _develop(rt, root)
        pending = s.propose_artifact(
            "plot.sequence",
            {
                "id": "scene-pending",
                "ordinal": 1,
                "viewpoint": "character-mara",
                "entry": "Mara enters the shed.",
                "exit": "Mara leaves for the west span.",
            },
            dependencies=["character-mara"],
        )

        before = copy.deepcopy(s.dataset)
        view = s.character_dossier("character-mara")
        if not check(view.get("derived") is True, "Character dossier is not derived"):
            return False
        if not check(view.get("authority_class") == "derived_view", "Character dossier acquired story authority"):
            return False
        if not check("freshness" not in view, "Character dossier cached a potentially false current/stale state"):
            return False
        if not check(view.get("freshness_basis") == "source_attribution", "Character dossier lacks explicit freshness basis"):
            return False
        if not check(s.dataset == before, "rendering Character dossier mutated governed Dataset"):
            return False

        sources = {x["id"]: x for x in view.get("source_attribution", [])}
        if not check(
            {"character-mara", "event-storm", "plot-synopsis", pending["id"]} <= set(sources),
            "Character dossier omitted material attributed sources",
        ):
            return False
        if not check(
            sources["character-mara"]["surface"] == "canon.character"
            and sources["character-mara"]["authority_class"] == "accepted_semantic"
            and isinstance(sources["character-mara"]["revision"], str),
            "Character dossier source attribution lost owner/status/revision",
        ):
            return False
        if not check(
            sources[pending["id"]]["authority_class"] == "candidate_semantic"
            and any(x.get("authority_class") == "accepted_semantic" for x in sources.values()),
            "Character dossier flattened accepted and candidate authority classes",
        ):
            return False

        return check(
            view["content"]["character"]["id"] == "character-mara"
            and "revision_candidates" not in view["content"]["character"]
            and any(x["id"] == "event-storm" for x in view["content"]["canon_events"])
            and any(x["id"] == "plot-synopsis" for x in view["content"]["plot_context"])
            and any(x["id"] == pending["id"] for x in view["content"]["plot_context"]),
            "Character dossier projection did not preserve cross-surface context",
        )


def task_freshness_regeneration():
    rt = _load_runtime()
    with tempfile.TemporaryDirectory() as temp:
        root = Path(temp)
        _fixture(root)
        s = _develop(rt, root)

        old = s.character_dossier("character-mara")
        revision = s.propose_revision("character-mara", {"traits": ["methodical", "skeptical"]})
        s.accept_revision(revision["id"])

        freshness = s.view_freshness(old)
        if not check(
            freshness["state"] == "stale"
            and any(x.get("id") == "character-mara" for x in freshness["affected_sources"]),
            "material source revision did not stale prior dossier",
        ):
            return False
        try:
            s.propose_view_edit(old, {
                "target_id": "character-mara",
                "changes": {"traits": ["methodical", "skeptical", "patient"]},
            })
        except rt.GV.GeneratedViewError:
            pass
        else:
            return check(False, "stale dossier edit was applied as current")

        fresh = s.refresh_view(old)
        if not (
            check(s.view_freshness(fresh)["state"] == "current", "regenerated dossier is not current")
            and check(fresh["id"] == old["id"], "dossier regeneration changed generated-view identity")
            and check(
                fresh["projection_revision"] != old["projection_revision"],
                "dossier regeneration did not advance projection revision",
            )
        ):
            return False

        # A nested FS-004 revision candidate is independently projected workflow
        # state. Its status can change without changing the accepted parent revision.
        candidate = s.propose_revision(
            "character-mara",
            {"knowledge": ["The west span must be inspected."]},
        )
        candidate_view = s.character_dossier("character-mara")
        workflow_ids = {
            item.get("candidate", {}).get("id")
            for item in candidate_view["content"]["workflow_context"]
            if isinstance(item, dict)
        }
        if not check(candidate["id"] in workflow_ids, "revision candidate was not projected as distinct workflow context"):
            return False
        if not check(
            any(
                source.get("kind") == "revision_candidate"
                and source.get("id") == candidate["id"]
                and source.get("status") == "candidate"
                for source in candidate_view["source_attribution"]
            ),
            "revision candidate lacks independent freshness attribution",
        ):
            return False

        parent_revision = rt.REV._artifact(s.dataset, "character-mara")["revision"]
        s.reject_revision(candidate["id"], reason="freshness validation")
        if not check(
            rt.REV._artifact(s.dataset, "character-mara")["revision"] == parent_revision,
            "revision-candidate status change unexpectedly changed parent revision",
        ):
            return False
        candidate_freshness = s.view_freshness(candidate_view)
        return check(
            candidate_freshness["state"] == "stale"
            and any(x.get("id") == candidate["id"] for x in candidate_freshness["affected_sources"]),
            "revision-candidate status change did not stale projected workflow context",
        )


def task_edit_routing():
    rt = _load_runtime()
    with tempfile.TemporaryDirectory() as temp:
        root = Path(temp)
        _fixture(root)
        s = _develop(rt, root)
        view = s.character_dossier("character-mara")

        try:
            s.propose_view_edit(view, {"changes": {"traits": ["reckless"]}})
        except rt.GV.GeneratedViewError:
            pass
        else:
            return check(False, "ambiguous dossier edit silently selected a governed target")

        before_character = copy.deepcopy(rt.REV._artifact(s.dataset, "character-mara"))
        single = s.propose_view_edit(view, {
            "target_id": "character-mara",
            "changes": {"traits": ["methodical", "skeptical"]},
        })
        after_character = rt.REV._artifact(s.dataset, "character-mara")
        if not check(
            single["classification"] == "unambiguous_governed_edit"
            and single["proposals"][0]["operation"] == "propose_revision",
            "unambiguous accepted semantic edit did not route to FS-004 revision",
        ):
            return False
        if not check(
            after_character["revision"] == before_character["revision"]
            and after_character["authority_class"] == "accepted_semantic",
            "dossier edit directly mutated accepted semantic state",
        ):
            return False

        s.reject_revision(
            single["proposals"][0]["proposal_id"],
            reason="validation continues with candidate edit",
        )

        pending = s.propose_artifact(
            "plot.sequence",
            {
                "id": "scene-candidate-edit",
                "ordinal": 2,
                "viewpoint": "character-mara",
                "entry": "Mara enters the signal shed.",
                "exit": "Mara starts west.",
            },
            dependencies=["character-mara"],
        )
        candidate_view = s.character_dossier("character-mara")
        candidate_result = s.propose_view_edit(candidate_view, {
            "target_id": pending["id"],
            "changes": {"exit": "Mara leaves immediately for the west span."},
        })
        if not check(
            candidate_result["proposals"][0]["operation"] == "revise_candidate",
            "pending candidate edit did not route to FS-005 candidate refinement",
        ):
            return False
        if not check(
            rt.REV._artifact(s.dataset, pending["id"])["authority_class"] == "candidate_semantic",
            "candidate edit changed authority instead of refining candidate",
        ):
            return False

        coordinated_view = s.character_dossier("character-mara")
        coordinated = s.propose_view_edit(coordinated_view, {
            "targets": [
                {
                    "target_id": "character-mara",
                    "changes": {"knowledge": ["The west span must be inspected."]},
                },
                {
                    "target_id": "plot-synopsis",
                    "changes": {"summary": "Mara inspects the west span after restoring the relay."},
                },
            ]
        })
        if not check(
            coordinated["classification"] == "coordinated_multi_target_governed_edit"
            and {x["surface"] for x in coordinated["proposals"]}
                == {"canon.character", "plot.synopsis"},
            "coordinated dossier edit collapsed distinct semantic owners",
        ):
            return False
        return check(
            all(x["operation"] == "propose_revision" for x in coordinated["proposals"]),
            "coordinated dossier edit bypassed existing revision governance",
        )


def task_edit_failure_atomicity():
    rt = _load_runtime()
    with tempfile.TemporaryDirectory() as temp:
        root = Path(temp)
        _fixture(root)
        s = _develop(rt, root)
        view = s.character_dossier("character-mara")
        before = copy.deepcopy(s.dataset)

        try:
            s.propose_view_edit(view, {
                "targets": [
                    {
                        "target_id": "character-mara",
                        "changes": {
                            "traits": ["methodical", "patient"],
                        },
                    },
                    {
                        "target_id": "plot-synopsis",
                        "changes": {
                            "id": "illegal-governed-identity-replacement",
                        },
                    },
                ],
            })
        except rt.REV.RevisionRuntimeError:
            pass
        else:
            return check(
                False,
                "FS-006: invalid later coordinated target was silently accepted",
            )

        return check(
            s.dataset == before,
            "FS-006: failed coordinated generated-view edit partially mutated working Dataset",
        )

def task_presentation_comparison():
    rt = _load_runtime()
    with tempfile.TemporaryDirectory() as temp:
        root = Path(temp)
        _fixture(root)
        s = _develop(rt, root)
        before_dataset = copy.deepcopy(s.dataset)
        view = s.character_dossier("character-mara")
        preferred = s.apply_view_preferences(view, {
            "collapsed_sections": ["production_context"],
            "detail": "compact",
        })
        if not check(s.dataset == before_dataset, "presentation preference changed governed state"):
            return False
        if not check(
            preferred["presentation"]["detail"] == "compact"
            and preferred["content"] == view["content"],
            "presentation preference changed projected story meaning",
        ):
            return False
        comparison = s.compare_views(view, preferred)
        return (
            check(comparison.get("derived") is True, "view comparison is not derived")
            and check(
                comparison.get("authority_class") == "derived_view",
                "view comparison acquired story authority",
            )
            and check(
                comparison["presentation_changed"] is True
                and comparison["content_changed"] is False,
                "view comparison did not distinguish presentation from story content",
            )
        )


def task_reconstruction():
    rt = _load_runtime()
    with tempfile.TemporaryDirectory() as temp:
        root = Path(temp)
        _fixture(root)
        first = _develop(rt, root)
        original = first.character_dossier(
            "character-mara",
            preferences={"detail": "compact"},
        )
        first.persist()

        fresh = rt.open_authoring_session(root)
        regenerated = fresh.character_dossier("character-mara")
        if not check(
            regenerated["id"] == original["id"]
            and regenerated["projection_revision"] == original["projection_revision"],
            "fresh session could not reconstruct generated view from governed sources",
        ):
            return False
        return check(
            "generated_views" not in fresh.dataset,
            "FS-006 introduced a second persisted story-state database",
        )


def task_dataset_boundary():
    return check(not (ROOT / "dataset").exists(), "story Dataset instance must remain external")


def task_manifest_bindings():
    text = REQS.read_text(encoding="utf-8")
    parsed = re.findall(
        r"^### (FS-006-NR-\d{3}).*?\n\*\*Classification: ([MSB])\*\*",
        text,
        re.M | re.S,
    )
    required = {rid for rid, cls in parsed if cls in {"M", "B"}}
    forbidden = {rid for rid, cls in parsed if cls == "S"}
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    bound = {
        x.get("requirement")
        for x in manifest["bindings"]
        if isinstance(x, dict)
    }
    return (
        check(required <= bound, f"manifest missing FS-006 bindings: {sorted(required - bound)}")
        and check(
            not (forbidden & bound),
            f"manifest binds semantic-only FS-006 requirements: {sorted(forbidden & bound)}",
        )
    )


TASKS = {
    "fs006-planning-binding": task_planning_binding,
    "fs006-generated-views": task_generated_views,
    "fs006-freshness-regeneration": task_freshness_regeneration,
    "fs006-edit-routing": task_edit_routing,
    "fs006-edit-failure-atomicity": task_edit_failure_atomicity,
    "fs006-presentation-comparison": task_presentation_comparison,
    "fs006-reconstruction": task_reconstruction,
    "fs006-dataset-boundary": task_dataset_boundary,
    "fs006-manifest-bindings": task_manifest_bindings,
}
