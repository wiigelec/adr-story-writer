---
functional_set: FS-007
artifact: normative-specification
title: Governed Prose Style Guidance and Generation Quality Requirements
---

# FS-007 — Normative Requirements

Evaluation classifications:

- **M** — mechanical
- **S** — semantic
- **B** — both mechanical and semantic

## Requirements

### FS-007-NR-001 — Exact Design Binding
**Classification: M**
The FS-007 scope and Plan shall identify the exact consumed Product Design
revision.

### FS-007-NR-002 — Persistent Style Profile State
**Classification: B**
The Product shall support persistent author-style profile state owned by Prose
production control and distinct from Canon, Plot, and Manuscript authority.

### FS-007-NR-003 — Sample Provenance
**Classification: B**
A derived style profile shall retain bounded provenance identifying its source
samples or source references sufficiently for later review without requiring the
source prose itself to be persisted as generation guidance.

### FS-007-NR-004 — Sample Normalization
**Classification: S**
Style analysis shall seek stable authorial realization tendencies and shall not
deliberately encode obvious spelling mistakes, grammatical accidents, isolated
drafting defects, or story-specific facts as desired style merely because they
appear in a sample.

### FS-007-NR-005 — Explicit Profile Approval
**Classification: B**
A newly derived or revised author-style profile shall remain a production
candidate until an explicit approval operation makes that revision
production-approved guidance.

### FS-007-NR-006 — General Generation-quality Guidance
**Classification: B**
The Ruleset shall provide general prose-generation quality guidance applicable
even when no author-specific style profile exists.

### FS-007-NR-007 — Common Model-pattern Restraint
**Classification: B**
General generation-quality guidance shall address common model-generation
defaults including redundant interpretation/restatement, patterned
constructions, excessive micro-reactions, generic filler description,
mechanically polished dialogue, and unjustified stylistic ornament without
categorically banning legitimate literary devices.

### FS-007-NR-008 — Guidance Layer Separation
**Classification: B**
General generation-quality guidance, accepted author-style guidance, and local
scene/mode guidance shall remain distinguishable in resolved generation control.

### FS-007-NR-009 — Resolved Style Projection
**Classification: B**
A scene generation operation shall resolve the applicable guidance layers into a
bounded structured style projection with explicit readiness state.

### FS-007-NR-010 — Production Contract Integration
**Classification: B**
The scene production contract shall include a ready resolved style projection,
and its identity shall materially reflect that projection.

### FS-007-NR-011 — Generation Package Integration
**Classification: B**
The generation package shall freeze the ready resolved style projection and
identify the selected author-style profile revision when one applies.

### FS-007-NR-012 — No Routine Raw-sample Injection
**Classification: B**
Ordinary generation packages shall use derived guidance and bounded provenance;
they shall not require or automatically embed the full author prose samples from
which a profile was derived.

### FS-007-NR-013 — Absent Profile Is Valid
**Classification: B**
An otherwise compatible Dataset with no FS-007 style profile shall remain valid
for generation and shall receive general generation-quality guidance with no
invented author profile.

### FS-007-NR-014 — Dataset Schema Continuity
**Classification: B**
FS-007 shall retain Dataset schema version 1 and shall not require Dataset
migration solely to represent optional style-profile state.

### FS-007-NR-015 — Ruleset Rebinding
**Classification: B**
A compatible schema-v1 Dataset bound to Ruleset `0.3.0` shall have an explicit
meaning-preserving rebinding path to Ruleset `0.4.0` rather than being classified
migration-required.

### FS-007-NR-016 — Authority Boundary
**Classification: S**
Author samples, extracted style profiles, generation-quality guidance, and
resolved style projections shall not acquire Canon, Plot, or Manuscript
authority merely through analysis, persistence, selection, or generation use.

### FS-007-NR-017 — Fresh-session Reconstruction
**Classification: B**
Persisted author-style profile and selection state required for continued
generation shall reconstruct in a fresh compatible session without reliance on
prior conversation or private model memory.

### FS-007-NR-018 — Material Conflict Safety
**Classification: B**
When the author or Semantic Review identifies a material semantic conflict among
applicable guidance, the Product shall preserve that conflict as explicit
unresolved control state and shall refuse generation-ready production-contract
construction until it is resolved. Determining whether arbitrary guidance is
materially conflicting remains a semantic evaluation.

### FS-007-NR-019 — End-to-end Style Demonstration
**Classification: S**
Semantic Review shall demonstrate author-sample analysis, candidate profile
review, explicit approval and revision, baseline quality guidance, local
guidance layering, conflict identification/refusal, generation-package
projection, and prose generation that uses the guidance without treating source
samples as story authority.

### FS-007-NR-020 — Requirement Evaluation Bindings
**Classification: M**
Every active M requirement and mechanically decidable portion of each active B
requirement shall have at least one exact Product Validation-task binding, and
semantic-only requirements shall not be mechanically claimed.

### FS-007-NR-021 — Dataset Boundary
**Classification: B**
Story-instance Dataset state and author sample fixtures shall remain outside this
Ruleset repository.

### FS-007-NR-022 — Stable Profile Revision
**Classification: B**
An approved author-style profile shall be revisable under the same stable profile
identity into a distinct production-candidate content revision that records the
immediately superseded revision and requires explicit production approval before
governing new generation. Previously frozen generation packages shall remain
unchanged.
