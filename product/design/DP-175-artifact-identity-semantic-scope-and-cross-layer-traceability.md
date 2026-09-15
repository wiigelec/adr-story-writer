---
doc_id: DP-175
title: Artifact Identity, Semantic Scope, and Cross-Layer Traceability
depends_on:
  - DP-100
  - DP-110
  - DP-120
  - DP-130
  - DP-140
  - DP-150
  - DP-160
  - DP-170
---

# Artifact Identity, Semantic Scope, and Cross-Layer Traceability

## Purpose

Long-form fiction remains coherent only if governed material can be targeted,
related, revised, migrated, retrieved, and reviewed across many artifacts and
sessions.

The Product therefore requires stable identity where durable targeting matters,
explicit semantic scope where an operation applies to only part of an artifact
or story surface, and enough cross-layer traceability to preserve meaning through
refinement, generation, revision, persistence, and migration.

Identity and traceability exist to support author control and model reliability.

They are not a requirement to assign identifiers to every sentence, phrase, or
incidental detail.

## Identity Principle

A governed object or region requires durable identity when later work must be
able to distinguish it reliably from neighboring, renamed, reordered, revised,
or replacement material.

Identity must remain stable through ordinary content revision when the same
semantic object continues to exist.

The Product must be able to distinguish:

- the same object revised;
- the same object renamed;
- the same object reordered;
- the same object represented in a different physical file;
- an object split into several continuing or replacement objects;
- several objects merged;
- an object superseded;
- an object retired;
- and a genuinely new object.

The exact identifier syntax, namespace strategy, encoding, and generation
mechanism are Planning decisions.

## Identity Is Not Presentation

Identity is distinct from presentation metadata.

The following do not inherently define semantic identity:

- filename;
- directory location;
- title;
- ordinal;
- array position;
- heading text;
- display label;
- scene number;
- chapter number;
- creation timestamp;
- or conversational description.

Any of these may help humans locate an object.

They must not be the sole identity mechanism when ambiguity could cause the
wrong governed material to be targeted.

## Identity Granularity

Identity should exist at the narrowest durable granularity that materially
supports governed operations.

Possible identity-bearing objects include, as applicable:

- story instance;
- Character or other Canon entity;
- Setting or world entity;
- Canon Event;
- relationship or state region when independently targetable;
- Plot unit;
- scene or sequence plan;
- reveal or viewpoint constraint;
- persistent Prose guidance region;
- production contract;
- Beat or other production-control unit;
- pseudo-prose or near-prose unit;
- generation package;
- generated prose candidate;
- accepted Manuscript unit;
- chapter or section manifest entry;
- reconciliation item;
- migration record;
- generated author view when independently persisted;
- or another governed object that participates in durable relationships.

This list is illustrative.

The Product does not require identity at every possible layer merely because a
layer can be named.

## Semantic Scope

Identity answers which object is being referenced.

Semantic scope answers which governed meaning within or across objects is
affected by an operation.

A scope may identify:

- an entire artifact;
- one semantic field;
- one Event;
- one Character state region;
- one Plot decision;
- one reveal constraint;
- one production-control unit;
- one paragraph-intent region;
- one Manuscript passage;
- one dependency edge;
- one accepted revision region;
- or another bounded governed area.

Scope is operation-relative.

The same artifact may participate in several distinct scopes for acceptance,
revision, dependency, generation, validation, or reconciliation.

When a semantic scope participates in a durable dependency, acceptance,
provenance, reconciliation, or cross-session reference, that scope must remain
resolvable across ordinary revisions or fail explicitly as stale or unresolved.

Line number, text offset, heading position, array index, or similar incidental
location must not be the sole durable scope reference when revision could make
the target ambiguous.

## Scope Precision

Governed operations should target the narrowest semantically useful scope that
preserves the intended meaning.

Scope must not be broadened merely because the physical representation is coarse.

For example, accepting one Plot reveal decision does not inherently accept every
other candidate decision stored in the same file.

Likewise, revising one Beat does not inherently revise the whole scene plan if
the remaining production controls are unaffected.

Physical file boundaries do not determine semantic scope.

