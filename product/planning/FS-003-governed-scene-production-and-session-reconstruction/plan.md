---
functional_set: FS-003
artifact: plan
title: Governed Scene Production, Persistence, and Session Reconstruction Plan
design_revision: 58ebbd0c90060c1fce9da6ac4e18835032ed2336
---

# FS-003 — Plan

## Objective

Build the smallest executable runtime that proves the accepted Story Writer
contracts can govern one real scene across process/session boundaries.

The implementation shall reuse FS-001 authority, production, review, and
persistence semantics and FS-002 compatibility behavior. It shall not create a
second authority model, a second compatibility model, or a parallel workflow
vocabulary.

## Runtime Entry Point

Provide one explicit runtime surface capable of operating on an external Dataset
for a requested target scene.

The runtime may be exposed initially as Python API and/or a narrow CLI. The
interface shall make the following operations independently observable:

1. load/reconstruct;
2. compatibility determination;
3. target-scene retrieval;
4. production-contract construction;
5. generation-package construction/freezing;
6. candidate registration or generation;
7. semantic review;
8. acceptance or rejection;
9. persistence; and
10. fresh-session reconstruction.

The exact module decomposition is a Build choice. Prefer a small cohesive runtime
over a generalized orchestration framework.

## Dataset Reconstruction

Implement a Dataset adapter sufficient for the accepted tree-backed story
realization used by the reference fixture.

The adapter shall reconstruct one logical Dataset from persisted runtime
material without treating conversation state, `init-config/`, construction
provenance, or repository metadata as story-semantic authority.

Where a physical realization mapping is required to locate Dataset material, the
mapping may be used operationally but shall not become semantic authority.

Reconstruction shall preserve at least:

- artifact identity;
- authority class;
- revision identity;
- material dependencies;
- production approval;
- generation provenance when present;
- accepted Manuscript state; and
- unresolved candidate/reconciliation state when present.

## Compatibility Gate

Before ordinary scene production, pass the reconstructed Dataset through the
accepted FS-002 compatibility contract.

The runtime shall support the already-implemented compatibility classifications
and shall not bypass migration/rebinding requirements merely because the target
scene can otherwise be parsed.

A supported transition may be executed only through the existing explicit
authorization path. Indeterminate or unsupported state shall not proceed as
ordinary scene production.

## Scene Retrieval

Given a target Plot scene identity, resolve the minimum sufficient governed
context required to produce that scene.

The projection shall include, as applicable:

- target Plot scope and revision;
- entry and exit conditions;
- narrative movement or local realization units;
- viewpoint identity and accessible knowledge;
- reader reveal/concealment constraints;
- accepted Canon dependencies;
- candidate dependencies;
- applicable Prose guidance;
- protected material;
- creative allowance;
- prohibited consequential invention;
- accepted prior Manuscript context required for continuity; and
- current target Manuscript state, if any.

Missing or ambiguous material required to bound the scene shall prevent
generation readiness rather than be guessed.

## Production Contract

Construct a concrete production-contract value from the reconstructed scene
projection using the capability vocabulary already defined by
`ruleset/production.json`.

The contract shall identify the target and stopping boundary and shall preserve
the distinction between generator-visible context and reviewer-only constraints
when disclosure of a hidden fact would itself violate the scene.

The contract is reusable control state for the bounded scene task. It is not
accepted story meaning.

## Generation Package

Construct a task-specific generation package from the production contract and
selected governed revisions.

The package shall:

- have stable identity;
- identify the contract and target scope;
- identify selected revisions;
- contain the exact generator-visible projection;
- retain reviewer-only constraints separately when required;
- record creative allowance and prohibited invention;
- have an explicit stopping boundary; and
- become stable once used for a generation attempt.

FS-003 may use an injected generator callback/adapter or externally supplied
candidate text. A provider-specific network integration is not required.

## Candidate Manuscript

Every generated or supplied scene attempt enters the runtime as
`candidate_manuscript`.

Candidate creation shall record enough provenance to identify the generation
package and attempt that governed it.

