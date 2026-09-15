---
doc_id: DP-170
title: Schema Evolution, Ruleset Compatibility, Migration, and Rebinding
depends_on:
  - DP-100
  - DP-110
  - DP-120
  - DP-130
  - DP-140
  - DP-150
  - DP-160
---

# Schema Evolution, Ruleset Compatibility, Migration, and Rebinding

## Purpose

ADR Story Writer must evolve without silently changing the meaning, authority
class, or continuity of persisted story projects.

A Dataset may outlive the exact schema realization or Ruleset realization under
which it was created.

The Product must therefore distinguish structural interpretability from
semantic compatibility and must provide governed ways to refuse, migrate, or
rebind a Dataset when ordinary operation is not safe.

## Compatibility Axes

Dataset schema identity and Ruleset identity are distinct compatibility axes.

A Dataset can be structurally readable while semantically incompatible with a
different Ruleset.

A Ruleset can preserve Product semantics while requiring a different Dataset
schema realization.

The Product must not collapse these questions into one version number.

## Dataset Schema Identity

A Dataset must identify its structural schema realization sufficiently for the
Product to determine whether persisted state can be interpreted safely.

Schema identity concerns the persisted representation needed to interpret such
things as:

- artifact roles;
- authority classification;
- semantic ownership;
- dependencies;
- stable identities;
- ordering;
- provenance;
- production-control state;
- candidate state;
- accepted Manuscript;
- and other persisted meanings required by applicable Design.

The exact identifier, version format, schema language, and storage mechanism are
Planning decisions.

Ruleset binding metadata does not by itself version the Dataset schema.

## Ruleset Identity

A Dataset must be associated with the Ruleset realization applicable to governed
operation.

Ruleset identity must be sufficient to determine whether the supplied Ruleset is
the one expected by the Dataset or is otherwise known to be compatible.

A Ruleset realizes Product-defined semantics.

Binding a Dataset to a Ruleset does not permit that Ruleset to redefine Product
meaning or reinterpret persisted authority classes for convenience.

## Binding

Binding identifies the Ruleset realization under which ordinary governed work
is expected to proceed.

Binding is not the same as:

- Dataset schema identity;
- semantic acceptance;
- save authorization;
- application configuration;
- or construction provenance.

The Product may store binding metadata in or alongside the Dataset.

The physical location is a Planning decision.

## Compatibility Determination

A Ruleset or Dataset schema realization must not be assumed compatible merely
because:

- a filename matches;
- a version number appears newer;
- semantic-version syntax suggests compatibility;
- a parser succeeds;
- required fields happen to exist;
- or most operations appear to work.

Compatibility is a governed determination.

The Product may classify a relationship as, for example:

- directly compatible;
- compatible with restricted operation;
- migration required;
- rebinding required;
- unsupported;
- or unresolved pending review.

The exact vocabulary may evolve when concrete compatibility needs arise.

Planning may implement Product-established compatibility classifications and
mechanically decidable criteria.

Compatibility classifications describe permitted operations and required
transitions. They do not themselves change the semantic meaning, authority
class, acceptance state, production approval, or Manuscript status of Dataset
contents.

Planning must not invent semantic compatibility merely to make a technical
upgrade path appear successful.

## Structural and Semantic Compatibility

Structural compatibility means persisted state can be parsed and represented
without losing required interpretation.

Semantic compatibility means the persisted meanings, authority classes,
ownership boundaries, dependency semantics, and operational expectations can be
preserved under the target realization.

Structural compatibility does not imply semantic compatibility.

A migration that makes files parse successfully is not complete if it changes
what accepted, candidate, production-approved, derived, protected, or
Manuscript material means.

## Compatibility Scope

Compatibility may be scoped.

A Dataset may be safe for inspection or export while unsafe for:

- semantic editing;
- acceptance;
- generation;
- reconciliation;
- save;
- migration chaining;
- or another governed operation.

The Product may permit restricted operation when the permitted scope can be
established safely.

Restricted compatibility must not be presented as full ordinary compatibility.

## Ordinary Initialization

Before ordinary governed operation, the Product must establish that the Dataset
schema and applicable Ruleset are sufficiently compatible for the requested
operation.

If compatibility cannot be established, ordinary operation must not proceed by
guessing.

The Product may instead enter a controlled inspection, recovery, migration, or
rebinding path.

## Migration

Migration is an explicit governed transformation from one supported persisted
realization to another.

Migration may change physical representation, schema shape, identifiers,
indexes, metadata, storage decomposition, or other implementation structure.

Migration must preserve governed meaning unless the migration explicitly
identifies a semantic decision that cannot be preserved mechanically.

Mechanical migration must not invent consequential story meaning.

It must not silently:

- accept candidates;
- demote accepted state;
- convert production approval into semantic acceptance;
- promote derived views into authority;
- change Canon or Plot ownership;
- change Manuscript acceptance;
- widen creative allowance;
- alter protected-material semantics;
- or erase material dependency or provenance information.