## Scope and Acceptance

Acceptance defined by DP-110 applies to identified semantic scope.

The Product must be able to determine what meaning an acceptance operation
covers and what nearby candidate meaning remains outside that acceptance.

Acceptance must not rely on vague textual proximity when a narrower governed
scope is available.

If acceptance scope cannot be established reliably, the Product must not infer a
broader acceptance merely because material appears adjacent or related.

## Scope and Revision

A revision must identify the governed scope it changes sufficiently for impact
analysis and reconciliation under DP-120.

A change to one object may preserve identity while altering some of its scoped
meaning.

A change that intentionally replaces the semantic object itself may require a
new identity and an explicit supersession or replacement relationship.

The Product must not silently reuse an old identity for a semantically distinct
replacement merely because it occupies the same file or narrative position.

## Identity Preservation

Ordinary edits preserve identity when the author still means "this is the same
governed thing, revised."

Examples may include:

- renaming a Character;
- changing a scene title;
- reordering a chapter;
- correcting an Event date while preserving the Event itself;
- revising a production contract;
- revising one generated prose candidate without replacing that candidate;
- or moving an artifact to another file.

Identity preservation does not mean every prior version remains current.

Stable semantic identity answers which continuing governed object is being
targeted.

Revision or version identity answers which state of that object is being
referenced.

Revision history and current identity are separate concerns.

## New Identity

A new identity is appropriate when the governed object is intentionally distinct
rather than merely revised.

Examples may include:

- replacing one planned scene with a fundamentally different scene;
- splitting one Event into two independently governed Events;
- replacing one production contract with a different narrative task;
- or creating a new chapter rather than retitling an existing chapter.

The Product must support deliberate distinction between revision and
replacement.

## Split

A split occurs when one identity-bearing object becomes two or more independently
governed objects.

The Product must preserve enough relationship information to identify the source
and resulting objects when that history matters to:

- dependency repair;
- accepted-scope interpretation;
- migration;
- generation attribution;
- Manuscript mapping;
- or reconciliation.

A split must not leave several new objects all silently claiming to be the same
continuing identity.

The original identity may continue only where semantic continuity with one
result can be established without material ambiguity.

Otherwise, the resulting objects require distinct identities with explicit
lineage to the source.

Planning determines how that continuity and lineage are represented, not which
semantic result is arbitrarily treated as the original object.

## Merge

A merge occurs when several previously independent governed objects become one.

The resulting object must have an unambiguous identity.

Where prior dependencies or provenance remain material, the Product must
preserve enough mapping to relate the merged result to its sources.

Merging objects must not silently collapse materially different authority
classes or acceptance states.

## Supersession

An object may be superseded without being erased from history.

Supersession means a newer governed object replaces an older object for a
defined purpose or scope.

The superseded object does not automatically become false history, nor does the
replacement inherit authority merely from the relationship.

Authority of the replacement follows the acceptance or production-approval
semantics of its owning surface.

The exact representation of supersession is a Planning decision.

## Retirement

An object may cease to participate in current governed work without being
replaced.

Retirement must remain distinguishable from deletion when historical identity or
dependencies still matter.

Removing an accepted object from current semantic authority requires an
accepted revision at its owning semantic surface.

Archiving, hiding, or deleting its physical representation does not itself remove
that accepted meaning from authority.

Retirement of representation and retirement of accepted semantic authority are
therefore distinct operations.

## Relationship Principle

Traceability records material relationships between identifiable scopes that are
relevant to governed work.

A relationship retains its own role as semantic, production-control, provenance,
projection, migration, or other traceability information.

Creating or recording a traceability relationship does not itself establish
Canon, Plot, Prose, or Manuscript meaning unless the owning semantic operation
separately establishes that meaning.

For example, recording that two Events are temporally adjacent does not create
Canon causality, and recording generation attribution does not create semantic
authority.

A relationship is not merely evidence that two artifacts were created near each
other or mentioned in the same conversation.

Relationships may express, as applicable:

