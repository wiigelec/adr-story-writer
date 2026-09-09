---
doc_id: DP-120
title: Workflow, Dependency, and Reconciliation
depends_on:
  - DP-100
  - DP-110
---

# Workflow, Dependency, and Reconciliation

## Purpose

Story artifacts refine and depend upon other story artifacts.

When accepted upstream meaning changes, dependent accepted artifacts must not
be silently rewritten or silently treated as still aligned.

## Principal Refinement Direction

The principal semantic direction is:

    Canon
      ↓
    Synopsis
      ↓
    Outline
      ↓
    Sequence
      ↓
    Beats
      ↓
    Modes
      ↓
    Pseudo-prose
      ↓
    Manuscript

This is a meaning relationship, not a requirement that every project fully
materialize every layer before useful work occurs.

## Plot Refinement

Synopsis establishes broad story-scale direction.

Outline decomposes accepted Synopsis meaning into ordered narrative structure.

Sequence provides the most concrete intended occurrence before prose
realization.

Lower Plot layers preserve accepted meaning of higher Plot layers unless the
author explicitly revises upstream meaning.

## Prose Refinement

Beats prepare the smallest governed narrative-intent units needed to realize
Sequence.

Modes distinguish the narrative mode used to realize those Beats.

Pseudo-prose establishes near-prose flow, emphasis, transitions, viewpoint, and
rough wording before accepted final manuscript text.

## Dependency

An artifact may depend on upstream, downstream, or related artifacts where
their meaning requires interpretation together.

Dependencies support diagnosis, reconciliation, validation, and long-form
navigation.

They do not transfer semantic ownership from one layer to another.

## Upstream Revision

An explicit accepted upstream revision supersedes the prior accepted meaning at
that scope.

It does not automatically rewrite dependent downstream artifacts.

Affected downstream artifacts become candidates for reconciliation when their
accepted meaning may no longer preserve current upstream meaning.

## Reconciliation

Reconciliation is the author-governed process of restoring semantic alignment
after a relevant accepted change.

A dependent artifact may be determined to:

- remain aligned without revision;
- require local downstream revision;
- require broader downstream revision;
- be superseded or removed;
- reveal another dependency requiring review;
- or expose a reason to reconsider the upstream revision.

Diagnosis may travel in either direction, but mutation occurs only at the layer
whose meaning is intentionally being revised.

## Known Misalignment

The product must be able to distinguish semantically aligned dependent state
from dependent state known or reasonably suspected to require review.

The exact persisted representation of stale, conflicted, superseded, or
review-required state is a Planning decision.

Known conflicting dependent material must not be presented as fully aligned
with current accepted upstream meaning.

## Minimal Reconciliation Scope

Reconciliation should be proportional to the changed meaning.

The system should identify the smallest materially affected dependency region
that preserves confidence in semantic alignment.

A local Canon change should not force whole-novel review unless actual
dependencies justify it.

## Propagation Boundary

Reconciliation is not automatic semantic propagation.

The system may propose coordinated multi-layer revisions, but consequential
changes remain subject to DP-110 acceptance rules.

Mechanical transformations are allowed only where already accepted meaning is
preserved and no unresolved semantic choice is invented.
