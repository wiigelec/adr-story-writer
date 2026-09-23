---
doc_id: DP-200
title: Live Dependency and Semantic Alignment Semantics
depends_on:
  - DP-120
  - DP-140
  - DP-150
  - DP-175
  - DP-180
---

# Live Dependency and Semantic Alignment Semantics

## Purpose

Long-form scene authoring must allow an AI agent to generate any scene from a
bounded, self-sufficient scene-generation artifact without requiring the prose
of earlier scenes or the whole story knowledge corpus.

This Design clarifies how live governed dependencies, Canon continuity,
scene-local semantic closure, revision history, and generation-package
provenance work together to support that property.

## Canon as Cross-Scene Continuity Authority

Canon is the durable continuity authority across scenes.

Consequential meaning that materially constrains later governed reasoning must
be represented at its owning Canon surface rather than remaining available only
through Manuscript prose.

A later scene that depends on an earlier occurrence depends on the relevant
Canon Event, Character state, Setting state, or other governed semantic object.
It does not require the earlier scene's Manuscript prose to exist.

Therefore a scene may be generation-ready even when prose for an earlier scene
has not yet been generated, provided the accepted Canon and Plot state needed by
the later scene is sufficiently governed.

## Top-Down Scene Refinement

Scene generation context is constructed through progressive refinement from
broader accepted meaning toward a bounded local execution artifact.

The Product must support refinement in which:

- accepted Canon provides applicable truth and continuity;
- accepted higher Plot layers provide story and structural intent;
- accepted scene-level Plot provides local intended occurrence;
- production-approved Prose controls refine realization detail;
- the generation package compiles the material state needed for one bounded
  generation attempt.

Each downstream layer preserves applicable accepted upstream meaning while
adding only the detail owned by that layer.

The final generator-facing artifact must be sufficient for a fresh generator to
realize the target scene without browsing the Dataset, depending on prior chat
memory, or reconstructing the whole story.

## Live Dependency Identity

A live governed dependency targets stable artifact identity.

Ordinary semantic dependencies do not pin their meaning to a historical target
revision. When a continuing governed artifact is revised and accepted under the
same stable identity, dependent artifacts continue to depend on that identity
and therefore resolve against its current accepted meaning.

Revision identifiers remain necessary for change detection, historical
provenance, review evidence, and reproducible execution context, but they do not
redefine the target of a continuing live semantic dependency.

Replacing an artifact with a different semantic identity remains an explicit
identity operation governed by DP-175 and reconciliation semantics.

## Alignment Evidence

Current semantic validity and historical dependency identity are distinct.

The Product must be able to preserve evidence of the revisions against which a
dependent scope was last semantically reviewed or otherwise proven aligned.

When the current accepted revision of a material upstream artifact differs from
the revision covered by that alignment evidence, the dependent scope's proof of
alignment is no longer current.

The dependency itself is not stale merely because the continuing upstream
artifact acquired a newer accepted revision.

The Product must classify and reconcile the affected dependent scope according
to materiality and semantic impact.

## Scene Semantic Closure

A scene is semantically closed only when its governed layers are aligned
top-to-bottom against current accepted upstream semantic authority.

Applicable closure includes:

- scene-level Plot preserves applicable accepted higher Plot and Canon meaning;
- Prose controls preserve the accepted scene Plot and applicable Canon meaning;
- candidate or accepted Manuscript conforms to its governing scene state;
- consequential meaning introduced downstream is either rejected or proposed
  and resolved at its owning Canon or Plot surface;
- all material upstream changes since the last successful alignment have been
  reconciled.

Local semantic closure against shared authority is the mechanism for cross-scene
consistency.

If Scene A and Scene B are each closed against the same current Canon and Plot
authority, cross-scene consistency is mediated through those shared governed
artifacts rather than through direct Manuscript-to-Manuscript comparison.

## Consequential Manuscript Discovery

Semantic review may discover consequential meaning in generated or accepted
prose that is not yet represented at the semantic surface that owns it.

Such meaning does not silently become Canon or Plot authority.

It becomes a candidate proposal at the owning surface. If accepted, affected
dependent scopes must be identified and their alignment re-evaluated against the
new current semantic state.

No consequential meaning that materially constrains later governed reasoning
should remain available only in Manuscript prose.

## Manuscript Independence

Earlier Manuscript prose is not a general continuity source for later scene
generation.

A later scene must not require earlier scene prose merely to know what happened,
what is true, what a character knows, what state an object is in, or what
consequential occurrence constrains the later scene. Such information belongs
in governed Canon and Plot state.

Exact prior wording or narrowly bounded textual handoff may be selected when a
specific generation task explicitly requires it. That is a production choice,
not the default cross-scene continuity mechanism.

## Generation Package Semantics

A generation package is a frozen execution artifact.

Unlike live dependencies, a used generation package may and should preserve the
exact revisions selected for that generation attempt so that later review can
identify the governing context that produced a candidate.

The Product must therefore distinguish:

- live semantic dependency identity;
- current alignment evidence;
- frozen generation provenance.

These concepts must not be represented as one interchangeable revision-pinned
dependency relation.

## Scalability Invariant

The context required to generate a scene should scale with the material needs of
that scene rather than with the total amount of earlier Manuscript prose or the
total size of the story Dataset.

A scene-generation package should be bounded primarily by:

- target scene intent;
- material Canon and Plot dependencies;
- applicable viewpoint and reader-information state;
- production-approved Prose controls;
- applicable style projection;
- explicitly selected local textual continuity when needed.

Routine scene generation must not require all prior Manuscript prose.

## Planning Boundary

Planning defines the concrete representation of:

- live identity-based dependency relations;
- alignment/review revision evidence;
- change detection and reconciliation;
- compilation of current accepted dependencies into a bounded scene-generation
  package;
- any explicitly selected local textual continuity;
- migration from revision-pinned live dependencies;
- validation and scale tests.

Planning may choose field names, record shapes, indexes, migration mechanics,
and runtime APIs. Those choices must preserve the semantic distinctions defined
here.
