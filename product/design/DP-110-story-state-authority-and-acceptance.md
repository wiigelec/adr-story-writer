---
doc_id: DP-110
title: Story State, Authority, Acceptance, and Reconciliation
depends_on:
  - DP-100
---

# Story State, Authority, Acceptance, and Reconciliation

## Purpose

Story Writer preserves author authority by distinguishing working material,
candidate state, accepted semantic state, accepted manuscript, and persistence.

Acceptance is an intentional operation on an identifiable target. It does not
arise from generation, storage, downstream use, repetition, implication, or
model inference.

The Product must allow useful multi-session candidate work without confusing
that work with accepted story truth.

## Authority Principle

Consequential meaning is authoritative only when it has been intentionally
accepted at the semantic surface that owns it.

The AI may infer, propose, compare, diagnose, draft, transform, elaborate, or
realize consequential possibilities. Those possibilities remain non-authoritative
until accepted at their owning surface.

Production-control artifacts may govern a particular generation task, but they
do not acquire independent semantic authority over Canon, Plot, Prose, or
Manuscript.

Persistence preserves state. It does not create authority.

## Consequential Meaning

A detail or decision is consequential when preserving it in later governed
reasoning could materially constrain story meaning or future work.

Consequential meaning includes, at minimum, meaning that can constrain:

- Canon truth, state, chronology, causality, relationships, knowledge, or belief;
- Plot selection, ordering, viewpoint access, revelation, concealment, or other
  presentation intent;
- persistent Prose guidance or realization constraints;
- Manuscript continuity;
- later character, setting, event, or relationship state;
- production-control artifacts that depend on governed meaning;
- or another accepted governed artifact.

Transient expressive detail that need not constrain later reasoning may remain
local realization detail.

When classification is uncertain and later reuse could create a meaningful
constraint, the Product must treat the detail as non-authoritative candidate
meaning rather than silently promote it.

## Story-State Classes

The Product distinguishes the following semantic classes.

### Conversational Material

Conversational material supplies immediate intent, discussion, explanation, and
interaction context.

Conversation may contain author decisions, but those decisions become durable
story authority only through an acceptance operation reflected in governed
state.

Conversation alone is not durable story memory.

### Working Material

Working material is temporary, non-authoritative material used during analysis,
planning, drafting, transformation, or review.

Working material may be discarded without altering accepted story state.

### Candidate State

Candidate state is intentionally retained non-authoritative work.

A candidate may represent proposed semantic meaning, a production-control
artifact, prose, manuscript text, a coordinated change, or another governed
proposal.

Candidate state may persist across sessions.

Persistence does not make a candidate accepted.

### Accepted Semantic State

Accepted semantic state is author-approved meaning at the semantic surface that
owns it.

Accepted semantic state constrains later governed reasoning until intentionally
revised.

### Accepted Manuscript State

Accepted manuscript state is author-approved reader-facing text.

Manuscript acceptance establishes textual acceptance, not implicit acceptance
of consequential Canon, Plot, or persistent Prose meaning that has not been
accepted at its owning surface.

## Acceptance Purposes

The Product distinguishes at least:

- **semantic acceptance** — accepts candidate consequential meaning at its
  owning semantic surface;
- **artifact acceptance** — accepts an artifact whose role is itself governed,
  such as a production-control artifact;
- **manuscript acceptance** — accepts specified reader-facing text;
- **revision acceptance** — intentionally supersedes previously accepted meaning
  at an identified scope;
- **coordinated acceptance** — accepts a coherent set of related semantic
  operations that together represent one author decision;
- and **persistence authorization** — permits working, candidate, or accepted
  state to be stored.

A single author interaction may intentionally combine several purposes, but one
purpose must not be silently inferred from another.

## Acceptance Scope

Acceptance applies only to an identifiable target and the meaning intentionally
included with that target.

Conversational approval such as "yes", "good", "use that", or equivalent
language is interpreted in the narrowest context that reliably identifies what
the author approved.

Where multiple consequential scopes are reasonably possible, the Product must
not silently choose the broader interpretation.

Unresolved scope remains non-authoritative.

Acceptance of a larger artifact does not automatically imply acceptance of
every embedded consequential proposition when those propositions belong to
different semantic surfaces.

## Candidate Dependencies

Candidate work may depend on accepted state, candidate state, or both.

For example:

- candidate Plot may depend on a proposed future Canon event;
- candidate Prose may realize Plot that depends on an unaccepted relationship;
- a generation package may combine accepted Canon with candidate Plot and a
  candidate pseudo-prose layout;
- candidate manuscript may depend on unresolved consequential invention
  discovered during prose realization.

Such work is permitted when the non-authoritative assumptions are identifiable.

The Product must preserve enough dependency information to determine which
candidate assumptions materially constrain a downstream candidate.

Candidate chaining is therefore allowed.

Candidate chaining does not collapse authority boundaries.

## Acceptance Closure

