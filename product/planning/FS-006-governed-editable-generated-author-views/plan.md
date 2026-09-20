---
functional_set: FS-006
artifact: implementation-plan
title: Governed Editable Generated Author Views Plan
design_revision: 22b8f2dcb3ff22b1ff1613fb965353dd2917d443
---

# FS-006 — Plan

## Objective

Extend the FS-005 author-workshop runtime with a generated-view contract and one
concrete Character-dossier realization that preserves source ownership,
traceability, freshness, and safe edit-through behavior.

## Runtime Shape

Add a generated-view module under `product/src/` and integrate it with
`AuthoringSession`.

The implementation shall provide operations equivalent to:

- create/render a Character dossier for a governed Character scope;
- inspect view source attribution and freshness;
- refresh/regenerate a view from current governed state;
- compare a prior projection with the current projection;
- apply presentation-only preferences;
- propose an edit through the view;
- resolve an unambiguous edit to one or more governed targets;
- route resolved edits into existing FS-005 candidate operations or FS-004
  accepted-revision operations;
- reject stale or ambiguous consequential edits without mutating governed state.

Exact function names and internal object layout remain Build decisions.

## Generated-view Representation

A generated view is derived state. Its representation shall retain only the
information needed for safe use, including as applicable:

- view identity and type;
- story identity;
- projected governed source identities and revisions;
- owning semantic surfaces;
- relevant authority/status;
- generation/refresh revision or equivalent freshness basis;
- presentation-only preferences;
- optional diagnostic or comparison material clearly distinguished from source
  meaning.

The representation must not duplicate authoritative story meaning as an
independent source of truth.

## Character Dossier Projection

The first concrete view is a Character dossier.

It may assemble Character Canon plus relevant state, knowledge/belief,
relationships, Events, Plot context, candidate material, and other already
governed information allowed by DP-190.

Each projected section must remain attributable to its owning governed source.
Combining material into one dossier does not combine semantic ownership.

## Freshness

Freshness is determined from material source identity/revision attribution.

A view is current when all material projected sources still match the revisions
on which the projection was based. A material source change makes the affected
view or affected region stale.

A stale view may be inspected or compared, but a consequential edit shall not be
applied as though it targeted unchanged current state.

Regeneration creates a new current projection from governed sources. It does not
change source authority.

## Edit-through Mapping

An edit through a generated view is first a proposal.

The runtime shall classify the requested change as:

- presentation-only;
- unambiguous governed edit;
- coordinated multi-target governed edit;
- ambiguous governed edit; or
- stale-target edit.

Presentation-only edits affect view preferences only.

An unambiguous governed edit is mapped to the underlying target and routed to
existing candidate/revision semantics. The view itself never directly mutates
accepted semantic state.

A coordinated edit may produce several proposed governed operations while
preserving each target's owning surface and explicit acceptance scope.

Ambiguous or stale consequential edits do not proceed silently.

## Persistence

Generated views may be regenerated on demand. Persist only view state that has
demonstrated workflow value, such as presentation preferences or an explicitly
retained comparison snapshot.

Persisted derived state must remain distinguishable from governed story
authority and retain sufficient source attribution to evaluate freshness.

No second story-state database is introduced.

## Integration

FS-006 reuses:

- FS-002 compatibility gating;
- FS-004 revision and reconciliation for accepted upstream changes;
- FS-005 candidate creation/refinement/acceptance and author-workshop
  reconstruction;
- existing Dataset coherent-save and stale-session conflict protection.

## Validation

Add FS-006 Product Validation covering exact Planning binding, derived-authority
separation, dossier projection attribution, freshness detection, regeneration,
presentation-only preferences, unambiguous edit routing, stale-edit refusal,
ambiguous-edit refusal, coordinated edit preservation, persistence/reconstruction,
and Dataset boundary.

Mechanical requirements receive exact task bindings in
`product/validation/requirement-evaluation.json`. Semantic-only obligations
remain for Semantic Review.

## Build Boundary

Do not introduce a universal view graph, a second semantic authority surface,
automatic semantic acceptance, arbitrary natural-language patch inversion,
provider-specific model calls, or a generalized UI framework.