## Meaning-Preserving Migration

A migration is meaning-preserving only when the target representation preserves
the material interpretation of the source state.

Preservation includes, where applicable:

- semantic content;
- authority class;
- accepted scope;
- candidate status;
- production-approval state;
- ownership surface;
- stable identity;
- ordering;
- dependency relationships;
- generation provenance;
- temporal meaning;
- ambiguity and unknown state;
- and author-declared constraints.

Representation may change substantially while these meanings remain preserved.

## Migration Requiring Author Decision

Some evolution cannot be completed mechanically without choosing among
materially different meanings.

Examples may include:

- splitting one old field into several semantically distinct concepts when the
  source does not identify which applies;
- adopting a new authority distinction absent from old persisted data;
- resolving an old ambiguity required by the new model;
- or mapping an old artifact whose ownership cannot be established reliably.

When migration requires such a choice, the Product must surface the decision.

The migration must not invent the answer merely to complete the upgrade.

Until resolved, the target migration remains incomplete or restricted for the
affected material.

Existing accepted meaning remains accepted in the source realization and must
not be demoted to candidate merely because the target cannot represent it
without an author decision.

Newly proposed target interpretations remain candidate until accepted according
to their owning semantics.

## Migration and Accepted State

Migration does not constitute semantic revision merely because accepted state is
rewritten into a new representation.

A meaning-preserving migration may carry accepted state forward without
requiring the author to re-accept identical meaning.

If migration changes governed meaning rather than representation, that change is
a semantic revision and must follow the acceptance semantics of DP-110.

The Product must distinguish these cases.

## Migration and Candidate State

Persisted candidate state should remain candidate through migration unless the
author separately accepts it.

Candidate dependencies and assumptions that remain material after migration must
remain identifiable.

Migration must not discard candidate status merely because the target schema has
a cleaner representation.

Where candidate material cannot be represented safely in the target realization,
the Product must preserve it through an explicit archival/recovery mechanism or
surface the loss before migration is authorized.

## Migration and Production Controls

Production contracts, Beats, pseudo-prose, generation-package provenance,
protected-material controls, and other persisted production state may require
migration.

Their migration must preserve production role and approval status.

Production-approved controls must not become semantic authority.

Candidate controls must not become production-approved merely because a target
schema requires a status value.

If an old production control cannot be interpreted under the new realization,
the Product must require regeneration, re-approval, repair, or another explicit
resolution rather than silently reinterpret it.

## Migration and Generated Candidates

Persisted generated prose candidates may depend on the exact generation package
or equivalent governing context used when they were produced.

Migration must preserve enough provenance for later review, regeneration, or
acceptance when that provenance remains material.

A migrated candidate is not revalidated merely because migration succeeded.

If its governing context can no longer be interpreted safely, that limitation
must be surfaced.

## Migration Atomicity

A migration must produce one coherent target Dataset state or fail without
presenting a partial target as successfully migrated.

The Product must not leave ordinary operation pointed at a mixed source/target
realization.

Physical implementation may use transactions, copies, Git commits, staged
directories, databases, object stores, or another mechanism.

The Product requirement is coherent migration outcome and recoverability.

An implementation may persist intermediate migration checkpoints, workspaces, or
recovery state. Such intermediate state must remain distinguishable from the
successfully migrated Dataset and must not be used for ordinary governed
operation as though migration had completed.

## Migration Provenance

The Product must preserve enough migration provenance to identify:

- the source realization;
- the target realization;
- the migration operation or path used;
- material unresolved decisions or losses;
- and whether semantic author decisions were required.

Migration provenance supports diagnosis, recovery, and later interpretation.

It is not story authority.

## Rebinding

Rebinding changes the Ruleset realization applicable to a Dataset.

Rebinding is not an ordinary save and is not implied by installing or selecting
a newer Ruleset.

A rebind requires explicit authorization.

Authorization to rebind does not authorize semantic revisions discovered during
compatibility evaluation. Any such revision requires the acceptance operation
appropriate to its owning semantic surface.

Before rebinding completes, the Product must establish that the Dataset can be
operated safely under the target Ruleset, either directly or after required
migration and review.

## Rebinding Without Migration

A Dataset may be rebound without structural migration when its existing schema
and persisted meanings are compatible with the target Ruleset.

The absence of a schema change does not remove the need to evaluate semantic
compatibility.

If the target Ruleset changes the interpretation of existing persisted material,
the operation is not a harmless rebind.

It requires semantic review, migration, revision, or refusal as appropriate.

## Migration Without Rebinding

A Dataset may undergo structural migration without changing the applicable
Ruleset when the Ruleset supports the target Dataset schema.

Migration and rebinding are therefore independent operations even though they may
occur together.

## Ruleset Upgrade

A newer Ruleset version must not automatically replace the Dataset's current
binding merely because it is available.

An upgrade path must establish compatibility or perform explicit rebinding and
any required migration.