A downstream candidate cannot be accepted in a way that silently promotes
unresolved consequential upstream assumptions.

Before or as part of accepting a downstream result, every consequential
candidate assumption required for that acceptance must be one of the following:

- accepted at its owning semantic surface;
- revised into an accepted alternative and reconciled downstream;
- explicitly excluded from the accepted downstream result;
- or left unresolved, in which case the dependent downstream result remains
  candidate at the affected scope.

This requirement is **acceptance closure**.

Acceptance closure does not require every upstream candidate used during
exploration to become accepted. It applies only to consequential assumptions
that the accepted result actually depends on.

## Downstream Discovery

Plotting, production planning, prose generation, manuscript review, continuity
analysis, or generated-view editing may expose missing, inconsistent, or
improved upstream meaning.

Such discovered meaning becomes a proposal at the semantic surface that owns it.

Its appearance in a downstream artifact does not grant it authority.

The Product may preserve the downstream candidate while the upstream proposal
is reviewed.

## Consequential Invention During Generation

Generated output may contain detail not explicitly present in its inputs.

If the detail falls within the generation package's permitted
non-consequential creative allowance, it may remain local realization detail.

If the detail is consequential, it becomes candidate meaning at the semantic
surface that owns it.

Generated prose, repeated use, successful validation, or manuscript approval
must not silently promote that consequential invention.

If accepted manuscript depends on the invention, acceptance closure applies.

## Production-Control Artifact Acceptance

Production-control artifacts may themselves require acceptance because they
constrain downstream generation.

Acceptance of a production-control artifact means that the author approves it
for its defined control role.

It does not create new story truth beyond the semantic meaning already accepted
or explicitly accepted together with it.

A production-control artifact that embeds unresolved consequential assumptions
must identify those assumptions as candidate dependencies.

## Manuscript Acceptance Boundary

Manuscript acceptance approves specified reader-facing text.

It does not silently:

- create Canon truth;
- accept Plot structure, reveal intent, or viewpoint rules;
- establish persistent Prose guidance;
- accept consequential invention;
- or resolve candidate assumptions.

Consequential meaning required by accepted manuscript must satisfy acceptance
closure before or as part of manuscript acceptance.

A user interface may present this reconciliation as one author action, but the
underlying semantic operations remain distinct.

## Coordinated Semantic Change

One author decision may require changes at multiple semantic surfaces or
multiple governed targets.

When those changes together represent one inseparable author decision, the
Product must support coordinated acceptance so governed state is not knowingly
left in a semantically partial result.

For example, an author may simultaneously accept:

- a new Canon event;
- a Plot reveal that presents it;
- and a revised scene control artifact that depends on both.

Coordinated acceptance preserves ownership. It does not merge Canon, Plot,
Prose, Manuscript, or production-control roles.

Planning may realize coordinated acceptance through transactions, staged
operations, validation gates, or another mechanism.

## Revision of Accepted Meaning

The author may intentionally revise accepted meaning.

Revision acceptance supersedes prior accepted meaning at the identified scope.

Revision does not silently rewrite dependent accepted artifacts.

Instead, affected dependents become subject to reconciliation.

The Product must preserve enough dependency information to identify materially
affected downstream state.

The precise dependency and reconciliation model is defined by later Design.

## Reconciliation Principle

Reconciliation determines what must happen to governed downstream state after
an accepted upstream change or resolution of a candidate assumption.

Reconciliation may conclude that a dependent artifact:

- remains valid unchanged;
- requires regeneration or revision;
- requires semantic review;
- must remain candidate until an assumption is resolved;
- or is no longer applicable.

Reconciliation must not invent replacement meaning merely to restore
consistency.

When automatic reconciliation cannot preserve author intent without making a
new consequential decision, the Product must surface that decision to the
author.

## Acceptance and Persistence

Acceptance and persistence are independent dimensions.

Accepted state may temporarily remain unpersisted.

Candidate state may be deliberately persisted across sessions.

Persisted working or candidate state remains non-authoritative unless accepted.

Saving accepted state preserves authority already established by acceptance; it
does not create that authority.

Later Design defines save boundaries, recovery, and durable Dataset behavior.

## Failure-Safe Interpretation

When the Product cannot determine whether an operation would broaden authority,
promote consequential meaning, or resolve a candidate assumption, it must
preserve the narrower authority interpretation.

The safe fallback is to retain candidate state and surface the unresolved
decision rather than silently promote meaning.

## Planning Boundary

This Design defines authority, candidate, acceptance, revision, and
reconciliation meaning.

Later Design may define:

- detailed dependency representation;
- reconciliation workflow;
- acceptance metadata;
- candidate lifecycle representation;
- coordinated-operation realization;
- persistence and save behavior;
- validation gates;
- and user-interface presentation.

Planning may choose schemas, identifiers, status values, transaction
mechanisms, storage layout, prompts, commands, and other technical realization.

Implementation convenience does not override these authority boundaries.
