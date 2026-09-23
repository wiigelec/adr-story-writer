---
functional_set: FS-008
artifact: implementation-plan
title: Live Dependency and Scene Semantic Alignment Plan
design_revision: 7867554b02d39a55b7171c992a61196a87863552
---

# FS-008 — Plan

## Objective

Replace revision-pinned live dependency behavior with stable-identity dependency
resolution, introduce explicit revision-specific alignment evidence, remove
routine prior-Manuscript continuity from scene package compilation, and preserve
exact revisions only where historical review and generation provenance require
them.

## Live Dependency Representation

For ordinary governed dependencies, retain `dependencies` as the stable list of
artifact IDs.

`dependency_relations` shall represent the live relationship using:

```json
{
  "target_id": "EVT-000005",
  "authority_basis": "accepted",
  "material": true
}
```

`target_revision` is not part of the live dependency relation for continuing
artifacts.

Candidate-only dependencies may retain the authority distinction needed for
acceptance closure, but once accepted the live relationship resolves by stable
identity to current accepted state.

## Alignment Evidence Representation

Add revision-specific alignment evidence to governed dependent artifacts.

Use a bounded mapping such as:

```json
{
  "alignment": {
    "dependencies": {
      "EVT-000005": "accepted-revision-..."
    }
  }
}
```

The exact durable field may also carry review outcome/provenance when required,
but it must remain distinguishable from `dependency_relations`.

For a material dependency, currentness compares:

- live `target_id`;
- current accepted target revision;
- last aligned revision for that target.

A mismatch means alignment evidence is non-current and triggers impact review;
it does not mean the live dependency points at the wrong object.

## Authoring Runtime

Update `authoring_runtime.py` so:

- new live dependencies are normalized without `target_revision`;
- dependency acceptance closure resolves the current target by ID;
- accepted coordinated operations do not rewrite a dependency revision;
- material dependency validity checks current authority/reconciliation state
  rather than equality with a pinned target revision;
- initial accepted alignment evidence is recorded when a dependent artifact is
  accepted against current accepted dependencies.

## Revision and Reconciliation Runtime

Update `revision_runtime.py` so:

- upstream revision impact discovery finds dependents by stable `target_id`;
- historical `from_revision` and `to_revision` remain in impact records;
- a continuing upstream identity change in content marks applicable dependent
  alignment `review_required` without changing the live relation;
- `preserve`, `revise`, `rebuild`, and equivalent successful reconciliation
  advance alignment evidence to the current upstream revision;
- replacement to a different stable identity may update `target_id` explicitly;
- `ensure_artifact_current()` validates alignment evidence against current
  accepted revisions rather than comparing live relation `target_revision`;
- reconciliation history retains prior revision evidence.

## Scene Context Compilation

Update `scene_runtime.py` so:

- accepted semantic dependencies are resolved by stable ID to current accepted
  state;
- the compiled scene contract uses those current semantic artifacts for
  continuity;
- `accepted_prior_manuscript` is removed from routine scene context projection;
- automatic `prior_manuscript_revisions` are removed from routine package
  selected revisions;
- current-target Manuscript may remain available for revision/repair workflows
  where the target itself already has accepted prose;
- any explicitly selected textual handoff must be bounded and task-specific,
  not inferred as all earlier prose by ordinal.

Automatic immediate-prior Plot state should not be required for correctness.
Where retained for local convenience, it must not substitute for declared
material dependencies and must not require prior Manuscript.

## Generation Package

`build_generation_package()` continues to freeze exact selected revisions.

Its `selected_revisions` shall contain:

- target scene revision;
- the current revisions of semantic dependencies actually selected for the
  package;
- applicable Prose-control revisions;
- style-profile revision when applicable;
- any explicitly selected bounded textual source revision when such a source is
  deliberately used.

This is historical execution provenance and does not alter live dependency
semantics.

## Semantic Review and Closure

Extend semantic-review handling so consequential invention discovered in scene
prose can be reported as unresolved owning-surface meaning.

After such meaning is accepted into Canon/Plot:

- dependency/impact analysis identifies affected downstream scopes;
- their alignment evidence is checked against current authority;
- downstream scopes requiring review cannot claim current semantic closure until
  reconciled.

Mechanical validation proves state transitions and provenance structure.
Whether arbitrary prose meaning is consequential and whether two meanings are
semantically aligned remains Semantic Review.

## Ruleset Changes

Update runtime Ruleset material to state:

- governed live dependency required fields do not include `target_revision`;
- revision-specific alignment evidence is separate durable governed state;
- generation packages still require `selected_revisions`;
- reconciliation tracks historical revision transitions while preserving
  continuing dependency identity;
- routine scene generation does not use prior Manuscript as the cross-scene
  continuity source.

Keep Canon Character/Setting/Events ownership and existing candidate/accepted
authority classes.

## Dataset Compatibility

Determine the smallest compatible migration path for existing Dataset state that
contains revision-pinned `dependency_relations`.

The migration shall:

- preserve each relation's `target_id`, `authority_basis`, and `material`;
- move the previously pinned accepted revision into alignment evidence when it
  accurately represents the dependent's last known alignment basis;
- remove `target_revision` from the live relation;
- preserve historical revision/reconciliation/generation provenance unchanged.

Because this changes governed Dataset representation, Build shall use the
existing DP-170 compatibility/migration machinery rather than silently
reinterpret persisted state.

## Manuscript Organization

FS-008 does not require changing physical Manuscript file organization.

The implementation shall only enforce that ordinary cross-scene continuity is
not derived from preceding Manuscript files.

Any broader chapter-versus-scene Manuscript persistence decision remains outside
this Functional Set unless Build discovers a direct blocker.

## Validation

Add `product/validation/fs008_validation.py` covering at least:

- exact Design binding;
- live relations contain stable target IDs without revision pins;
- accepted dependency revision changes make alignment evidence non-current;
- reconciliation preserves continuing target identity and advances alignment;
- replacement identity handling remains explicit;
- frozen old generation packages retain historical selected revisions;
- new packages select current dependency revisions;
- later-scene generation succeeds when required earlier scene prose is absent;
- current Canon/Plot dependency state appears in the compiled scene contract;
- no automatic all-prior-Manuscript content or revision set is present;
- a synthetic long-story fixture demonstrates bounded package behavior;
- migration converts legacy pinned relations into live relation plus alignment
  evidence without losing historical provenance;
- Requirement Evaluation Manifest coverage is complete.

## Build Boundary

Do not introduce physical per-scene sharding, vector retrieval, provider SDKs,
whole-story semantic search, a second state store, or automatic literary
judgment.

Build should modify the existing dependency, reconciliation, scene compilation,
compatibility/migration, Ruleset, and validation mechanisms only as required to
realize DP-200.
