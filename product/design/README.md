# ADR Story Writer Product Design

This directory contains the normative Product Design for ADR Story Writer.

The Design defines Product meaning, authority boundaries, control semantics, and
constraints that Planning and Build must preserve.

This README is a navigation aid only. It does not create or override Product
semantics. Where this index and a DP appear to differ, the applicable DP governs.

## Product Thesis

ADR Story Writer is a persistent control system for AI-assisted long-form
fiction.

Its architecture addresses two primary risks:

- loss of continuity when model context or chat sessions end; and
- semantic drift when a generative model is asked to make too many consequential
  narrative decisions at once.

The Product therefore externalizes governed story state and progressively
reduces broad author intent into bounded generation work.

The top-level control loop is defined by DP-100:

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

## Semantic Surfaces

The principal story-semantic direction is:

    Canon
      ↓
    Plot
      ↓
    Prose
      ↓
    Manuscript

These are semantic ownership boundaries, not mandatory storage partitions.

Production-control artifacts, validation results, metadata, indexes, and
generated author views may support this flow without becoming additional story
authority surfaces.

## Design Map

### DP-100 — Story Writer Product Architecture

Defines the Product problem, architectural invariants, semantic surfaces,
control loop, bounded-generation principle, context projection, runtime roles,
and Product-level simplicity boundary.

Start here.

### DP-110 — Story State, Authority, Acceptance, and Reconciliation

Defines authority classes and intentional authority transitions.

Covers conversational, working, candidate, accepted semantic, and accepted
Manuscript state; semantic acceptance; production approval; Manuscript
acceptance; acceptance scope and closure; consequential invention; and
failure-safe authority interpretation.

### DP-120 — Workflow, Refinement, Dependency, and Reconciliation

Defines progressive top-down refinement, generation readiness, material
dependency, dependency precision, impact analysis, mechanical propagation
boundaries, reconciliation, and re-refinement after upstream change.

This DP defines how broad intent becomes reliably bounded work without requiring
one fixed artifact hierarchy.

### DP-130 — Canon, Plot, Viewpoint, and Reader Information

Defines the Canon/Plot boundary.

Canon owns story-world truth and epistemic state. Plot owns intentional dramatic
presentation, information access, focalization, reveal and concealment, and
reader-information intent.

### DP-140 — Canon State, Events, Knowledge, and Narrative Time

Defines Canon state and occurrence semantics.

Covers Events, constitutive effects, downstream consequences, objective truth,
knowledge and belief, unresolved truth, chronology, temporal precision, and the
relationship between state and occurrence.

### DP-150 — Prose Control and Generation Packages

Defines controlled realization of Plot into prose.

Covers persistent Prose guidance, Beats, Modes, pseudo-prose and near-prose,
production contracts, generation packages, minimum-sufficient context,
information-access safety, creative allowance, protected material, package
freezing, bounded generation, candidate prose, validation before acceptance, and
local regeneration.

### DP-160 — Dataset Persistence and Session Reconstruction

Defines the Dataset as durable story memory.

Covers persistence classes, fresh-session reconstruction, task-specific
retrieval, candidate and production-control continuity, save authorization and
coherence, autosave, concurrency, recovery, and the separation of durability from
authority.

### DP-170 — Schema Evolution, Ruleset Compatibility, Migration, and Rebinding

Defines safe Product evolution across Dataset and Ruleset versions.

Covers schema identity, Ruleset identity, binding, structural versus semantic
compatibility, operation-scoped compatibility, migration, rebinding, downgrade,
lossy transformation, partial recovery, and meaning-preserving evolution.

### DP-175 — Artifact Identity, Semantic Scope, and Cross-Layer Traceability

Defines stable identity and semantic targeting where durable governed operations
require them.

Covers identity granularity, semantic scope, revision versus replacement,
split/merge/supersession/retirement, material relationships, generation
attribution, Manuscript mappings, migration mapping, stale references, and
traceability simplicity boundaries.

### DP-180 — Validation, Semantic Review, and Integrity

Defines the distinction between mechanical validation and semantic review.

Covers review scope and context, generation-readiness and package validation,
generated-prose review, consequential-invention detection, viewpoint and reveal
integrity, conforming/non-conforming/indeterminate outcomes, freshness, repair
boundaries, blocking gates, and the separation of validation from acceptance.

### DP-190 — Generated Author Views, Metadata, Extensibility, and Simplicity Boundaries

Defines author-facing projections and extensibility without shadow authority.

Covers dossiers and other generated views, metadata, edit-through-view
semantics, view freshness, summaries, diagnostic inference, forward
extensibility, unknown fields, human readability, progressive disclosure,
portability, and architecture-wide simplicity constraints.

## Reading Paths

For the shortest architectural path, read:

1. DP-100
2. DP-110
3. DP-120
4. DP-150
5. DP-160
6. DP-180
7. DP-190

For story-semantic modeling, add DP-130 and DP-140.

For persistence evolution and durable cross-layer targeting, add DP-170 and
DP-175.

The full normative corpus is DP-100 through DP-190.

## Authority and Supporting Structure

A useful corpus-wide distinction is:

- **Story-semantic authority:** Canon, Plot, Prose, and Manuscript.
- **Production control:** refinement artifacts, production contracts, generation
  packages, and generated candidates.
- **Operational and durability support:** Dataset persistence, identity,
  migration, validation evidence, generated views, metadata, indexes, and
  compatibility machinery.

Supporting structure may constrain an operation or preserve continuity without
becoming a competing source of story truth.

## Planning Boundary

Product Design defines meaning and required behavior.

Planning chooses schemas, file layouts, identifiers, commands, workflows,
validators, prompts, storage mechanisms, indexes, UI realization, migration
mechanics, and other implementation structure consistent with that meaning.

Implementation convenience does not override Product Design.
