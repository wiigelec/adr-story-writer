#!/usr/bin/env python3
from __future__ import annotations

import copy
import importlib.util
import json
import re
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REQS = ROOT / "product" / "specs" / "FS-007-requirements.md"
MANIFEST = ROOT / "product" / "validation" / "requirement-evaluation.json"
DESIGN_REVISION = "33fa138f69b85a15877610760006d7a98e6e376b"


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


STYLE = _load("fs007_style_runtime", "product/src/style_runtime.py")
SCENE = _load("fs007_scene_runtime", "product/src/scene_runtime.py")
COMPAT = _load("fs007_compatibility", "product/src/compatibility.py")


def _dataset() -> dict:
    return {
        "schema": {"id": "adr-story-writer.dataset", "version": 1},
        "ruleset_binding": {
            "application": "adr-story-writer",
            "component": "ruleset",
            "version": "0.4.0",
        },
        "compatibility_history": [],
        "instance": {"id": "fs007-fixture"},
        "story": {
            "application": "adr-story-writer",
            "dataset_role": "story",
            "title": "FS-007 fixture",
            "status": "active",
        },
        "canon": {
            "character": {
                "character-mara": {
                    "id": "character-mara",
                    "surface": "canon.character",
                    "authority_class": "accepted_semantic",
                    "revision": "character-r1",
                    "knowledge": ["The relay failed."],
                }
            },
            "setting": {},
            "events": [],
        },
        "plot": {
            "synopsis": {},
            "outline": [],
            "sequence": [
                {
                    "id": "scene-1",
                    "surface": "plot.sequence",
                    "authority_class": "accepted_semantic",
                    "revision": "scene-r1",
                    "ordinal": 1,
                    "viewpoint": "character-mara",
                    "entry": "Mara enters the relay shed.",
                    "exit": "Mara leaves for the west span.",
                    "required_movements": ["Mara confirms the relay failure."],
                    "dependencies": ["character-mara"],
                    "reader_information": {
                        "may_reveal": ["The relay failed."],
                        "must_conceal": [],
                    },
                }
            ],
        },
        "prose": {
            "beats": {
                "beat-1": {
                    "id": "beat-1",
                    "surface": "prose.beats",
                    "authority_class": "production_approved",
                    "revision": "beat-r1",
                    "target_scope": "scene-1",
                    "beats": ["Mara tests the relay once and confirms the fault."],
                }
            },
            "modes": {
                "mode-default": {
                    "id": "mode-default",
                    "surface": "prose.modes",
                    "authority_class": "production_approved",
                    "revision": "mode-r1",
                    "target_scope": None,
                    "style": [
                        "Keep the physical procedure concrete and advance once established."
                    ],
                }
            },
            "pseudo_prose": {},
        },
        "chapters": {"format": "markdown", "files": []},
    }


def task_planning_binding():
    for rel in (
        "product/planning/FS-007-governed-prose-style-guidance-and-generation-quality/functional-set.md",
        "product/planning/FS-007-governed-prose-style-guidance-and-generation-quality/plan.md",
    ):
        text = (ROOT / rel).read_text(encoding="utf-8")
        if not check(
            f"design_revision: {DESIGN_REVISION}" in text,
            f"{rel}: missing exact Design binding",
        ):
            return False
    return check(REQS.is_file(), "FS-007 normative requirements missing")


def task_style_state():
    dataset = _dataset()
    raw_sample = "This exact source manuscript text must not enter generation packages."
    candidate = STYLE.propose_style_profile(
        dataset,
        profile_id="author-default",
        guidance={
            "narration": {
                "person": "third",
                "tense": "past",
                "distance": "close",
            },
            "diction": ["Prefer direct, concrete language."],
        },
        source_samples=[
            {
                "kind": "author_sample",
                "reference": "drive:author-sample/ch01",
                "label": "representative chapter",
                "sample_text_forbidden": raw_sample,
            }
        ],
    )
    if not check(
        candidate["authority_class"] == "production_candidate",
        "derived style profile was not created as production_candidate",
    ):
        return False
    try:
        STYLE.select_default_style_profile(dataset, "author-default")
    except STYLE.StyleRuntimeError:
        pass
    else:
        return check(False, "unapproved style profile was selectable")

    approved = STYLE.approve_style_profile(dataset, "author-default")
    STYLE.select_default_style_profile(dataset, "author-default")
    return (
        check(
            approved["authority_class"] == "production_approved",
            "style profile approval did not produce production-approved guidance",
        )
        and check(
            approved["source_samples"][0]["reference"] == "drive:author-sample/ch01",
            "style source provenance was not preserved",
        )
        and check(
            "sample_text_forbidden" not in approved["source_samples"][0],
            "style profile persisted unbounded author-sample content",
        )
    )