Ordinary Dataset save must not update the Ruleset binding as a side effect.

## Downgrade

Compatibility must not assume that an older schema or Ruleset can safely consume
newer persisted state.

A downgrade is a migration or rebinding operation subject to the same
meaning-preservation requirements as an upgrade.

If the older realization cannot represent material newer meaning or authority
classification, the Product must refuse the downgrade or require an explicit
loss-bearing transformation.

Loss must not be silent.

## Lossy Transformation

A migration or rebinding operation that intentionally discards material governed
state is not meaning-preserving.

If such an operation is supported, it must:

- identify the material loss;
- distinguish accepted, candidate, production, derived, and provenance loss;
- require explicit authorization appropriate to the impact;
- require deliberate semantic authorization when accepted semantic or
  Manuscript authority would be discarded or changed;
- avoid representing the result as semantically equivalent to the source; and
- preserve recovery or export access to the source where reasonably required by
  the operation.

A lossy transformation must not masquerade as ordinary migration.

## Unknown or Unsupported Realizations

When Dataset schema identity, Ruleset identity, or compatibility cannot be
established reliably, the Product must fail safely.

Safe responses may include:

- read-only inspection;
- export;
- diagnostic reporting;
- backup;
- controlled repair;
- controlled migration;
- or refusal.

The Product must not invent a schema mapping or semantic interpretation merely
because the persisted files appear understandable.

## Corrupt or Partially Interpretable State

A Dataset may be structurally damaged or only partially interpretable.

The Product may recover unaffected regions when their identity, role, authority,
and material dependencies can be established independently.

If a recovered region materially depends on damaged or unrecoverable state, that
dependency must be satisfied, repaired, or surfaced as unresolved before the
region is used for governed work.

Recovered regions must not be treated as sufficient to infer the meaning of
unrecoverable material.

Repair tooling must not silently manufacture missing consequential story state.

## Construction Inputs and Lineage

Retained initialization inputs, templates, construction payloads, or similar
materials may support:

- lineage;
- reproducibility;
- diagnosis;
- migration;
- repair;
- or reconstruction.

They do not become current runtime story authority merely because they describe
how the Dataset was originally constructed.

Current governed Dataset state, applicable compatible Ruleset, and explicit
binding remain the operational basis.

## Derived Indexes and Caches

Indexes, caches, search structures, generated views, and other reconstructable
derived artifacts need not constrain compatibility when they can be safely
rebuilt from governed state.

If a derived artifact is stale or incompatible, the Product should prefer
reconstruction over treating it as authoritative migration input.

Rebuilding derived state must not invent missing governed meaning.

## Identity Preservation

Migration should preserve durable identity when the same governed entity,
artifact, or semantic region continues to exist across realizations.

If identity must change for technical reasons, the Product must preserve enough
mapping or provenance to maintain dependency, reconciliation, ordering,
generation attribution, and cross-session targeting where materially required.

A migration must not silently create duplicate authorities by treating one
continuing semantic object as unrelated old and new objects.

Detailed identity and traceability semantics are defined by DP-175.

## Validation and Semantic Review

Migration and rebinding may require both mechanical validation and semantic
review.

Mechanical validation may establish structure, references, required fields,
schema conformance, or mechanically decidable compatibility properties.

Semantic review evaluates whether governed meaning and authority have been
preserved.

Mechanical success does not prove semantic equivalence.

Validation does not create compatibility or authorize semantic changes beyond
the governing migration/rebinding decision.

## Compatibility Test

The Product should be able to distinguish at least these scenarios:

1. Same compatible Ruleset and schema: ordinary session reconstruction may
   proceed.
2. Structurally different but meaning-preservable schema: migration may proceed
   without semantic revision.
3. New Ruleset with compatible semantics: explicit rebind may proceed without
   story revision.
4. Migration requiring an author semantic choice: ordinary migration pauses for
   resolution.
5. Unsupported or ambiguous realization: ordinary governed work is refused.
6. Lossy downgrade: loss is surfaced and requires explicit authorization.

If the Product cannot distinguish these cases, schema evolution risks silently
changing story meaning.

## Evolution Simplicity

The Product does not require speculative migration engines or compatibility
matrices before concrete incompatible evolution exists.

It does require enough identity and boundary semantics that the first real
incompatible change can be handled deliberately.

Compatibility infrastructure should grow in response to actual evolution rather
than imagined future complexity.

## Planning Boundary

This Design defines Dataset-schema identity, Ruleset identity, binding,
compatibility semantics, migration, rebinding, downgrade, loss, refusal, and
authority-preservation requirements.

Planning may choose version formats, compatibility manifests, migration
registries, converters, backup strategy, schema languages, transaction
mechanisms, repair tools, binding storage, provenance records, and other
technical realization.

Implementation convenience does not justify silent semantic reinterpretation,
candidate promotion, authority loss, unreviewed lossy migration, or guessing at
unknown compatibility.
