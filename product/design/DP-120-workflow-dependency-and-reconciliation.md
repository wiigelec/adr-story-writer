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

Refinement reduces or makes explicit decisions that would otherwise be left to
downstream generation.

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

Each control-bearing refinement step reduces or makes explicit decisions that
would otherwise be left to downstream generation.

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

The contract must be capable of expressing the local boundary, required
narrative intent, applicable semantic dependencies, information-access
constraints, invention boundaries, and other controls needed to make the task
reliably bounded.

A production contract may be refined further into smaller realization units
before generation.

The production contract constrains generation. It does not become an
independent source of story truth.

DP-150 defines the semantic roles and required control properties of production
contracts and generation packages. Planning defines their detailed fields and
representation.

## Generation Readiness

Generation readiness is relative to a specific generation task and its intended
execution context.

A unit is generation-ready for that task when:

- its generation boundary is identifiable;
- the intended narrative movement is sufficiently specified;
- material Canon and Plot dependencies for the task are available;
- unresolved candidate dependencies are explicitly declared as working
  assumptions;
- applicable viewpoint, information-access, reveal, and persistent Prose/style
  constraints are available where needed;
- permitted and prohibited invention are sufficiently clear;
- and remaining model discretion is primarily local realization rather than
  consequential planning.

A unit that is ready for one task size, model capability, or execution context
may require further refinement for another.

Generation readiness does not require that every dependency be semantically
accepted.

Candidate dependencies may be used under DP-110 only when their
non-authoritative status is preserved and their use is declared for the
generation task.

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

A dependency is material for a particular dependent scope or operation when
changing or removing the upstream target could reasonably change the
interpretation, validity, intended realization, or acceptability of that scope
or operation.

Materiality is therefore evaluated against current state and the purpose for
which the dependency is being considered. It is not necessarily a permanent
global property of the relationship.

Historical derivation may be retained separately for provenance and
reproducibility.

## Dependency on Candidate State

Dependencies on candidate state must remain distinguishable from dependencies
on accepted authority.

Candidate chains are permitted.

A downstream candidate may continue to depend on unresolved upstream candidate
meaning as long as that dependency remains identifiable.

When candidate meaning is used to construct or execute a generation task, it
must be declared as a working assumption for that task rather than silently
included as if it were accepted authority.

Production approval or further refinement does not silently convert the
candidate dependency into accepted authority.

Acceptance remains governed by DP-110 acceptance closure.

## Dependency Precision

Dependency should be recorded at the narrowest semantically useful scope.

A scene should depend on the specific facts, events, relationships, reveal
decisions, style constraints, or candidate assumptions that materially govern
it rather than indiscriminately depending on an entire novel when narrower
dependency is practical.

Dependency precision supports bounded context construction, local regeneration,
minimal reconciliation, meaningful validation, and long-form navigation.

The goal is useful semantic precision, not maximal granularity. The Product does
not require atom-level dependency bookkeeping when a broader relationship is
sufficient to preserve correctness and support reliable impact analysis.

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

For each materially affected dependent, the Product must be able to determine
whether confidence in alignment remains sufficient or whether review,
reconciliation, revision, regeneration, supersession, or removal is required.

This Design does not require a fixed persisted status taxonomy. DP-180 and
Planning may define operation-relevant review or validation classifications where
useful without turning them into new semantic authority.

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

Automatic propagation is permitted only when accepted state determines the
semantic result and the transformation introduces no unresolved consequential
choice.

Examples may include updating a reference, carrying forward an accepted name
change, rebuilding a context projection, or regenerating a derived view when
the required semantic result is determined by governed inputs.

If more than one consequentially distinct result is semantically valid, the
system must not select among them automatically.

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

Dependency and refinement jointly determine what a generation context must
represent.

Refinement defines the local task.

Dependencies identify the governed and declared candidate inputs materially
needed to perform that task.

Context construction must provide sufficient governing information without
making correctness depend on unrelated whole-story material.

Detailed context projection and generation-package semantics are defined by
DP-150.

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

DP-150, DP-160, DP-175, DP-180, and DP-190 define the corresponding Prose
control, generation-package, persistence, identity/traceability, validation, and
generated-view semantics.

Planning may choose dependency representations, graph structures, status
values, invalidation algorithms, workflow commands, context-selection
algorithms, regeneration strategies, and other technical realization.

Implementation convenience does not override the requirement for bounded
generation or materially scoped reconciliation.