Generation alone shall not change Canon, Plot, Prose approval, accepted
Manuscript state, or persistence authorization.

## Semantic Review

Provide an executable review operation that evaluates a candidate against the
frozen package and reviewer constraints.

The runtime shall represent the accepted FS-001 outcomes:

- `conforming`;
- `non_conforming`; and
- `indeterminate`.

FS-003 does not require a universally autonomous literary critic. The review
operation may consume structured reviewer findings supplied by an agent or human,
but the runtime must enforce their governed consequences.

For the reference demonstration, review shall detect or receive evidence that a
candidate disclosed a fact marked concealed for the target scene. That candidate
must remain candidate and must not alter upstream authority.

## Repair Path

Support at least one local repair/regeneration path.

A rejected candidate may be replaced by a new candidate governed by the same
production contract and an appropriate stable package/attempt record.

If repair instead requires consequential upstream semantic change, that change
must remain outside ordinary Manuscript acceptance until handled at its owning
surface.

## Acceptance

A conforming candidate may be explicitly accepted as an identifiable Manuscript
scope only when applicable acceptance-closure requirements are satisfied.

Acceptance shall:

- preserve the distinction between Manuscript acceptance and semantic
  acceptance;
- identify the accepted candidate/revision;
- not silently promote unresolved candidate dependencies; and
- not itself imply that persistence has occurred.

## Persistence

Provide coherent Dataset persistence sufficient for the reference realization.

One authorized save shall either persist the logically coherent resulting
Dataset state or fail without reporting success.

Existing FS-002 atomic-save behavior should be reused where applicable rather
than introducing a competing persistence primitive.

Non-Dataset repository material shall remain untouched by an ordinary Dataset
save.

## Fresh-session Continuation

The required test shall destroy all in-memory runtime/session state after
persistence.

A newly constructed runtime shall then:

1. load the persisted Dataset;
2. establish compatibility;
3. reconstruct the accepted target scene as accepted Manuscript;
4. reconstruct its governing authority and provenance sufficiently for later
   interpretation; and
5. retrieve the following planned scene and construct enough context to begin its
   production workflow.

No prior conversation, process memory, or hidden model memory may be required.

## Validation Strategy

Build shall extend Product Validation with deterministic tasks for mechanically
decidable FS-003 behavior, including:

- exact FS-003 Planning/Design binding;
- Dataset reconstruction and external-Dataset boundary;
- compatibility gating before ordinary scene work;
- target-scene dependency projection;
- production-contract construction;
- stable generation-package identity/provenance;
- candidate-only generation state;
- review-outcome enforcement;
- refusal of acceptance for non-conforming/indeterminate candidates;
- explicit Manuscript acceptance;
- coherent persistence; and
- fresh-process/session reconstruction.

Behavioral tests should use temporary Dataset copies so validation never mutates
the reference repository.

## Semantic Review Demonstration

Semantic Review shall execute the complete workflow against the external Red
Hollow reference fixture or an equivalent exported snapshot.

At minimum:

1. reconstruct the fixture;
2. perform any required supported FS-002 transition;
3. select `scene-002-signal-shed`;
4. construct its production contract;
5. freeze a generation package;
6. register/generate a candidate that improperly reveals the concealed dispatch
   satchel;
7. classify that attempt non-conforming and preserve upstream authority;
8. register/generate a corrected candidate;
9. review it as conforming;
10. explicitly accept it as Manuscript;
11. persist the Dataset;
12. discard session state;
13. reconstruct in a fresh runtime; and
14. prepare `scene-003-first-message` from persisted governed state.

The fixture identity and branch are evidence inputs, not Product authority.

## Build Boundary

Do not introduce:

- a general workflow engine;
- a generalized object database;
- hidden automatic semantic repair;
- provider-specific LLM coupling in core governed-state code;
- automatic acceptance;
- story-instance data in this repository; or
- author-facing governance ceremony beyond what is needed to make the state
  transitions explicit and safe.

Prefer direct data structures, explicit functions, and scenario tests until the
vertical slice proves a need for additional abstraction.
