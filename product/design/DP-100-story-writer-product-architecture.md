---
doc_id: DP-100
title: Story Writer Product Architecture
depends_on: []
---

# Story Writer Product Architecture

## Purpose

ADR Story Writer is a persistent control system for AI-assisted long-form
fiction.

Its primary purpose is to let an author use generative AI across many sessions
without trusting the model to remember the story, reconstruct prior decisions,
or independently plan consequential long-form narrative meaning.

The Product externalizes author-approved story state, progressively reduces
broad writing intent into reliably bounded generation work, and evaluates
generated results before they may become accepted story state or manuscript.

The Product is not autonomous authorship. The AI may propose, analyze, plan,
transform, realize, critique, and revise, but consequential authority remains
with the author.

## Product Problem

Long-form generative writing creates two related control problems.

First, model context is temporary and incomplete. Conversation cannot be
treated as durable story memory. Facts, decisions, dependencies, character
knowledge, reveal boundaries, style constraints, and accepted text must survive
across sessions independently of chat history.

Second, unconstrained generation requires the model to make too many decisions
at once. When asked to move directly from broad story intent to finished prose,
the model may invent consequential details, alter intended events, violate
viewpoint or reveal constraints, drift stylistically, or continue beyond the
requested narrative unit.

The Product addresses these problems through durable governed state and
progressive top-down constraint.

## Architectural Invariants

The following invariants govern the Product:

1. **The Dataset, not conversation, is durable story memory.**
   A fresh session must be able to reconstruct the governed state needed to
   continue work without relying on prior chat history or private model memory.

2. **Consequential story meaning has an authoritative semantic home outside
   generated prose.**
   Generated language may realize accepted or candidate meaning, but generation
   must not silently become the source of consequential truth.

3. **Generation is reliably bounded before it begins.**
   A generation task must be constrained enough that the model is primarily
   deciding how to realize established intent rather than independently deciding
   consequential narrative meaning.

4. **Creative freedom is explicit rather than assumed.**
   Generation may define details the model may invent and details or meanings it
   must not invent.

5. **Generated output is candidate output until accepted.**
   Generation does not imply semantic acceptance, manuscript acceptance, or
   persistence as accepted state.

6. **Accepting prose does not silently accept consequential invention.**
   If generated prose contains consequential meaning that is not already
   governed by the semantic surface that owns it, that meaning must be
   separately proposed and reconciled before it can become accepted story state.

7. **Validation and semantic review precede acceptance where failure would alter
   governed meaning.**
   Mechanical correctness and semantic suitability remain distinct.

8. **Meaning-changing revision propagates deliberately.**
   Revision may move upstream when necessary, but downstream artifacts must not
   silently rewrite their authorities.

9. **Generated work is attributable to its governing context.**
   The Product must preserve enough provenance to determine which governed
   inputs, candidate inputs, boundaries, and constraints formed the context for
   a generated candidate.

## Story Semantic Architecture

The Product separates governed story meaning into four principal semantic
surfaces.

### Canon

**Canon owns what is true in the story world.**

Canon includes accepted facts, state, chronology, events, relationships,
causes, constraints, and character knowledge or belief where those are facts
about the story world.

An accepted occurrence is Canon whether it is historical, off-page, currently
occurring, future relative to the present drafting position, revealed to the
reader, or still concealed.

Canon is author knowledge. It is not limited to what any character or reader
currently knows.

### Plot

**Plot owns how Canon is intentionally presented as narrative.**

Plot selects, orders, omits, emphasizes, delays, juxtaposes, reveals, and
conceals Canon material.

Plot owns dramatic presentation concerns such as scene purpose, narrative
selection, ordering, focal access, reveal intent, concealment, and intended
reader-information progression.

Plot may refer to Canon occurrence, but Plot is not the authoritative home of
whether that occurrence is true.

### Prose

**Prose owns controlled linguistic realization of Plot intent.**

Prose includes the preparation and expression needed to turn a bounded
narrative unit into reader-facing language.

The Product may use intermediate Prose control structures such as beats,
narrative modes, movement, pseudo-prose, transition intent, rhythm guidance, or
other near-prose structures. These structures reduce generation freedom and
preserve intended meaning; they do not become independent story truth merely
because they are detailed.

