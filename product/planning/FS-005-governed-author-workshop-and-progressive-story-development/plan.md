---
functional_set: FS-005
artifact: implementation-plan
title: Governed Author Workshop and Progressive Story Development Plan
design_revision: 21e017572c31f0aa9b95b9de0785f557511949b1
---

# FS-005 — Plan

## Objective

Implement an agent-facing authoring facade that realizes ordinary progressive
story development while preserving the authority, revision, dependency,
compatibility, production, and persistence contracts established by FS-001
through FS-004.

## Runtime Shape

Add `product/src/authoring_runtime.py`.

`AuthoringSession` extends FS-004 `RevisionSession` and exposes:

- `overview(view, scope=None)`
- `propose_artifact(surface, artifact, dependencies=None, assumptions=None)`
- `revise_candidate(artifact_id, changes)`
- `accept_artifact(artifact_id)`
- `accept_artifacts(artifact_ids)` for explicit coordinated acceptance
- `withdraw_artifact(artifact_id)`
- `readiness(scene_id)`
- inherited FS-004 revision/reconciliation operations
- inherited FS-003 context/contract/package/Manuscript operations
- coherent `persist()`

## New-artifact Representation

New governed candidates live directly on their owning Dataset surface:
`canon.character`, `canon.setting`, `canon.events`, `plot.synopsis`,
`plot.outline`, `plot.sequence`, `prose.beats`, `prose.modes`, and
`prose.pseudo_prose`.

Canon/Plot candidates use `candidate_semantic`. Prose-control candidates use
`production_candidate`. Acceptance changes only targeted authority after closure:
semantic candidates become `accepted_semantic`; production candidates become
`production_approved`.

Revision of an already accepted Canon or Plot artifact remains owned by FS-004
`propose_revision` / `accept_revision`.

## Identity, Dependencies, and Closure

Every proposal receives durable identity and revision. Candidate refinement
preserves identity and records prior candidate revision snapshots.

Explicit proposal dependencies are normalized into material dependency relations
with target identity, revision, and authority basis.

Single-scope acceptance requires every material dependency to be accepted.
Coordinated acceptance permits candidate dependencies only when those exact
targets are explicitly included in the same acceptance scope. Scope is never
expanded automatically.

## Progressive Refinement and Readiness

The runtime does not invent refinement content. The agent proposes it.

The supported path is:

Canon → Plot synopsis/outline/sequence → Prose Beats/Modes/pseudo-prose →
generation readiness → existing FS-003 context/contract/package.

Production approval is explicit. Readiness delegates to current FS-003/FS-004
gates and returns not-ready rather than synthesizing missing consequential intent.

## Author-facing Views

`overview()` provides derived structured projections for `story`, `canon`, `plot`,
`prose`, `manuscript`, `candidates`, and bounded `readiness`.

Views are regenerated from governed state and do not acquire authority.

## Persistence and Reconstruction

Reuse the existing tree Dataset backend and FS-004 coherent-save behavior.
Pending candidates may be persisted and remain candidates. Fresh sessions recover
candidate/accepted state and readiness solely from the Dataset. Existing digest
conflict detection remains authoritative.

## Validation

Add `product/validation/fs005_validation.py`, register it in Product Validation,
and bind mechanically evaluable FS-005 requirements in the Requirement Evaluation
Manifest.

Validation covers candidate creation/refinement/acceptance, dependency closure,
coordinated acceptance, production approval, not-ready→ready refinement, FS-003
package handoff, author views, FS-004 revision integration, candidate persistence,
fresh reconstruction, withdrawal, stale-save conflict, exact Planning binding,
and Dataset boundary.

## Build Boundary

Do not add provider-specific model calls, a second candidate database, graph
infrastructure, automatic semantic acceptance, automatic story completion, or
storage structures that merely mirror existing semantic surfaces.
