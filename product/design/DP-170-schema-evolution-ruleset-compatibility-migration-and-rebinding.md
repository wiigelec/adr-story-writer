---
doc_id: DP-170
title: Schema Evolution, Ruleset Compatibility, Migration, and Rebinding
depends_on:
  - DP-100
  - DP-160
---

# Schema Evolution, Ruleset Compatibility, Migration, and Rebinding

## Purpose

Story Writer must evolve without silently changing the meaning of persisted
stories.

Ruleset identity and Dataset schema identity are separate axes of compatibility.

## Dataset Schema Identity

A Dataset must have an identifiable schema realization sufficient to determine
whether its persisted structure can be interpreted safely.

The exact schema identifier, version format, and compatibility representation
are Planning decisions.

Binding metadata that identifies an external Ruleset does not by itself version
the Dataset schema.

## Ruleset Identity

A Dataset is bound to an applicable Ruleset realization through the runtime
binding contract.

A supplied Ruleset realization must be verified against that binding before
ordinary initialization.

## Compatibility

A different Ruleset realization or Dataset schema version must not be assumed
compatible merely because names or semantic versions appear similar.

Compatibility is a governed determination.

It may be exact, backward-compatible, migration-required, unsupported, or
otherwise classified as later Product Design establishes.

Planning defines the technical realization and mechanically decidable criteria
needed to apply Product-established compatibility classifications; Planning
does not invent new semantic compatibility classes.

## Migration

Migration is an explicit governed transformation from one supported persisted
realization to another.

Migration must preserve author-approved meaning unless the migration operation
explicitly identifies a semantic change requiring author decision.

Mechanical schema transformation must not invent new story meaning.

## Rebinding

Rebinding changes the Ruleset realization to which a Dataset is bound.

Rebinding is not an ordinary save.

It requires explicit authorization and whatever compatibility, migration,
validation, or semantic review is necessary to establish that the Dataset can
operate safely under the new Ruleset.

## Recovery and Refusal

When safe interpretation cannot be established, the system may refuse ordinary
operation rather than guess.

Recovery mechanisms may allow inspection, export, repair, or controlled
migration without pretending the Dataset is already aligned.

## Version 0.1 Simplicity

The product does not require speculative migration machinery before an actual
incompatible evolution exists.

However, the semantic boundaries in this document must be preserved so that
the first incompatible change can be handled intentionally rather than by
retroactive invention.

## Construction Inputs

Retained initialization or construction inputs provide lineage and
reproducibility but do not become mutable runtime authority.

They may assist reconstruction or migration tooling without replacing current
Ruleset, Dataset, schema, or binding authority.
