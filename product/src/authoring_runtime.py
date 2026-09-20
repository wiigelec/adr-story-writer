#!/usr/bin/env python3
from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
from pathlib import Path
from typing import Any


class AuthoringRuntimeError(ValueError):
    pass


def _load_revision_runtime():
    path = Path(__file__).resolve().with_name("revision_runtime.py")
    spec = importlib.util.spec_from_file_location("story_writer_revision_fs005", path)
    if spec is None or spec.loader is None:
        raise AuthoringRuntimeError("cannot load revision runtime")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


REV = _load_revision_runtime()
SCENE = REV.SCENE


def _canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def _stable_id(prefix: str, value: Any) -> str:
    return f"{prefix}-{hashlib.sha256(_canonical(value)).hexdigest()[:20]}"


SURFACES = {
    "canon.character": ("semantic", "mapping"),
    "canon.setting": ("semantic", "mapping"),
    "canon.events": ("semantic", "sequence"),
    "plot.synopsis": ("semantic", "singleton"),
    "plot.outline": ("semantic", "sequence"),
    "plot.sequence": ("semantic", "sequence"),
    "prose.beats": ("production", "mapping"),
    "prose.modes": ("production", "mapping"),
    "prose.pseudo_prose": ("production", "mapping"),
}


def _surface_container(dataset: dict[str, Any], surface: str):
    if surface == "canon.character":
        return dataset["canon"]["character"]
    if surface == "canon.setting":
        return dataset["canon"]["setting"]
    if surface == "canon.events":
        return dataset["canon"]["events"]
    if surface == "plot.synopsis":
        return dataset["plot"], "synopsis"
    if surface == "plot.outline":
        return dataset["plot"]["outline"]
    if surface == "plot.sequence":
        return dataset["plot"]["sequence"]
    if surface == "prose.beats":
        return dataset["prose"]["beats"]
    if surface == "prose.modes":
        return dataset["prose"]["modes"]
    if surface == "prose.pseudo_prose":
        return dataset["prose"]["pseudo_prose"]
    raise AuthoringRuntimeError(f"unsupported authoring surface: {surface}")


def _candidate_authority(surface: str) -> str:
    kind = SURFACES.get(surface, (None, None))[0]
    if kind == "semantic":
        return "candidate_semantic"
    if kind == "production":
        return "production_candidate"
    raise AuthoringRuntimeError(f"unsupported authoring surface: {surface}")


def _accepted_authority(surface: str) -> str:
    kind = SURFACES.get(surface, (None, None))[0]
    if kind == "semantic":
        return "accepted_semantic"
    if kind == "production":
        return "production_approved"
    raise AuthoringRuntimeError(f"unsupported authoring surface: {surface}")


def _find(dataset: dict[str, Any], artifact_id: str) -> dict[str, Any]:
    try:
        return REV._artifact(dataset, artifact_id)
    except REV.RevisionRuntimeError as exc:
        raise AuthoringRuntimeError(str(exc)) from exc


def _authority_basis(artifact: dict[str, Any] | None) -> str:
    if not isinstance(artifact, dict):
        return "unresolved"
    authority = artifact.get("authority_class")
    if authority in {"accepted_semantic", "accepted_manuscript", "production_approved"}:
        return "accepted"
    if authority in {"candidate_semantic", "candidate_manuscript", "production_candidate"}:
        return "candidate"
    return "unresolved"


def _normalize_dependencies(dataset: dict[str, Any], dependencies: list[str] | None):
    if dependencies is None:
        return [], []
    if not isinstance(dependencies, list) or any(not isinstance(x, str) or not x for x in dependencies):
        raise AuthoringRuntimeError("dependencies must be an array of non-empty artifact ids")
    ids = []
    relations = []
    for target_id in dependencies:
        if target_id in ids:
            continue
        target = _find(dataset, target_id)
        revision = target.get("revision")
        if not isinstance(revision, str) or not revision:
            raise AuthoringRuntimeError(f"dependency {target_id} has no durable revision")
        basis = _authority_basis(target)
        if basis == "unresolved":
            raise AuthoringRuntimeError(f"dependency {target_id} has unsupported authority state")
        ids.append(target_id)
        relations.append({
            "target_id": target_id,
            "target_revision": revision,
            "authority_basis": basis,
            "material": True,
        })
    return ids, relations


