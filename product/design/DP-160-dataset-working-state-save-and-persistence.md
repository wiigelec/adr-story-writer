---
doc_id: DP-160
title: Dataset, Working State, Save, and Persistence
depends_on:
  - DP-100
  - DP-110
  - DP-120
  - DP-130
  - DP-140
  - DP-150
---

# Dataset, Working State, Save, and Persistence

## Purpose

A Dataset persists one coherent accepted story state while remaining separate
from conversation and unsaved working state.

## Dataset Authority

The Dataset is persisted story authority for its story instance.

It does not define Ruleset semantics.

It stores accepted story state according to the applicable Ruleset and Dataset
schema realization.

## Working State

Active governed working state is initialized from persisted Dataset state.

Working state may contain:

- unchanged persisted accepted state,
- accepted-but-unsaved revisions,
- candidate artifacts,
- unresolved proposals,
- and reconciliation work.

Conversation is not automatically copied into Dataset state.

## Session Loss

If a session ends without successful authorized persistence, persisted Dataset
state remains story authority.

Unsaved ephemeral working state is not assumed to survive.

An implementation may provide explicit recovery mechanisms, but hidden
autosave must not silently redefine the save boundary established by the
product.

## Save Authorization

Save requires user request or accepted save authorization.

Semantic acceptance and save authorization are distinct.

## Save Result

A successful save persists one coherent governed Dataset state.

A partially written physical Dataset must not be treated as a successful save.

The implementation may use filesystem writes, Git commits, transactions, or
other mechanisms, but the logical result must be coherent.

## Save Scope

The product may support:

- saving all current governed accepted state,
- or saving a specifically authorized coherent subset.

A partial save must not knowingly produce semantic inconsistency across
dependencies.

Unresolved consequential candidates do not become persisted accepted authority
merely because related accepted material is saved.

## External Change and Concurrency

If persisted Dataset state changes after working state was initialized, the
system must not silently overwrite the newer persisted state.

The conflict must be detected and resolved before successful save.

The exact concurrency token, Git comparison, merge strategy, conflict UI, or
recovery mechanism is a Planning decision.

## Dataset Structure

A Dataset must be able to persist:

- story instance identity and story metadata,
- Canon,
- Plot,
- governed Prose state,
- persistent prose guidance where applicable,
- manuscript manifest and accepted chapter files,
- stable identities and relationships,
- semantic alignment or review state needed for reconciliation,
- and Dataset schema identity.

The exact physical file decomposition is a Planning decision.

## Persistence Boundary

Ordinary saves mutate Dataset-owned runtime state only.

Ruleset realization, application definition, construction provenance,
initialization inputs, and binding metadata are distinct roles and are not
ordinary story-save targets except where a separately governed operation
explicitly changes them.