- semantic dependency;
- refinement;
- realization;
- projection;
- chronology;
- causal relationship;
- state effect;
- viewpoint or reveal constraint;
- production governance;
- generation attribution;
- Manuscript realization;
- supersession;
- migration mapping;
- derived-view projection;
- reconciliation impact;
- or another Product-relevant connection.

Not every relationship requires a distinct persisted edge if the relationship
can be reconstructed reliably without ambiguity.

## Dependency Traceability

Dependencies defined by DP-120 require enough identity and scope to determine
what materially relies on what.

A dependency should target the narrowest semantically useful source scope.

The Product must not require downstream work to depend on an entire artifact
when only one governed decision is material and a narrower target is practical.

Likewise, dependency precision must not become so fine-grained that maintaining
the relationships costs more than the control value they provide.

## Refinement Traceability

Progressive refinement under DP-120 may create several production-control
artifacts from broader intent.

The Product should be able to identify which upstream scope a downstream control
realizes when that relationship is needed for:

- bounded context construction;
- revision impact;
- local regeneration;
- semantic review;
- or author navigation.

A refinement relationship does not grant semantic authority to the downstream
artifact.

## Plot and Prose Traceability

Plot governs dramatic projection and Prose governs linguistic realization.

Where useful, the Product must be able to trace Prose controls or generated
candidate regions to the Plot scopes they realize.

This traceability supports review of questions such as:

- what Plot decision is this paragraph realizing;
- which reveal constraint governs this Beat;
- which viewpoint-access rule applies here;
- or which downstream passage may be affected by a Plot revision.

Traceability does not move ownership from Plot into Prose.

## Canon Traceability

Canon relationships may connect Events, state, Characters, Settings, knowledge,
belief, chronology, and other accepted reality.

Traceability should support materially useful questions such as:

- which Event established this state;
- which Event changed this relationship;
- what accepted knowledge state applies at this point;
- which later Plot decision depends on this hidden Canon fact;
- or what accepted future occurrence constrains this scene.

The Product need not record a provenance edge for every true fact when current
meaning can be interpreted reliably without one.

## Generation Attribution

A new generation attempt is a distinct execution event even when it uses the same
bounded task, production contract, or generation package as an earlier attempt.

A newly generated candidate must therefore remain distinguishable from earlier
generated candidates unless the author is revising one existing candidate rather
than performing a new generation attempt.

Every persisted generated prose candidate that may later be reviewed,
regenerated, compared, accepted, or migrated must be attributable to the
generation package or equivalent governing execution context that produced it.

Attribution must preserve enough identity to determine, as applicable:

- the bounded task;
- governing production contract;
- selected Canon and Plot dependencies;
- declared candidate assumptions;
- Prose guidance;
- resolved style;
- creative allowance;
- protected material;
- generation boundary;
- and other package state material to interpretation.

Generation attribution is execution provenance.

It does not grant authority to the generated candidate or package.

## Candidate Attribution

A candidate derived from other candidate state should retain enough traceability
to identify material candidate assumptions when later interpretation depends on
them.

The Product must not present such a candidate as independently grounded merely
because its upstream candidate source is no longer visually nearby.

This requirement supports DP-110 acceptance closure and DP-160 candidate
continuity.

## Manuscript Identity

Stable Manuscript identity, ordering, filename, and title are distinct concepts.

Changing a chapter's title, filename, physical location, or ordinal does not
inherently create a new chapter.

The Product must preserve stable targeting and ordering independently from
filesystem naming when ambiguity would otherwise result.

Accepted Manuscript wording belongs to Manuscript even when it can be traced to
upstream Canon, Plot, Prose controls, or generated candidates.

## Manuscript Mapping

The Product should support tracing accepted Manuscript regions to governing
upstream scopes when that traceability materially helps:

- continuity analysis;
- revision impact;
- local regeneration;
- semantic review;
- reveal auditing;
- or author navigation.

A Manuscript passage may realize several upstream scopes.

One upstream scope may also be realized across several Manuscript passages.

The Product must not assume one-to-one mapping.

## Manuscript Reordering

Reordering Manuscript units changes presentation order without inherently
changing identity.

If the reorder changes Plot meaning, reveal timing, or other governed semantics,
those semantic changes must be handled at their owning surfaces.