def _insert(dataset: dict[str, Any], surface: str, artifact: dict[str, Any]) -> None:
    _, shape = SURFACES[surface]
    container = _surface_container(dataset, surface)
    if shape == "singleton":
        parent, key = container
        current = parent.get(key)
        if isinstance(current, dict) and current.get("id"):
            raise AuthoringRuntimeError(f"{surface} already has a governed artifact; use FS-004 revision")
        parent[key] = artifact
    elif shape == "sequence":
        if not isinstance(container, list):
            raise AuthoringRuntimeError(f"{surface} container must be an array")
        container.append(artifact)
    elif shape == "mapping":
        if not isinstance(container, dict):
            raise AuthoringRuntimeError(f"{surface} container must be an object")
        if artifact["id"] in container:
            raise AuthoringRuntimeError(f"surface key already exists: {artifact['id']}")
        container[artifact["id"]] = artifact
    else:
        raise AuthoringRuntimeError(f"unsupported container shape for {surface}")


def _remove(dataset: dict[str, Any], artifact_id: str) -> dict[str, Any]:
    container, key = REV._location(dataset, artifact_id)
    artifact = container[key]
    if isinstance(container, list):
        del container[key]
    elif key == "synopsis":
        container[key] = {}
    else:
        del container[key]
    return artifact


def _material_blockers(dataset: dict[str, Any], artifact: dict[str, Any], coordinated_ids: set[str]) -> list[str]:
    blockers = []
    relations = artifact.get("dependency_relations")
    if not isinstance(relations, list):
        relations = []
        deps = artifact.get("dependencies", [])
        for target_id in deps if isinstance(deps, list) else []:
            try:
                target = _find(dataset, target_id)
            except AuthoringRuntimeError:
                target = None
            relations.append({
                "target_id": target_id,
                "target_revision": target.get("revision") if target else None,
                "authority_basis": _authority_basis(target),
                "material": True,
            })

    for relation in relations:
        if not isinstance(relation, dict) or relation.get("material") is not True:
            continue
        target_id = relation.get("target_id")
        if not isinstance(target_id, str) or not target_id:
            blockers.append("invalid material dependency")
            continue
        try:
            target = _find(dataset, target_id)
        except AuthoringRuntimeError:
            blockers.append(f"missing dependency {target_id}")
            continue

        expected_revision = relation.get("target_revision")
        if not isinstance(expected_revision, str) or not expected_revision:
            blockers.append(f"dependency {target_id} has unresolved revision")
            continue
        if target.get("revision") != expected_revision:
            blockers.append(f"dependency {target_id} is stale")
            continue
        if REV._blocked(target):
            blockers.append(f"dependency {target_id} has unresolved reconciliation")
            continue

        basis = _authority_basis(target)
        if basis == "accepted":
            continue
        if basis == "candidate" and target_id in coordinated_ids:
            continue
        blockers.append(f"dependency {target_id} is not accepted in scope")

    surface = artifact.get("surface")
    if isinstance(surface, str) and surface.startswith("prose."):
        target_scope = artifact.get("target_scope")
        if surface != "prose.modes" or target_scope is not None:
            if not isinstance(target_scope, str) or not target_scope:
                blockers.append(f"{surface} requires target_scope")
            else:
                try:
                    target = _find(dataset, target_scope)
                except AuthoringRuntimeError:
                    blockers.append(f"missing target scope {target_scope}")
                else:
                    if REV._blocked(target):
                        blockers.append(f"target scope {target_scope} has unresolved reconciliation")
                    elif _authority_basis(target) != "accepted" and target_scope not in coordinated_ids:
                        blockers.append(f"target scope {target_scope} is not accepted in scope")
    return blockers