Prose may introduce non-consequential realization detail within an explicit
creative allowance. Consequential invention must be proposed or reconciled at
the semantic surface that owns it.

### Manuscript

**Manuscript owns accepted final reader-facing text.**

Manuscript text is not authoritative merely because it was generated.
Acceptance establishes that a prose candidate is satisfactory as manuscript.

Manuscript acceptance and semantic acceptance are distinct. Accepted manuscript
may expose inconsistencies or motivate upstream revision, but it does not
silently redefine Canon or Plot or silently promote consequential invention.

## Semantic Direction

The ordinary semantic direction is:

    Canon
      ↓
    Plot
      ↓
    Prose
      ↓
    Manuscript

The arrows mean dependency and realization, not mandatory storage shape.

Work may move backward for diagnosis or intentional revision. Backward movement
must be explicit when it changes accepted upstream meaning.

## Production-Control Architecture

The Product may use **production-control artifacts** to constrain, project, and
coordinate AI work.

Examples include scene contracts, beats, mode assignments, pseudo-prose
layouts, resolved style projections, continuity reports, generation packages,
and similar task-specific structures.

Production-control artifacts may be normative for a particular downstream
generation task, but they are not additional sources of story truth. Their
authority derives from the governed semantic state and author-approved candidate
intent they project.

A production-control artifact must not silently compete with Canon, Plot,
Prose, or Manuscript for ownership of consequential meaning.

## AI Control Architecture

The Product constrains AI work through a separate control pipeline:

    Persist
      ↓
    Retrieve
      ↓
    Refine
      ↓
    Package
      ↓
    Generate
      ↓
    Validate
      ↓
    Accept
      ↓
    Persist

### Persist

Accepted governed state, and candidate state when intentionally saved, is
stored outside conversation.

### Retrieve

The Product reconstructs relevant current state for the task from the Dataset
and applicable Ruleset rather than relying on conversational memory.

### Refine

Broad author intent is progressively decomposed into smaller, more explicit
planning and realization units.

Refinement is top-down. Each stage reduces unresolved decisions left to later
stages.

The Product may employ structures such as synopsis, outline, sequence, scene
contract, beats, modes, and pseudo-prose where they improve control. The exact
artifact vocabulary may evolve; the architectural requirement is that final
generation be bounded enough that the model need not independently plan
consequential narrative meaning.

The required generation granularity is determined by reliability, not by a
fixed textual size. If a scene is too broad for reliable realization, it must
be refined into smaller units. If necessary, refinement may reach
paragraph-scale, sentence-scale, or another local narrative-intent unit.

### Package

Before generation, the Product constructs a bounded generation package for the
specific requested unit.

The package is a reproducible context projection: it identifies the governed
and candidate inputs, boundaries, permissions, prohibitions, and applicable
guidance used to produce the candidate.

A generation package must be capable of expressing:

- the exact generation boundary;
- required narrative movements or beats;
- viewpoint and information-access constraints;
- reveal and concealment boundaries;
- relevant Canon and Plot dependencies;
- applicable style and voice guidance;
- protected terminology or text where required;
- details the model may invent;
- details or consequential meanings the model must not invent;
- and validation expectations for the generated result.

The package may include accepted and explicitly selected candidate inputs.
Candidate use must be identifiable so later acceptance or revision can be
reconciled deliberately.

The package is a production-control artifact, not a new semantic authority
surface.

### Generate

The AI generates only the bounded unit requested by the package.

At this stage, the model should primarily make local realization choices.
Generation must not depend on the model reconstructing the whole story or
remembering unstated prior-session decisions.

### Validate

The Product evaluates generated output against applicable mechanical
requirements and semantic constraints.

Validation may detect missing required movement, boundary violations,
viewpoint leakage, forbidden invention, style conflicts, structural defects,
or other package nonconformance.

Mechanical validation does not establish semantic acceptance.

### Accept

The author accepts, rejects, or revises the candidate at the appropriate scope.

