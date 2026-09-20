#!/usr/bin/env python3
from __future__ import annotations

import copy
import hashlib
import json
from typing import Any


class GeneratedViewError(ValueError):
    pass


def _canonical(value: Any) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")


def _stable_id(prefix: str, value: Any) -> str:
    return f"{prefix}-{hashlib.sha256(_canonical(value)).hexdigest()[:20]}"


def _iter_artifacts(dataset: dict[str, Any]):
    canon = dataset.get("canon", {})
    for surface, key in (
        ("canon.character", "character"),
        ("canon.setting", "setting"),
    ):
        values = canon.get(key, {})
        if isinstance(values, dict):
            for artifact in values.values():
                if isinstance(artifact, dict):
                    yield surface, artifact

    events = canon.get("events", [])
    if isinstance(events, list):
        for artifact in events:
            if isinstance(artifact, dict):
                yield "canon.events", artifact

    plot = dataset.get("plot", {})
    synopsis = plot.get("synopsis")
    if isinstance(synopsis, dict) and synopsis.get("id"):
        yield "plot.synopsis", synopsis
    for surface, key in (
        ("plot.outline", "outline"),
        ("plot.sequence", "sequence"),
    ):
        values = plot.get(key, [])
        if isinstance(values, list):
            for artifact in values:
                if isinstance(artifact, dict):
                    yield surface, artifact

    prose = dataset.get("prose", {})
    for surface, key in (
        ("prose.beats", "beats"),
        ("prose.modes", "modes"),
        ("prose.pseudo_prose", "pseudo_prose"),
    ):
        values = prose.get(key, {})
        if isinstance(values, dict):
            for artifact in values.values():
                if isinstance(artifact, dict):
                    yield surface, artifact

    files = dataset.get("chapters", {}).get("files", [])
    if isinstance(files, list):
        for artifact in files:
            if isinstance(artifact, dict):
                yield "manuscript", artifact


def _index(dataset: dict[str, Any]) -> dict[str, tuple[str, dict[str, Any]]]:
    result: dict[str, tuple[str, dict[str, Any]]] = {}
    for surface, artifact in _iter_artifacts(dataset):
        artifact_id = artifact.get("id")
        if isinstance(artifact_id, str) and artifact_id:
            if artifact_id in result:
                raise GeneratedViewError(f"duplicate governed identity: {artifact_id}")
            result[artifact_id] = (surface, artifact)
    return result


def _relation_targets(artifact: dict[str, Any]) -> set[str]:
    targets: set[str] = set()
    dependencies = artifact.get("dependencies")
    if isinstance(dependencies, list):
        targets.update(x for x in dependencies if isinstance(x, str) and x)
    relations = artifact.get("dependency_relations")
    if isinstance(relations, list):
        for relation in relations:
            if isinstance(relation, dict):
                target = relation.get("target_id")
                if isinstance(target, str) and target:
                    targets.add(target)
    for field in ("viewpoint", "target_scope", "plot_scope"):
        value = artifact.get(field)
        if isinstance(value, str) and value:
            targets.add(value)
    return targets


def _project_artifact(artifact: dict[str, Any]) -> dict[str, Any]:
    value = copy.deepcopy(artifact)
    # Revision candidates are workflow state with their own identity/revision/status.
    # Project them separately so authority and freshness are not flattened into the
    # accepted artifact that owns their storage.
    value.pop("revision_candidates", None)
    return value


def _source_record(surface: str, artifact: dict[str, Any]) -> dict[str, Any]:
    artifact_id = artifact.get("id")
    revision = artifact.get("revision")
    if not isinstance(artifact_id, str) or not artifact_id:
        raise GeneratedViewError("projected governed source requires durable identity")
    if not isinstance(revision, str) or not revision:
        raise GeneratedViewError(f"{artifact_id}: projected governed source requires durable revision")
    return {
        "kind": "artifact",
        "id": artifact_id,
        "surface": surface,
        "revision": revision,
        "authority_class": artifact.get("authority_class", "unresolved"),
    }