def _candidate_artifacts(dataset: dict[str, Any]) -> list[dict[str, Any]]:
    result = []
    for artifact in SCENE._iter_artifacts(dataset):
        if artifact.get("authority_class") in {"candidate_semantic", "production_candidate", "candidate_manuscript"}:
            result.append(copy.deepcopy(artifact))
        revisions = artifact.get("revision_candidates", [])
        if isinstance(revisions, list):
            for candidate in revisions:
                if isinstance(candidate, dict) and candidate.get("status") == "candidate":
                    item = copy.deepcopy(candidate)
                    item["candidate_kind"] = "revision"
                    result.append(item)
    return result


def propose_artifact(dataset: dict[str, Any], surface: str, artifact: dict[str, Any], *, dependencies=None, assumptions=None):
    if surface not in SURFACES:
        raise AuthoringRuntimeError(f"unsupported authoring surface: {surface}")
    if not isinstance(artifact, dict):
        raise AuthoringRuntimeError("artifact proposal must be an object")

    value = copy.deepcopy(artifact)
    for field in ("authority_class", "revision"):
        if field in value:
            raise AuthoringRuntimeError(f"artifact proposal cannot supply governed field {field}")
    if value.get("surface") not in (None, surface):
        raise AuthoringRuntimeError("artifact surface does not match target surface")
    value["surface"] = surface

    semantic_payload = copy.deepcopy(value)
    semantic_payload.pop("id", None)
    artifact_id = value.get("id")
    if artifact_id is None:
        artifact_id = _stable_id(surface.replace(".", "-"), semantic_payload)
        value["id"] = artifact_id
    if not isinstance(artifact_id, str) or not artifact_id:
        raise AuthoringRuntimeError("artifact id must be a non-empty string")
    try:
        _find(dataset, artifact_id)
    except AuthoringRuntimeError:
        pass
    else:
        raise AuthoringRuntimeError(f"governed artifact {artifact_id} already exists; revise it instead")

    dep_ids, relations = _normalize_dependencies(dataset, dependencies)
    if dep_ids:
        value["dependencies"] = dep_ids
        value["dependency_relations"] = relations

    if assumptions is not None:
        if not isinstance(assumptions, list) or any(not isinstance(x, str) or not x for x in assumptions):
            raise AuthoringRuntimeError("assumptions must be an array of non-empty strings")
        value["candidate_assumptions"] = list(assumptions)

    value["authority_class"] = _candidate_authority(surface)
    value["candidate_status"] = "candidate"
    value["revision"] = _stable_id("candidate-revision", {
        "id": artifact_id,
        "surface": surface,
        "payload": {k: v for k, v in value.items() if k != "revision"},
    })
    _insert(dataset, surface, value)
    return copy.deepcopy(value)


def revise_candidate(dataset: dict[str, Any], artifact_id: str, changes: dict[str, Any]):
    artifact = _find(dataset, artifact_id)
    if artifact.get("authority_class") not in {"candidate_semantic", "production_candidate"}:
        raise AuthoringRuntimeError("candidate refinement requires a pending new artifact")
    if artifact.get("candidate_status", "candidate") != "candidate":
        raise AuthoringRuntimeError("candidate is not pending")
    if not isinstance(changes, dict) or not changes:
        raise AuthoringRuntimeError("candidate refinement requires changes")
    protected = {"id", "surface", "authority_class", "revision", "dependency_relations"}
    if protected & set(changes):
        raise AuthoringRuntimeError("candidate refinement cannot replace governed identity/control fields")
    normalized_changes = copy.deepcopy(changes)
    if "dependencies" in normalized_changes:
        dep_ids, relations = _normalize_dependencies(dataset, normalized_changes["dependencies"])
        normalized_changes["dependencies"] = dep_ids
        normalized_changes["dependency_relations"] = relations
    history = artifact.setdefault("candidate_revision_history", [])
    if not isinstance(history, list):
        raise AuthoringRuntimeError("candidate_revision_history must be an array")
    previous = copy.deepcopy(artifact)
    previous.pop("candidate_revision_history", None)
    history.append(previous)
    for key, value in normalized_changes.items():
        artifact[key] = copy.deepcopy(value)
    artifact["revision"] = _stable_id("candidate-revision", {
        "id": artifact["id"],
        "prior_revision": previous["revision"],
        "changes": normalized_changes,
    })
    return copy.deepcopy(artifact)


