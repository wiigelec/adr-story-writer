---
doc_id: DP-100
title: Story Writer Product Architecture
depends_on: []
---

# Story Writer Product Architecture

## Purpose

ADR Story Writer is an author-workshop application for governed development of
long-form fiction.

Its purpose is not autonomous authorship. It provides an author-controlled
environment in which an AI agent may guide, critique, propose, transform,
realize, revise, and diagnose story material without confusing suggestion,
accepted meaning, manuscript text, conversation, or persistence.

## Narrative Architecture

The product separates narrative meaning into four principal surfaces:

- **Canon** owns what is true.
- **Plot** owns what is intended to happen.
- **Prose** owns how intended occurrence is prepared and expressed.
- **Manuscript** owns author-facing accepted final text.

The normal forward realization direction is:

    Canon
      ↓
    Plot
      ↓
    Prose
      ↓
    Manuscript

The workflow may be navigated backward for diagnosis and collaborative
revision. Backward navigation does not grant permission for silent upstream
mutation.

## Runtime Architecture

The applicable Ruleset defines story-governance meaning and allowed semantic
operations.

A Dataset persists one story instance.

Active governed working state is initialized from persisted Dataset state and
may advance beyond it during a session.

Conversation supplies context and intent but is not automatically story state.

The workshop agent may propose and transform, but consequential story authority
remains with the author.

## Product State Distinctions

The product distinguishes:

1. ordinary conversation,
2. working candidate state,
3. accepted governed artifact state,
4. accepted manuscript state,
5. persisted Dataset state.

These states may contain overlapping content but are not interchangeable.

A proposal does not become accepted because it was generated.

Acceptance does not inherently imply persistence.

Persistence does not retroactively make an ungoverned invention semantically
valid.

## Lowest-Layer Principle

A problem is resolved at the lowest workflow layer capable of preserving
required accepted meaning.

If a Prose revision solves a problem without changing Plot, Plot remains
unchanged.

If Plot cannot solve the problem without changing Canon, the issue is
explicitly escalated to Canon.

The principle reduces unnecessary semantic disturbance while still permitting
intentional upstream revision.

## Long-Form Integrity

Long-form work must remain interpretable across many sessions, revisions,
chapters, and dependent artifacts.

The product therefore requires:

- scoped author acceptance;
- explicit handling of consequential downstream invention;
- dependency awareness and reconciliation after meaning-changing revision;
- stable artifact identity where durable relationships require it;
- cross-layer traceability sufficient for long-form navigation;
- coherent Canon state and occurrence;
- explicit separation of chronology and narrative presentation where needed;
- governed prose realization and support for persistent style/voice guidance;
- stable manuscript identity independent of filename and title;
- coherent save and persistence semantics;
- Dataset schema identity separate from Ruleset identity;
- controlled compatibility, migration, recovery, and rebinding;
- mechanical validation distinct from semantic review;
- and simplicity boundaries that prevent governance machinery from becoming
  more complex than the authoring problem requires.

## Planning Boundary

This Design establishes product meaning.

Planning may later divide the Design into bounded Functional Sets and choose
schemas, identifier formats, status representations, validation mechanisms,
migration algorithms, persistence strategies, and other technical
realizations.

Implementation convenience does not override this Design.