The manifest or equivalent ordering mechanism must not itself become a hidden
substitute for Plot authority.

## Cross-Layer Traceability

Cross-layer traceability should be sufficient to answer practical questions such
as:

- Which Plot scopes depend on this Canon fact?
- Which production controls realize this Plot scene?
- Which generation package governed this candidate?
- Which candidate assumptions were active for this generated passage?
- Which accepted Manuscript regions realize this Plot reveal?
- Which downstream scopes may be affected by this revision?
- Which migration mapping preserved this identity?
- Which object superseded this one?
- Which current object corresponds to this historical identity?

The Product does not require one universal graph implementation.

It requires that these relationships be recoverable reliably where they are
material.

## Traceability and Retrieval

Session reconstruction and task-specific retrieval under DP-160 may use identity
and traceability to locate relevant governed state.

Retrieval should prefer explicit durable relationships over fuzzy semantic
inference when the relationship is already known and material.

Semantic search remains useful for discovery.

Search similarity must not replace a known identity or dependency relation when
precise targeting is required.

## Traceability and Context Construction

Generation packages under DP-150 should use identity and traceability to select
the material dependencies required by the bounded task.

Context construction may project only the portions of identified sources needed
for the task.

The package need not copy complete upstream artifacts merely because it depends
on one scope within them.

The projected context must preserve enough source attribution to support later
review and regeneration where material.

## Traceability and Reconciliation

Revision impact under DP-120 follows material dependencies and affected scopes.

Traceability should make it possible to start from a changed scope and identify
likely downstream regions requiring review or reconciliation.

Traceability does not decide the semantic outcome of reconciliation.

It identifies relationships and affected regions.

The author or governed semantic process decides what changes.

## Traceability and Migration

Migration under DP-170 should preserve identity and materially required
traceability when the same governed meaning continues across realizations.

If a migration changes identifiers, it must preserve enough mapping to relate
source identities to target identities for as long as that relationship remains
material.

Migration mappings are provenance.

They do not create new semantic authority.

## Historical Identity

Historical identity may remain useful after an object is superseded, retired,
migrated, or revised.

The Product may retain historical identity references for:

- provenance;
- diagnosis;
- migration;
- comparison;
- reconciliation;
- or author navigation.

Historical identity must not be mistaken for current authority.

## Identity Collision

Two distinct current governed objects must not silently share an identity where
that collision could cause ambiguous targeting or authority confusion.

If a collision is detected, ordinary governed operations that depend on the
identity must not proceed as though the target were unambiguous.

Repair may preserve one identity and reassign another, or use another governed
resolution.

If an established identity changes, materially affected dependencies,
provenance, migration mappings, Manuscript mappings, or cross-session references
must be preserved, remapped, or surfaced as unresolved.

The exact repair mechanism is Planning.

## Missing Identity

Older, imported, damaged, or external material may lack durable identity.

The Product may assign identity mechanically when the continuing semantic object
can be established without consequential interpretation.

If assigning identity requires deciding whether two pieces of material are the
same semantic object, that decision must be surfaced when materially ambiguous.

Identity repair must not invent semantic equivalence merely to satisfy a schema.

## Imported Material

Imported source material does not become governed story authority merely because
the Product assigns it an identity.

Identity enables targeting.

Authority remains determined by the material's governed role and acceptance
state.

This distinction also applies to imported notes, source references, templates,
or generated views.

## Derived Views

Generated dossiers, reports, indexes, summaries, and other derived views may
have stable identity for persistence, caching, user targeting, or refresh.

Their identity does not grant them semantic authority.

Where a derived view projects governed sources, traceability should permit the
Product to identify those sources when needed for refresh or safe editing.

Edits intended to change story meaning must map back to the appropriate owning
semantic surface rather than treating the derived view as a competing authority.

## Traceability Completeness

Traceability should be complete enough for the operation being performed.

The Product does not require every possible relationship to be precomputed.

When a governed operation requires a material relationship that is missing or
ambiguous, the Product must:

- retrieve or reconstruct it safely;
- request or perform governed reconciliation;
- narrow the operation;
- or surface the uncertainty.