def accept_artifacts(dataset: dict[str, Any], artifact_ids: list[str]):
    if not isinstance(artifact_ids, list) or not artifact_ids:
        raise SCENE.AcceptanceError("acceptance requires explicit artifact scope")
    if any(not isinstance(x, str) or not x for x in artifact_ids) or len(set(artifact_ids)) != len(artifact_ids):
        raise SCENE.AcceptanceError("invalid or duplicate acceptance scope")

    scope = set(artifact_ids)
    artifacts = [_find(dataset, artifact_id) for artifact_id in artifact_ids]
    for artifact in artifacts:
        if artifact.get("authority_class") not in {"candidate_semantic", "production_candidate"}:
            raise SCENE.AcceptanceError(f"{artifact.get('id')}: artifact is not an accept-ready candidate")
        blockers = _material_blockers(dataset, artifact, scope)
        if blockers:
            raise SCENE.AcceptanceError(f"{artifact.get('id')}: acceptance closure failed: {blockers}")

    # Compute the whole coordinated transition before mutating anything.
    transitions = {}
    for artifact in artifacts:
        candidate_revision = artifact["revision"]
        accepted_authority = _accepted_authority(artifact["surface"])
        accepted_revision = _stable_id("accepted-revision", {
            "id": artifact["id"],
            "candidate_revision": candidate_revision,
            "authority_class": accepted_authority,
        })
        transitions[artifact["id"]] = {
            "candidate_revision": candidate_revision,
            "accepted_authority": accepted_authority,
            "accepted_revision": accepted_revision,
        }

    for artifact in artifacts:
        transition = transitions[artifact["id"]]
        artifact["authority_class"] = transition["accepted_authority"]
        artifact["revision"] = transition["accepted_revision"]
        artifact["accepted_from_candidate_revision"] = transition["candidate_revision"]
        artifact["acceptance"] = {
            "operation": "semantic_acceptance" if transition["accepted_authority"] == "accepted_semantic" else "production_approval",
            "scope": artifact["id"],
            "candidate_revision": transition["candidate_revision"],
            "accepted_revision": transition["accepted_revision"],
        }
        artifact.pop("candidate_status", None)

    # Only dependencies accepted in this same coordinated operation need their
    # candidate revision advanced to the corresponding accepted revision.
    for artifact in artifacts:
        relations = artifact.get("dependency_relations")
        if not isinstance(relations, list):
            continue
        for relation in relations:
            if not isinstance(relation, dict):
                continue
            target_id = relation.get("target_id")
            if target_id in transitions:
                relation["target_revision"] = transitions[target_id]["accepted_revision"]
                relation["authority_basis"] = "accepted"

    return [copy.deepcopy(artifact) for artifact in artifacts]


def withdraw_artifact(dataset: dict[str, Any], artifact_id: str, *, reason=None):
    artifact = _find(dataset, artifact_id)
    if artifact.get("authority_class") not in {"candidate_semantic", "production_candidate"}:
        raise AuthoringRuntimeError("only pending new-artifact candidates may be withdrawn")
    result = copy.deepcopy(_remove(dataset, artifact_id))
    result["candidate_status"] = "withdrawn"
    if reason:
        result["resolution_reason"] = reason
    return result


