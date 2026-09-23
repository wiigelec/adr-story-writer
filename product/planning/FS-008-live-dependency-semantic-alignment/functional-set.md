---
functional_set: FS-008
artifact: functional-set-scope
title: Live Dependency and Scene Semantic Alignment
design_revision: 7867554b02d39a55b7171c992a61196a87863552
---

# FS-008 — Live Dependency and Scene Semantic Alignment

## Purpose

FS-008 realizes DP-200 by separating live semantic dependency identity from
historical revision evidence and frozen generation provenance.

The Product shall let scenes and other governed artifacts depend on stable
Canon/Plot identities, resolve those dependencies against current accepted
meaning, detect when prior semantic alignment evidence is no longer current,
and rebuild bounded scene-generation packages without requiring earlier
Manuscript prose.

## Exact Design Binding

Planning consumes Product Design at repository revision:

`7867554b02d39a55b7171c992a61196a87863552`

This revision adds DP-200 and establishes:

- Canon as the cross-scene continuity authority;
- stable-identity live dependency semantics;
- alignment evidence distinct from dependency identity;
- scene-local top-to-bottom semantic closure;
- Manuscript independence for ordinary cross-scene continuity;
- frozen revision provenance for generation attempts;
- bounded scene-generation context as a scalability invariant.

## Functional Boundary

FS-008 begins with compatible governed story state containing stable artifact
identities, accepted revisions, scene Plot, Prose controls, and optional
Manuscript.

FS-008 ends when the Product can:

1. represent a live material dependency by stable `target_id` without pinning
   that relationship to a target content revision;
2. resolve the dependency to the current accepted artifact state when checking
   readiness or compiling a production contract;
3. preserve revision-specific alignment evidence showing which upstream
   revisions were covered by the last successful semantic alignment;
4. mark alignment review-required when a material upstream accepted revision
   changes without treating the stable dependency identity itself as obsolete;
5. reconcile a dependent scope while retaining the same live target identity
   for continuing upstream artifacts;
6. preserve exact selected revisions in frozen generation-package provenance;
7. compile scene-generation context from the target scene, current accepted
   referenced Canon/Plot state, applicable Prose controls, viewpoint and
   information-access constraints, and style projection;
8. avoid routine inclusion of all prior accepted Manuscript;
9. generate a later scene when an earlier scene's prose does not exist, provided
   required accepted Canon/Plot state exists;
10. surface consequential prose invention for upstream semantic resolution and
    require affected downstream alignment to be reconsidered after acceptance.

## Dependency Boundary

A live dependency identifies the semantic object depended upon.

For a continuing object, revision changes do not replace the dependency target.
Revision-specific values belong to:

- alignment evidence;
- reconciliation/impact records;
- revision history;
- frozen production/generation provenance.

Replacement with a new semantic identity remains an explicit replacement and
may require updating the dependency target identity.

## Alignment Boundary

Alignment evidence is proof about a dependent scope, not semantic authority.

For each material live dependency, the Product must be able to determine whether
the dependent scope has been reviewed against the dependency's current accepted
revision.

A changed upstream revision may produce `still_valid`, `review_required`,
`superseded`, or `unresolved` according to existing reconciliation semantics.

Successful preserve/revise/rebuild reconciliation advances alignment evidence to
the current accepted upstream revision without converting the live dependency
into a revision-pinned relationship.

## Scene-generation Boundary

The generator-facing package is a compiled execution artifact.

Routine package construction shall not depend on prior Manuscript text for
cross-scene factual continuity. Earlier scene consequences required by the
target scene must arrive through governed Canon/Plot dependencies.

The package may include explicitly selected bounded textual material when exact
wording or immediate textual handoff is required, but no automatic
all-prior-Manuscript accumulation is permitted.

## Nonlinear-generation Demonstration

The executable demonstration shall include a case where:

- an earlier scene establishes accepted semantic state used by a later scene;
- the earlier scene has no Manuscript prose;
- the later scene directly references the required Canon/Plot artifacts;
- the later scene reaches generation-ready state;
- its generation package contains the required current semantic state and no
  dependency on the missing earlier prose.

## Revision and Realignment Demonstration

The executable demonstration shall also:

1. establish a scene aligned to an accepted Canon artifact;
2. revise that Canon artifact under the same stable identity;
3. prove the scene retains the same live `target_id`;
4. prove its prior alignment evidence becomes non-current;
5. reconcile/review the scene against the new accepted Canon revision;
6. prove the live dependency target remains unchanged;
7. prove new generation provenance records the new selected revision while an
   older frozen package retains the old selected revision.

## Scale Demonstration

Validation shall construct or synthesize enough prior scene/manuscript state to
prove that the target scene's generator payload does not grow by automatically
including all preceding Manuscript.

The exact synthetic story size is a Planning/Build fixture choice, but the test
must demonstrate the architectural property rather than only a small fixed
example.

## Explicit Deferrals

FS-008 does not require:

- physical Dataset sharding;
- semantic/vector search over historical prose;
- a second continuity database;
- automatic promotion of generated prose into Canon;
- provider-specific LLM integration;
- automatic semantic equivalence judgment;
- whole-story prose comparison;
- a new artifact identity for ordinary content revision.

## Completion Criterion

FS-008 is complete when a fresh generator can receive one bounded scene package
whose continuity comes from current governed semantic dependencies rather than
the story's preceding prose, while the Product separately preserves historical
alignment and generation revision evidence.