Acceptance may apply to manuscript text, candidate planning or control
artifacts, or proposed consequential story changes. These are distinct semantic
operations even when a user interface combines them into a simple interaction.

If accepted manuscript contains consequential meaning not already accepted at
its owning semantic surface, the Product must surface that meaning for explicit
reconciliation rather than treating manuscript acceptance as implicit Canon or
Plot acceptance.

## Runtime Architecture

The applicable **Ruleset** defines Product semantics, allowed operations,
governed structures, and validation meaning.

A **Dataset** persists one story instance and the durable state required to
resume governed work.

A **working session** retrieves applicable persisted state and may create
temporary or persisted candidates that advance beyond currently accepted state.

**Conversation** supplies immediate intent and interaction context. It is
operationally useful but is not, by itself, durable story authority.

A new session with the same applicable Ruleset and Dataset must be able to
resume governed work without access to the prior conversation.

## State and Persistence Principles

The Product distinguishes conversational material, working material, persisted
candidate material, accepted semantic state, and accepted manuscript state.

Persistence and acceptance are independent. Persisted candidates may support
multi-session work without becoming accepted truth or accepted manuscript.

Generated content does not acquire authority merely because it was saved.

Later Design defines detailed candidate dependency, acceptance, save, and
reconciliation semantics.

## Context Projection Principle

Generation must not depend on whole-story context being loaded into the model.

The Product constructs task-specific context from durable governed state and
explicitly selected candidate state.

A context projection should be small enough for reliable local reasoning while
remaining complete enough that the model does not need to guess consequential
missing information.

Loading broader story context is permitted when useful, but correctness must
not depend on a model remembering or inferring unstated consequential state from
that broader context.

Where completeness and boundedness conflict, the Product must refine the task,
retrieve additional dependencies deliberately, or surface the ambiguity to the
author rather than silently permitting invention.

## Lowest-Layer Revision Principle

A problem is resolved at the lowest semantic layer capable of preserving the
author's intended meaning.

If a Prose revision solves a problem without changing Plot, Plot remains
unchanged.

If Plot cannot solve the problem without changing Canon, the proposed change is
explicitly escalated to Canon.

Changing a local production-control artifact must not rewrite broader accepted
intent unless the local problem actually requires that change.

## Generated Views

The Product may generate dossiers, summaries, reports, indexes, continuity
views, context projections, or other views for authors or agents.

Generated views are non-authoritative unless later Design explicitly assigns
them an authority role.

An edit made through a generated view must resolve to an operation on the
underlying governed state or candidate state rather than silently creating a
competing source of truth.

## Long-Form Success Criteria

The architecture is successful only if it supports all of the following:

- a fresh session can continue governed work without prior-chat memory;
- accepted facts and character state remain stable across distant scenes;
- viewpoint and character-knowledge limits can be preserved;
- planned reveal timing can remain stable across long spans;
- generation can stop at the requested local boundary;
- the model can be creative inside explicit allowances without being free to
  invent consequential meaning;
- a local prose unit can be regenerated without re-planning the whole story;
- style and voice guidance can remain stable yet locally resolved;
- revisions can be traced to the story meaning they depend on;
- generated candidates can be traced to the context and constraints that
  produced them;
- and persisted candidate work can survive session boundaries without being
  mistaken for accepted state.

## Simplicity Boundary

Governance exists to improve author control and model reliability.

The Product should expose author-meaningful decisions while hiding mechanical
bookkeeping wherever possible.

The architecture does not require giant registries, visible transaction
ceremonies, hashes on every artifact, numerous user-facing status labels, or
other governance machinery unless later Design demonstrates that such machinery
is necessary to preserve required semantics or reliability.

Internal rigor is permitted. Accidental author-facing bureaucracy is not a
Product goal.

## Planning Boundary

This Design establishes Product meaning and architectural invariants.

Later Design may define specific authority, acceptance, Canon, Plot, Prose,
production-control, generation-package, persistence, identity, reconciliation,
validation, and compatibility semantics.

Planning may choose schemas, identifiers, file layouts, workflow commands,
retrieval mechanisms, status representations, validation implementations,
prompt construction, persistence strategies, and other technical realization.

Implementation convenience does not override this Design.
