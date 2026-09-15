---
doc_id: DP-120
title: Workflow, Refinement, Dependency, and Reconciliation
depends_on:
  - DP-100
  - DP-110
---

# Workflow, Refinement, Dependency, and Reconciliation

## Purpose

Story Writer controls long-form AI generation through progressive refinement,
explicit dependency, bounded generation readiness, and deliberate
reconciliation after change.

Refinement reduces unresolved decisions before generation.

Dependency records which governed or candidate meaning materially constrains
other work.

Reconciliation restores confidence in downstream alignment after material
change without silently propagating new semantic decisions.

## Workflow Direction

The principal semantic direction remains:

    Canon
      ↓ dramatic projection
    Plot
      ↓ controlled realization
    Prose
      ↓ manuscript acceptance
    Manuscript

This semantic direction does not require a single fixed artifact hierarchy.

Authoring may move in any useful direction for discovery, diagnosis, revision,
or review.

Mutation occurs only at the semantic surface or production-control artifact
whose meaning or control role is intentionally being changed.

## Progressive Refinement Principle

The Product must support top-down refinement from broad author intent to work
that is sufficiently bounded for reliable model execution.

Each refinement step reduces unresolved decisions left to later steps.

Refinement may add:

- scope;
- ordering;
- required content;
- exclusions;
- viewpoint;
- reveal boundaries;
- emotional or dramatic movement;
- local transitions;
- style realization guidance;
- generation boundaries;
- or other constraints needed by downstream work.

Refinement must preserve the accepted meaning it depends on unless the author
explicitly revises that meaning.

A refinement artifact may itself remain candidate.

## Refinement Vocabulary

The Product may use structures such as:

    Synopsis
      ↓
    Outline
      ↓
    Sequence or Scene Plan
      ↓
    Beats
      ↓
    Modes
      ↓
    Pseudo-prose or Near-prose Layout
      ↓
    Generation Package
      ↓
    Generated Prose

These names are not additional semantic authority layers.

They are production-control structures that progressively reduce the model's
planning freedom.

The exact decomposition may vary by task, project, genre, model capability, or
author preference, provided the Product preserves the required control
properties.

Skipping an intermediate named artifact is permitted only when the downstream
task remains reliably bounded without it.

## Refinement Sufficiency

Refinement is sufficient for a generation task only when the model can perform
the requested work without independently deciding consequential narrative
meaning that should already be governed upstream.

A generation task is not sufficiently refined when successful completion would
require the model to guess or invent material consequences such as:

- what materially happens next;
- which character knows or reveals governed information;
- whether a consequential fact is true;
- what dramatic turn the author intends;
- where the requested unit should stop;
- or another decision owned by Canon, Plot, or accepted persistent Prose
  guidance.

When refinement is insufficient, the Product must refine the task further,
retrieve missing dependencies, or surface the unresolved decision.

It must not treat model improvisation as a substitute for missing author intent.

## Reliability-Based Granularity

Generation granularity is determined by reliable execution, not by a fixed
textual size.

A scene may be generated as one task when its intent and constraints are
sufficiently bounded.

When that leaves excessive model discretion, the scene must be decomposed into
smaller units.

Refinement may reach beat-scale, paragraph-scale, sentence-scale, or another
local unit when required.

The Product should prefer the largest unit that remains reliably bounded,
because unnecessary fragmentation creates authoring overhead without improving
control.

## Production Contracts

Before prose generation, the Product may assemble a production-control artifact
that states the local narrative contract for the requested unit.

A production contract may define:

- purpose and boundary;
- entry and exit conditions;
- required beats or movements;
- viewpoint and focal access;
- character knowledge limits;
- reveal and concealment rules;
- emotional progression;
- setting and sensory constraints;
- applicable style guidance;
- protected text or terminology;
- permitted non-consequential invention;
- prohibited consequential invention;
- and dependencies required for interpretation.

A production contract may be refined further into near-prose units before
generation.

The production contract constrains generation. It does not become an
independent source of story truth.

## Generation Readiness

A unit is generation-ready when all of the following are true:

- its generation boundary is identifiable;
- the intended narrative movement is sufficiently specified;
- material Canon and Plot dependencies are available;
- unresolved candidate dependencies are explicitly identifiable;
- viewpoint and information-access constraints are known where applicable;
- reveal boundaries are known where applicable;
- applicable persistent Prose/style guidance is available;
- permitted and prohibited invention are sufficiently clear;
- and remaining model discretion is primarily local realization rather than
  consequential planning.

Generation readiness does not require that every dependency be semantically
accepted.

Candidate dependencies may be used under DP-110 when their non-authoritative
status is preserved.

## Dependency Principle

A dependency exists when current interpretation, validity, realization, or
acceptance of one artifact materially relies on another governed or candidate
target.

Dependencies may connect:

- Canon facts, state, relationships, knowledge, beliefs, and events;
- Plot structures to Canon they present;
- Plot structures to other Plot structures;
- Prose structures to Plot they realize;
- production-control artifacts to semantic or candidate inputs;
- generated candidates to the context that constrained them;
- Manuscript units to the semantic and production-control state they realize;
- generated views to their governed sources;
- and other targets whose meaning must remain coherent.

Dependency does not transfer semantic ownership.

## Material Dependency

The Product need not treat every historical influence, retrieval, prompt input,
or nearby artifact as a semantic dependency.

A dependency is material when changing or removing the upstream target could
reasonably change the interpretation, validity, intended realization, or
acceptability of the dependent target.

Material dependency is evaluated against current state.

