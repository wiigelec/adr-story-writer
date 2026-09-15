---
functional_set: FS-001
artifact: normative-specification
title: Governed Prose Production and Acceptance Requirements
---

# FS-001 — Normative Requirements

Evaluation classifications:

- **M** — mechanical
- **S** — semantic
- **B** — both mechanical and semantic

## Requirements

### FS-001-NR-001 — Exact Design Binding
**Classification: M**
The FS-001 scope and Plan shall identify the exact consumed Product Design revision.

### FS-001-NR-002 — Fresh-session Reconstruction
**Classification: B**
The Product shall reconstruct enough governed state from the Dataset and applicable Ruleset to continue requested story work without prior conversation or private model memory while preserving authority classifications and material unresolved dependencies.

### FS-001-NR-003 — Governed Identity
**Classification: M**
Every persisted governed artifact or durable semantic scope used by FS-001 shall be identifiable sufficiently to support acceptance, dependency tracking, revision, provenance, and later reconstruction.

### FS-001-NR-004 — Authority Classification
**Classification: B**
The Product shall distinguish accepted semantic, candidate semantic, production candidate, production approved, candidate Manuscript, and accepted Manuscript state. Persistence shall not itself change authority classification.

### FS-001-NR-005 — Candidate Dependency Preservation
**Classification: B**
Material unresolved candidate dependencies shall remain identifiable through review, acceptance, persistence, and later reconstruction.

### FS-001-NR-006 — Lowest-layer Navigation
**Classification: S**
The Product shall resolve work at the lowest semantic layer capable of preserving intended meaning and shall surface consequential upstream change at the owning layer.

### FS-001-NR-007 — Production Contract
**Classification: B**
Before bounded prose generation, the Product shall establish a production contract capable of representing applicable scope, stopping boundary, narrative movement, local realization units, information-access constraints, reveal/concealment obligations, entry/exit conditions, Prose/style guidance, protected material, creative allowance, prohibited invention, and accepted/candidate dependencies.

### FS-001-NR-008 — Generation Readiness
**Classification: S**
If a task cannot be bounded reliably, the Product shall refine it or surface the unresolved decision before generation.

### FS-001-NR-009 — Generation Package
**Classification: B**
Each generation attempt shall consume a task-specific generation package derived from the applicable production contract and governed state with enough revision/scope identity to determine what governed the attempt.

### FS-001-NR-010 — Stable Generation Provenance
**Classification: M**
Once used, a generation package or equivalent provenance record shall preserve a stable representation of the governing execution context.

### FS-001-NR-011 — Information-access Safety
**Classification: B**
Generation shall preserve the distinction between objective Canon and information available to the current viewpoint or reader; hidden Canon used as a constraint shall not thereby become authorized for disclosure.

### FS-001-NR-012 — Candidate-only Generation
**Classification: B**
Generated prose shall begin as candidate state and shall not by generation alone create accepted semantic state, production approval, accepted Manuscript, or persistence authorization.

### FS-001-NR-013 — Generation Boundary
**Classification: B**
Every generation attempt shall have an explicit stopping boundary; overflow remains candidate and is not governed continuation.

### FS-001-NR-014 — Generated-prose Review
**Classification: S**
Before candidate prose is accepted as Manuscript, the Product shall support semantic review against the applicable governing context.

### FS-001-NR-015 — Indeterminate Review
**Classification: B**
When stale, incomplete, or ambiguous governing context could materially alter a review conclusion, the affected criterion shall be unresolved or indeterminate rather than passed by guessing.

### FS-001-NR-016 — Consequential Invention
**Classification: S**
Consequential meaning introduced downstream without governing authority shall remain candidate meaning at its owning semantic surface.

### FS-001-NR-017 — Explicit Acceptance Operations
**Classification: B**
Semantic acceptance, production approval, Manuscript acceptance, revision acceptance, and persistence authorization shall remain distinct operations applied to identifiable scopes.

### FS-001-NR-018 — Acceptance Closure
**Classification: B**
A downstream candidate shall not be accepted in a way that silently promotes materially required unresolved consequential meaning.

### FS-001-NR-019 — Coherent Persistence
**Classification: B**
Authorized persistence shall preserve authority classification, material dependencies, and required generation provenance; persisted candidates remain candidates and failed/partial saves are not successful logical saves.

### FS-001-NR-020 — Fresh-session Continuation
**Classification: B**
Persisted FS-001 state shall contain enough information for a fresh session to interpret accepted and intentionally persisted candidate state without prior-chat memory.

### FS-001-NR-021 — Mechanical Validation Boundary
**Classification: S**
Mechanical validation shall enforce only mechanically decidable structure and explicit invariants and shall not claim semantic acceptance or story-meaning correctness.

### FS-001-NR-022 — Requirement Evaluation Bindings
**Classification: M**
Every active M requirement and mechanically decidable portion of each B requirement shall have at least one exact product Validation-task binding before Acceptance.

### FS-001-NR-023 — Required Demonstration
**Classification: S**
Semantic Review shall verify the complete end-to-end workflow selected by the FS-001 scope.

### FS-001-NR-024 — Dataset Boundary
**Classification: B**
Story-instance Dataset state shall remain external to this Ruleset repository.
