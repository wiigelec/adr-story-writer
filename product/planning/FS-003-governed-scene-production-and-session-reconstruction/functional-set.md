---
functional_set: FS-003
artifact: functional-set-scope
title: Governed Scene Production, Persistence, and Session Reconstruction
design_revision: 58ebbd0c90060c1fce9da6ac4e18835032ed2336
---

# FS-003 — Governed Scene Production, Persistence, and Session Reconstruction

## Purpose

FS-003 selects the minimum executable Product capability required to turn the
accepted governed prose, compatibility, persistence, and review contracts into a
real end-to-end scene-production workflow.

FS-001 established the semantic and operational contracts for bounded prose
production, candidate state, review, acceptance, persistence, and fresh-session
continuation. FS-002 established Dataset-schema and Ruleset compatibility,
migration, rebinding, and safe failure. FS-003 does not redefine either
Functional Set. It realizes enough runtime behavior to exercise them together.

The Functional Set establishes one executable vertical slice:

> Given one externally persisted story Dataset and an applicable compatible
> Ruleset, the Product can reconstruct the governed state required for one
> already-planned scene, construct a bounded production contract and stable
> generation package, produce or receive candidate prose, review that candidate
> against the governing context, reject or repair a semantic violation, accept a
> conforming Manuscript unit at an explicit scope, persist the resulting Dataset
> coherently, and reconstruct the accepted result in a later fresh session.

Consequential story authority remains with the author.

## Exact Design Binding

Planning consumes Product Design at repository revision:

`58ebbd0c90060c1fce9da6ac4e18835032ed2336`

No new Product Design is introduced by FS-003. The accepted Design already
defines the required meaning. FS-003 selects executable realization obligations
from that Design together with the accepted FS-001 and FS-002 contracts.

Selected Product Design obligations are:

- **DP-100:** Dataset-backed continuity, Canon → Plot → Prose → Manuscript
  ownership, bounded generation, and the retrieve/refine/package/generate/
  review/accept/persist control loop;
- **DP-110:** authority-class separation, explicit scoped acceptance,
  acceptance closure, and persistence independent from authority;
- **DP-120:** lowest-layer navigation, material dependencies, and sufficient
  refinement before generation;
- **DP-130 / DP-140:** viewpoint, reader-information, accepted Canon truth,
  character knowledge, and event/state constraints required by the active scene;
- **DP-150:** production contracts, generation packages, minimum-sufficient
  context, protected material, creative allowance, information-access safety,
  stable package provenance, candidate-only generation, and local correction;
- **DP-160:** Dataset reconstruction, coherent persistence, generation
  provenance continuity, and fresh-session continuation;
- **DP-175:** identity, revision, dependency targeting, and generation
  attribution needed by the executable slice;
- **DP-180:** semantic review outcomes, consequential-invention handling,
  information-boundary review, and acceptance gating; and
- **DP-170:** compatibility gating and any supported transition required before
  ordinary FS-003 operation.

## Functional Boundary

FS-003 begins with:

1. one externally persisted story Dataset;
2. an applicable Story Writer Ruleset;
3. an already-planned scene whose governing Canon, Plot, and Prose material is
   sufficiently explicit to attempt bounded generation; and
4. compatibility established directly or through an explicitly supported
   FS-002 transition.

FS-003 ends when:

1. one target scene has a stable generation package;
2. candidate prose has been semantically reviewed;
3. at least one intentionally non-conforming candidate path has been rejected or
   repaired without silent upstream authority change;
4. a conforming scene has been explicitly accepted as Manuscript;
5. the authorized resulting Dataset state has been persisted coherently; and
6. a later fresh session reconstructs that accepted result and can prepare the
   next planned scene without prior-chat memory.

## Reference Demonstration

Semantic Review shall use an external story fixture equivalent in capability to
`wiigelec/sw-test-story` branch `fs003-reference-fixture`.

The fixture is demonstration evidence only. The Ruleset repository shall not
store, depend on, or reverse-bind to that story-instance Dataset.

The required demonstration shall include:

- an accepted prior Manuscript unit;
- a target scene with viewpoint and reveal/concealment constraints;
- accepted Canon and Plot dependencies;
- production-approved local Prose guidance;
- at least one concealed fact unavailable for disclosure in the target scene;
- a candidate that violates that concealment boundary and is rejected or
  repaired;
- a conforming candidate that is explicitly accepted and persisted; and
- fresh-session reconstruction followed by preparation of the next scene.

## Explicit Deferrals

FS-003 does not require:

- general Canon or Plot authoring workflows;
- automatic scene invention from an unrefined premise;
- generalized repository discovery for arbitrary Dataset layouts;
- multiple concurrent Dataset backends;
- multiple LLM provider integrations;
- automatic semantic acceptance;
- universal automatic continuity detection;
- manuscript-wide editing or export;
- general accepted-upstream revision propagation;
- concurrent-save conflict resolution;
- arbitrary migration chaining or downgrade support;
- generalized search/indexing;
- generated author views from DP-190; or
- the full artifact split/merge/supersession lifecycle from DP-175.

## Completion Criterion

FS-003 is complete only when the executable workflow, not merely the Ruleset
contracts, performs the required demonstration end to end.
