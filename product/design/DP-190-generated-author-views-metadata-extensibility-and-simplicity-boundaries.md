---
doc_id: DP-190
title: Generated Author Views, Metadata, Extensibility, and Simplicity Boundaries
depends_on:
  - DP-100
  - DP-110
  - DP-120
  - DP-130
  - DP-140
  - DP-150
  - DP-160
  - DP-170
  - DP-175
  - DP-180
---

# Generated Author Views, Metadata, Extensibility, and Simplicity Boundaries

## Purpose

ADR Story Writer needs author-friendly views, useful story metadata, and room to
evolve without turning convenient projections, schemas, or framework machinery
into competing semantic authority.

This Design governs:

- generated author views;
- story-level metadata;
- operational lifecycle metadata;
- extensibility;
- projection/edit boundaries;
- human readability;
- and simplicity limits.

The Product should make governed story state easier to understand and manipulate
without forcing the author to reason directly about internal governance
machinery.

## Story Instance Identity

Each Dataset represents one story instance and requires stable story identity.

Story identity distinguishes one governed story workspace from another.

Story identity is not the same as:

- story title;
- filename;
- directory name;
- display label;
- lifecycle status;
- Ruleset binding;
- Dataset schema identity;
- or application configuration.

Changing descriptive metadata does not inherently create a new story instance.

Splitting, cloning, importing, forking, or otherwise creating a distinct story
instance requires distinct identity where the resulting work may diverge
independently.

Detailed identifier representation is Planning.

## Story Metadata

A Dataset may carry author-useful descriptive metadata such as:

- title;
- subtitle;
- series information;
- project notes;
- genre labels;
- intended audience;
- target length;
- descriptive tags;
- author-facing labels;
- or other useful non-semantic project information.

Metadata exists to support organization, display, search, filtering, workflow,
or author convenience.

Metadata must not silently substitute for Canon, Plot, Prose, production-control,
or Manuscript meaning.

If a value materially constrains story meaning, generation, acceptance, or
semantic interpretation, that constraint must have an appropriate governed home
rather than relying on an incidental metadata field.

## Metadata Authority

Metadata may itself be authoritative for its own operational or descriptive
purpose without becoming story-semantic authority.

For example, a story title may be authoritative as the current project title
without becoming Canon.

Likewise, a workflow label may be authoritative for scheduling or UI behavior
without becoming Plot or Manuscript meaning.

The Product must preserve the distinction between metadata authority and story
semantic authority.

## Story Status

A story may use operational lifecycle concepts such as:

- template;
- development;
- drafting;
- revision;
- complete;
- archived;
- or another useful project state.

Lifecycle status should be introduced only when it has demonstrated behavioral or
authoring value.

If status affects governed behavior, its meaning and transitions must be defined
rather than inferred from arbitrary strings.

Story status does not by itself:

- accept or reject semantic state;
- approve production controls;
- accept Manuscript;
- complete reconciliation;
- make validation current;
- or establish publication readiness.

Those concerns remain governed by their owning semantics.

## Generated Author Views

Authors need human-readable ways to inspect, navigate, compare, and reason about
governed story state.

Generated author views are projections of governed sources.

They are not independent semantic layers.

Useful views may include:

- character dossiers;
- setting encyclopedia entries;
- chronology views;
- Event histories;
- relationship summaries;
- character arc summaries;
- reveal maps;
- viewpoint-access summaries;
- knowledge and belief summaries;
- scene-relevant Canon briefs;
- Plot summaries;
- Prose-guidance summaries;
- generation-package summaries;
- candidate comparison views;
- validation or semantic-review reports;
- reconciliation reports;
- Manuscript impact views;
- migration reports;
- or other author-facing projections.

The existence of a view type does not require a corresponding storage partition
or semantic ontology.

## Projection Principle

A generated view derives from governed source state.

A view may project:

- one semantic surface;
- several semantic surfaces;
- accepted and candidate state together;
- production controls;
- derived review evidence;
- historical state;
- or another useful combination.

Combining material in one human-facing view does not combine its semantic
ownership.

The view must preserve enough distinction for the author and system to know what
the represented material means and where edits belong.

## Projection Context

A view should preserve, as applicable:

