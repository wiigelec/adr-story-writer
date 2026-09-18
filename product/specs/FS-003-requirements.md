---
functional_set: FS-003
artifact: normative-specification
title: Governed Scene Production, Persistence, and Session Reconstruction Requirements
---

# FS-003 — Normative Requirements

Evaluation classifications:

- **M** — mechanical
- **S** — semantic
- **B** — both mechanical and semantic

FS-003 requirements are active for Build, Validation, Semantic Review, and Acceptance.

## Requirements

### FS-003-NR-001 — Exact Design Binding
**Classification: M**
The FS-003 scope and Plan shall identify the exact consumed Product Design revision.

### FS-003-NR-002 — External Dataset Reconstruction
**Classification: B**
The Product shall reconstruct governed working state for the requested scene from an external persisted Dataset and applicable Ruleset without requiring prior conversation or private model memory and without treating construction metadata as story-semantic authority.

### FS-003-NR-003 — Compatibility Gate Before Scene Work
**Classification: B**
Before ordinary FS-003 scene production, the Product shall establish compatibility for the requested operation using the accepted FS-002 compatibility semantics and shall not bypass a required migration, rebinding, restriction, or indeterminate result merely because scene material can be parsed.

### FS-003-NR-004 — Target-scene Resolution
**Classification: B**
Given an identifiable planned scene, the Product shall resolve the governing Plot scope and enough applicable Canon, Prose, Manuscript, dependency, viewpoint, and reader-information state to determine whether the scene is generation-ready.

### FS-003-NR-005 — Minimum-sufficient Context Projection
**Classification: B**
The Product shall construct a bounded context projection sufficient for the target scene while excluding unrelated story material and preserving any generator-visible versus reviewer-only information distinction required for information-access safety.

### FS-003-NR-006 — Missing-context Safe Failure
**Classification: B**
When missing, stale, ambiguous, or unresolved governed state is material to bounding the target scene, the Product shall return an unresolved or not-ready result rather than synthesize the missing consequential meaning.

### FS-003-NR-007 — Executable Production Contract
**Classification: B**
The Product shall construct a concrete production contract for the target scene using the accepted FS-001 production capabilities, including explicit target scope, stopping boundary, narrative movement or local realization units, applicable information constraints, Prose guidance, protected material, creative allowance, prohibited consequential invention, and material dependencies.

### FS-003-NR-008 — Stable Generation Package
**Classification: B**
Each generation attempt shall use an identifiable task-specific generation package derived from the production contract and selected governed revisions, and the package representation governing an attempt shall remain stable after use.

### FS-003-NR-009 — Information-access Safety in Execution
**Classification: B**
A hidden Canon fact may constrain generation or review without thereby becoming generator-visible or authorized for disclosure in the produced scene.

### FS-003-NR-010 — Candidate-only Scene Attempts
**Classification: B**
Generated or externally supplied scene prose shall enter governed state as candidate Manuscript associated with its generation-package provenance and shall not by creation alone alter accepted Canon, Plot, Prose approval, accepted Manuscript, or persistence authorization.

### FS-003-NR-011 — Executable Review Outcomes
**Classification: B**
The runtime shall represent and enforce conforming, non-conforming, and indeterminate review outcomes for a candidate scene, or an equivalent unambiguous vocabulary preserving those meanings.

### FS-003-NR-012 — Non-conforming Candidate Containment
**Classification: B**
A candidate found to violate reveal/concealment, viewpoint, protected-material, consequential-invention, stopping-boundary, or other material governing constraints shall remain candidate and shall not silently modify upstream semantic authority.

### FS-003-NR-013 — Local Repair or Replacement
**Classification: B**
The Product shall permit a rejected scene candidate to be locally repaired or replaced under governed production context while preserving the history or provenance necessary to distinguish the rejected attempt from the later candidate.

### FS-003-NR-014 — Manuscript Acceptance Gate
**Classification: B**
Only a candidate with a conforming review result and satisfied acceptance-closure requirements may be accepted as the target Manuscript scope through the ordinary FS-003 path; non-conforming or materially indeterminate candidates shall not be accepted by that path.

### FS-003-NR-015 — Acceptance Does Not Imply Persistence
**Classification: M**
Manuscript acceptance and Dataset persistence shall remain distinct operations, and acceptance alone shall not be reported as a successful save.

### FS-003-NR-016 — Coherent Dataset Persistence
**Classification: B**
An authorized FS-003 save shall persist one coherent Dataset state preserving applicable authority classes, accepted Manuscript identity, material dependencies, and required generation/review provenance, or shall fail without reporting a partial state as successfully saved.

### FS-003-NR-017 — Fresh-session Reconstruction
**Classification: B**
After successful persistence, a new runtime with no prior session state shall reconstruct the accepted scene and enough governing state to interpret it correctly and continue with the next planned scene.

### FS-003-NR-018 — Reference Semantic Failure Demonstration
**Classification: S**
Semantic Review shall demonstrate at least one target-scene candidate that improperly discloses a concealed fact or otherwise violates a material information boundary, verify that the candidate is rejected or repaired without silent upstream authority change, and then demonstrate acceptance of a conforming replacement.

### FS-003-NR-019 — Reference End-to-end Continuation Demonstration
**Classification: S**
Semantic Review shall demonstrate reconstruction, compatibility handling, target retrieval, production-contract creation, stable generation packaging, candidate creation, semantic review, explicit Manuscript acceptance, coherent persistence, session destruction, fresh-session reconstruction, and preparation of the next planned scene.

### FS-003-NR-020 — Requirement Evaluation Bindings
**Classification: M**
Before FS-003 Acceptance, every active M requirement and mechanically decidable portion of each active B requirement shall have at least one exact Product Validation-task binding.

### FS-003-NR-021 — Dataset Boundary
**Classification: B**
Story-instance Dataset state and the external reference fixture shall remain outside this Ruleset repository; Product code and Ruleset contracts may interpret or test exported copies of Dataset state but shall not create a reverse binding to a particular story instance.
