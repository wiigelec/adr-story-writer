---
functional_set: FS-004
artifact: normative-specification
title: Governed Upstream Revision, Impact, and Reconciliation Requirements
---

# FS-004 — Normative Requirements

Evaluation classifications:

- **M** — mechanical
- **S** — semantic
- **B** — both mechanical and semantic

FS-004 requirements are active for Build, Validation, Semantic Review, and Acceptance.

## Requirements

### FS-004-NR-001 — Exact Design Binding
**Classification: M**
The FS-004 scope and Plan shall identify the exact consumed Product Design revision.

### FS-004-NR-002 — External Governed Reconstruction
**Classification: B**
Before ordinary FS-004 revision work, the Product shall reconstruct the applicable accepted and candidate governed state, stable identities, material dependencies, production state, Manuscript state, and unresolved reconciliation state from an external persisted Dataset and applicable compatible Ruleset without relying on prior conversation or private model memory.

### FS-004-NR-003 — Compatibility Gate
**Classification: B**
FS-004 ordinary revision, reconciliation, and persistence operations shall require compatibility established under the accepted FS-002 semantics and shall not bypass required migration, rebinding, restriction, unsupported, or indeterminate states merely because the target artifact can be parsed.

### FS-004-NR-004 — Candidate Upstream Revision
**Classification: B**
The Product shall permit an identifiable Canon or Plot semantic target to receive a candidate revision whose creation or persistence alone does not alter the currently accepted semantic revision or downstream authority.

### FS-004-NR-005 — Revision Scope and Ownership
**Classification: B**
Every upstream semantic revision shall identify its target scope and owning semantic surface sufficiently to distinguish Canon truth revision from Plot presentation revision and shall not silently transfer consequential meaning between semantic surfaces.

### FS-004-NR-006 — Explicit Revision Acceptance
**Classification: B**
An upstream candidate revision shall become accepted only through an explicit semantic or revision acceptance operation at its owning surface and identifiable scope.

### FS-004-NR-007 — Revision Identity
**Classification: B**
When revision preserves the continuing semantic object, acceptance shall preserve that object's stable identity while establishing a distinct current revision and retaining enough prior revision provenance for impact analysis and reconciliation.

### FS-004-NR-008 — Ambiguous Identity Safe Failure
**Classification: B**
When the Product cannot determine without consequential interpretation whether proposed material is revision of an existing semantic object or replacement by a different object, ordinary revision shall not silently choose identity continuity and shall remain unresolved or require an explicit replacement/supersession decision.

### FS-004-NR-009 — No Automatic Downstream Rewrite
**Classification: B**
Accepting an upstream semantic revision shall not by itself rewrite, reaccept, revoke, replace, or otherwise change the semantic content or authority class of dependent Plot, Prose, production-control, or Manuscript artifacts.

### FS-004-NR-010 — Material Dependency Distinction
**Classification: B**
Impact and acceptance decisions shall distinguish current material dependency from historical derivation or incidental relationship, and historical influence alone shall not require a downstream artifact to be treated as materially stale.

### FS-004-NR-011 — Bounded Impact Analysis
**Classification: B**
After an accepted upstream revision, the Product shall identify known downstream relationships whose current meaning or governed role may materially depend on the revised scope and shall not require unrelated governed state to be invalidated merely because it shares story context.

### FS-004-NR-012 — Impact Outcome Semantics
**Classification: B**
For each affected relationship required by the bounded operation, the Product shall represent an unambiguous outcome equivalent to still-valid, review-required or stale, superseded, or unresolved, and shall not classify unresolved semantic equivalence as still-valid merely to permit continued operation.

### FS-004-NR-013 — Staleness Does Not Change Authority
**Classification: B**
Marking an accepted or candidate artifact stale, review-required, or unresolved shall not itself change its authority class, historical acceptance, semantic content, stable identity, or persistence authorization.

### FS-004-NR-014 — Stale Dependency Gate
**Classification: B**
A materially stale or unresolved governing dependency shall not be consumed by ordinary generation, production approval, or downstream acceptance as though it were current.

### FS-004-NR-015 — Reconciliation Targeting
**Classification: B**
A reconciliation operation shall identify both the upstream change being reconciled and the dependent semantic or production scope being resolved.

### FS-004-NR-016 — Deliberate Reconciliation
**Classification: B**
The Product shall permit an affected dependent to be deliberately preserved, revised, replaced or superseded, withdrawn when candidate, narrowed in scope, rebuilt when production-control state, or left unresolved as applicable, without inventing consequential replacement meaning merely to restore consistency.

### FS-004-NR-017 — Preserve-unmodified Path
**Classification: B**
When semantic review establishes that an affected dependent remains materially valid under the new upstream revision, the Product shall permit the dependent to remain current without forcing a meaningless content revision solely to satisfy revision bookkeeping.

### FS-004-NR-018 — Plot Reconciliation Preserves Canon Boundary
**Classification: B**
Reconciliation of affected Plot shall preserve the accepted boundary that Canon owns story-world truth and Plot owns intentional narrative presentation; accepting revised Plot shall not silently create, replace, or accept Canon truth.

