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
realize consequential possibilities. Those possibilities remain
non-authoritative until accepted at their owning surface.

Production-control artifacts may constrain a particular generation task, but
they do not acquire independent semantic authority over Canon, Plot, Prose, or
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
- **production approval** — approves a production-control artifact for its
  defined downstream control role without granting it independent story
  authority;
- **manuscript acceptance** — accepts specified reader-facing text;
- **revision acceptance** — intentionally supersedes previously accepted meaning
  at an identified scope;
- **coordinated acceptance** — records one author decision that intentionally
  resolves multiple related semantic targets without leaving known partial
  semantic state;
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

Acceptance may be partial. Selected portions of an artifact may become accepted
while other portions remain candidate when the accepted scope and its
dependencies are unambiguous.

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
candidate assumptions currently and materially constrain a downstream
candidate.

Candidate chaining is therefore allowed.

Candidate chaining does not collapse authority boundaries.

## Dependency and Derivation

A candidate's derivation history and its current semantic dependencies are not
the same thing.

An exploratory assumption may have influenced an earlier draft but cease to
constrain a later revision.

Acceptance decisions are based on the consequential dependencies of the
current candidate being accepted, not every proposal, prompt input, or
historical assumption that contributed to its derivation.

Derivation may still be retained for provenance, diagnosis, or reproducibility,
but historical influence alone does not create an acceptance dependency.

## Acceptance Closure

A downstream candidate cannot be accepted in a way that silently promotes
unresolved consequential meaning on which the accepted result currently and
materially depends.

Before or as part of accepting a downstream result, each unresolved
consequential candidate dependency required by the accepted scope must be one
of the following:

- accepted at its owning semantic surface;
- revised into an accepted alternative and reconciled in the downstream result;
- explicitly excluded from the accepted scope;
- or left unresolved, in which case the dependent portion remains candidate.

This requirement is **acceptance closure**.

Acceptance closure is evaluated against the current accepted scope and its
material dependencies. It does not require acceptance of exploratory
assumptions, historical derivation inputs, deliberately unresolved
interpretations that the accepted text does not semantically depend on, or
unrelated candidate material.

Deliberate ambiguity may remain in accepted Manuscript when the text does not
require the Product to adopt one unresolved consequential interpretation as
accepted story truth.

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

Generated prose, repeated use, successful validation, production approval, or
manuscript acceptance must not silently promote that consequential invention.

If an accepted scope materially depends on the invention, acceptance closure
applies.

## Production-Control Approval

Production-control artifacts may require author approval because they constrain
downstream generation.

Production approval means that the author approves the artifact for its defined
control role.

Production approval does not create new story truth beyond semantic meaning
already accepted or intentionally accepted together with it.

A production-control artifact that contains unresolved consequential
assumptions must identify those assumptions as candidate dependencies.

Approval may be partial when only a clearly identified portion of the
production-control artifact is ready to govern downstream work.

## Manuscript Acceptance Boundary

Manuscript acceptance approves specified reader-facing text.

It does not silently:

- create Canon truth;
- accept Plot structure, reveal intent, or viewpoint rules;
- establish persistent Prose guidance;
- accept consequential invention;
- or resolve candidate assumptions.

Consequential meaning materially required by accepted Manuscript must satisfy
acceptance closure before or as part of manuscript acceptance.

A user interface may present this reconciliation as one author action, but the
underlying semantic operations remain distinct.

## Coordinated Semantic Change

One author decision may intentionally change multiple semantic surfaces or
governed targets.

When those changes are inseparable parts of one decision, the Product must not
knowingly leave accepted state in a partial semantic result.

For example, an author may decide together to accept a new Canon event, a Plot
reveal that presents it, and a revised scene control artifact that depends on
both.

The coordinated decision preserves ownership at each semantic surface.

Planning may choose how to realize this semantic requirement.

## Revision of Accepted Meaning

The author may intentionally revise accepted meaning.

Revision acceptance supersedes prior accepted meaning at the identified scope.

Revision does not silently rewrite dependent accepted artifacts.

Affected dependents become subject to reconciliation according to later Design.

The Product must preserve enough dependency information to identify materially
affected downstream state.

## Candidate Rejection and Withdrawal

A candidate may be rejected, withdrawn, or superseded without altering accepted
state.

Rejecting or withdrawing a candidate does not retroactively change accepted
meaning merely because accepted or candidate work was historically derived from
it.

If current accepted or candidate state materially depends on the rejected or
withdrawn candidate, that dependency must be reconciled.

## Reconciliation Principle

An accepted upstream change, resolution of a candidate dependency, or removal of
a material candidate assumption may require downstream reconciliation.

Reconciliation must preserve authority boundaries and must not invent new
consequential meaning merely to restore consistency.

When reconciliation cannot preserve author intent without a new consequential
decision, that decision remains candidate until the author resolves it.

Later Design defines detailed dependency and reconciliation behavior.

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
promote consequential meaning, or resolve a candidate assumption, ambiguity
degrades to candidate state rather than broader acceptance.

The Product preserves the narrower authority interpretation and surfaces the
unresolved decision.

## Planning Boundary

This Design defines authority, candidate, acceptance, revision, and
reconciliation meaning.

Later Design may define detailed dependency and reconciliation behavior,
acceptance metadata, candidate lifecycle representation, coordinated-operation
realization, persistence and save behavior, validation gates, and
user-interface presentation.

Planning may choose schemas, identifiers, status values, transaction
mechanisms, storage layout, prompts, commands, and other technical realization.

Implementation convenience does not override these authority boundaries.
