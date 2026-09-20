---
functional_set: FS-006
artifact: functional-set-scope
title: Governed Editable Generated Author Views
design_revision: 22b8f2dcb3ff22b1ff1613fb965353dd2917d443
---

# FS-006 — Governed Editable Generated Author Views

## Purpose

FS-006 realizes the next bounded author-workshop capability already defined by
Product Design: durable, human-oriented generated views that can be inspected,
refreshed, compared, and edited through without becoming shadow story authority.

FS-005 established derived author views over current governed state but
intentionally deferred sophisticated editable dossiers. FS-006 extends that
surface while preserving the authority, identity, revision, dependency,
reconciliation, compatibility, persistence, and acceptance semantics already
established by FS-001 through FS-005.

The principal demonstration is a Character dossier because DP-190 defines it as a
representative multi-source author view. The architecture must remain generic
enough that later Setting, chronology, reveal, knowledge, reconciliation, and
other generated views can use the same projection/freshness/edit-through
contract without creating a universal view ontology.

## Exact Design Binding

Planning consumes Product Design at repository revision:

`22b8f2dcb3ff22b1ff1613fb965353dd2917d443`

FS-006 introduces no new Product Design. It selects already accepted obligations
primarily from DP-175 and DP-190, with applicable authority, revision,
reconciliation, persistence, compatibility, and review semantics from DP-100
through DP-180.

## Functional Boundary

FS-006 begins with a compatible external Story Writer Dataset and the FS-005
author-workshop runtime capable of reconstructing governed state and producing
derived overview projections.

FS-006 ends when the Product can:

1. construct an identifiable Character dossier projection from current governed
   sources without making the dossier a story-semantic authority surface;
2. preserve source identity, semantic ownership, source revision, authority
   status, and projection freshness information sufficient for safe author use;
3. regenerate a dossier from current governed sources;
4. detect when a persisted or previously rendered dossier is stale because a
   material source changed;
5. represent presentation-only dossier preferences separately from story meaning;
6. interpret an author edit to a dossier as a proposed governed edit against the
   underlying owning source or sources;
7. refuse silent application when an edit is ambiguous about its governed target;
8. refuse silent application when the view is materially stale relative to the
   targeted governed source;
9. route unambiguous consequential edits into existing candidate/revision
   operations rather than directly mutating accepted state;
10. preserve multi-surface ownership when one human-facing edit implies several
    governed operations;
11. expose comparison between current governed projection and a proposed edited
    projection without treating the comparison as acceptance evidence;
12. persist optional derived-view state only when useful while retaining its
    derived classification and reconstructability from authoritative sources.

## Reference Demonstration

The executable demonstration shall construct a Character dossier from accepted
Canon plus relevant Plot/candidate context, persist or retain a view snapshot,
change a material governed source, prove the prior view stale, regenerate it,
apply one unambiguous edit through the dossier into a governed candidate or
revision path, refuse one ambiguous edit, preserve a presentation-only preference
without changing story meaning, and prove that neither rendering nor editing the
view itself accepts semantic state.

## Agent Boundary

The agent may summarize, organize, compare, explain, and propose mappings from
human edits to governed operations. Deterministic runtime behavior owns
mechanically decidable source attribution, freshness checks, identity/revision
matching, candidate/revision routing, and persistence classification.

When semantic interpretation of an edit is consequentially ambiguous, the agent
must surface the ambiguity rather than silently choose a target.

## Explicit Deferrals

FS-006 does not require arbitrary natural-language edit inversion, graphical UI
implementation, provider-specific model calls, collaborative editing, multi-user
merge resolution, generalized document patch languages, universal generated-view
schemas, exhaustive view caching, story-wide search indexing, publication
formatting, or full split/merge/supersession tooling.

## Completion Criterion

FS-006 is complete when an author can use a generated Character dossier as a
safe working projection: inspect it, refresh it, preserve presentation
preferences, propose governed changes through it, and receive stale/ambiguous
edit protection without the dossier becoming a competing source of story truth.
