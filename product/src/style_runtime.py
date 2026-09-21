#!/usr/bin/env python3
from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
RULESET_PROSE = ROOT / "ruleset" / "prose.json"


class StyleRuntimeError(ValueError):
    pass


def _canonical(value: Any) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")


def _profile_revision(
    profile_id: str,
    guidance: dict[str, Any],
    source_samples: list[dict[str, Any]],
) -> str:
    value = {
        "id": profile_id,
        "guidance": guidance,
        "source_samples": source_samples,
    }
    return f"style-{hashlib.sha256(_canonical(value)).hexdigest()[:20]}"


def _prose_state(dataset: dict[str, Any], *, initialize: bool) -> dict[str, Any]:
    prose = dataset.get("prose")
    if not isinstance(prose, dict):
        raise StyleRuntimeError("Dataset prose state must be an object")
    if initialize:
        prose.setdefault("style_profiles", {})
        prose.setdefault("style_selection", {"default_profile": None})
    profiles = prose.get("style_profiles", {})
    selection = prose.get("style_selection", {"default_profile": None})
    if not isinstance(profiles, dict):
        raise StyleRuntimeError("prose.style_profiles must be an object")
    if not isinstance(selection, dict):
        raise StyleRuntimeError("prose.style_selection must be an object")
    return prose


