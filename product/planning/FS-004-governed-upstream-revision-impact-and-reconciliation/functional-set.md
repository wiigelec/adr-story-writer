---
functional_set: FS-004
artifact: functional-set-scope
title: Governed Upstream Revision, Impact, and Reconciliation
design_revision: 0ab706c19fcca4f133188393529e386662d1126e
---

# FS-004 — Governed Upstream Revision, Impact, and Reconciliation

## Purpose

FS-004 establishes the executable Product capability required to change accepted
story meaning safely after downstream work already exists.

FS-001 established governed authority, candidate state, production control,
review, acceptance, and persistence semantics. FS-002 established Dataset and
Ruleset compatibility. FS-003 demonstrated bounded scene production and
fresh-session continuation from already-prepared governed state.

FS-004 addresses the complementary problem:

> Given an accepted story with existing downstream Plot, Prose, production, and
> Manuscript work, the author can intentionally revise accepted Canon or Plot,
> identify which downstream state is materially affected, preserve unaffected
> work, prevent stale state from silently governing new generation, reconcile
> affected dependents without automatic semantic rewriting, restore selected
> scopes to generation readiness, persist the coherent result, and reconstruct
> that reconciliation state in a fresh session.

Consequential story authority remains with the author. Impact analysis and
reconciliation may identify required work, but neither operation grants semantic
authority or invents replacement meaning.

## Exact Design Binding

Planning consumes Product Design at repository revision:

`0ab706c19fcca4f133188393529e386662d1126e`

No new Product Design is introduced by FS-004. The accepted Product Design
already defines the required authority, dependency, revision, reconciliation,
identity, persistence, and review semantics.

Selected Product Design obligations are:

- **DP-100:** Canon → Plot → Prose → Manuscript ownership, deliberate backward
  movement for intentional revision, bounded generation, and Dataset-backed
  continuity;
- **DP-110:** semantic acceptance, revision acceptance, coordinated acceptance,
  candidate dependencies, acceptance closure, rejection/withdrawal, and the rule
  that accepted upstream change does not silently rewrite dependents;
- **DP-120:** material dependency, dependency precision, impact analysis,
  reconciliation, re-refinement, lowest-layer repair, and deliberate propagation
  after upstream change;
- **DP-130:** Canon/Plot ownership, viewpoint and reader-information boundaries,
  and separation of story truth from narrative presentation;
- **DP-140:** Canon state, Event, chronology, causal, knowledge, belief, and
  narrative-time meaning that may be revised or affected;
- **DP-150:** production-contract and generation-package dependence on selected
  governed revisions, local regeneration, protected material, and generation
  readiness;
- **DP-160:** durable candidate and accepted state, save coherence, concurrency,
  and fresh-session reconstruction of unresolved reconciliation state;
- **DP-175:** stable semantic identity, revision versus replacement,
  split/merge/supersession boundaries, material relationships, stale references,
  and cross-layer traceability;
- **DP-180:** freshness, semantic review, indeterminate outcomes, repair
  boundaries, consequential-invention handling, and acceptance gates; and
- **DP-190:** simplicity boundaries requiring author-facing behavior to expose
  consequential decisions without forcing unnecessary internal governance
  ceremony onto ordinary author work.

## Functional Boundary

FS-004 begins with:

1. one externally persisted, compatible story Dataset;
2. accepted governed semantic state;
3. at least one accepted Canon or Plot object eligible for intentional revision;
4. existing downstream governed state materially related to that object; and
5. enough stable identity and dependency information to determine whether those
   downstream relationships remain valid, require review, or are unresolved.

FS-004 ends when the Product can:

1. create and retain a candidate upstream semantic revision without changing
   accepted meaning;
2. explicitly accept an upstream revision at an identifiable semantic scope;
3. preserve the revised object's continuing identity when the semantic object
   remains the same, or require explicit replacement/supersession treatment when
   it does not;
4. determine which downstream dependencies are materially affected by the
   accepted change;
5. distinguish affected material from unrelated or historically derived material
   that no longer depends on the changed meaning;
6. prevent stale or unresolved downstream state from silently governing new
   production or acceptance;
7. reconcile affected Plot, Prose, production-control, or Manuscript state
   through explicit preserve, revise, replace, withdraw, or unresolved paths as
   applicable;
8. invalidate or retire generation packages whose frozen governing revisions no
   longer describe the current task;
9. restore at least one affected scene to generation-ready state without
   requiring unrelated scenes to be regenerated;
10. persist the resulting authority, dependency, freshness, reconciliation, and
    provenance state coherently; and
11. reconstruct that state in a fresh session without relying on prior
    conversation or private model memory.

## Required Reference Demonstration

Semantic Review shall exercise an external story fixture with at least:

- one accepted upstream Canon object;
- one accepted Plot scene materially dependent on that Canon meaning;
- one production-approved Prose/control artifact materially dependent on the
  scene;
- one accepted Manuscript unit materially dependent on the same chain;
- one unrelated accepted scene that shares historical context but does not
  materially depend on the revised meaning;
- one frozen generation package built from the pre-revision governing state; and
- a later planned scene whose readiness can be restored after reconciliation.

The demonstration shall intentionally revise accepted upstream meaning and prove
that:

1. candidate revision alone does not alter accepted state;
2. accepted revision supersedes the prior accepted revision at the identified
   scope;
3. materially affected dependents are identified for reconciliation;
4. unrelated dependents remain usable;
5. stale production state and generation packages do not silently govern new
   generation;
6. no downstream semantic content is automatically rewritten merely because the
   upstream revision was accepted;
7. the author can reconcile the affected chain deliberately;
8. the reconciled scene can return to generation-ready state;
9. persistence records the new accepted revision and remaining unresolved state
   coherently; and
10. a fresh session reconstructs both the resolved and unresolved consequences
    correctly.

## Revision Scenario

The reference scenario should use a consequential revision whose effects cross
multiple semantic surfaces rather than a cosmetic text edit.

A suitable shape is:

- accepted Canon establishes a character fact, relationship, knowledge state,
  chronology fact, event consequence, or hidden truth;
- accepted Plot and Manuscript currently depend on that meaning;
- the author intentionally revises the Canon meaning;
- one downstream scene must be reconsidered because its current meaning depends
  on the prior revision;
- another scene remains valid because its relationship is merely historical,
  incidental, or non-material;
- the Product surfaces the difference;
- the affected scene is reconciled deliberately; and
- a replacement generation package is built only after current governing state
  is again sufficient.

The exact story content is demonstration evidence, not Product authority.

## Explicit Deferrals

FS-004 does not require:

- generalized automatic story rewriting;
- autonomous acceptance of upstream or downstream semantic changes;
- universal semantic dependency inference across arbitrary free text;
- whole-manuscript automatic continuity repair;
- generalized graph-database infrastructure;
- arbitrary multi-branch collaborative merge resolution;
- full generalized Event split/merge lifecycle beyond what the reference
  revision requires;
- arbitrary schema migration or Ruleset rebinding beyond accepted FS-002
  behavior;
- provider-specific LLM integration;
- generated dossier or author-view editing from DP-190 except where a minimal
  view is useful for demonstrating impact;
- manuscript-wide export or publication tooling; or
- optimization of large-story indexing beyond what the bounded demonstration
  requires.

## Completion Criterion

FS-004 is complete only when executable behavior proves that an accepted
upstream semantic revision can be introduced, its material downstream effects
can be identified without broad false invalidation, affected work can be
reconciled without silent semantic rewriting, unaffected work remains usable,
generation readiness can be restored, and the resulting state survives a fresh
session.