- source identity and semantic scope;
- owning semantic surface;
- accepted, candidate, production-approved, generated, derived, unresolved, or
  other relevant status;
- revision or version identity;
- temporal scope;
- viewpoint or focalization scope;
- objective truth versus knowledge, belief, memory, misunderstanding, rumor, or
  unresolved status;
- reader-information intent where relevant;
- projection freshness;
- and traceability needed for safe author action.

Not every view needs to display all such information visibly.

The Product must preserve enough of it to avoid authority confusion and unsafe
edit interpretation.

## Character Dossiers

A character dossier may assemble author-useful material such as:

- identity;
- background;
- current and historical state;
- motives;
- values;
- fears;
- capabilities;
- behavioral tendencies;
- knowledge;
- beliefs;
- memories;
- misunderstandings;
- relationships;
- relevant Events;
- transformations;
- unresolved questions;
- Plot-relevant context;
- and other useful material.

The dossier itself is not durable Character authority merely because it is
convenient or comprehensive.

Different dossier sections may project different Canon scopes, Plot context,
candidate proposals, review findings, or production information.

Their ownership must remain distinct.

## Setting and World Views

A setting or world view may combine geography, institutions, culture, rules,
history, current conditions, relevant Events, and other author-useful material.

Such a view does not require "Setting" to be a mandatory physical storage domain.

The view projects governed meaning from wherever that meaning is owned.

## Chronology Views

A chronology view may project accepted and candidate temporal information from
Canon.

It may display:

- exact dates;
- relative ordering;
- intervals;
- approximate placement;
- unknown placement;
- intentional ambiguity;
- or competing candidate interpretations.

The view must not manufacture false temporal precision merely to produce a neat
timeline.

Plot presentation order and Manuscript order remain distinct from Canon
chronology.

## Reveal and Knowledge Views

A reveal or knowledge view may combine:

- objective Canon truth;
- Character knowledge and belief;
- Plot reader-information intent;
- viewpoint access;
- and Manuscript realization.

Such a view is especially useful because these concepts are related but owned by
different semantic surfaces.

The view must preserve those distinctions rather than flattening them into a
single "who knows what" authority.

## Review and Reconciliation Views

Validation, semantic-review, and reconciliation reports are derived views.

They may summarize:

- affected scopes;
- review outcomes;
- stale dependencies;
- contradictions;
- unresolved questions;
- blocking findings;
- candidate assumptions;
- or recommended next actions.

They remain evidence and workflow aids.

They do not become story truth or acceptance authority.

## Editing Generated Views

An author may edit through a generated view.

Such an edit is interpreted as a proposed operation against the underlying
governed target or targets.

Editing rendered text does not silently:

- transfer semantic ownership to the view;
- overwrite accepted source state;
- accept candidate meaning;
- approve production controls;
- revise Manuscript;
- or create Canon.

The Product must map consequential edits back to their appropriate owning
surfaces before they become authoritative.

## Coordinated View Edits

One human-facing edit may imply several governed changes.

For example, changing a Character's age may affect:

- Character state;
- chronology;
- historical Events;
- relationship timing;
- accepted future occurrence;
- downstream Plot assumptions;
- production controls;
- or Manuscript reconciliation.

The Product may present this as one author action while preserving the distinct
semantic operations and acceptance scopes involved.

Convenient editing does not justify collapsing semantic ownership.

## Ambiguous View Edits

A rendered edit may not map unambiguously to one governed operation.

When a consequential interpretation is ambiguous, the Product must:

- preserve the edit as a proposal;
- narrow the target;
- request author resolution;
- or otherwise surface the ambiguity.

It must not silently choose the broadest or most convenient interpretation.

The Product does not require arbitrary natural-language edits to be perfectly
invertible.

## View Regeneration

Several views may display the same governed meaning.

This duplication does not create multiple authorities.

Generated views should therefore be regenerated or refreshed from current
governed sources rather than treating older rendered copies as competing truth.

If a view contains author-customized presentation such as:

- section order;
- collapsed regions;
- display labels;
- annotations;
- filters;
- layout;
- or other presentation preferences,

those preferences may be persisted separately from projected story meaning.

## View Freshness

A generated view may become stale when a material source changes.

A stale view must not continue to be presented as current when that staleness
could mislead governed authoring or generation.