def generation_quality_guidance() -> dict[str, Any]:
    try:
        data = json.loads(RULESET_PROSE.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise StyleRuntimeError(f"cannot load Ruleset prose guidance: {exc}") from exc
    value = data.get("generation_quality_guidance")
    if not isinstance(value, dict) or not value:
        raise StyleRuntimeError("Ruleset generation_quality_guidance is missing")
    return copy.deepcopy(value)


def _normalize_source_samples(
    source_samples: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    if not isinstance(source_samples, list) or not source_samples:
        raise StyleRuntimeError("style profile requires at least one source sample reference")

    field_limits = {
        "kind": 128,
        "reference": 2048,
        "label": 512,
        "revision": 256,
        "digest": 256,
    }
    normalized_sources = []
    for source in source_samples:
        if not isinstance(source, dict):
            raise StyleRuntimeError("style source reference must be an object")
        reference = source.get("reference")
        if not isinstance(reference, str) or not reference.strip():
            raise StyleRuntimeError("style source reference requires reference")

        normalized = {}
        for key, limit in field_limits.items():
            if key not in source:
                continue
            value = source[key]
            if not isinstance(value, str):
                raise StyleRuntimeError(
                    f"style source provenance field {key} must be a string"
                )
            if len(value) > limit:
                raise StyleRuntimeError(
                    f"style source provenance field {key} exceeds {limit} characters"
                )
            normalized[key] = value
        normalized_sources.append(normalized)
    return normalized_sources


def propose_style_profile(
    dataset: dict[str, Any],
    *,
    profile_id: str,
    guidance: dict[str, Any],
    source_samples: list[dict[str, Any]],
) -> dict[str, Any]:
    if not isinstance(profile_id, str) or not profile_id:
        raise StyleRuntimeError("style profile requires a non-empty id")
    if not isinstance(guidance, dict) or not guidance:
        raise StyleRuntimeError("style profile requires normalized guidance")
    normalized_sources = _normalize_source_samples(source_samples)

    prose = _prose_state(dataset, initialize=True)
    profiles = prose["style_profiles"]
    if profile_id in profiles:
        raise StyleRuntimeError(f"style profile already exists: {profile_id}")

    normalized_guidance = copy.deepcopy(guidance)
    profile = {
        "id": profile_id,
        "surface": "prose.style_profile",
        "authority_class": "production_candidate",
        "revision": _profile_revision(
            profile_id,
            normalized_guidance,
            normalized_sources,
        ),
        "guidance": normalized_guidance,
        "source_samples": normalized_sources,
    }
    profiles[profile_id] = profile
    return copy.deepcopy(profile)


def revise_style_profile(
    dataset: dict[str, Any],
    *,
    profile_id: str,
    guidance: dict[str, Any],
    source_samples: list[dict[str, Any]],
) -> dict[str, Any]:
    if not isinstance(guidance, dict) or not guidance:
        raise StyleRuntimeError("style profile requires normalized guidance")
    normalized_sources = _normalize_source_samples(source_samples)
    prose = _prose_state(dataset, initialize=True)
    profile = prose["style_profiles"].get(profile_id)
    if not isinstance(profile, dict):
        raise StyleRuntimeError(f"unknown style profile: {profile_id}")
    if profile.get("authority_class") != "production_approved":
        raise StyleRuntimeError("only a production_approved style profile may be revised")
    prior_revision = profile.get("revision")
    if not isinstance(prior_revision, str) or not prior_revision:
        raise StyleRuntimeError("approved style profile lacks durable revision")

    normalized_guidance = copy.deepcopy(guidance)
    new_revision = _profile_revision(
        profile_id,
        normalized_guidance,
        normalized_sources,
    )
    if new_revision == prior_revision:
        raise StyleRuntimeError("style profile revision must change governed content")

    profile["authority_class"] = "production_candidate"
    profile["revision"] = new_revision
    profile["guidance"] = normalized_guidance
    profile["source_samples"] = normalized_sources
    profile["supersedes_revision"] = prior_revision
    return copy.deepcopy(profile)


def approve_style_profile(
    dataset: dict[str, Any],
    profile_id: str,
) -> dict[str, Any]:
    prose = _prose_state(dataset, initialize=True)
    profile = prose["style_profiles"].get(profile_id)
    if not isinstance(profile, dict):
        raise StyleRuntimeError(f"unknown style profile: {profile_id}")
    if profile.get("authority_class") != "production_candidate":
        raise StyleRuntimeError("only a production_candidate style profile may be approved")
    profile["authority_class"] = "production_approved"
    return copy.deepcopy(profile)


def select_default_style_profile(
    dataset: dict[str, Any],
    profile_id: str | None,
) -> dict[str, Any]:
    prose = _prose_state(dataset, initialize=True)
    if profile_id is not None:
        profile = prose["style_profiles"].get(profile_id)
        if not isinstance(profile, dict):
            raise StyleRuntimeError(f"unknown style profile: {profile_id}")
        if profile.get("authority_class") != "production_approved":
            raise StyleRuntimeError("default style profile must be production_approved")
    prose["style_selection"] = {"default_profile": profile_id}
    return copy.deepcopy(prose["style_selection"])


def resolve_style_projection(
    dataset: dict[str, Any],
    *,
    scene_id: str,
    local_style_guidance: list[Any] | None = None,
    material_conflicts: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    prose = _prose_state(dataset, initialize=False)
    profiles = prose.get("style_profiles", {})
    selection = prose.get("style_selection", {"default_profile": None})
    selected_id = selection.get("default_profile")

    author_profile = None
    author_guidance: dict[str, Any] = {}
    if selected_id is not None:
        if not isinstance(selected_id, str) or not selected_id:
            raise StyleRuntimeError("default style profile identity is invalid")
        profile = profiles.get(selected_id)
        if not isinstance(profile, dict):
            raise StyleRuntimeError(
                f"selected style profile is missing: {selected_id}"
            )
        if profile.get("authority_class") != "production_approved":
            raise StyleRuntimeError(
                "selected style profile is not production_approved"
            )
        if not isinstance(profile.get("revision"), str) or not profile["revision"]:
            raise StyleRuntimeError("selected style profile lacks durable revision")
        guidance = profile.get("guidance")
        if not isinstance(guidance, dict):
            raise StyleRuntimeError("selected style profile guidance must be an object")
        author_guidance = copy.deepcopy(guidance)
        author_profile = {
            "id": selected_id,
            "revision": profile["revision"],
        }

    local = [] if local_style_guidance is None else copy.deepcopy(local_style_guidance)
    if not isinstance(local, list):
        raise StyleRuntimeError("local style guidance must be an array")

    raw_conflicts = [] if material_conflicts is None else material_conflicts
    if not isinstance(raw_conflicts, list):
        raise StyleRuntimeError("material style conflicts must be an array")
    if len(raw_conflicts) > 32:
        raise StyleRuntimeError("material style conflicts exceed the bounded limit")

    allowed_conflict_fields = {"description", "layers", "references"}
    allowed_layers = {
        "generation_quality_guidance",
        "author_style_guidance",
        "local_style_guidance",
    }
    conflicts = []
    for conflict in raw_conflicts:
        if not isinstance(conflict, dict):
            raise StyleRuntimeError("material style conflict must be an object")
        unknown = set(conflict) - allowed_conflict_fields
        if unknown:
            raise StyleRuntimeError(
                f"material style conflict has unsupported fields: {sorted(unknown)}"
            )

        description = conflict.get("description")
        if (
            not isinstance(description, str)
            or not description.strip()
            or len(description) > 2048
        ):
            raise StyleRuntimeError(
                "material style conflict requires a non-empty description "
                "of at most 2048 characters"
            )

        normalized_conflict = {"description": description}

        if "layers" in conflict:
            layers = conflict["layers"]
            if (
                not isinstance(layers, list)
                or len(layers) > 3
                or any(
                    not isinstance(layer, str) or layer not in allowed_layers
                    for layer in layers
                )
            ):
                raise StyleRuntimeError(
                    "material style conflict layers must be known style layers"
                )
            normalized_conflict["layers"] = copy.deepcopy(layers)

        if "references" in conflict:
            references = conflict["references"]
            if (
                not isinstance(references, list)
                or len(references) > 32
                or any(
                    not isinstance(reference, str)
                    or not reference.strip()
                    or len(reference) > 2048
                    for reference in references
                )
            ):
                raise StyleRuntimeError(
                    "material style conflict references must be bounded non-empty strings"
                )
            normalized_conflict["references"] = copy.deepcopy(references)

        conflicts.append(normalized_conflict)

    return {
        "status": "unresolved" if conflicts else "ready",
        "material_conflicts": conflicts,
        "target_scope": scene_id,
        "generation_quality_guidance": generation_quality_guidance(),
        "author_profile": author_profile,
        "author_style_guidance": author_guidance,
        "local_style_guidance": local,
        "layers": [
            "generation_quality_guidance",
            "author_style_guidance",
            "local_style_guidance",
        ],
        "conflict_policy": (
            "material semantic conflicts require review; locality does not "
            "silently authorize contradiction of accepted broader guidance"
        ),
    }
