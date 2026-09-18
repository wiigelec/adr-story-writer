#!/usr/bin/env python3
from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import os
import shutil
import tempfile
from pathlib import Path
from typing import Any


class SceneRuntimeError(ValueError):
    pass


class CompatibilityGateError(SceneRuntimeError):
    def __init__(self, status: dict[str, Any]):
        super().__init__(f"ordinary scene operation is not compatible: {status.get('state')}")
        self.status = copy.deepcopy(status)


class SceneNotReadyError(SceneRuntimeError):
    pass


class AcceptanceError(SceneRuntimeError):
    pass


class PersistenceConflictError(SceneRuntimeError):
    pass


def _load_compatibility_module():
    path = Path(__file__).resolve().with_name("compatibility.py")
    spec = importlib.util.spec_from_file_location("story_writer_compatibility", path)
    if spec is None or spec.loader is None:
        raise SceneRuntimeError("cannot load compatibility runtime")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


COMPAT = _load_compatibility_module()


def _canonical(value: Any) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")


def _stable_id(prefix: str, value: Any) -> str:
    return f"{prefix}-{hashlib.sha256(_canonical(value)).hexdigest()[:20]}"


def _read_object(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SceneRuntimeError(f"{path}: {exc}") from exc
    if not isinstance(value, dict):
        raise SceneRuntimeError(f"{path}: expected JSON object")
    return value


def _read_value(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SceneRuntimeError(f"{path}: {exc}") from exc


def _write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


class TreeDatasetBackend:
    """Adapter for the accepted split/tree story Dataset realization."""

    REQUIRED = {
        "instance": "instance.json",
        "story": "story.json",
        "canon.character": "canon/character.json",
        "canon.setting": "canon/setting.json",
        "canon.events": "canon/events.json",
        "plot.synopsis": "plot/synopsis.json",
        "plot.outline": "plot/outline.json",
        "plot.sequence": "plot/sequence.json",
        "prose.beats": "prose/beats.json",
        "prose.modes": "prose/modes.json",
        "prose.pseudo_prose": "prose/pseudo-prose.json",
        "chapters": "chapters/manifest.json",
    }

    def __init__(self, repository_root: Path):
        self.repository_root = Path(repository_root).resolve()
        self.dataset_root = self.repository_root / "dataset"

    def _required_path(self, rel: str) -> Path:
        path = self.dataset_root / rel
        if not path.is_file():
            raise SceneRuntimeError(f"missing Dataset component: dataset/{rel}")
        return path

    def load(self) -> dict[str, Any]:
        d = self.dataset_root
        dataset: dict[str, Any] = {
            "instance": _read_object(self._required_path("instance.json")),
            "story": _read_object(self._required_path("story.json")),
            "canon": {
                "character": _read_value(self._required_path("canon/character.json")),
                "setting": _read_value(self._required_path("canon/setting.json")),
                "events": _read_value(self._required_path("canon/events.json")),
            },
            "plot": {
                "synopsis": _read_value(self._required_path("plot/synopsis.json")),
                "outline": _read_value(self._required_path("plot/outline.json")),
                "sequence": _read_value(self._required_path("plot/sequence.json")),
            },
            "prose": {
                "beats": _read_value(self._required_path("prose/beats.json")),
                "modes": _read_value(self._required_path("prose/modes.json")),
                "pseudo_prose": _read_value(self._required_path("prose/pseudo-prose.json")),
            },
            "chapters": _read_object(self._required_path("chapters/manifest.json")),
        }

        # These fields are introduced by the supported FS-002 migration. They are
        # Dataset state, not root binding/provenance/construction metadata.
        optional = {
            "schema": "schema.json",
            "ruleset_binding": "ruleset-binding.json",
            "compatibility_history": "compatibility-history.json",
        }
        for key, rel in optional.items():
            path = d / rel
            if path.is_file():
                dataset[key] = _read_value(path)

        files = dataset["chapters"].get("files")
        if not isinstance(files, list):
            raise SceneRuntimeError("chapters.files must be an array")
        for entry in files:
            if not isinstance(entry, dict):
                raise SceneRuntimeError("chapter manifest entry must be an object")
            rel = entry.get("path")
            if not isinstance(rel, str) or not rel:
                raise SceneRuntimeError("chapter manifest entry requires path")
            chapter_path = d / rel
            if not chapter_path.is_file():
                raise SceneRuntimeError(f"missing chapter content: dataset/{rel}")
            entry["content"] = chapter_path.read_text(encoding="utf-8")

        return dataset

    def _materialize(self, target: Path, dataset: dict[str, Any]) -> None:
        _write_json(target / "instance.json", dataset["instance"])
        _write_json(target / "story.json", dataset["story"])
        _write_json(target / "canon/character.json", dataset["canon"]["character"])
        _write_json(target / "canon/setting.json", dataset["canon"]["setting"])
        _write_json(target / "canon/events.json", dataset["canon"]["events"])
        _write_json(target / "plot/synopsis.json", dataset["plot"]["synopsis"])
        _write_json(target / "plot/outline.json", dataset["plot"]["outline"])
        _write_json(target / "plot/sequence.json", dataset["plot"]["sequence"])
        _write_json(target / "prose/beats.json", dataset["prose"]["beats"])
        _write_json(target / "prose/modes.json", dataset["prose"]["modes"])
        _write_json(target / "prose/pseudo-prose.json", dataset["prose"]["pseudo_prose"])

        chapters = copy.deepcopy(dataset["chapters"])
        files = chapters.get("files", [])
        for entry in files:
            content = entry.pop("content", None)
            rel = entry.get("path")
            if content is not None:
                if not isinstance(content, str):
                    raise SceneRuntimeError("chapter content must be text")
                chapter_path = target / rel
                chapter_path.parent.mkdir(parents=True, exist_ok=True)
                chapter_path.write_text(content, encoding="utf-8")
        _write_json(target / "chapters/manifest.json", chapters)

        for key, rel in (
            ("schema", "schema.json"),
            ("ruleset_binding", "ruleset-binding.json"),
            ("compatibility_history", "compatibility-history.json"),
        ):
            if key in dataset:
                _write_json(target / rel, dataset[key])

    def digest(self) -> str:
        """Return a logical digest of the currently persisted Dataset tree."""
        return hashlib.sha256(_canonical(self.load())).hexdigest()

    def save(self, dataset: dict[str, Any], *, expected_digest: str) -> str:
        """Replace the complete Dataset tree as one logical save with rollback.

        Refuse the save when persisted state has changed since the session loaded.
        """
        current_digest = self.digest()
        if current_digest != expected_digest:
            raise PersistenceConflictError(
                "persisted Dataset changed after session reconstruction"
            )

        parent = self.dataset_root.parent
        parent.mkdir(parents=True, exist_ok=True)
        stage = Path(tempfile.mkdtemp(prefix=".dataset-stage-", dir=parent))
        backup = parent / f".dataset-backup-{os.getpid()}"
        if backup.exists():
            shutil.rmtree(backup)
        try:
            if self.dataset_root.exists():
                shutil.copytree(self.dataset_root, stage, dirs_exist_ok=True)
            self._materialize(stage, dataset)
            if self.dataset_root.exists():
                os.replace(self.dataset_root, backup)
            try:
                os.replace(stage, self.dataset_root)
            except Exception:
                if backup.exists() and not self.dataset_root.exists():
                    os.replace(backup, self.dataset_root)
                raise
            if backup.exists():
                shutil.rmtree(backup, ignore_errors=True)
        except Exception:
            if stage.exists():
                shutil.rmtree(stage, ignore_errors=True)
            raise
        return self.digest()


def _iter_artifacts(dataset: dict[str, Any]):
    canon = dataset.get("canon", {})
    for collection in ("character", "setting"):
        value = canon.get(collection, {})
        if isinstance(value, dict):
            for artifact in value.values():
                if isinstance(artifact, dict):
                    yield artifact
    events = canon.get("events", [])
    if isinstance(events, list):
        for artifact in events:
            if isinstance(artifact, dict):
                yield artifact

    plot = dataset.get("plot", {})
    synopsis = plot.get("synopsis")
    if isinstance(synopsis, dict) and synopsis.get("id"):
        yield synopsis
    for collection in ("outline", "sequence"):
        value = plot.get(collection, [])
        if isinstance(value, list):
            for artifact in value:
                if isinstance(artifact, dict):
                    yield artifact

    prose = dataset.get("prose", {})
    for collection in ("beats", "modes", "pseudo_prose"):
        value = prose.get(collection, {})
        if isinstance(value, dict):
            for artifact in value.values():
                if isinstance(artifact, dict):
                    yield artifact

    chapters = dataset.get("chapters", {}).get("files", [])
    if isinstance(chapters, list):
        for artifact in chapters:
            if isinstance(artifact, dict):
                yield artifact


def artifact_index(dataset: dict[str, Any]) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for artifact in _iter_artifacts(dataset):
        artifact_id = artifact.get("id")
        if isinstance(artifact_id, str) and artifact_id:
            if artifact_id in result:
                raise SceneRuntimeError(f"duplicate governed artifact id: {artifact_id}")
            result[artifact_id] = artifact
    return result


def _scene_by_id(dataset: dict[str, Any], scene_id: str) -> dict[str, Any]:
    sequence = dataset.get("plot", {}).get("sequence", [])
    for scene in sequence if isinstance(sequence, list) else []:
        if isinstance(scene, dict) and scene.get("id") == scene_id:
            return scene
    raise SceneNotReadyError(f"unknown target scene: {scene_id}")


def _prose_for_scene(dataset: dict[str, Any], scene_id: str) -> dict[str, list[dict[str, Any]]]:
    result = {"beats": [], "modes": [], "pseudo_prose": []}
    prose = dataset.get("prose", {})
    for name in result:
        collection = prose.get(name, {})
        if not isinstance(collection, dict):
            raise SceneNotReadyError(f"prose.{name} must be an object")
        for artifact in collection.values():
            if not isinstance(artifact, dict):
                raise SceneNotReadyError(f"prose.{name} contains a non-object artifact")
            target = artifact.get("target_scope")
            applicable = target == scene_id or (name == "modes" and target is None)
            if not applicable:
                continue
            if artifact.get("authority_class") != "production_approved":
                raise SceneNotReadyError(
                    f"{scene_id}: applicable {name} control {artifact.get('id')} "
                    "is not production_approved"
                )
            if not isinstance(artifact.get("revision"), str) or not artifact["revision"]:
                raise SceneNotReadyError(
                    f"{scene_id}: applicable {name} control {artifact.get('id')} "
                    "has no durable revision"
                )
            result[name].append(copy.deepcopy(artifact))
    return result

def _hidden_dependency_ids(scene: dict[str, Any], index: dict[str, dict[str, Any]]) -> set[str]:
    hidden: set[str] = set()
    reader = scene.get("reader_information", {})
    must_conceal = reader.get("must_conceal", []) if isinstance(reader, dict) else []
    for item in must_conceal if isinstance(must_conceal, list) else []:
        if isinstance(item, str) and item in index:
            hidden.add(item)

    viewpoint = scene.get("viewpoint")
    scene_id = scene.get("id")
    for dep_id in scene.get("dependencies", []) if isinstance(scene.get("dependencies"), list) else []:
        artifact = index.get(dep_id)
        if not artifact:
            continue
        concealed = artifact.get("concealed_from", [])
        if isinstance(concealed, list):
            if viewpoint in concealed or f"reader-through-{scene_id}" in concealed:
                hidden.add(dep_id)
    return hidden


def _authority_basis(artifact: dict[str, Any], *, context: str) -> str:
    authority = artifact.get("authority_class")
    revision = artifact.get("revision")
    if not isinstance(revision, str) or not revision:
        raise SceneNotReadyError(f"{context}: governed artifact lacks durable revision")
    if authority in {"accepted_semantic", "accepted_manuscript", "production_approved"}:
        return "accepted"
    if authority in {"candidate_semantic", "candidate_manuscript", "production_candidate"}:
        return "candidate"
    raise SceneNotReadyError(
        f"{context}: unresolved or unsupported authority_class {authority!r}"
    )


def _revision_map(artifacts: list[dict[str, Any]]) -> dict[str, str]:
    result: dict[str, str] = {}
    for artifact in artifacts:
        artifact_id = artifact.get("id")
        revision = artifact.get("revision")
        if isinstance(artifact_id, str) and isinstance(revision, str):
            result[artifact_id] = revision
    return result


def _generator_artifact(artifact: dict[str, Any], viewpoint_id: str) -> dict[str, Any]:
    value = copy.deepcopy(artifact)
    # A prior Plot scene may itself contain reviewer-facing purpose or concealment
    # wording. Downstream generation gets only the reader-safe dramatic surface;
    # accepted prior Manuscript supplies reader-facing continuity.
    if value.get("surface") == "plot.sequence":
        keep = (
            "id",
            "surface",
            "authority_class",
            "revision",
            "ordinal",
            "viewpoint",
            "entry",
            "exit",
            "required_movements",
        )
        safe = {key: copy.deepcopy(value[key]) for key in keep if key in value}
        reader = value.get("reader_information", {})
        if isinstance(reader, dict) and isinstance(reader.get("may_reveal"), list):
            safe["reader_information"] = {
                "may_reveal": copy.deepcopy(reader["may_reveal"])
            }
        return safe

    # The active viewpoint may expose positively authorized knowledge, but
    # negative/private epistemic fields can themselves name concealed facts.
    value.pop("does_not_know", None)
    value.pop("intent", None)
    if value.get("id") != viewpoint_id:
        value.pop("knowledge", None)
    value.pop("concealed_from", None)
    value.pop("known_by", None)
    return value


def _generator_scene(scene: dict[str, Any], visible_dependency_ids: list[str]) -> dict[str, Any]:
    # Do not pass must-conceal wording or purpose text through automatically:
    # either can name the very fact the generator is forbidden to disclose.
    keep = (
        "id", "surface", "authority_class", "revision", "ordinal", "viewpoint",
        "entry", "exit", "required_movements",
    )
    value = {key: copy.deepcopy(scene[key]) for key in keep if key in scene}
    value["dependencies"] = list(visible_dependency_ids)
    reader = scene.get("reader_information", {})
    if isinstance(reader, dict) and isinstance(reader.get("may_reveal"), list):
        value["reader_information"] = {"may_reveal": copy.deepcopy(reader["may_reveal"])}
    return value


def _generator_manuscript(entry: dict[str, Any]) -> dict[str, Any]:
    keep = (
        "id",
        "surface",
        "authority_class",
        "revision",
        "ordinal",
        "plot_scope",
        "content",
    )
    return {key: copy.deepcopy(entry[key]) for key in keep if key in entry}


def _generator_prose(prose: dict[str, list[dict[str, Any]]]) -> dict[str, list[dict[str, Any]]]:
    value = copy.deepcopy(prose)
    for beat in value.get("beats", []):
        beat.pop("protected_meaning", None)
    return value


def project_scene_context(dataset: dict[str, Any], scene_id: str) -> dict[str, Any]:
    scene = copy.deepcopy(_scene_by_id(dataset, scene_id))
    index = artifact_index(dataset)

    for field in ("id", "revision", "viewpoint", "entry", "exit"):
        if not scene.get(field):
            raise SceneNotReadyError(f"{scene_id}: missing required scene field {field}")
    scene_authority_basis = _authority_basis(
        scene,
        context=f"{scene_id}: target scene",
    )

    dependencies = scene.get("dependencies")
    if not isinstance(dependencies, list):
        raise SceneNotReadyError(f"{scene_id}: dependencies must be an array")
    missing = [dep for dep in dependencies if dep not in index]
    if missing:
        raise SceneNotReadyError(f"{scene_id}: unresolved dependencies: {missing}")

    for dep_id in dependencies:
        _authority_basis(index[dep_id], context=f"{scene_id}: dependency {dep_id}")

    viewpoint_id = scene["viewpoint"]
    viewpoint = index.get(viewpoint_id)
    if not isinstance(viewpoint, dict):
        raise SceneNotReadyError(f"{scene_id}: unresolved viewpoint {viewpoint_id}")
    _authority_basis(viewpoint, context=f"{scene_id}: viewpoint {viewpoint_id}")

    prose = _prose_for_scene(dataset, scene_id)
    if not prose["beats"] or not prose["modes"]:
        raise SceneNotReadyError(
            f"{scene_id}: production-approved beats and mode are required"
        )

    hidden_ids = _hidden_dependency_ids(scene, index)
    visible_dependency_ids = [dep for dep in dependencies if dep not in hidden_ids]
    visible_dependencies = [
        _generator_artifact(index[dep], viewpoint_id) for dep in visible_dependency_ids
    ]
    hidden_dependencies = [
        copy.deepcopy(index[dep]) for dep in dependencies if dep in hidden_ids
    ]

    generator_scene = _generator_scene(scene, visible_dependency_ids)
    viewpoint_visible = _generator_artifact(viewpoint, viewpoint_id)

    prior_manuscript: list[dict[str, Any]] = []
    current_target_manuscript: list[dict[str, Any]] = []
    scene_ordinal = scene.get("ordinal")
    chapters = dataset.get("chapters", {}).get("files", [])
    if isinstance(scene_ordinal, int) and isinstance(chapters, list):
        for chapter in chapters:
            if not isinstance(chapter, dict):
                raise SceneNotReadyError("chapter manifest contains a non-object entry")
            if chapter.get("authority_class") != "accepted_manuscript":
                continue
            _authority_basis(
                chapter,
                context=f"{scene_id}: Manuscript {chapter.get('id')}",
            )
            if chapter.get("plot_scope") == scene_id:
                current_target_manuscript.append(_generator_manuscript(chapter))
            elif (
                isinstance(chapter.get("ordinal"), int)
                and chapter["ordinal"] < scene_ordinal
            ):
                prior_manuscript.append(_generator_manuscript(chapter))

    protected_material = [
        item
        for artifact in prose["beats"]
        for item in artifact.get("protected_meaning", [])
        if isinstance(item, str)
    ]
    reviewer = {
        "must_conceal": copy.deepcopy(
            scene.get("reader_information", {}).get("must_conceal", [])
        ),
        "hidden_dependencies": hidden_dependencies,
        "viewpoint_exclusions": copy.deepcopy(viewpoint.get("does_not_know", [])),
        "protected_material": protected_material,
    }
    generator = {
        "target_scene": generator_scene,
        "viewpoint": viewpoint_visible,
        "accepted_dependencies": visible_dependencies,
        "prose_guidance": _generator_prose(prose),
        "accepted_prior_manuscript": prior_manuscript,
        "current_target_manuscript": current_target_manuscript,
    }

    generator_payload = json.dumps(generator, ensure_ascii=False).lower()
    for hidden in hidden_dependencies:
        summary = hidden.get("summary")
        if isinstance(summary, str) and summary.lower() in generator_payload:
            raise SceneRuntimeError("hidden Canon leaked into generator-visible context")

    return {
        "target_scope": scene_id,
        "scene_revision": scene["revision"],
        "scene_authority_basis": scene_authority_basis,
        "generator_visible": generator,
        "reviewer_only": reviewer,
        "hidden_dependency_ids": sorted(hidden_ids),
        "prose_control_revisions": {
            name: _revision_map(artifacts) for name, artifacts in prose.items()
        },
        "prior_manuscript_revisions": _revision_map(prior_manuscript),
        "current_target_manuscript_revisions": _revision_map(
            current_target_manuscript
        ),
    }

def build_production_contract(dataset: dict[str, Any], scene_id: str) -> dict[str, Any]:
    projection = project_scene_context(dataset, scene_id)
    scene = projection["generator_visible"]["target_scene"]
    prose = projection["generator_visible"]["prose_guidance"]
    all_deps = artifact_index(dataset)

    accepted_dependencies = []
    candidate_dependencies = []
    for dep_id in _scene_by_id(dataset, scene_id).get("dependencies", []):
        artifact = all_deps[dep_id]
        dep = {
            "target_id": dep_id,
            "target_revision": artifact["revision"],
            "authority_basis": _authority_basis(
                artifact,
                context=f"{scene_id}: dependency {dep_id}",
            ),
            "material": True,
        }
        (
            candidate_dependencies
            if dep["authority_basis"] == "candidate"
            else accepted_dependencies
        ).append(dep)

    protected = copy.deepcopy(
        projection["reviewer_only"].get("protected_material", [])
    )

    contract_seed = {
        "target_scope": scene_id,
        "scene_revision": projection["scene_revision"],
        "stop_boundary": scene["exit"],
        "projection": projection,
    }
    return {
        "id": _stable_id("contract", contract_seed),
        "target_scope": scene_id,
        "stop_boundary": scene["exit"],
        "narrative_movement": copy.deepcopy(
            scene.get("required_movements", scene.get("purpose"))
        ),
        "local_realization_units": copy.deepcopy(
            [u for a in prose["beats"] for u in a.get("beats", [])]
            + [u for a in prose["pseudo_prose"] for u in a.get("units", [])]
        ),
        "viewpoint_access": {
            "viewpoint": scene["viewpoint"],
            "knowledge": copy.deepcopy(
                projection["generator_visible"]["viewpoint"].get("knowledge", [])
            ),
        },
        "reveal_concealment": {
            "generator_visible": copy.deepcopy(
                scene.get("reader_information", {})
            ),
            "reviewer_only": copy.deepcopy(
                projection["reviewer_only"].get("must_conceal", [])
            ),
        },
        "entry_exit_conditions": {"entry": scene["entry"], "exit": scene["exit"]},
        "prose_guidance": copy.deepcopy(prose),
        "style_voice": copy.deepcopy(
            [s for a in prose["modes"] for s in a.get("style", [])]
        ),
        "protected_material": protected,
        "creative_allowance": [
            "local sensory detail",
            "non-consequential connective action",
            "wording and sentence-level realization",
        ],
        "prohibited_consequential_invention": [
            "new Canon truth",
            "new Plot outcome beyond the stop boundary",
            "disclosure of reviewer-only information",
        ],
        "accepted_dependencies": accepted_dependencies,
        "candidate_dependencies": candidate_dependencies,
        "target_authority_basis": projection["scene_authority_basis"],
        "context_projection": projection,
    }

def build_generation_package(contract: dict[str, Any]) -> dict[str, Any]:
    projection = contract["context_projection"]
    selected_revisions = {
        "scene": projection["scene_revision"],
        "dependencies": {
            dep["target_id"]: dep["target_revision"]
            for dep in contract["accepted_dependencies"]
            + contract["candidate_dependencies"]
        },
        "prose_controls": copy.deepcopy(projection["prose_control_revisions"]),
        "prior_manuscript": copy.deepcopy(projection["prior_manuscript_revisions"]),
        "current_target_manuscript": copy.deepcopy(
            projection["current_target_manuscript_revisions"]
        ),
    }
    seed = {
        "contract_id": contract["id"],
        "target_scope": contract["target_scope"],
        "selected_revisions": selected_revisions,
        "generator_visible_context": projection["generator_visible"],
        "reviewer_only_constraints": projection["reviewer_only"],
        "stop_boundary": contract["stop_boundary"],
    }
    package = {
        "id": _stable_id("package", seed),
        "contract_id": contract["id"],
        "target_scope": contract["target_scope"],
        "stop_boundary": contract["stop_boundary"],
        "selected_revisions": selected_revisions,
        "creative_allowance": copy.deepcopy(contract["creative_allowance"]),
        "prohibited_invention": copy.deepcopy(
            contract["prohibited_consequential_invention"]
        ),
        "generator_visible_context": copy.deepcopy(
            projection["generator_visible"]
        ),
        "reviewer_only_constraints": copy.deepcopy(
            projection["reviewer_only"]
        ),
        "candidate_dependencies": copy.deepcopy(contract["candidate_dependencies"]),
        "target_authority_basis": contract["target_authority_basis"],
        "provenance": {
            "contract_id": contract["id"],
            "package_digest": None,
        },
    }
    digest_source = copy.deepcopy(package)
    digest_source["provenance"]["package_digest"] = None
    package["provenance"]["package_digest"] = hashlib.sha256(
        _canonical(digest_source)
    ).hexdigest()
    return package


def _verify_package_digest(package: dict[str, Any]) -> None:
    expected = package.get("provenance", {}).get("package_digest")
    if not isinstance(expected, str) or not expected:
        raise SceneRuntimeError("generation package has no stable digest")
    digest_source = copy.deepcopy(package)
    digest_source["provenance"]["package_digest"] = None
    observed = hashlib.sha256(_canonical(digest_source)).hexdigest()
    if observed != expected:
        raise SceneRuntimeError("generation package changed after it was frozen")

def create_candidate(package: dict[str, Any], text: str, attempt: int) -> dict[str, Any]:
    _verify_package_digest(package)
    if not isinstance(text, str) or not text.strip():
        raise SceneRuntimeError("candidate text must be non-empty")
    seed = {
        "package_id": package["id"],
        "attempt": attempt,
        "text": text,
    }
    revision = _stable_id("candidate-revision", seed)
    return {
        "id": _stable_id("candidate", seed),
        "surface": "manuscript",
        "authority_class": "candidate_manuscript",
        "revision": revision,
        "target_scope": package["target_scope"],
        "generation_package_id": package["id"],
        "generation_provenance": {
            "package_id": package["id"],
            "contract_id": package["contract_id"],
            "package_digest": package["provenance"]["package_digest"],
            "selected_revisions": copy.deepcopy(package["selected_revisions"]),
            "package_snapshot": copy.deepcopy(package),
        },
        "attempt": attempt,
        "text": text,
        "review": None,
    }


def review_candidate(
    candidate: dict[str, Any],
    package: dict[str, Any],
    findings: list[dict[str, Any]] | None = None,
    *,
    indeterminate: bool = False,
    unresolved_consequential_dependencies: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    _verify_package_digest(package)
    if candidate.get("generation_package_id") != package.get("id"):
        raise SceneRuntimeError("candidate/package provenance mismatch")
    snapshot = (
        candidate.get("generation_provenance", {})
        .get("package_snapshot")
    )
    if snapshot != package:
        raise SceneRuntimeError("candidate was not governed by this frozen package")

    findings = copy.deepcopy(findings or [])
    unresolved = copy.deepcopy(unresolved_consequential_dependencies or [])
    if indeterminate:
        outcome = "indeterminate"
    elif any(bool(f.get("material", True)) for f in findings):
        outcome = "non_conforming"
    else:
        outcome = "conforming"
    review = {
        "outcome": outcome,
        "candidate_id": candidate["id"],
        "package_id": package["id"],
        "findings": findings,
        "unresolved_consequential_dependencies": unresolved,
    }
    candidate["review"] = copy.deepcopy(review)
    return review


def accept_candidate(candidate: dict[str, Any], package: dict[str, Any]) -> dict[str, Any]:
    _verify_package_digest(package)
    review = candidate.get("review")
    if not isinstance(review, dict) or review.get("outcome") != "conforming":
        raise AcceptanceError(
            "candidate requires a conforming review before Manuscript acceptance"
        )
    if package.get("target_authority_basis") != "accepted":
        raise AcceptanceError(
            "candidate target Plot scope blocks Manuscript acceptance"
        )
    if package.get("candidate_dependencies"):
        raise AcceptanceError(
            "material candidate dependencies block Manuscript acceptance"
        )
    if review.get("unresolved_consequential_dependencies"):
        raise AcceptanceError(
            "acceptance closure is incomplete for consequential candidate meaning"
        )
    accepted = copy.deepcopy(candidate)
    accepted["authority_class"] = "accepted_manuscript"
    accepted["accepted_from_candidate"] = candidate["id"]
    accepted["revision"] = _stable_id(
        "manuscript-revision",
        {"candidate": candidate["revision"], "review": review},
    )
    return accepted

class SceneSession:
    def __init__(
        self,
        backend: TreeDatasetBackend,
        dataset: dict[str, Any],
        compatibility_status: dict[str, Any],
        baseline_digest: str,
    ):
        self.backend = backend
        self.dataset = dataset
        self.compatibility_status = compatibility_status
        self.baseline_digest = baseline_digest

    def context(self, scene_id: str) -> dict[str, Any]:
        return project_scene_context(self.dataset, scene_id)

    def contract(self, scene_id: str) -> dict[str, Any]:
        return build_production_contract(self.dataset, scene_id)

    def package(self, scene_id: str) -> dict[str, Any]:
        return build_generation_package(self.contract(scene_id))

    def persist_accepted(self, accepted: dict[str, Any]) -> None:
        if accepted.get("authority_class") != "accepted_manuscript":
            raise AcceptanceError(
                "only accepted Manuscript state may be persisted by this operation"
            )
        scene = _scene_by_id(self.dataset, accepted["target_scope"])
        ordinal = scene.get("ordinal")
        if not isinstance(ordinal, int):
            raise SceneRuntimeError(
                "target scene requires ordinal for Manuscript persistence"
            )

        updated = copy.deepcopy(self.dataset)
        files = updated["chapters"]["files"]
        existing = next(
            (
                entry
                for entry in files
                if entry.get("plot_scope") == accepted["target_scope"]
            ),
            None,
        )
        record = {
            "id": f"manuscript-{accepted['target_scope']}",
            "surface": "manuscript",
            "authority_class": "accepted_manuscript",
            "revision": accepted["revision"],
            "ordinal": ordinal,
            "plot_scope": accepted["target_scope"],
            "path": f"chapters/{ordinal:03d}-{accepted['target_scope']}.md",
            "generation_package_id": accepted["generation_package_id"],
            "generation_provenance": copy.deepcopy(
                accepted["generation_provenance"]
            ),
            "review": copy.deepcopy(accepted["review"]),
            "accepted_from_candidate": accepted["accepted_from_candidate"],
            "content": accepted["text"],
        }
        if existing is None:
            files.append(record)
        else:
            files[files.index(existing)] = record
        files.sort(key=lambda entry: entry.get("ordinal", 0))

        self.baseline_digest = self.backend.save(
            updated,
            expected_digest=self.baseline_digest,
        )
        self.dataset = updated

    def next_scene(self, after_scene_id: str) -> dict[str, Any] | None:
        current = _scene_by_id(self.dataset, after_scene_id)
        ordinal = current.get("ordinal")
        if not isinstance(ordinal, int):
            return None
        later = [
            s
            for s in self.dataset.get("plot", {}).get("sequence", [])
            if isinstance(s, dict)
            and isinstance(s.get("ordinal"), int)
            and s["ordinal"] > ordinal
        ]
        if not later:
            return None
        return copy.deepcopy(min(later, key=lambda s: s["ordinal"]))

def open_scene_session(
    repository_root: Path,
    *,
    authorize_transition: bool = False,
) -> SceneSession:
    backend = TreeDatasetBackend(repository_root)
    dataset = backend.load()
    baseline_digest = hashlib.sha256(_canonical(dataset)).hexdigest()
    status = COMPAT.classify(dataset, requested_operation="ordinary")
    if status.get("state") == "migration_required":
        if not authorize_transition:
            raise CompatibilityGateError(status)
        dataset = COMPAT.migrate(
            dataset,
            status["transition"],
            authorized=True,
        )
        status = COMPAT.classify(dataset, requested_operation="ordinary")
    elif status.get("state") == "rebinding_required":
        if not authorize_transition:
            raise CompatibilityGateError(status)
        dataset = COMPAT.rebind(
            dataset,
            status["transition"],
            authorized=True,
        )
        status = COMPAT.classify(dataset, requested_operation="ordinary")

    if status.get("state") != "directly_compatible":
        raise CompatibilityGateError(status)
    return SceneSession(
        backend,
        dataset,
        status,
        baseline_digest=baseline_digest,
    )
