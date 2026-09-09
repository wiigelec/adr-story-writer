---
doc_id: DP-190
title: Story Metadata, Extensibility, and Simplicity Boundaries
depends_on:
  - DP-100
  - DP-130
  - DP-160
---

# Story Metadata, Extensibility, and Simplicity Boundaries

## Purpose

Story Writer needs enough metadata and extensibility to support real projects
without turning authoring into governance bureaucracy.

## Story Identity

Each Dataset represents one story instance and requires stable instance
identity.

Story-facing metadata may include title and other author-useful descriptive
fields.

Metadata does not replace semantic Canon, Plot, Prose, or Manuscript state.

## Story Status

A story may need operational status such as template, development, draft,
revision, complete, or other lifecycle concepts.

Status should be introduced only when the product has a concrete behavioral or
authoring need for it.

If status affects behavior, allowed meanings and transitions must be designed
rather than inferred from arbitrary strings.

## Extensibility

The product may evolve to include additional Canon domains, Prose guidance,
metadata, relationships, or workflow concepts.

Extensions must preserve the authority boundaries of the existing
architecture.

An implementation must not treat unknown future fields as permission to invent
semantics.

## Avoiding Accidental Schema Authority

Examples, initial Dataset skeletons, implementation convenience, historical
files, or generated runtime structures do not independently define Product
schema meaning.

Normative schema behavior belongs to Planning and specifications derived from
reviewed Product Design.

## Avoiding Excessive Identity

Stable identity is used where durable targeting and relationships require it.

The system should not assign governed identity to every sentence, paragraph,
adjective, conversational utterance, or ephemeral candidate merely because it
is technically possible.

## Avoiding Excessive Provenance

The product does not require generalized provenance linking every manuscript
phrase back through all intermediate generation steps.

Traceability should be as light as possible while remaining sufficient for
long-form integrity, reconciliation, and author control.

## Avoiding False Precision

The system must not force exact chronology, rigid workflow completion, fixed
story-development order, or metadata values merely because they are easier to
validate mechanically.

Unknown, partial, approximate, intentionally ambiguous, or not-yet-developed
meaning is valid story-development state when the author intends it.

## Human Readability

Author-facing state should remain understandable without requiring the author
to reason directly about internal governance machinery.

Machine structure exists to preserve the author's story, not to make the story
serve the structure.

## Planning Decomposition

Planning may decompose this complete Product Design into bounded Functional
Sets.

Functional Set boundaries are implementation and delivery boundaries, not
semantic limits on the Product meaning established by this Design.