The Product should be able to:

- refresh the view;
- mark it stale;
- identify affected regions;
- or reconstruct it on demand.

Exact freshness tracking is Planning.

View freshness does not change source authority.

## Persisted Views

A generated view may be persisted when doing so improves:

- author navigation;
- performance;
- offline use;
- comparison;
- history;
- diagnosis;
- export;
- or another demonstrated workflow.

Persistence does not change the view's derived status.

Where safe regeneration is possible, the Product may prefer rebuilding the view
from sources rather than migrating or preserving every historical rendering.

## Editable Presentation Metadata

Presentation preferences may be author-owned without becoming story semantics.

Examples include:

- dossier section ordering;
- preferred labels;
- display grouping;
- UI expansion state;
- visual filters;
- report layout;
- or export formatting.

Such metadata should remain separate from semantic state when mixing them would
create authority confusion.

## Derived Summaries

Summaries generated from governed state remain derived unless intentionally
accepted into an owning semantic surface.

A summary may omit detail.

Omission does not delete source meaning.

A summary may paraphrase source meaning.

Paraphrase does not replace the source.

A summary may combine multiple sources.

Combination does not create new semantic ownership.

## Diagnostic Inference

Generated views may contain diagnostic inference, such as:

- likely reader interpretation;
- possible continuity risk;
- suspected contradiction;
- predicted emotional effect;
- or inferred thematic pattern.

Diagnostic inference must remain distinguishable from governed story meaning.

A model's plausible inference is not Canon, Plot intent, Prose guidance, or
Manuscript authority unless separately proposed and accepted at the owning
surface.

## Search and Navigation Views

Search results, semantic retrieval, indexes, link maps, and navigation panels are
views over governed state.

Search prominence, embedding similarity, ranking, or model confidence does not
determine authority.

Where a precise identity or traceability relationship is already known, a
navigation view should prefer that governed relationship over fuzzy matching.

## Exported Views

An export may contain:

- Manuscript;
- generated views;
- metadata;
- reports;
- or combinations of these.

Exporting material does not change its authority classification.

An exported character dossier remains derived unless separately accepted into an
owning semantic surface.

An exported accepted Manuscript remains accepted Manuscript.

The export container itself does not redefine ownership.

## Extensibility Principle

The Product may evolve to support additional:

- Canon concepts;
- Plot concepts;
- Prose guidance;
- production controls;
- generated views;
- metadata;
- relationships;
- validation criteria;
- workflow concepts;
- or authoring features.

Extensions must preserve the established authority and ownership boundaries.

A new feature must not acquire semantic authority merely because it stores or
displays story information.

## New Semantic Concepts

When a proposed extension introduces consequential story meaning that does not
fit an existing owning semantic surface, that is a Product Design question.

Planning must not create a new semantic authority class merely to accommodate a
schema field or implementation feature.

A genuinely new semantic concept requires intentional Design placement within
the architecture.

## New Metadata

New metadata may be added without new Product Design when it is purely
descriptive, operational, or presentational and does not alter existing semantic
meaning or authority.

If metadata begins to govern generation, acceptance, interpretation, or
downstream reasoning materially, its role must be designed explicitly.

The Product must not smuggle semantic requirements into "metadata" merely to
avoid Design work.

## Unknown Fields and Forward Extensibility

A newer realization may contain fields or structures unknown to an older one.

Unknown material must not be treated as permission to invent semantics.

An implementation may:

- preserve unknown material opaquely;
- expose it for inspection;
- ignore it for operations where doing so is declared safe;
- restrict operations;
- require migration;
- or refuse governed use.

It must not silently reinterpret unknown material into a familiar but different
semantic role.

Compatibility behavior follows DP-170.

## Extensions and Authority

An extension may define:

- a new view;
- new metadata;
- a new validator;
- a new export;
- a new production-control representation;
- or another capability.

None of those additions changes Canon, Plot, Prose, or Manuscript ownership
unless Product Design explicitly says so.

The default extension rule is preservation of existing authority boundaries.

## Avoiding Accidental Schema Authority

Examples, templates, initial Dataset skeletons, test fixtures, file layouts,
generated runtime structures, existing implementations, and historical artifacts
do not independently define Product meaning.

