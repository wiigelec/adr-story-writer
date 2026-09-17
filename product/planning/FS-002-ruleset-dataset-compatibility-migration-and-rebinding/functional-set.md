---
functional_set: FS-002
artifact: functional-set-scope
title: Ruleset-Dataset Compatibility, Migration, and Rebinding
design_revision: 325c7f22cd140dee43c01dbf7f93500325585ce9
---

# FS-002 — Ruleset-Dataset Compatibility, Migration, and Rebinding

## Purpose

FS-002 selects the minimum coherent Product capability required to evolve a
persisted story Dataset or its bound Ruleset without silently changing governed
story meaning, authority class, continuity, or operational safety.

FS-002 builds on the governed-state, persistence, provenance, review, and
acceptance contracts established by FS-001. It does not redefine those
contracts.

## Exact Design Binding

Planning consumes Product Design at repository revision:

`325c7f22cd140dee43c01dbf7f93500325585ce9`

Selected obligations are:

- **DP-170:** Dataset schema identity, Ruleset identity, binding, compatibility
  determination, restricted operation, governed migration, meaning preservation,
  author-decision boundaries, and rebinding required for safe ordinary
  operation;
- **DP-160:** persisted-state interpretation and fresh-session reconstruction
  constraints necessary to preserve Dataset continuity across a compatibility
  transition;
- **DP-175:** durable identity and provenance preservation necessary to keep
  migrated or rebound state traceable; and
- **DP-180:** validation/review boundaries necessary to prevent an indeterminate
  compatibility or migration result from being treated as safe.

## Functional Boundary

FS-002 begins with an existing persisted Dataset whose schema identity and
Ruleset binding are known or discoverable.

FS-002 ends when the Product can:

1. determine whether the Dataset schema and supplied Ruleset are safe for the
   requested governed operation;
2. refuse or restrict ordinary operation when compatibility cannot be
   established;
3. perform an explicitly supported meaning-preserving migration or Ruleset
   rebinding transition when mechanically decidable;
4. surface unresolved semantic choices for author decision rather than inventing
   them; and
5. preserve the authority classes, semantic ownership, stable identities,
   dependencies, ordering, and provenance required to interpret the resulting
   Dataset correctly.

## Required Demonstration

The implemented Product must demonstrate both a safe and an unsafe transition:

- a supported Dataset/Ruleset transition preserves governed meaning and permits
  the authorized operation after migration or rebinding; and
- an incompatible or semantically indeterminate transition is refused or
  restricted without silently promoting, demoting, rewriting, or inventing
  story authority.

A fresh session after the successful transition must reconstruct the migrated or
rebound Dataset without relying on prior conversation history.

## Explicit Deferrals

FS-002 does not require:

- a generalized migration graph or arbitrary migration chaining;
- downgrade support;
- compatibility inference from semantic-version syntax alone;
- automatic resolution of semantically ambiguous legacy state;
- migration of unsupported historical formats;
- a generalized migration plugin framework;
- automatic acceptance of migrated or rebound story meaning;
- broad generated-view work from DP-190; or
- the full general split/merge/supersession lifecycle from DP-175.

## Planning-Structure Cleanup

This branch also normalizes accepted FS-001 Planning artifacts into the canonical
Product Planning tree. That relocation changes lifecycle ownership
representation only; it does not change FS-001 Product meaning or normative
requirements.
