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
revision acceptance, and persistence authorization distinctly.

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