Normative structural behavior belongs to Planning and specifications derived from
reviewed Product Design.

A schema may encode Product meaning.

It does not create Product meaning merely by containing a field.

## Avoiding Mandatory Storage Ontology

Character, Setting, Event, chapter, scene, dossier, report, and other useful
author-facing concepts do not automatically imply mandatory storage partitions.

The Product defines semantic concepts and authority boundaries.

Planning may choose physical decomposition that serves implementation,
performance, author usability, migration, or validation.

Storage layout must not silently redefine semantic ownership.

## Avoiding Excessive Identity

Stable identity is required where durable targeting, dependency, provenance,
migration, reconciliation, or cross-session reference materially requires it.

The Product does not require governed identity for every:

- sentence;
- word;
- adjective;
- incidental detail;
- temporary prompt;
- conversational utterance;
- transient search result;
- or ephemeral intermediate.

Identity granularity follows DP-175 and demonstrated control value.

## Avoiding Excessive Provenance

The Product does not require generalized lineage linking every Manuscript phrase
through every prompt, model token, search result, and intermediate artifact.

Traceability should be as light as possible while still supporting:

- continuity;
- author control;
- acceptance;
- reconciliation;
- local regeneration;
- review;
- migration;
- and diagnosis.

More provenance is not inherently more correct.

## Avoiding Excessive Status Taxonomy

The Product should not create large status taxonomies merely to classify every
intermediate condition.

Status distinctions are justified when they change:

- author understanding;
- allowed operations;
- validation behavior;
- acceptance;
- persistence;
- migration;
- or another material workflow outcome.

Where no behavior depends on a distinction, additional status vocabulary adds
governance burden without Product value.

## Avoiding Excessive Registries

The Product does not require one universal registry containing every artifact,
identity, relationship, view, status, validation result, and workflow object.

Registries, manifests, or indexes may be introduced where they solve a concrete
problem.

They must not become shadow semantic authority merely because other tooling reads
them.

## Avoiding Excessive Workflow Ceremony

The Product exists to reduce AI drift and preserve author control.

It does not require visible transactions, proof objects, confirmation objects,
startup receipts, operation journals, mode banners, or multi-step approval
ceremony for every ordinary action.

Such mechanisms may be justified when they materially improve safety,
recoverability, or author confidence.

They are not Product goals in themselves.

## Avoiding False Precision

The Product must not force exact values or completed decisions merely because
they are easier to represent or validate.

Valid governed state may include:

- unknown values;
- partial information;
- approximate chronology;
- bounded ranges;
- intentionally unresolved questions;
- accepted ambiguity;
- candidate alternatives;
- incomplete refinement;
- or not-yet-developed story areas.

False precision is semantic drift.

## Avoiding Premature Completion

The Product must not treat an incomplete story as invalid merely because some
possible fields, relationships, scenes, or decisions have not yet been filled.

Completeness is scope- and operation-relative.

A generation task may require a particular reveal decision without requiring the
entire novel's chronology to be complete.

A scene may be production-ready while unrelated future chapters remain largely
undeveloped.

## Avoiding Fixed Development Order

The Product uses progressive refinement to bound generation work.

That does not require the author to develop the entire story in one fixed global
order.

The author may move between:

- Canon;
- Plot;
- Prose guidance;
- production refinement;
- Manuscript;
- review;
- reconciliation;
- and generated views,

provided governed dependencies and authority boundaries remain explicit.

Top-down refinement is required for a generation task to become reliably bounded,
not as a compulsory whole-project authoring sequence.

## Avoiding Universal Granularity

The Product does not require every story or task to use the same:

- number of Plot levels;
- Beat size;
- paragraph count;
- scene size;
- package size;
- identity granularity;
- review scope;
- or refinement depth.

Granularity should be chosen by reliability and authoring value.

The smallest possible unit is not automatically the safest or best unit.

## Avoiding Hidden Defaults

Defaults may reduce author effort.

A default must not silently create consequential story meaning.

Defaults may safely fill:

- presentation preferences;
- mechanically determined representation;
- explicitly author-approved conventions;
- or other non-consequential values.

Where a default would choose consequential Canon, Plot, Prose intent, production
intent, reveal timing, or Manuscript wording, it must remain a proposal or require
governed authorization.