def _revision_candidate_records(
    surface: str,
    artifact: dict[str, Any],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    sources: list[dict[str, Any]] = []
    projected: list[dict[str, Any]] = []
    values = artifact.get("revision_candidates", [])
    if not isinstance(values, list):
        return sources, projected

    parent_id = artifact.get("id")
    if not isinstance(parent_id, str) or not parent_id:
        return sources, projected

    for candidate in values:
        if not isinstance(candidate, dict):
            continue
        candidate_id = candidate.get("id")
        revision = candidate.get("revision")
        if not isinstance(candidate_id, str) or not candidate_id:
            continue
        if not isinstance(revision, str) or not revision:
            continue
        sources.append({
            "kind": "revision_candidate",
            "id": candidate_id,
            "parent_id": parent_id,
            "surface": surface,
            "revision": revision,
            "authority_class": candidate.get("authority_class", "candidate_semantic"),
            "status": candidate.get("status", "unresolved"),
        })
        projected.append({
            "owner_id": parent_id,
            "owner_surface": surface,
            "candidate": copy.deepcopy(candidate),
        })
    return sources, projected


def _find_revision_candidate(
    dataset: dict[str, Any],
    parent_id: str,
    candidate_id: str,
) -> tuple[str, dict[str, Any], dict[str, Any]] | None:
    located = _index(dataset).get(parent_id)
    if located is None:
        return None
    surface, parent = located
    values = parent.get("revision_candidates", [])
    if not isinstance(values, list):
        return None
    for candidate in values:
        if isinstance(candidate, dict) and candidate.get("id") == candidate_id:
            return surface, parent, candidate
    return None


def _source_basis(source: dict[str, Any]) -> tuple[Any, ...]:
    return (
        source.get("kind", "artifact"),
        source.get("id"),
        source.get("parent_id"),
        source.get("surface"),
        source.get("revision"),
        source.get("authority_class"),
        source.get("status"),
    )


def character_dossier(
    dataset: dict[str, Any],
    character_id: str,
    *,
    preferences: dict[str, Any] | None = None,
) -> dict[str, Any]:
    if not isinstance(character_id, str) or not character_id:
        raise GeneratedViewError("character dossier requires character identity")

    index = _index(dataset)
    located = index.get(character_id)
    if located is None or located[0] != "canon.character":
        raise GeneratedViewError(f"unknown Character scope: {character_id}")
    _, character = located

    related: list[tuple[str, dict[str, Any]]] = []
    for surface, artifact in _iter_artifacts(dataset):
        if artifact is character:
            continue
        if character_id in _relation_targets(artifact):
            related.append((surface, artifact))

    projected_artifacts = [("canon.character", character), *related]
    sources: list[dict[str, Any]] = []
    workflow_context: list[dict[str, Any]] = []
    for surface, artifact in projected_artifacts:
        sources.append(_source_record(surface, artifact))
        candidate_sources, candidate_context = _revision_candidate_records(
            surface,
            artifact,
        )
        sources.extend(candidate_sources)
        workflow_context.extend(candidate_context)
    sources.sort(
        key=lambda item: (
            item.get("surface", ""),
            item.get("parent_id", ""),
            item.get("id", ""),
            item.get("kind", ""),
        )
    )

    canon_events = [
        _project_artifact(artifact)
        for surface, artifact in related
        if surface == "canon.events"
    ]
    plot_context = [
        _project_artifact(artifact)
        for surface, artifact in related
        if surface.startswith("plot.")
    ]
    production_context = [
        _project_artifact(artifact)
        for surface, artifact in related
        if surface.startswith("prose.")
    ]

    story_identity = dataset.get("instance", {}).get("id")
    view_basis = {
        "story": story_identity,
        "type": "character-dossier",
        "character": character_id,
        "sources": [_source_basis(x) for x in sources],
    }
    return {
        "id": _stable_id("generated-view", {
            "story": story_identity,
            "type": "character-dossier",
            "character": character_id,
        }),
        "view_type": "character-dossier",
        "derived": True,
        "authority_class": "derived_view",
        "story_id": story_identity,
        "character_scope": character_id,
        "projection_revision": _stable_id("projection", view_basis),
        "source_attribution": sources,
        # Current/stale is intentionally not cached in the view. It is computed
        # against current governed state with view_freshness().
        "freshness_basis": "source_attribution",
        "presentation": copy.deepcopy(preferences or {}),
        "content": {
            "character": _project_artifact(character),
            "canon_events": canon_events,
            "plot_context": plot_context,
            "production_context": production_context,
            "workflow_context": workflow_context,
        },
    }


def view_freshness(dataset: dict[str, Any], view: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(view, dict) or view.get("derived") is not True:
        raise GeneratedViewError("generated-view freshness requires a derived view")
    sources = view.get("source_attribution")
    if not isinstance(sources, list):
        raise GeneratedViewError("generated view lacks source attribution")

    current = _index(dataset)
    affected: list[dict[str, Any]] = []
    for source in sources:
        if not isinstance(source, dict):
            affected.append({"reason": "invalid-source-attribution"})
            continue

        kind = source.get("kind", "artifact")
        source_id = source.get("id")
        expected_revision = source.get("revision")

        if kind == "revision_candidate":
            parent_id = source.get("parent_id")
            if not isinstance(parent_id, str) or not isinstance(source_id, str):
                affected.append({
                    "id": source_id,
                    "reason": "invalid-revision-candidate-attribution",
                })
                continue
            located_candidate = _find_revision_candidate(dataset, parent_id, source_id)
            if located_candidate is None:
                affected.append({
                    "id": source_id,
                    "parent_id": parent_id,
                    "reason": "missing",
                    "expected_revision": expected_revision,
                    "current_revision": None,
                })
                continue
            surface, _, candidate = located_candidate
            current_revision = candidate.get("revision")
            current_status = candidate.get("status", "unresolved")
            current_authority = candidate.get(
                "authority_class",
                "candidate_semantic",
            )
            if (
                current_revision != expected_revision
                or surface != source.get("surface")
                or current_status != source.get("status")
                or current_authority != source.get("authority_class")
            ):
                affected.append({
                    "id": source_id,
                    "parent_id": parent_id,
                    "reason": "changed",
                    "expected_revision": expected_revision,
                    "current_revision": current_revision,
                    "expected_status": source.get("status"),
                    "current_status": current_status,
                    "expected_surface": source.get("surface"),
                    "current_surface": surface,
                })
            continue

        located = current.get(source_id) if isinstance(source_id, str) else None
        if located is None:
            affected.append({
                "id": source_id,
                "reason": "missing",
                "expected_revision": expected_revision,
                "current_revision": None,
            })
            continue
        surface, artifact = located
        current_revision = artifact.get("revision")
        current_authority = artifact.get("authority_class", "unresolved")
        if (
            current_revision != expected_revision
            or surface != source.get("surface")
            or current_authority != source.get("authority_class")
        ):
            affected.append({
                "id": source_id,
                "reason": "changed",
                "expected_revision": expected_revision,
                "current_revision": current_revision,
                "expected_surface": source.get("surface"),
                "current_surface": surface,
                "expected_authority_class": source.get("authority_class"),
                "current_authority_class": current_authority,
            })

    return {
        "state": "stale" if affected else "current",
        "affected_sources": affected,
    }


def refresh_view(dataset: dict[str, Any], view: dict[str, Any]) -> dict[str, Any]:
    if view.get("view_type") != "character-dossier":
        raise GeneratedViewError(f"unsupported generated view type: {view.get('view_type')}")
    character_id = view.get("character_scope")
    if not isinstance(character_id, str) or not character_id:
        raise GeneratedViewError("character dossier has no Character scope")
    preferences = view.get("presentation")
    if preferences is not None and not isinstance(preferences, dict):
        raise GeneratedViewError("generated-view presentation metadata must be an object")
    return character_dossier(dataset, character_id, preferences=preferences)


def apply_presentation_preferences(
    view: dict[str, Any],
    preferences: dict[str, Any],
) -> dict[str, Any]:
    if not isinstance(view, dict) or view.get("derived") is not True:
        raise GeneratedViewError("presentation preferences require a derived view")
    if not isinstance(preferences, dict):
        raise GeneratedViewError("presentation preferences must be an object")
    result = copy.deepcopy(view)
    current = result.get("presentation")
    if not isinstance(current, dict):
        current = {}
    current.update(copy.deepcopy(preferences))
    result["presentation"] = current
    return result


def compare_views(before: dict[str, Any], after: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(before, dict) or not isinstance(after, dict):
        raise GeneratedViewError("view comparison requires two views")
    if before.get("id") != after.get("id"):
        raise GeneratedViewError("view comparison requires the same generated-view identity")

    before_sources = {
        (
            x.get("kind", "artifact"),
            x.get("parent_id"),
            x.get("id"),
        ): x
        for x in before.get("source_attribution", [])
        if isinstance(x, dict) and isinstance(x.get("id"), str)
    }
    after_sources = {
        (
            x.get("kind", "artifact"),
            x.get("parent_id"),
            x.get("id"),
        ): x
        for x in after.get("source_attribution", [])
        if isinstance(x, dict) and isinstance(x.get("id"), str)
    }
    changed = []
    for source_key in sorted(set(before_sources) | set(after_sources)):
        old = before_sources.get(source_key)
        new = after_sources.get(source_key)
        if old != new:
            changed.append({
                "kind": source_key[0],
                "parent_id": source_key[1],
                "id": source_key[2],
                "before": copy.deepcopy(old),
                "after": copy.deepcopy(new),
            })
    return {
        "view": "generated-view-comparison",
        "derived": True,
        "authority_class": "derived_view",
        "view_id": before.get("id"),
        "before_projection_revision": before.get("projection_revision"),
        "after_projection_revision": after.get("projection_revision"),
        "changed_sources": changed,
        "content_changed": before.get("content") != after.get("content"),
        "presentation_changed": before.get("presentation") != after.get("presentation"),
    }


def _normalize_edit_targets(edit: dict[str, Any]) -> list[dict[str, Any]]:
    if not isinstance(edit, dict):
        raise GeneratedViewError("generated-view edit must be an object")
    if "targets" in edit:
        targets = edit.get("targets")
        if not isinstance(targets, list) or not targets:
            raise GeneratedViewError("generated-view coordinated edit requires targets")
    elif "target_id" in edit or "changes" in edit:
        targets = [{
            "target_id": edit.get("target_id"),
            "changes": edit.get("changes"),
        }]
    else:
        raise GeneratedViewError("generated-view edit is ambiguous: governed target is not explicit")

    normalized: list[dict[str, Any]] = []
    seen: set[str] = set()
    for target in targets:
        if not isinstance(target, dict):
            raise GeneratedViewError("generated-view edit target must be an object")
        target_id = target.get("target_id")
        changes = target.get("changes")
        if not isinstance(target_id, str) or not target_id:
            raise GeneratedViewError("generated-view edit is ambiguous: target identity is required")
        if target_id in seen:
            raise GeneratedViewError(f"duplicate generated-view edit target: {target_id}")
        if not isinstance(changes, dict) or not changes:
            raise GeneratedViewError(f"{target_id}: generated-view edit requires explicit changes")
        seen.add(target_id)
        normalized.append({
            "target_id": target_id,
            "changes": copy.deepcopy(changes),
        })
    return normalized


def _propose_view_edit_in_place(
    session: Any,
    view: dict[str, Any],
    edit: dict[str, Any],
) -> dict[str, Any]:
    targets = _normalize_edit_targets(edit)
    artifact_sources = {
        source.get("id"): source
        for source in view.get("source_attribution", [])
        if isinstance(source, dict)
        and source.get("kind", "artifact") == "artifact"
        and isinstance(source.get("id"), str)
    }
    current = _index(session.dataset)

    plans: list[dict[str, Any]] = []
    for target in targets:
        target_id = target["target_id"]
        if target_id not in artifact_sources:
            raise GeneratedViewError(
                f"generated-view edit is ambiguous: {target_id} is not an attributed governed artifact"
            )
        located = current.get(target_id)
        if located is None:
            raise GeneratedViewError(f"generated-view edit target disappeared: {target_id}")
        surface, artifact = located
        source = artifact_sources[target_id]
        if (
            artifact.get("revision") != source.get("revision")
            or surface != source.get("surface")
            or artifact.get("authority_class", "unresolved")
                != source.get("authority_class")
        ):
            raise GeneratedViewError(f"generated-view edit target is stale: {target_id}")

        authority = artifact.get("authority_class")
        if authority in {"candidate_semantic", "production_candidate"}:
            operation = "revise_candidate"
        elif authority == "accepted_semantic" and (
            surface.startswith("canon.") or surface.startswith("plot.")
        ):
            operation = "propose_revision"
        else:
            raise GeneratedViewError(
                f"{target_id}: no existing governed edit operation for {surface}/{authority}"
            )
        plans.append({
            "target_id": target_id,
            "surface": surface,
            "authority_class": authority,
            "operation": operation,
            "changes": target["changes"],
        })

    proposals = []
    for plan in plans:
        if plan["operation"] == "revise_candidate":
            proposal = session.revise_candidate(plan["target_id"], plan["changes"])
            proposal_id = proposal.get("id")
        else:
            proposal = session.propose_revision(plan["target_id"], plan["changes"])
            proposal_id = proposal.get("id")
        proposals.append({
            "target_id": plan["target_id"],
            "surface": plan["surface"],
            "operation": plan["operation"],
            "proposal_id": proposal_id,
            "proposal": copy.deepcopy(proposal),
        })

    return {
        "view": "generated-view-edit-proposal",
        "derived": True,
        "authority_class": "derived_workflow_evidence",
        "classification": (
            "coordinated_multi_target_governed_edit"
            if len(proposals) > 1
            else "unambiguous_governed_edit"
        ),
        "source_view_id": view.get("id"),
        "source_projection_revision": view.get("projection_revision"),
        "proposals": proposals,
    }

def propose_view_edit(
    session: Any,
    view: dict[str, Any],
    edit: dict[str, Any],
) -> dict[str, Any]:
    before = copy.deepcopy(session.dataset)
    try:
        return _propose_view_edit_in_place(session, view, edit)
    except Exception:
        session.dataset.clear()
        session.dataset.update(before)
        raise
