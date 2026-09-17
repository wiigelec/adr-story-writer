---
functional_set: FS-002
artifact: plan
title: Ruleset-Dataset Compatibility, Migration, and Rebinding Plan
design_revision: 325c7f22cd140dee43c01dbf7f93500325585ce9
---

# FS-002 — Plan

## Objective

Extend the accepted Story Writer Ruleset with a compact compatibility contract
for persisted Dataset schema identity and Ruleset binding, together with bounded
migration and rebinding behavior that preserves governed meaning.

FS-002 must not weaken the authority, persistence, dependency, generation, or
review invariants established by FS-001.

## Compatibility Model

Represent Dataset schema identity and Ruleset identity as distinct compatibility
axes.

The runtime contract must distinguish at least:

- directly compatible;
- restricted operation;
- migration required;
- rebinding required;
- unsupported; and
- indeterminate.

Exact stored labels remain a Build choice so long as their semantics remain
unambiguous.

Ordinary governed operation must not proceed when required compatibility cannot
be established.

## Binding Contract

Define a Dataset-side binding contract identifying the Ruleset realization
expected for ordinary governed work without creating a reverse
Ruleset-to-Dataset instance binding.

Binding metadata remains distinct from Dataset schema identity, semantic
acceptance, production approval, save authorization, application configuration,
and construction provenance.

The Ruleset repository continues to contain no story-instance Dataset state.

## Migration Contract

Add a compact Ruleset-owned compatibility/migration surface describing
explicitly supported transitions.

A supported mechanical migration may change representation but must preserve, as
applicable:

- semantic content;
- authority class;
- owning semantic surface;
- accepted/candidate status;
- production approval;
- stable identity;
- ordering;
- material dependencies;
- generation provenance;
- ambiguity or unknown state; and
- author-declared constraints.

A migration requiring a consequential semantic choice must stop and surface that
choice rather than synthesize an answer.

## Rebinding Contract

Rebinding must be explicit and scoped to a known compatibility determination.

Rebinding alone must not accept or reject story meaning, change authority
classes, change Manuscript acceptance, alter production approval, or imply that
structural migration succeeded.

If the target Ruleset cannot safely interpret the Dataset for the requested
operation, rebinding must not authorize ordinary governed work.

## Persistence and Reconstruction

A successful migration or rebinding transition must produce one coherent
persisted Dataset state.

A later fresh session must be able to determine Dataset schema identity, current
Ruleset binding, required transition provenance, preserved authority and
dependencies, and unresolved compatibility decisions without relying on prior
conversation history.

## Review and Failure Behavior

Mechanical checks may establish structural facts and explicitly encoded
compatibility predicates.

Semantic compatibility that cannot be established mechanically remains a
Semantic Review concern and may yield an indeterminate result.

Failure or partial transformation must not be presented as successful migration
or rebinding.

## Validation Planning

After FS-002 normative requirements are distilled and classified, Build must add
deterministic Product Validation tasks for mechanically decidable portions,
including:

- exact FS-002 Design binding;
- compatibility-contract structure;
- distinct schema and Ruleset identity;
- ordinary-operation compatibility gating;
- mechanically representable meaning-preservation invariants;
- migration/rebinding transition identity and provenance;
- unsupported and indeterminate handling; and
- preservation of the Dataset boundary.

The Product Requirement Evaluation Manifest is extended only when those
normative requirements and their mechanical bindings exist.

## FS-001 Planning Relocation

Relocate the accepted FS-001 Functional Set scope and Plan from `product/specs/`
to:

`product/planning/FS-001-governed-prose-production-and-acceptance/`

using `functional-set.md` and `plan.md`.

Update Product Validation paths referencing the old locations. Do not alter
FS-001 normative requirements or requirement-evaluation bindings solely because
of the relocation.

## Build Boundary

Do not introduce a generalized migration engine, compatibility inferred from
version ordering alone, automatic semantic repair, hidden Ruleset rebinding,
reverse Ruleset-to-Dataset instance bindings, or a second authority model.

Exact JSON decomposition, identifiers, transition storage, and helper
organization remain ordinary Build choices.