def task_generation_quality():
    guidance = STYLE.generation_quality_guidance()
    required = {
        "semantic_restraint",
        "pattern_restraint",
        "physical_reaction_restraint",
        "description_restraint",
        "dialogue_restraint",
        "style_restraint",
        "variation",
    }
    return (
        check(
            required <= set(guidance),
            "Ruleset generation-quality guidance categories are incomplete",
        )
        and check(
            all(isinstance(guidance[k], list) and guidance[k] for k in required),
            "generation-quality guidance categories must be non-empty arrays",
        )
    )


def task_style_projection():
    dataset = _dataset()
    baseline = STYLE.resolve_style_projection(
        dataset,
        scene_id="scene-1",
        local_style_guidance=["Use the scene's established practical tone."],
    )
    if not check(
        baseline["author_profile"] is None
        and baseline["author_style_guidance"] == {}
        and baseline["generation_quality_guidance"],
        "Dataset without author profile did not resolve baseline guidance",
    ):
        return False

    STYLE.propose_style_profile(
        dataset,
        profile_id="author-default",
        guidance={"voice": ["direct", "character-centered"]},
        source_samples=[{"kind": "author_sample", "reference": "drive:sample-set"}],
    )
    STYLE.approve_style_profile(dataset, "author-default")
    STYLE.select_default_style_profile(dataset, "author-default")
    projection = STYLE.resolve_style_projection(
        dataset,
        scene_id="scene-1",
        local_style_guidance=["Keep the repair action concrete."],
    )
    return (
        check(
            projection["layers"]
            == [
                "generation_quality_guidance",
                "author_style_guidance",
                "local_style_guidance",
            ],
            "resolved style projection collapsed guidance layers",
        )
        and check(
            projection["author_profile"]["id"] == "author-default",
            "resolved style projection omitted selected profile identity",
        )
        and check(
            projection["local_style_guidance"]
            == ["Keep the repair action concrete."],
            "resolved style projection omitted local guidance",
        )
    )


def task_generation_package():
    dataset = _dataset()
    raw_marker = "RAW SAMPLE PROSE MUST NOT BE IN PACKAGE"
    STYLE.propose_style_profile(
        dataset,
        profile_id="author-default",
        guidance={
            "narration": {"person": "third", "tense": "past"},
            "interiority": ["Use direct self-questioning selectively."],
        },
        source_samples=[
            {
                "kind": "author_sample",
                "reference": "drive:author-sample",
                "private_test_marker": raw_marker,
            }
        ],
    )
    approved = STYLE.approve_style_profile(dataset, "author-default")
    STYLE.select_default_style_profile(dataset, "author-default")

    contract = SCENE.build_production_contract(dataset, "scene-1")
    package = SCENE.build_generation_package(contract)

    if not check(
        package["style_projection"] == contract["style_projection"],
        "generation package did not freeze contract style projection",
    ):
        return False
    if not check(
        package["selected_revisions"]["style_profile"]
        == {"author-default": approved["revision"]},
        "generation package omitted selected style-profile revision",
    ):
        return False
    serialized = json.dumps(package, sort_keys=True)
    if not check(
        raw_marker not in serialized and "source_samples" not in serialized,
        "generation package injected author sample material",
    ):
        return False

    frozen = copy.deepcopy(package)
    dataset["prose"]["style_profiles"]["author-default"]["guidance"]["extra"] = [
        "new later guidance"
    ]
    return check(
        package == frozen,
        "existing generation package changed after later style-state mutation",
    )


