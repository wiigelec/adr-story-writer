---
functional_set: FS-004
artifact: plan
title: Governed Upstream Revision, Impact, and Reconciliation Plan
design_revision: 0ab706c19fcca4f133188393529e386662d1126e
---

# FS-004 — Plan

## Objective

Extend the accepted Story Writer runtime from safe continuation of prepared story
state to safe revision of governed story meaning after downstream work already
exists.

FS-004 shall reuse the authority, compatibility, production, review, persistence,
and scene-runtime semantics already accepted in FS-001 through FS-003. It shall
not introduce a second dependency model, a parallel acceptance vocabulary, or an
automatic propagation mechanism that changes story meaning merely to restore
consistency.

The central technical capability is a governed reconciliation cycle:

    reconstruct
      ↓
    propose upstream revision
      ↓
    accept identified revision
      ↓
    compute material impact
      ↓
    classify downstream freshness
      ↓
    reconcile selected dependents
      ↓
    rebuild production context
      ↓
    restore generation readiness
      ↓
    persist
      ↓
    reconstruct

## Runtime Surface

Extend the existing runtime with an explicit upstream-revision and
reconciliation surface.

The runtime shall make the following operations independently observable:

1. resolve current governed target;
2. create or register a candidate semantic revision;
3. inspect candidate dependencies and affected scope;
4. explicitly accept, reject, withdraw, or replace the candidate revision;
5. compute impact from an accepted upstream change;
6. inspect downstream freshness/reconciliation state;
7. reconcile a selected dependent;
8. determine generation readiness after reconciliation;
9. rebuild a production contract and generation package when prior production
   state is stale;
10. persist; and
11. reconstruct the resulting state in a fresh session.

The exact API/module organization is a Build choice. Prefer extending the
existing runtime and contracts over creating a generalized workflow engine.

## Upstream Revision Representation

Represent an upstream revision as a candidate semantic change to an identifiable
Canon or Plot target.

A candidate revision shall identify at least:

- target semantic identity;
- target surface;
- current accepted revision, when one exists;
- candidate revision identity;
- proposed semantic content or change;
- known material dependencies or assumptions required by the proposal; and
- whether the operation is revision of the same semantic object or replacement
  of that object.

Creating or persisting a candidate revision does not change accepted semantic
state.

Where identity continuity is semantically ambiguous, ordinary revision shall not
silently choose continuity. The operation must remain unresolved or use an
explicit replacement/supersession path.

## Revision Acceptance

Revision acceptance shall be an explicit acceptance operation at the semantic
surface that owns the meaning.

A successful revision acceptance shall:

- identify the accepted target scope;
- preserve stable semantic identity when the object continues;
- create a new accepted revision identity;
- supersede the prior accepted revision without deleting historical provenance
  required by downstream reconciliation;
- preserve authority-class separation;
- not automatically revise dependent Plot, Prose, production, or Manuscript
  state; and
- initiate or expose impact analysis for materially dependent current state.

Coordinated acceptance may be used when one author decision intentionally
changes several semantic targets, but each target's ownership must remain
identifiable.

## Material Dependency Model

Use the accepted DP-110/DP-120 distinction between material dependency and
historical derivation.

A dependency is material when the current downstream meaning or governed
operation still relies on the referenced upstream meaning.

Historical derivation alone shall not make a downstream artifact stale.

The implementation must preserve enough relationship information to determine,
for the bounded reference case:

- dependency target identity;
- dependency target revision or accepted basis;
- dependent identity and semantic/production surface;
- whether the dependency is material;
- whether it is accepted- or candidate-based where relevant; and
- current relationship freshness or reconciliation state.

The exact persisted representation is a Build choice. Do not require a universal
graph database.

## Impact Analysis

Given an accepted upstream revision, compute the bounded set of known downstream
relationships that may be materially affected.

Impact analysis shall classify each applicable relationship as one of the
following meanings, using any unambiguous implementation vocabulary:

- **still valid** — the dependent remains semantically valid under the new
  upstream revision;
- **review required / stale** — the dependent may no longer be safe to use
  without reconciliation;
- **superseded** — the relationship targeted an object/revision that is no longer
  current and has a known replacement path; or
- **unresolved** — the Product cannot determine the continuing relationship
  without semantic judgment.

Impact analysis may narrow the affected set mechanically when exact dependencies
and revisions establish the answer. It shall not manufacture semantic
equivalence to avoid review.

## Downstream Freshness

Persist freshness/reconciliation state where needed so a later session can
distinguish valid current work from work requiring review.

Staleness is not a new story-authority class. It describes whether an existing
artifact or relationship remains safe for its governed downstream role.

Marking an artifact stale shall not:

- revoke its historical acceptance;
- rewrite its semantic content;
- accept a replacement;
- delete it; or
- imply that every historically related artifact is also stale.

Ordinary generation or acceptance shall not consume a materially stale or
unresolved dependency as though it were current.

## Reconciliation Operations

Provide a bounded reconciliation surface that can resolve one affected dependent
through deliberate operations such as:

- preserve unchanged after review;
- revise while preserving identity;
- replace/supersede with a different semantic object;
- regenerate/rebuild production control;
- withdraw candidate state;
- narrow the dependent scope;
- or leave unresolved.

The exact command vocabulary is a Build choice.

A reconciliation operation must identify the upstream change being reconciled
and the dependent scope being resolved.

Reconciliation must not invent consequential replacement meaning merely to make
the dependency graph mechanically clean.

## Plot Reconciliation

For an affected Plot target, support at least:

- inspection of the changed Canon dependency;
- retaining the Plot unchanged when semantic review establishes that it does not
  materially depend on the changed meaning;
- candidate Plot revision when presentation meaning must change;
- explicit acceptance of that Plot revision; and
- downstream impact continuation into Prose/production/Manuscript only when the
  current downstream state materially depends on the changed Plot.

FS-004 shall preserve the accepted Product Design boundary that Canon owns story
truth while Plot owns narrative presentation.

Implementation terminology shall not treat Plot acceptance as implicit creation
of Canon truth.

## Prose and Production Reconciliation

A production-approved Prose/control artifact whose governing semantic
dependencies have changed shall not continue to control generation without
reconciliation when the change is material.

The runtime shall be able to:

- mark the prior control state stale/review-required;
- retain it if review proves it still valid;
- revise or replace it deliberately;
- rebuild a production contract from current governed state; and
- produce a new generation package after readiness is restored.

Historical production artifacts remain available for provenance but do not
automatically govern current work.

## Generation-package Invalidation

Generation packages are frozen records of the context used for a particular
attempt.

FS-004 shall never mutate a used generation package to make it appear current.

When a selected governing revision changes materially:

- the prior package remains immutable historical provenance;
- the Product shall not use it for a new ordinary generation attempt;
- the affected task becomes not-ready or package-rebuild-required until current
  governing context is sufficient; and
- a later package shall receive its own identity and provenance.

Package invalidation does not invalidate the historical candidate generated from
that package; it changes whether that package can govern future attempts.

## Manuscript Reconciliation

Accepted Manuscript that materially depends on superseded semantic meaning may
require review, but its historical acceptance shall not disappear automatically.

FS-004 shall permit:

- retaining accepted text after review when still semantically valid;
- creating candidate replacement/revision text when necessary;
- preserving the prior accepted text until a replacement is explicitly accepted;
- applying normal Manuscript acceptance gates to the replacement; and
- retaining provenance sufficient to explain the revision chain.

An accepted upstream revision must not directly rewrite chapter files.

## Generation Readiness

After reconciliation, determine whether a target scene is ready for ordinary
FS-003 production.

Generation readiness requires, for the bounded target:

- current compatible Dataset/Ruleset state;
- resolved material dependencies;
- no governing stale/unresolved relationship that blocks the task;
- current Plot intent;
- applicable Prose/production guidance;
- current information-access boundaries;
- a valid stopping boundary; and
- enough current governed revisions to construct a new production contract and
  package.

Missing consequential meaning shall produce not-ready/unresolved rather than
automatic invention.

## Persistence

Persist upstream revision, impact, freshness, reconciliation, acceptance, and
production provenance as one coherent Dataset transition.

A successful save shall preserve:

- current accepted semantic revision;
- prior revision identity needed for history/reconciliation;
- material dependency relationships;
- downstream freshness/reconciliation state;
- unresolved decisions;
- current production approval;
- immutable historical generation-package provenance;
- current accepted Manuscript state; and
- replacement/revision provenance where applicable.

Reuse the existing coherent-save and conflict-detection behavior. Ordinary save
must not overwrite a newer external Dataset state.

## Fresh-session Reconstruction

The required test shall destroy all in-memory state after persistence.

A newly constructed runtime shall then:

1. establish compatibility;
2. reconstruct the accepted upstream revision;
3. reconstruct which downstream dependents were preserved, reconciled, replaced,
   or left unresolved;
4. retain unaffected work as current;
5. prevent unresolved stale state from ordinary generation;
6. identify the current accepted Manuscript revision;
7. reconstruct immutable historical package provenance; and
8. prepare a reconciled target scene for a new current generation package.

No prior conversation, process memory, or hidden model memory may be required.

## Validation Strategy

Build shall extend Product Validation with deterministic tasks for mechanically
decidable FS-004 behavior, including:

- exact FS-004 Planning/Design binding;
- candidate revision does not mutate accepted state;
- explicit revision acceptance and revision identity;
- dependency-target and dependent identity preservation;
- distinction between material dependency and unrelated/historical relation in
  the reference fixture;
- bounded impact classification;
- stale/unresolved state blocking ordinary dependent use;
- no automatic downstream semantic rewrite;
- package immutability and refusal to reuse materially stale packages;
- generation-readiness restoration after reconciliation;
- coherent persistence;
- save-conflict behavior; and
- fresh-process reconstruction.

Validation must not claim semantic equivalence merely because dependency fields
are structurally valid.

## Semantic Review Demonstration

Semantic Review shall execute a complete revision-and-reconciliation scenario
against an external reference story fixture.

At minimum:

1. reconstruct a compatible Dataset containing accepted Canon, Plot, Prose,
   production, Manuscript, and package provenance;
2. select an accepted Canon or Plot target with at least one material and one
   non-material/historical downstream relationship;
3. create a candidate semantic revision;
4. verify accepted state is unchanged;
5. explicitly accept the upstream revision;
6. run impact analysis;
7. verify the materially dependent scene requires reconciliation;
8. verify the unrelated scene remains usable;
9. verify the old frozen generation package remains historical and cannot govern
   a new ordinary attempt;
10. reconcile the affected Plot/Prose/production chain without automatic
    semantic rewriting;
11. repair or replace affected Manuscript through ordinary candidate/review/
    acceptance semantics when required;
12. restore generation readiness;
13. construct a new production contract and package from current revisions;
14. persist coherently;
15. discard the runtime; and
16. reconstruct the resolved and any deliberately unresolved state in a fresh
    session.

Semantic Review shall also verify at least one case where impact cannot be
resolved mechanically and therefore remains review-required or unresolved rather
than being guessed.

## Build Boundary

Do not introduce:

- automatic global propagation of semantic edits;
- whole-story rewrite orchestration;
- a generalized graph database;
- event sourcing merely to obtain revision history;
- automatic semantic acceptance;
- hidden identity replacement;
- mutation of used generation packages;
- provider-specific LLM coupling in core reconciliation state;
- story-instance data in this Ruleset repository; or
- broad author-facing governance ceremony for mechanically obvious unchanged
  scopes.

Prefer explicit relationships and bounded scenario behavior until larger-story
scale demonstrates a need for additional indexing or abstraction.
