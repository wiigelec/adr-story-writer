---
doc_id: DP-180
title: Validation, Semantic Review, and Integrity
depends_on:
  - DP-100
  - DP-120
  - DP-130
  - DP-140
  - DP-150
  - DP-160
  - DP-170
---

# Validation, Semantic Review, and Integrity

## Purpose

Story Writer requires both mechanical integrity checks and semantic review.

These concerns are complementary and must not be confused.

## Mechanical Validation

Mechanical validation evaluates decidable invariants.

It may verify matters such as:

- JSON or other syntax validity,
- Dataset schema conformance,
- required components,
- unique stable identities,
- valid references,
- relationship integrity,
- chapter manifest/file consistency,
- known prose-mode values,
- binding identity,
- Dataset schema identity,
- deterministic realization correspondence,
- and other mechanically decidable structural conditions.

Mechanical validation may prevent persistence or ordinary initialization when a
required invariant fails.

## Semantic Review

Semantic review evaluates meaning.

It may determine whether:

- lower Plot layers preserve accepted higher Plot meaning,
- Prose preserves accepted Plot and Canon,
- manuscript realizes accepted intended occurrence,
- consequential meaning has been introduced downstream without acceptance,
- Canon state and Events remain coherent,
- a revision has left affected dependents unreconciled,
- or a proposed change still reflects author intent.

These questions cannot be reduced to mechanical validation merely because an
agent can discuss them.

## Validation Does Not Create Meaning

A validation rule does not become Product meaning merely because an
implementation can enforce it.

Mechanical checks must trace to established Product or Planning requirements.

Likewise, a validation pass does not prove literary quality, semantic fidelity,
or authorial acceptance.

## Semantic Alignment State

The product must support detecting and communicating when known dependent state
requires semantic reconciliation.

Mechanical tooling may identify structural evidence of possible misalignment,
but semantic resolution remains governed by the owning story layers and author
authority.

## Save and Initialization Gates

Planning may designate specific mechanical checks required before save,
initialization, migration, rebinding, or publication.

Such gates preserve established Product semantics; they do not invent them.

## Integrity Over Convenience

When the system cannot establish whether persisted or working state is
structurally safe to interpret, it should fail or enter controlled recovery
rather than silently guessing.

When the issue is semantic rather than structural, it should preserve the
author's unresolved decision instead of mechanically forcing one interpretation.
