---
functional_set: FS-002
artifact: normative-specification
title: Ruleset-Dataset Compatibility, Migration, and Rebinding Requirements
---

# FS-002 — Normative Requirements

Evaluation classifications:

- **M** — mechanical
- **S** — semantic
- **B** — both mechanical and semantic

All FS-002 requirements are inactive during Planning and become active when
FS-002 enters Build.

## Requirements

### FS-002-NR-001 — Exact Design Binding
**Classification: M**
**State: Inactive**
The FS-002 scope and Plan shall identify the exact consumed Product Design revision.

### FS-002-NR-002 — Distinct Compatibility Axes
**Classification: M**
**State: Inactive**
The Product shall represent Dataset schema identity and Ruleset identity as distinct compatibility axes and shall not collapse them into one version or binding value.

### FS-002-NR-003 — Dataset Schema Identity
**Classification: B**
**State: Inactive**
A persisted Dataset shall identify its structural schema realization sufficiently for the Product to determine whether authority classes, semantic ownership, dependencies, stable identities, ordering, provenance, production-control state, candidate state, accepted Manuscript state, and other required persisted meanings can be interpreted safely.

### FS-002-NR-004 — Ruleset Binding Identity
**Classification: B**
**State: Inactive**
A Dataset shall identify the Ruleset realization applicable to ordinary governed operation sufficiently to determine whether the supplied Ruleset is the expected realization or is otherwise known to be compatible.

### FS-002-NR-005 — Governed Compatibility Determination
**Classification: B**
**State: Inactive**
Compatibility shall be an explicit governed determination and shall not be inferred solely from filenames, version ordering, semantic-version syntax, parser success, field presence, or apparent partial operation.

### FS-002-NR-006 — Compatibility Classification and Scope
**Classification: B**
**State: Inactive**
The Product shall distinguish directly compatible, restricted-operation, migration-required, rebinding-required, unsupported, and indeterminate compatibility states, or an equivalent unambiguous vocabulary, and shall associate compatibility with the governed operations it permits.

### FS-002-NR-007 — Ordinary-operation Gate
**Classification: B**
**State: Inactive**
Before ordinary governed operation, the Product shall establish sufficient Dataset-schema and Ruleset compatibility for the requested operation; when compatibility cannot be established, ordinary operation shall not proceed by guessing.

### FS-002-NR-008 — Explicit Supported Migration
**Classification: B**
**State: Inactive**
Migration shall be an explicit governed transition between identified supported persisted realizations and shall not be implied by ordinary load, save, parsing, or Ruleset selection.

### FS-002-NR-009 — Meaning-preserving Migration
**Classification: B**
**State: Inactive**
A migration represented as meaning-preserving shall preserve, as applicable, semantic content, authority class, owning semantic surface, accepted scope, candidate status, production approval, stable identity, ordering, material dependencies, generation provenance, temporal meaning, ambiguity or unknown state, and author-declared constraints.

### FS-002-NR-010 — No Silent Authority Change
**Classification: B**
**State: Inactive**
Migration shall not silently accept candidates, demote accepted state, convert production approval into semantic acceptance, promote derived material into authority, change semantic ownership, change Manuscript acceptance, widen creative allowance, alter protected-material semantics, or erase material dependency or provenance information.

### FS-002-NR-011 — Author-decision Boundary
**Classification: B**
**State: Inactive**
When a migration requires a materially consequential semantic choice that cannot be preserved mechanically, the Product shall surface the unresolved decision and shall not invent an answer merely to complete the transition.

### FS-002-NR-012 — Candidate and Accepted-state Preservation
**Classification: B**
**State: Inactive**
Meaning-preserving migration shall carry accepted meaning forward without requiring re-acceptance solely because representation changed, while persisted candidate state and material candidate dependencies shall remain candidate unless separately accepted.

### FS-002-NR-013 — Migration Atomicity
**Classification: B**
**State: Inactive**
A migration shall produce one coherent target Dataset state or fail without presenting a partial or mixed source/target realization as successfully migrated or safe for ordinary governed operation.

### FS-002-NR-014 — Transition Provenance
**Classification: M**
**State: Inactive**
A completed migration or rebinding transition shall preserve enough explicit provenance to identify the source realization, target realization, transition operation or path, material unresolved decisions or losses, and whether semantic author decisions were required.

### FS-002-NR-015 — Explicit Rebinding
**Classification: B**
**State: Inactive**
Changing the Ruleset realization applicable to a Dataset shall require explicit rebinding authorization after compatibility for the target Ruleset has been established, including any required migration or review.

### FS-002-NR-016 — Rebinding Does Not Change Story Authority
**Classification: B**
**State: Inactive**
Rebinding alone shall not accept or reject story meaning, change authority classes, change Manuscript acceptance, alter production approval, authorize semantic revision, or imply that required structural migration succeeded.

### FS-002-NR-017 — Coherent Transition Persistence
**Classification: B**
**State: Inactive**
A successful migration or rebinding shall persist one coherent Dataset state containing enough schema identity, Ruleset binding, transition provenance, authority classification, material dependency state, and unresolved-decision state for later governed interpretation.

### FS-002-NR-018 — Fresh-session Post-transition Reconstruction
**Classification: B**
**State: Inactive**
After a successful migration or rebinding, a fresh session shall reconstruct the resulting governed Dataset state and determine its applicable schema identity, Ruleset binding, preserved authority and dependencies, and unresolved compatibility decisions without prior conversation or private model memory.

### FS-002-NR-019 — Unsupported or Indeterminate Safe Failure
**Classification: B**
**State: Inactive**
When Dataset schema identity, Ruleset identity, or required compatibility cannot be established reliably, the Product shall restrict, inspect, recover, migrate, rebind, or refuse as explicitly authorized and shall not invent a schema mapping or semantic interpretation.

### FS-002-NR-020 — Mechanical Validation Boundary
**Classification: S**
**State: Inactive**
Mechanical validation may establish structure, references, required fields, schema conformance, and mechanically decidable compatibility properties, but mechanical success shall not claim semantic equivalence, semantic acceptance, or authorization of consequential semantic change.

### FS-002-NR-021 — Requirement Evaluation Bindings
**Classification: M**
**State: Inactive**
Every active M requirement and mechanically decidable portion of each B requirement shall have at least one exact Product Validation-task binding before Acceptance.

### FS-002-NR-022 — Required Demonstration
**Classification: S**
**State: Inactive**
Semantic Review shall verify both a supported transition that preserves governed meaning and permits the authorized operation after migration or rebinding, and an incompatible or semantically indeterminate transition that is refused or restricted without silent authority change or invented meaning.

### FS-002-NR-023 — Dataset Boundary
**Classification: B**
**State: Inactive**
Story-instance Dataset state shall remain external to this Ruleset repository; Ruleset-owned compatibility definitions may describe Dataset interpretation and transition semantics but shall not become reverse bindings to particular story-instance Datasets.