## Human Readability

Author-facing state should remain understandable without requiring the author to
reason directly about internal IDs, schemas, registries, migration machinery, or
validation implementation.

Machine structure exists to preserve the author's story.

The story does not exist to satisfy the structure.

Human-facing views should prefer meaningful names, labels, context, and narrative
organization while preserving precise underlying identity and scope.

## Human Editability

Where practical, the Product should let authors work through familiar story
concepts such as:

- characters;
- events;
- scenes;
- chapters;
- relationships;
- timelines;
- reveal plans;
- prose guidance;
- and Manuscript text.

The Product should not require authors to manipulate raw storage structures for
ordinary work when safe higher-level interaction is possible.

Convenience must still preserve semantic ownership and traceability.

## Progressive Disclosure

Governance detail should be shown when it helps the author make a safe decision.

The Product need not expose every dependency, identifier, review record, or
authority label at all times.

Interfaces may progressively disclose:

- source ownership;
- candidate status;
- affected dependencies;
- stale views;
- validation findings;
- or migration detail

when those distinctions become relevant.

Hiding complexity for usability must not erase the underlying distinction.

## Author Override

The author may intentionally choose to proceed despite advisory findings,
subject to blocking integrity requirements established elsewhere in Product
Design or approved Planning.

An override does not convert a failed criterion into a passing criterion.

It records or permits an intentional workflow decision where such discretion is
allowed.

The Product should distinguish author judgment from validator conclusion.

## Portability

Core story meaning should remain portable enough that the Dataset does not depend
on one specific UI or generated-view format for interpretation.

A generated dossier format may change.

A timeline renderer may be replaced.

A report layout may evolve.

The underlying governed story state must remain interpretable independently of
those presentation mechanisms.

## Degraded Presentation

Failure to render a generated view must not inherently make the underlying
governed story state unavailable or invalid.

Where source state remains interpretable, the Product should prefer degrading the
presentation capability rather than treating a view-rendering defect as loss of
story meaning.

This does not prevent a view from being required for a particular workflow when
Planning explicitly establishes that requirement.

## Extensibility Test

The Product should support at least these scenarios:

1. A character dossier combines accepted Canon, candidate Canon, Plot context,
   and review findings without becoming a competing Character authority.
2. Editing a dossier field proposes a change to the underlying governed scope
   rather than silently overwriting the dossier as truth.
3. A stale chronology view is refreshed after Canon changes without changing
   Canon itself.
4. Adding a descriptive project tag does not require a new semantic layer.
5. A new field that materially governs reveal timing is recognized as a semantic
   design concern rather than hidden metadata.
6. An older implementation encounters an unknown extension field and restricts or
   preserves it instead of inventing meaning.
7. A story remains usable if a generated report or dossier renderer fails.
8. The Product can add a new author view without requiring a new storage domain.
9. The Product can leave a future event date approximate rather than forcing an
   exact value for schema convenience.
10. A generation task can be deeply refined while unrelated portions of the novel
    remain incomplete.

Failure of these scenarios indicates that presentation, metadata, or framework
machinery has begun to govern the story instead of serving it.

## Simplicity Invariant

Every new structural mechanism should justify itself by materially improving at
least one of:

- reduction of AI hallucination or drift;
- cross-session continuity;
- bounded generation reliability;
- author control;
- semantic integrity;
- safe persistence;
- reconciliation;
- migration;
- review;
- or author usability.

If a mechanism adds ceremony, state, identity, provenance, status, or indirection
without demonstrated value in one of these areas, the Product should prefer the
simpler design.

## Planning Boundary

This Design defines generated-view semantics, metadata boundaries, view editing,
projection freshness, extension authority, forward-extensibility behavior, human
readability, portability, and Product simplicity constraints.

Planning may choose:

- metadata schemas;
- generated-view formats;
- rendering technology;
- projection mechanisms;
- edit-translation workflows;
- view freshness tracking;
- cache behavior;
- extension points;
- unknown-field preservation;
- UI behavior;
- report layouts;
- export formats;
- lifecycle-status representation;
- registries or indexes;
- and other technical realization.

Planning and implementation must not turn presentation, metadata, defaults,
schemas, registries, or convenience mechanisms into shadow semantic authority.
