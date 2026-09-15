---
functional_set: FS-001
artifact: functional-set-scope
title: Governed Prose Production and Acceptance
design_revision: 3ba9e3f600adf2a5ccae8db8aca00ebbbb9c17c9
---

# FS-001 — Governed Prose Production and Acceptance

## Purpose

FS-001 selects the minimum coherent Product capability required to turn the
accepted ADR Story Writer Product Design into an operable governed prose
workflow.

The Functional Set establishes one end-to-end vertical slice:

> An author can reconstruct governed story state from a Dataset, prepare a
> bounded prose-generation task from governed Canon and Plot, generate candidate
> prose, review consequential invention and other semantic violations, accept or
> reject the result at explicit scopes, and persist the resulting state without
> confusing candidate, accepted semantic, production-approved, and accepted
> Manuscript authority.

Consequential story authority remains with the author.

## Exact Design Binding

Planning consumes Product Design at repository revision:

`3ba9e3f600adf2a5ccae8db8aca00ebbbb9c17c9`

FS-001 selects only the Product Design obligations required by this vertical
slice. A Design Proposal being named below does not mean that every capability
defined by that Proposal is implemented by FS-001.

Selected obligations are:

- **DP-100:** Dataset-backed continuity, Canon → Plot → Prose → Manuscript
  semantic ownership, bounded generation, the retrieve/refine/package/generate/
  validate/accept/persist control loop, and the Product simplicity boundary;
- **DP-110:** authority-class separation, intentional scoped acceptance,
  candidate dependencies, consequential-invention handling, acceptance closure,
  distinct production/Manuscript/revision/coordinated/persistence operations,
  and the independence of persistence from authority;
- **DP-120:** progressive refinement until a generation task is reliably
  bounded, lowest-layer problem solving, declared accepted/candidate material
  dependencies for the active task, and reconciliation of candidate
  dependencies exposed by this prose-production slice;
- **DP-130:** viewpoint and reader-information boundaries needed to construct
  and review the active generation task without leaking hidden Canon;
- **DP-140:** accepted Canon truth, knowledge, and temporal/event facts only as
  required to constrain and review the active generation task;
- **DP-150:** production contracts, generation packages, minimum-sufficient
  context, information-access safety, persistent/local Prose guidance, creative
  allowance, protected material, package freezing/provenance, bounded
  candidate-only generation, review-before-acceptance, and local correction of
  generated prose;
- **DP-160:** Dataset durability, authority-preserving persistence, intentional
  candidate and production-control continuity, save authorization/coherence,
  generation provenance required for later interpretation, and fresh-session
  reconstruction for continued governed work;
- **DP-175:** durable identity, revision identity, dependency targeting, and
  generation attribution only to the degree required for FS-001 acceptance,
  provenance, persistence, and fresh-session reconstruction; and
- **DP-180:** mechanical-validation versus semantic-review separation,
  generation readiness/package/prose review for the active task,
  conforming/non-conforming/indeterminate outcomes, consequential-invention
  review, information-boundary review, and acceptance gating.

The following broader capabilities remain applicable Product Design but are
outside FS-001 unless another selected obligation above requires them:

- DP-120 general accepted-upstream revision impact analysis, broad propagation,
  and general re-refinement/reconciliation across arbitrary downstream regions;
- DP-130 and DP-140 comprehensive Canon/Plot epistemic, chronology, state-effect,
  and unresolved-truth modeling beyond the active prose-production task;
- DP-160 autosave, concurrency/conflict resolution, recovery mechanisms, and
  broader persistence policy not needed by this slice;
- DP-175 general semantic-scope infrastructure, revision-versus-replacement
  lifecycle, split/merge/supersession/retirement, comprehensive Manuscript
  identity/mapping, and migration traceability;
- DP-170 migration, rebinding, downgrade, and general compatibility machinery;
  and
- DP-190 generated-view and general extensibility capabilities.

## Functional Boundary

FS-001 begins with an identified compatible Story Writer Ruleset and one story
Dataset.

FS-001 ends when a bounded prose candidate and consequential discoveries have
been resolved at the applicable authority scopes, accepted or rejected by the
author, and the authorized resulting state has been persisted coherently.

## Required Demonstration

The implemented Product must demonstrate fresh-session reconstruction, bounded
task refinement, production-contract creation, stable generation packaging,
candidate generation, semantic review, consequential-invention handling,
author-authorized acceptance with acceptance closure, coherent persistence, and
correct reconstruction in a subsequent fresh session.

## Explicit Deferrals

FS-001 does not require a general migration engine, downgrade support, arbitrary
Ruleset rebinding, a comprehensive generated-view system, a universal visible
status taxonomy, deterministic reproduction of literary wording, autonomous
acceptance of consequential story decisions, general upstream-impact analysis,
concurrent-save conflict resolution, or the full artifact-lifecycle and
cross-layer mapping model described by DP-175.