def _write_json(path: Path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def task_reconstruction():
    dataset = _dataset()
    STYLE.propose_style_profile(
        dataset,
        profile_id="author-default",
        guidance={"voice": ["direct"]},
        source_samples=[{"kind": "author_sample", "reference": "drive:sample-set"}],
    )
    STYLE.approve_style_profile(dataset, "author-default")
    STYLE.select_default_style_profile(dataset, "author-default")

    with tempfile.TemporaryDirectory() as temp:
        root = Path(temp)
        d = root / "dataset"
        _write_json(d / "schema.json", dataset["schema"])
        _write_json(d / "ruleset-binding.json", dataset["ruleset_binding"])
        _write_json(d / "compatibility-history.json", [])
        _write_json(d / "instance.json", dataset["instance"])
        _write_json(d / "story.json", dataset["story"])
        _write_json(d / "canon/character.json", dataset["canon"]["character"])
        _write_json(d / "canon/setting.json", dataset["canon"]["setting"])
        _write_json(d / "canon/events.json", dataset["canon"]["events"])
        _write_json(d / "plot/synopsis.json", dataset["plot"]["synopsis"])
        _write_json(d / "plot/outline.json", dataset["plot"]["outline"])
        _write_json(d / "plot/sequence.json", dataset["plot"]["sequence"])
        _write_json(d / "prose/beats.json", dataset["prose"]["beats"])
        _write_json(d / "prose/modes.json", dataset["prose"]["modes"])
        _write_json(d / "prose/pseudo-prose.json", dataset["prose"]["pseudo_prose"])
        _write_json(d / "prose/style-profiles.json", dataset["prose"]["style_profiles"])
        _write_json(d / "prose/style-selection.json", dataset["prose"]["style_selection"])
        _write_json(d / "chapters/manifest.json", dataset["chapters"])

        backend = SCENE.TreeDatasetBackend(root)
        loaded = backend.load()
        return check(
            loaded["prose"]["style_profiles"]["author-default"]["authority_class"]
            == "production_approved"
            and loaded["prose"]["style_selection"]["default_profile"]
            == "author-default",
            "fresh Dataset reconstruction lost FS-007 style state",
        )


def task_rebinding():
    contract = COMPAT.load_contract()
    if not check(
        contract["dataset_schema"]["current"]["version"] == 1,
        "FS-007 unexpectedly changed Dataset schema version",
    ):
        return False
    dataset = _dataset()
    dataset["ruleset_binding"]["version"] = "0.3.0"
    dataset["prose"].pop("style_profiles", None)
    dataset["prose"].pop("style_selection", None)
    status = COMPAT.classify(dataset, contract=contract)
    if not check(
        status["state"] == "rebinding_required"
        and status["transition"] == "ruleset-0.3.0-to-0.4.0",
        "schema-v1 Ruleset 0.3.0 Dataset did not require explicit FS-007 rebind",
    ):
        return False
    rebound = COMPAT.rebind(
        dataset,
        status["transition"],
        authorized=True,
        contract=contract,
    )
    return check(
        rebound["schema"]["version"] == 1
        and rebound["ruleset_binding"]["version"] == "0.4.0"
        and "style_profiles" not in rebound["prose"],
        "FS-007 rebind changed schema or invented author-style state",
    )


def task_dataset_boundary():
    return check(
        not (ROOT / "dataset").exists(),
        "FS-007 story Dataset or author samples must remain external",
    )


def task_manifest_bindings():
    text = REQS.read_text(encoding="utf-8")
    parsed = re.findall(
        r"^### (FS-007-NR-\d{3}).*?\n\*\*Classification: ([MSB])\*\*",
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
            f"manifest missing FS-007 bindings: {sorted(required - bound)}",
        )
        and check(
            not (forbidden & bound),
            f"manifest binds semantic-only FS-007 requirements: {sorted(forbidden & bound)}",
        )
    )


TASKS = {
    "fs007-planning-binding": task_planning_binding,
    "fs007-style-state": task_style_state,
    "fs007-generation-quality": task_generation_quality,
    "fs007-style-projection": task_style_projection,
    "fs007-generation-package": task_generation_package,
    "fs007-reconstruction": task_reconstruction,
    "fs007-rebinding": task_rebinding,
    "fs007-dataset-boundary": task_dataset_boundary,
    "fs007-manifest-bindings": task_manifest_bindings,
}