Historical derivation may be retained separately for provenance and
reproducibility.

## Dependency on Candidate State

Dependencies on candidate state must remain distinguishable from dependencies
on accepted authority.

Candidate chains are permitted.

A downstream candidate may continue to depend on unresolved upstream candidate
meaning as long as that dependency remains identifiable.

Production approval or further refinement does not silently convert the
candidate dependency into accepted authority.

Acceptance remains governed by DP-110 acceptance closure.

## Dependency Precision

Dependency should be recorded at the narrowest useful scope.

A scene should depend on the specific facts, events, relationships, reveal
decisions, style constraints, or candidate assumptions that materially govern
it rather than indiscriminately depending on an entire novel when narrower
dependency is practical.

Dependency precision supports:

- bounded context construction;
- local regeneration;
- minimal reconciliation;
- meaningful validation;
- and long-form navigation.

The Product does not require maximal fine-grained bookkeeping when broader
dependency is sufficient to preserve correctness.

## Upstream Revision

An accepted upstream revision supersedes prior accepted meaning at its scope.

It does not automatically rewrite dependent downstream artifacts.

Potentially affected dependents become subject to impact analysis and
reconciliation.

Typical semantic impact follows the ownership direction:

- Canon revision may affect Plot, Prose, production-control artifacts, and
  Manuscript;
- Plot revision may affect Prose, production-control artifacts, and Manuscript
  without changing Canon;
- persistent Prose revision may affect production-control artifacts and
  Manuscript without changing Canon or Plot;
- production-control revision may affect generated candidates without itself
  changing accepted story truth.

These are possible impacts, not mandatory invalidation of every downstream
artifact.

## Impact Analysis

Impact analysis determines the smallest set of current dependents that may no
longer preserve their governing meaning after a material change.

Impact analysis follows material dependencies rather than merely artifact
location or workflow depth.

The Product may determine that a dependent:

- remains aligned;
- requires review;
- requires local revision or regeneration;
- is blocked by an unresolved candidate dependency;
- has been superseded;
- or is no longer applicable.

These outcomes describe semantic condition; later Planning may choose persisted
labels or status representations.

## Reconciliation

Reconciliation is the author-governed process of restoring confidence in
alignment after a material accepted change or candidate-dependency resolution.

Reconciliation may:

- confirm an affected dependent unchanged;
- revise or regenerate local downstream work;
- revise a broader dependent region when actual impact requires it;
- supersede or remove obsolete material;
- resolve or replace candidate dependencies;
- reveal another dependency requiring review;
- or expose a reason for the author to reconsider the upstream change.

Reconciliation does not grant permission to invent new consequential meaning
solely to make downstream state appear consistent.

Any new consequential decision remains candidate until accepted according to
DP-110.

## Minimal Reconciliation Scope

Reconciliation must be proportional to actual semantic impact.

The Product should identify the smallest materially affected dependency region
that preserves confidence in alignment.

A local change must not force whole-story regeneration or review merely because
broad invalidation is easier to implement.

When dependency precision is insufficient to establish a narrower safe scope,
broader review may be required.

## Mechanical Propagation Boundary

Mechanical propagation is permitted only when the transformation preserves
already-governed meaning and introduces no unresolved consequential choice.

Examples may include updating a reference, carrying forward an accepted name
change, rebuilding a context projection, or regenerating a derived view when
the semantic result is determined by accepted state.

When multiple semantically valid outcomes exist and choosing among them would
change consequential meaning, automatic propagation must stop.

The unresolved choice becomes candidate work for author review.

## Re-Refinement After Change

An upstream change may invalidate not only generated prose but the refinement
path that produced it.

The Product must therefore be able to resume refinement from the highest
affected production-control point rather than always restarting from the
broadest story level or merely regenerating prose from stale controls.

For example, a changed Plot reveal may require revising a scene contract and
pseudo-prose layout before prose regeneration, while leaving broader Synopsis
and Outline intent unchanged.

## Context Construction Relationship

Dependency and refinement jointly determine what enters a generation context.

Refinement defines the local task.

Dependencies identify the semantic and candidate inputs materially needed to
perform that task.

Context construction should include enough information to make the task
complete while avoiding unrelated story material that increases model
distraction or encourages unsupported inference.

The generation package records the selected projection and its provenance as
required by DP-100.

## Validation Relationship

Validation may test whether:

- required dependencies exist;
- candidate dependencies are identifiable;
- the refinement is generation-ready;
- generated output remains within its boundary;
- required movements are present;
- prohibited invention occurred;
- or a dependent remains aligned after change.

Validation may diagnose a problem.

Validation does not create missing semantic meaning, accept a candidate, or
choose among unresolved consequential alternatives.

## Failure-Safe Behavior

When the Product cannot determine whether refinement is sufficient, whether a
dependency is material, or whether a downstream target remains aligned after a
change, it must not silently assume safety.

The Product may require further refinement, additional retrieval, or semantic
review.

Uncertainty degrades to review or candidate state rather than automatic
acceptance or propagation.

## Planning Boundary

This Design defines progressive refinement, generation readiness, dependency,
impact, propagation, and reconciliation meaning.

Later Design may define specific Prose control structures, generation-package
semantics, context construction, identity and traceability, persistence,
validation, and generated-view behavior.

Planning may choose dependency representations, graph structures, status
values, invalidation algorithms, workflow commands, context-selection
algorithms, regeneration strategies, and other technical realization.

Implementation convenience does not override the requirement for bounded
generation or materially scoped reconciliation.