def story_overview(dataset: dict[str, Any]):
    artifacts = list(SCENE._iter_artifacts(dataset))
    unresolved = [
        a["id"] for a in artifacts
        if isinstance(a.get("reconciliation"), dict)
        and a["reconciliation"].get("state") in {"review_required", "stale", "unresolved", "superseded"}
        and isinstance(a.get("id"), str)
    ]
    return {
        "view": "story",
        "derived": True,
        "story": copy.deepcopy(dataset.get("story", {})),
        "counts": {
            "accepted_semantic": sum(a.get("authority_class") == "accepted_semantic" for a in artifacts),
            "candidate_semantic": sum(a.get("authority_class") == "candidate_semantic" for a in artifacts),
            "production_approved": sum(a.get("authority_class") == "production_approved" for a in artifacts),
            "production_candidate": sum(a.get("authority_class") == "production_candidate" for a in artifacts),
            "accepted_manuscript": sum(a.get("authority_class") == "accepted_manuscript" for a in artifacts),
        },
        "pending_candidates": [c.get("id") for c in _candidate_artifacts(dataset)],
        "unresolved_reconciliation": unresolved,
    }


def overview(dataset: dict[str, Any], view="story", *, scope=None):
    if view == "story":
        return story_overview(dataset)
    if view == "canon":
        return {"view": "canon", "derived": True, **copy.deepcopy(dataset.get("canon", {}))}
    if view == "plot":
        return {"view": "plot", "derived": True, **copy.deepcopy(dataset.get("plot", {}))}
    if view == "prose":
        return {"view": "prose", "derived": True, **copy.deepcopy(dataset.get("prose", {}))}
    if view == "manuscript":
        return {"view": "manuscript", "derived": True, "chapters": copy.deepcopy(dataset.get("chapters", {}).get("files", []))}
    if view == "candidates":
        return {"view": "candidates", "derived": True, "candidates": _candidate_artifacts(dataset)}
    if view == "readiness":
        if not isinstance(scope, str) or not scope:
            raise AuthoringRuntimeError("readiness view requires scene scope")
        return readiness(dataset, scope)
    raise AuthoringRuntimeError(f"unknown author view: {view}")


def readiness(dataset: dict[str, Any], scene_id: str):
    try:
        REV.ensure_scene_ready(dataset, scene_id)
        SCENE.project_scene_context(dataset, scene_id)
    except (SCENE.SceneRuntimeError, REV.RevisionRuntimeError) as exc:
        return {"view": "readiness", "derived": True, "scene_id": scene_id, "ready": False, "blockers": [str(exc)]}
    return {"view": "readiness", "derived": True, "scene_id": scene_id, "ready": True, "blockers": []}


class AuthoringSession(REV.RevisionSession):
    def overview(self, view="story", *, scope=None):
        return overview(self.dataset, view, scope=scope)

    def propose_artifact(self, surface, artifact, *, dependencies=None, assumptions=None):
        return propose_artifact(self.dataset, surface, artifact, dependencies=dependencies, assumptions=assumptions)

    def revise_candidate(self, artifact_id, changes):
        return revise_candidate(self.dataset, artifact_id, changes)

    def accept_artifact(self, artifact_id):
        return accept_artifacts(self.dataset, [artifact_id])[0]

    def accept_artifacts(self, artifact_ids):
        return accept_artifacts(self.dataset, artifact_ids)

    def withdraw_artifact(self, artifact_id, *, reason=None):
        return withdraw_artifact(self.dataset, artifact_id, reason=reason)

    def readiness(self, scene_id):
        return readiness(self.dataset, scene_id)


def open_authoring_session(repository_root: Path, *, authorize_transition=False):
    base = REV.open_revision_session(repository_root, authorize_transition=authorize_transition)
    return AuthoringSession(
        base.backend,
        base.dataset,
        base.compatibility_status,
        base.baseline_digest,
    )
