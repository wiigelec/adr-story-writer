---
functional_set: FS-006
artifact: normative-specification
title: Governed Editable Generated Author Views Requirements
---

# FS-006 — Normative Requirements

Evaluation classifications:

- **M** — mechanical
- **S** — semantic
- **B** — both mechanical and semantic

## Requirements

### FS-006-NR-001 — Exact Design Binding
**Classification: M**
The FS-006 scope and Plan shall identify the exact consumed Product Design
revision.

### FS-006-NR-002 — Compatibility Gate
**Classification: B**
Ordinary FS-006 generated-view and edit-through operations shall require
compatibility established under FS-002.

### FS-006-NR-003 — Derived View Authority
**Classification: B**
A generated Character dossier or other FS-006 view shall remain derived and shall
not become Canon, Plot, Prose, production, or Manuscript authority merely because
it is rendered, persisted, edited, or reused.

### FS-006-NR-004 — Source Attribution
**Classification: B**
A generated view shall retain sufficient source identity, semantic ownership, and
source revision attribution for materially projected governed content to support
freshness evaluation and safe edit targeting.

### FS-006-NR-005 — Character Dossier Projection
**Classification: B**
The Product shall provide a Character dossier projection that can combine
author-useful governed Character information and relevant cross-surface context
without collapsing the ownership of those sources.

### FS-006-NR-006 — Authority/status Distinction
**Classification: B**
Where a view combines accepted, candidate, production, generated, unresolved, or
other materially distinct states, it shall preserve enough distinction to avoid
presenting them as one authority class.

### FS-006-NR-007 — View Regeneration
**Classification: B**
The Product shall be able to regenerate a generated view from current governed
sources without changing those sources or their authority.

### FS-006-NR-008 — Material Freshness Detection
**Classification: B**
A material revision to a projected governed source shall cause the affected prior
view or affected region to be recognized as stale for governed edit use.

### FS-006-NR-009 — No False Currentness
**Classification: S**
A materially stale generated view shall not be represented to the author as
current when that representation could mislead governed authoring.

### FS-006-NR-010 — Presentation Metadata Separation
**Classification: B**
Presentation-only preferences may be persisted independently, but shall not alter
governed story meaning or be interpreted as story-semantic edits.

### FS-006-NR-011 — Edit Is Proposal
**Classification: S**
Editing a generated view shall be interpreted as a proposal against underlying
governed targets and shall not itself constitute semantic acceptance, production
approval, Manuscript acceptance, or direct mutation of accepted story meaning.

### FS-006-NR-012 — Unambiguous Edit Routing
**Classification: B**
When a consequential generated-view edit maps unambiguously to a governed target,
the Product shall route it through the existing candidate or accepted-revision
operation appropriate to that target's owning surface.

### FS-006-NR-013 — Stale Edit Protection
**Classification: B**
A consequential edit based on a materially stale view shall not be applied as
though it targeted unchanged current source state.

### FS-006-NR-014 — Ambiguous Edit Protection
**Classification: B**
When a consequential generated-view edit does not map unambiguously to governed
target meaning, the Product shall preserve or surface the ambiguity and shall not
silently select a target or interpretation.

### FS-006-NR-015 — Coordinated Edit Ownership
**Classification: B**
When one human-facing edit implies multiple governed changes, the Product shall
preserve the distinct owning surfaces, targets, and acceptance scopes of those
changes rather than collapsing them into one view-owned mutation.

### FS-006-NR-016 — Comparison Is Derived
**Classification: B**
A comparison between prior, current, or proposed generated views shall remain
derived workflow evidence and shall not by itself create or accept story meaning.

### FS-006-NR-017 — Optional View Persistence
**Classification: B**
If a generated view or retained snapshot is persisted, it shall retain derived
classification and sufficient source attribution to determine whether it remains
current or stale.

### FS-006-NR-018 — Fresh-session Reconstruction
**Classification: B**
Persisted FS-006 view state that is required for continued workflow shall be
reconstructable in a fresh compatible session without relying on prior
conversation or private model memory.

### FS-006-NR-019 — Existing Governance Reuse
**Classification: B**
FS-006 shall reuse existing FS-004 revision/reconciliation and FS-005
candidate/acceptance semantics rather than introducing a second authority or
acceptance mechanism for generated-view edits.

### FS-006-NR-020 — No Silent Consequential Invention
**Classification: S**
The Product shall not invent missing consequential story meaning merely to
complete a dossier, resolve an ambiguous edit, or make a view structurally
uniform.

### FS-006-NR-021 — End-to-end Editable-view Demonstration
**Classification: S**
Semantic Review shall demonstrate dossier construction, source attribution,
staleness after a material source change, regeneration, one unambiguous governed
edit-through operation, one ambiguous-edit refusal, and one presentation-only
preference that does not alter story meaning.

### FS-006-NR-022 — Requirement Evaluation Bindings
**Classification: M**
Every active M requirement and mechanically decidable portion of each active B
requirement shall have at least one exact Product Validation-task binding, and
semantic-only requirements shall not be mechanically claimed.

### FS-006-NR-023 — Dataset Boundary
**Classification: B**
Story-instance Dataset state and external reference fixtures shall remain outside
this Ruleset repository.
