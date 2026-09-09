---
doc_id: DP-130
title: Artifact Identity and Cross-Layer Traceability
depends_on:
  - DP-100
  - DP-120
---

# Artifact Identity and Cross-Layer Traceability

## Purpose

Long-form fiction must remain navigable across many artifacts and revisions.

Stable identity is required where it materially improves targeting,
cross-layer relationships, reconciliation, revision, or manuscript mapping.

Identity is not required for every sentence, phrase, or incidental detail.

## Stable Identity

Governed artifacts intended to participate in durable relationships require
stable identity while in governed working state. That identity is preserved
through ordinary persistence and content revision.

Stable identity lets the system distinguish:

- the same artifact revised,
- an artifact reordered,
- an artifact renamed,
- an artifact superseded,
- and a genuinely new artifact.

The exact identifier syntax, namespace strategy, and generation mechanism are
Planning decisions.

## Identity Scope

Identity should exist where durable targeting or relationships require it,
including as appropriate:

- Character entities,
- Setting entities,
- Canon Events,
- Outline units,
- Sequence units,
- governed Prose units,
- and manuscript units or manifest entries.

The product does not require a single flat global namespace.

## Relationship Types

Relationships may express:

- refinement,
- realization,
- dependency,
- chronology,
- state effect,
- manuscript mapping,
- supersession,
- or other product-relevant semantic connections.

Examples include:

- Sequence units realizing an Outline unit;
- Beats preparing one or more Sequence units;
- Pseudo-prose realizing accepted Beats;
- a chapter realizing one or more accepted Sequence regions;
- an Event affecting Character or Setting state.

## Traceability Requirement

The system must not rely solely on fuzzy semantic inference to reconstruct
durable long-form relationships that can be represented explicitly.

Traceability must remain sufficient to answer practical questions such as:

- Which Sequence units realize this Outline unit?
- Which Beats realize this Sequence unit?
- Which manuscript chapter realizes these accepted story events?
- Which accepted Event changed this Character state?
- Which downstream artifacts may be affected by this revision?

## Traceability Boundary

Traceability exists to preserve story meaning and support authoring operations.

It must not become generalized provenance machinery recording every model
utterance, historical intermediate, or textual derivation.

Git history, conversation history, and construction provenance do not replace
semantic artifact relationships.

## Revision and Replacement

Editing an artifact without changing its semantic identity preserves its stable
identity.

When the author intentionally replaces one semantic artifact with a distinct
artifact, the product must be able to represent that distinction rather than
silently reusing identity.

The exact supersession representation is a Planning decision.

## Manuscript Identity

Stable manuscript identity, chapter ordinal, filename, and title are distinct
concepts.

Changing filename, order, or title does not inherently create a new chapter.

The manuscript manifest or equivalent persisted structure must preserve stable
targeting and order independently from filesystem naming.