### FS-004-NR-019 — Production-control Freshness
**Classification: B**
A production-approved Prose or production-control artifact whose material governing semantic dependencies are no longer current shall not continue to govern ordinary generation until it is reviewed, preserved as still valid, revised, or replaced through reconciliation.

### FS-004-NR-020 — Used Generation-package Immutability
**Classification: M**
A generation package that has governed an attempt shall remain immutable historical provenance and shall not be modified to replace superseded selected revisions or otherwise make the used package appear current.

### FS-004-NR-021 — Stale Generation-package Gate
**Classification: B**
When a material selected governing revision of a used or prepared generation package has changed, that package shall not govern a new ordinary generation attempt; the task shall require current context and a new package before ordinary generation proceeds.

### FS-004-NR-022 — Historical Candidate Preservation
**Classification: B**
A candidate or accepted Manuscript produced under an older generation package shall retain its historical package provenance even when the package can no longer govern new generation.

### FS-004-NR-023 — Manuscript Revision Boundary
**Classification: B**
An accepted upstream semantic revision shall not directly overwrite accepted Manuscript; when accepted text materially requires change, replacement or revised text shall proceed through candidate, applicable review, acceptance-closure, and explicit Manuscript acceptance semantics.

### FS-004-NR-024 — Unaffected Work Preservation
**Classification: B**
Governed downstream state demonstrated not to materially depend on the accepted upstream revision shall remain usable and shall not require regeneration, reacceptance, or artificial revision solely because neighboring or historically related state changed.

### FS-004-NR-025 — Readiness Restoration
**Classification: B**
After reconciliation of the material dependencies required for a target scene, the Product shall be able to determine whether the scene is generation-ready under current governed state and, when ready, construct a new production contract and generation package using current selected revisions.

### FS-004-NR-026 — Missing or Ambiguous Reconciliation Safe Failure
**Classification: B**
When material impact or required replacement meaning cannot be established without a consequential semantic decision, the Product shall preserve an unresolved or not-ready state and shall not synthesize the missing decision to complete reconciliation.

### FS-004-NR-027 — Reconciliation Provenance
**Classification: B**
The Product shall preserve enough provenance to determine the accepted upstream revision, materially affected dependent, reconciliation action or unresolved state, resulting current revision or replacement when any, and relationship to superseded state.

### FS-004-NR-028 — Coherent Persistence
**Classification: B**
An authorized FS-004 save shall persist one coherent Dataset state containing the current accepted upstream revision, applicable prior revision provenance, dependency freshness, reconciliation state, unresolved decisions, current production approval, generation provenance, and accepted Manuscript state, or shall fail without reporting a partial state as successfully saved.

### FS-004-NR-029 — Persistence Conflict Safety
**Classification: M**
A stale FS-004 runtime/session shall not silently overwrite newer persisted Dataset state and shall surface a persistence conflict rather than reporting successful save.

### FS-004-NR-030 — Fresh-session Reconstruction
**Classification: B**
After successful persistence, a new runtime with no prior session state shall reconstruct the accepted upstream revision, current material dependencies, preserved/reconciled/replaced/unresolved downstream state, historical package provenance, accepted Manuscript state, and generation-readiness status sufficiently to continue governed work.

### FS-004-NR-031 — Material-versus-historical Demonstration
**Classification: S**
Semantic Review shall demonstrate one accepted upstream revision with at least one materially dependent downstream scope and one historically related or context-sharing scope that is not materially dependent, and shall verify that the Product requires reconciliation only where warranted.

### FS-004-NR-032 — No-silent-propagation Demonstration
**Classification: S**
Semantic Review shall demonstrate that accepting an upstream revision identifies affected downstream work without automatically rewriting or accepting replacement Plot, Prose, production-control, or Manuscript meaning.

### FS-004-NR-033 — Indeterminate-impact Demonstration
**Classification: S**
Semantic Review shall demonstrate at least one material relationship whose continuing validity cannot be established mechanically and verify that it remains review-required or unresolved rather than being guessed current.

### FS-004-NR-034 — End-to-end Reconciliation Demonstration
**Classification: S**
Semantic Review shall demonstrate reconstruction, candidate upstream revision, explicit revision acceptance, impact analysis, preservation of unaffected work, deliberate reconciliation of affected downstream state, rejection of stale package reuse, readiness restoration, new package construction, coherent persistence, session destruction, and fresh-session reconstruction.

### FS-004-NR-035 — Requirement Evaluation Bindings
**Classification: M**
Before FS-004 Acceptance, every active M requirement and mechanically decidable portion of each active B requirement shall have at least one exact Product Validation-task binding.

### FS-004-NR-036 — Dataset Boundary
**Classification: B**
Story-instance Dataset state and any external reference fixture shall remain outside this Ruleset repository; Product code and Ruleset contracts may interpret or test exported copies of Dataset state but shall not create a reverse binding to a particular story instance.
