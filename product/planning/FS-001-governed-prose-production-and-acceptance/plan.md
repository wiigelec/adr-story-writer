---
functional_set: FS-001
artifact: plan
title: Governed Prose Production and Acceptance Plan
design_revision: 3ba9e3f600adf2a5ccae8db8aca00ebbbb9c17c9
---

# FS-001 — Plan

## Objective

Extend the existing Ruleset from descriptive semantic guidance into a compact
governed runtime contract for an external story Dataset.

FS-001 implements only the Design obligations selected by the Functional Set
scope. It does not claim complete implementation of every capability in each
referenced Design Proposal.

For this vertical slice, Planning carries forward:

- DP-100/110 authority boundaries, bounded control flow, candidate state,
  intentional acceptance, acceptance closure, and persistence separation;
- DP-120 refinement sufficiency, lowest-layer navigation, active-task material
  dependencies, and candidate-dependency reconciliation;
- DP-130/140 viewpoint, reader-information, accepted Canon truth, knowledge, and
  temporal/event constraints required by the bounded prose task;
- DP-150 production contracts, generation packages, minimum-sufficient context,
  information-access safety, creative allowance, protected material, stable
  provenance, bounded candidate generation, and local correction;
- DP-160 authority-preserving persistence, candidate/production continuity,
  coherent authorized saves, provenance continuity, and fresh-session
  reconstruction;
- DP-175 durable identity/revision/dependency targeting and generation
  attribution required by this slice; and
- DP-180 mechanical/semantic review separation, indeterminate handling,
  generated-prose review, consequential-invention review, and acceptance gates.

General upstream revision-impact analysis, concurrency/recovery machinery,
comprehensive Canon/Plot epistemic and temporal modeling, the full DP-175
artifact lifecycle and Manuscript mapping model, migration/rebinding, and
generated-view/extensibility systems are deferred beyond FS-001.

## Runtime Structure

Preserve the existing Canon, Plot, Prose, Manuscript, Workflow, Authority, and
Workshop Agent surfaces. Add:

- `ruleset/governed-state.json` for artifact identity, authority classes,
  dependencies, reconstruction, persistence, and acceptance closure;
- `ruleset/production.json` for production contracts, generation packages,
  information access, creative allowance, protected material, stopping
  boundaries, and generation provenance;
- `ruleset/review.json` for review outcomes, stale/incomplete-context handling,
  consequential invention, and acceptance gating.

Dataset instance contents remain external to this repository.

## Governed Artifact Model

Use one minimal common governed-artifact vocabulary with stable identity,
semantic surface, authority class, revision identity, material dependencies, and
generation provenance where applicable.

Required authority classes are `accepted_semantic`, `candidate_semantic`,
`production_candidate`, `production_approved`, `candidate_manuscript`, and
`accepted_manuscript`.

Dependencies identify target identity/revision and whether the material basis is
accepted or candidate. Material unresolved candidate dependencies participate in
acceptance closure.

## Acceptance

Represent semantic acceptance, production approval, Manuscript acceptance,
revision acceptance, coordinated acceptance, and persistence authorization
distinctly.

Acceptance targets an identifiable scope. Material unresolved candidate
dependencies block acceptance of the dependent scope unless accepted,
reconciled, excluded from that scope, or left candidate.

## Production

A production contract is reusable control state for one bounded task. A
generation package is the stable task-specific execution projection used for one
generation attempt.

Generation packages identify selected revisions, explicit stopping boundaries,
creative allowance, prohibited invention, protected material, and provenance.
They can separate generator-visible information from reviewer-only constraints
when required for information-access safety.

Generation produces candidate Manuscript/prose only.

## Review

Semantic review supports `conforming`, `non_conforming`, and `indeterminate`.
Stale, missing, or ambiguous governing context that could materially affect the
judgment yields `indeterminate`.

Consequential downstream invention is surfaced as candidate meaning at its
owning semantic surface.

## Validation

Extend `product/validation/validate_product.py` with deterministic tasks for:

- exact Planning/Design binding;
- governed-state contract structure;
- production-contract structure;
- generation-package/provenance structure;
- review structure;
- explicit authority operations;
- Dataset boundary; and
- product requirement-binding completeness.

Update `product/validation/requirement-evaluation.json` with exact bindings.

Mechanical validation checks structure and explicit invariants only. Semantic
meaning remains a Semantic Review responsibility.

## Build Boundary

Do not introduce a generalized workflow engine, a second authority hierarchy, or
author-facing governance bureaucracy. Exact JSON nesting and validator helper
organization remain ordinary Build choices.