It must not silently fabricate the relationship when doing so could change
consequential meaning.

## Traceability Freshness

Traceability can become stale when governed state changes.

A stale relationship must not continue to govern downstream work when the change
invalidates its meaning.

The Product must be able to distinguish, as needed, between:

- still-valid relationship;
- relationship requiring review;
- superseded relationship;
- and unresolved relationship.

The exact status vocabulary is a Planning decision.

## Traceability Is Not Authority

Identity and traceability describe what an object is and how governed scopes
relate.

They do not create semantic authority.

A relationship to accepted Canon does not automatically make a candidate Plot
accepted.

A generated candidate attributable to an approved production contract does not
become accepted Manuscript.

A Manuscript passage tracing to candidate Canon does not accept that Canon.

Authority continues to follow DP-110 and the owning semantic surface.

## Traceability Is Not Acceptance Closure

Traceability may reveal dependencies relevant to acceptance closure.

It does not itself decide whether every traced historical influence must be
accepted.

DP-110 governs acceptance closure based on current material dependency.

Historical derivation may be retained without becoming a current acceptance
dependency.

## Traceability Boundary

Traceability exists to preserve meaning and support practical governed
operations.

The Product does not require generalized provenance machinery recording:

- every model token;
- every chat utterance;
- every discarded thought;
- every intermediate prompt;
- every temporary search result;
- every unchanged file read;
- or every historical textual derivation.

Conversation history, Git history, filesystem history, and model logs may support
diagnosis.

They do not replace semantic identity and current governed relationships.

## Physical Representation

One semantic object may span several physical files.

One physical file may contain several semantic objects.

Identity and scope must therefore remain conceptually separate from physical
storage layout.

Planning may choose embedded identifiers, manifests, indexes, relationship
tables, structured documents, graph representations, databases, or other
mechanisms.

The Product does not require a universal artifact registry.

## Identity and Human Usability

Stable identifiers may be machine-oriented.

The Product should also support human-readable labels, titles, names, and
context sufficient for authors to recognize targets.

Human labels may change without changing identity.

The author should not be required to manipulate opaque identifiers directly for
ordinary work when the Product can resolve a target safely through human-facing
context.

## Identity Test

The Product should be able to handle at least these scenarios:

1. A chapter is renamed and reordered without losing its identity.
2. A scene plan is revised while downstream dependencies still target the same
   scene identity.
3. One Event is split into two distinct Events without both inheriting one
   ambiguous identity.
4. A generated prose candidate remains attributable to the package that governed
   it across a fresh session.
5. A migrated Dataset preserves correspondence between source and target
   identities.
6. A derived character dossier can be refreshed from governing Canon without
   becoming competing authority.
7. A revision to one Plot reveal can identify the downstream production and
   Manuscript regions likely to require review.
8. A stale or ambiguous identity relation blocks precise governed targeting
   rather than silently selecting a plausible object.

Failure of these scenarios indicates that long-form continuity depends too much
on filenames, conversational memory, or fuzzy semantic inference.

## Simplicity Boundary

The Product requires stable identity and traceability only where they materially
improve correctness, continuity, targeting, review, reconciliation, migration,
or local generation control.

It does not require:

- one identifier per sentence;
- a universal graph database;
- a global flat namespace;
- exhaustive lineage for every intermediate;
- cryptographic hashes as semantic identity;
- immutable event sourcing;
- or generalized provenance infrastructure.

Additional identity machinery requires demonstrated Product value.

## Planning Boundary

This Design defines semantic identity, semantic scope, identity preservation,
replacement/split/merge/supersession behavior, cross-layer traceability,
generation attribution, Manuscript mapping, migration mapping, and the boundary
between traceability and authority.

Planning may choose identifier formats, namespaces, manifests, storage layout,
edge representation, indexing, lookup APIs, revision metadata, migration maps,
human-facing labels, and other technical realization.

Implementation convenience does not justify ambiguous targeting, identity
collision, authority inference from location, dependence on fuzzy matching where
known relationships exist, or loss of material traceability across sessions and
migrations.
