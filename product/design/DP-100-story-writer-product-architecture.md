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

The Product therefore externalizes author-approved story state, progressively
reduces broad writing intent into bounded generation work, and validates
generated results before they may become accepted story state or manuscript.

The Product is not autonomous authorship. The AI may propose, analyze, plan,
transform, realize, critique, and revise, but consequential authority remains
with the author.

## Product Problem

Long-form generative writing creates two related control problems.

First, model context is temporary and incomplete. A conversation cannot be
treated as durable story memory. Important facts, decisions, dependencies,
character knowledge, reveal boundaries, style constraints, and prior accepted
text must survive across sessions independently of chat history.

Second, unconstrained generation requires the model to make too many decisions
at once. When asked to move directly from broad story intent to finished prose,
the model is likely to invent consequential details, alter intended events,
violate viewpoint or reveal constraints, drift stylistically, or continue
beyond the requested narrative unit.

The Product addresses these problems through durable governed state and
progressive top-down constraint.

## Architectural Invariants

The following invariants govern the Product:

1. **The Dataset, not conversation, is durable story memory.**
   A fresh session must be able to reconstruct the governed state needed to
   continue work without relying on prior chat history or private model memory.

2. **Consequential story meaning must have an authoritative home outside
   generated prose.**
   Generated language may realize accepted or candidate meaning, but prose
   generation must not silently become the source of consequential truth.

3. **Generation is bounded before it begins.**
   The model must be given a sufficiently constrained local task so that it is
   primarily deciding how to express already-established intent rather than
   deciding what consequentially happens next.

4. **Creative freedom is explicit rather than assumed.**
   A generation task may define details the model may invent and details or
   meanings it must not invent.

5. **Generated output is candidate output until accepted.**
   Generation does not imply semantic acceptance, manuscript acceptance, or
   persistence as accepted state.

6. **Validation and semantic review precede acceptance where failure would
   alter governed meaning.**
   Mechanical correctness and semantic suitability remain distinct.

7. **Meaning-changing revision propagates deliberately.**
   Revision may move upstream when necessary, but downstream artifacts must not
   silently rewrite their authorities.

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

The Product may use intermediate Prose control artifacts such as beats,
narrative modes, paragraph-scale movement, pseudo-prose, transition intent,
rhythm guidance, or other near-prose structures. These structures exist to
reduce generation freedom and preserve intended meaning; they do not become
independent story truth merely because they are detailed.

Prose may introduce non-consequential realization detail within an explicit
creative allowance. Consequential invention must be proposed or reconciled at
the semantic surface that owns it.

### Manuscript

**Manuscript owns accepted final reader-facing text.**

Manuscript text is not authoritative merely because it was generated.
Acceptance establishes that a prose candidate is satisfactory as manuscript.

Accepted manuscript may expose inconsistencies or motivate upstream revision,
but it does not silently redefine Canon or Plot.

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

The Product reconstructs the relevant current state for the task from the
Dataset and applicable Ruleset rather than relying on conversational memory.

### Refine

Broad author intent is progressively decomposed into smaller, more explicit
planning and realization units.

Refinement is top-down. Each stage reduces unresolved decisions left to later
stages.

The Product may employ structures such as synopsis, outline, sequence, scene
contract, beats, modes, and pseudo-prose where they improve control. The exact
artifact vocabulary may evolve, but the requirement to bound generation before
final prose is architectural.

For prose generation, refinement must be capable of reaching approximately
paragraph-scale or similarly local narrative-intent units when broader
generation would leave the model excessive planning freedom.

### Package

Before generation, the Product constructs a bounded generation package for the
specific requested unit.

The package projects only the authoritative and candidate information needed
for that task and records enough provenance to determine what governed inputs
the generation was based on.

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

The package is a context projection, not a new authority surface.

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

The author accepts, rejects, or revises the candidate at the appropriate
semantic scope.

Acceptance may accept manuscript text, accept a planning artifact, or accept a
proposed consequential story change. These are distinct operations even when a
user interface combines them into a simple interaction.

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

## State Distinctions

The Product distinguishes at least:

- conversational material;
- transient working material;
- persisted candidate material;
- accepted governed semantic state;
- accepted manuscript state;
- and persisted representations of those states.

These distinctions may share storage mechanisms or user-interface surfaces,
but they are not semantically interchangeable.

Persistence does not imply acceptance.

Acceptance does not require that every intermediate artifact become permanent.

Generated content does not acquire authority merely because it was saved.

## Context Projection Principle

The Product must not solve context limits by repeatedly loading the entire
story into the model.

Instead, it constructs task-specific context from durable governed state.

A context projection should be small enough for reliable local reasoning while
remaining complete enough that the model does not need to guess consequential
missing information.

Where completeness and boundedness conflict, the Product must refine the task
further, retrieve additional dependencies deliberately, or surface the
ambiguity to the author rather than silently permitting invention.

## Lowest-Layer Revision Principle

A problem is resolved at the lowest semantic layer capable of preserving the
author's intended meaning.

If a Prose revision solves a problem without changing Plot, Plot remains
unchanged.

If Plot cannot solve the problem without changing Canon, the proposed change is
explicitly escalated to Canon.

The same principle applies to control artifacts: changing a local realization
plan should not rewrite broader accepted intent unless the local problem
actually requires that change.

## Generated Views

The Product may generate dossiers, summaries, reports, indexes, context
packages, continuity views, or other projections for authors or agents.

Generated views are non-authoritative unless Design explicitly assigns them an
authority role.

An edit made through a generated view must resolve to a semantic operation on
the underlying governed state rather than silently creating a competing source
of truth.

## Long-Form Success Criteria

The architecture is successful only if it supports all of the following:

- a fresh session can continue governed work without prior-chat memory;
- accepted facts and character state remain stable across distant scenes;
- viewpoint and character-knowledge limits can be preserved;
- planned reveal timing can remain stable across long spans;
- prose generation can stop at the requested local boundary;
- the model can be creative inside explicit allowances without being free to
  invent consequential meaning;
- a local prose unit can be regenerated without re-planning the whole story;
- style and voice guidance can remain stable yet locally resolved;
- revisions can be traced to the story meaning they depend on;
- and generated output can be checked against the context and constraints that
  produced it.

## Simplicity Boundary

Governance exists to improve author control and model reliability.

The Product should therefore expose author-meaningful decisions while hiding
mechanical bookkeeping wherever possible.

The architecture does not require giant registries, visible transaction
ceremonies, hashes on every artifact, numerous user-facing status labels, or
other governance machinery unless a later Design decision demonstrates that
such machinery is necessary to preserve the required semantics or reliability.

Internal rigor is permitted. Accidental author-facing bureaucracy is not a
Product goal.

## Planning Boundary

This Design establishes Product meaning and architectural invariants.

Later Design may define specific authority, acceptance, Canon, Plot, Prose,
generation-package, persistence, identity, reconciliation, validation, and
compatibility semantics.

Planning may choose schemas, identifiers, file layouts, workflow commands,
retrieval mechanisms, status representations, validation implementations,
prompt construction, persistence strategies, and other technical realization.

Implementation convenience does not override this Design.
