---
doc_id: DP-160
title: Dataset Persistence and Session Reconstruction
depends_on:
  - DP-100
  - DP-110
  - DP-120
  - DP-130
  - DP-140
  - DP-150
---

# Dataset Persistence and Session Reconstruction

## Purpose

The Dataset is the durable project workspace for one story instance.

It preserves governed story state across sessions so that the Product does not
depend on chat history, model memory, or an uninterrupted authoring session for
continuity.

Persistence preserves state and authority classification.

It does not create semantic authority merely because material survives a save.

## Dataset as Durable Memory

The Dataset is the Product's durable story memory.

A fresh session must be able to reconstruct the governed project state needed
for continued work from persisted Dataset state together with the applicable
and compatible Product or Ruleset definition.

Compatibility and migration semantics are defined by DP-170.

Prior conversation may be useful historical context, but it is not required for
authoritative continuity.

The Product must not require the model to remember earlier conversations in
order to recover accepted story meaning, persisted candidate work, production
controls, or current reconciliation state.

## Persisted Authority

Accepted governed state persisted in the Dataset is persisted story authority
within its owning semantic surface.

Persisted candidate state remains candidate.

Persisted production-approved state remains production control rather than
Canon, Plot, or Manuscript authority.

Persisted generated text remains candidate unless accepted according to DP-110.

Persistence must preserve enough classification to prevent a later session from
mistaking survival for acceptance.

## Conversation Boundary

Conversation is operational context, not durable project authority.

A statement made in chat does not become governed story state merely because it
was useful, repeated, summarized, or remembered by the model.

Conversation-derived meaning becomes durable only through the governed
proposal, approval, acceptance, and persistence behavior appropriate to its
owning surface.

The Product may persist an explicit summary, decision, candidate, note, or other
artifact derived from conversation.

Once persisted, that artifact is governed according to its stored role and
authority class, not according to the conversation from which it originated.

## Fresh-Session Reconstruction

A fresh session begins without assuming access to prior chat reasoning.

Before governed work continues, the Product must be able to reconstruct enough
project state to determine, as applicable:

- story identity;
- accepted Canon;
- accepted Plot;
- persistent Prose guidance;
- accepted Manuscript;
- intentionally persisted candidate work;
- production-approved controls;
- material candidate dependencies and assumptions;
- unresolved reconciliation state;
- applicable generation-package provenance where relevant;
- and other persisted state required to interpret the current task.

Reconstruction does not mean eagerly loading the entire Dataset into model
context.

Its purpose is to establish an interpretable governed project state, preserve
authority classification, and make reliable task-specific retrieval possible.

Task-specific retrieval then selects the material needed for the current work.

## Reconstruction Correctness

Session reconstruction must preserve semantic ownership and authority class.

A reconstructed session must not:

- treat candidate material as accepted;
- treat production approval as semantic acceptance;
- treat accepted Manuscript wording as upstream Canon or Plot authority;
- infer missing acceptance from repeated use;
- infer authority from file location or naming alone;
- or treat prior conversation memory as a substitute for persisted governed
  state.

Where persisted state is ambiguous about authority or dependency, the session
must surface that ambiguity rather than silently choosing the more authoritative
interpretation.

When persisted role or authority classification cannot be established reliably,
the artifact must be treated as unresolved for governed use rather than promoted
by inference.

## Retrieval

The Dataset may be larger than the context window used for any one task.

The Product must therefore support retrieval of task-relevant persisted state.

Retrieval should be guided by the current task, declared dependencies, stable
identity, semantic scope, chronology, viewpoint, and other governed
relationships where useful.

Search convenience does not determine authority.

A retrieved artifact carries the authority of its persisted governed role, not
the confidence of a search system or the prominence of a search result.

## Retrieval Completeness

A retrieval result used for governed work must be sufficient for the task.

When material dependencies are known, the Product must retrieve or otherwise
make available the state necessary to satisfy them.

If retrieval is incomplete or uncertain, the Product must surface that
condition, refine the query or task, or defer governed generation.

It must not fill retrieval gaps from model memory, generic genre expectation, or
unstated inference when doing so could introduce consequential meaning.

## Working State

Active working state is initialized from persisted Dataset state and may contain:

- unchanged persisted accepted state;
- accepted-but-not-yet-persisted revisions;
- persisted candidate state;
- newly created candidate state;
- persisted or new production-control state;
- declared candidate assumptions and dependencies;
- generated prose candidates;
- reconciliation work;
- and other governed session-local work.

Working state may therefore be newer than the last persisted Dataset state.

During the active session, current accepted-but-unpersisted changes govern
subsequent work at their accepted scope.

They do not become persisted recovery state until successfully saved.

## Persistence Classes

The Product must be able to persist more than accepted semantic state.

Persistable governed state may include, as applicable:

- accepted semantic state;
- accepted Manuscript;
- persisted candidate semantic state;
- persisted candidate prose;
- production-approved controls;
- candidate production controls;
- generation packages or sufficient provenance for them;
- reconciliation state;
- generated views or preferences when intentionally durable;
- and metadata required to interpret the above.

The Product may omit ephemeral intermediate material that has no continuity
value.

Persistence selection must not blur authority classes.

## Candidate Continuity

Candidate work may be intentionally persisted so that exploration can continue
across sessions without premature acceptance.

Persisted candidate dependencies must remain interpretable in a later session.

Where a candidate materially depends on another candidate or assumption, the
Dataset must preserve enough dependency or provenance information to avoid
presenting the dependent artifact as independently grounded.

Candidate persistence is a continuity mechanism.

It is not semantic promotion.

## Production-Control Continuity

Production-control artifacts may need to survive across sessions.

Examples include:

- production contracts;
- Beats;
- pseudo-prose or near-prose layouts;
- resolved style projections where intentionally persisted;
- production approvals;
- generation-package provenance;
- protected-material rules;
- and local regeneration state.

Persisting these artifacts preserves production continuity.

It does not create Canon, Plot, or Manuscript authority.

## Save Authorization

Persistence requires an authorized save operation.

Save authorization is distinct from semantic acceptance, production approval,
and Manuscript acceptance.

An accepted semantic change may remain unpersisted.

A candidate may be persisted without being accepted.

A production-control artifact may be persisted without being
production-approved.

The Product must not collapse these actions into one implicit meaning.

## Save Scope

The Product may support saving:

- all current governed state;
- accepted state while omitting unrelated candidate work where coherence is
  preserved;
- selected candidate work required for later continuation;
- selected production-control state;
- or another specifically authorized coherent subset.

A partial save must not knowingly produce a persisted state that cannot be
interpreted correctly.

It must not separate a persisted dependent artifact from material assumptions,
dependencies, authority classification, identity, production controls, or
generation provenance needed to understand that artifact.

A generated candidate whose later interpretation materially depends on a
generation package must not be persisted without retaining the package or enough
equivalent provenance to identify what governed that generation attempt.

## Save Coherence

A successful save produces one coherent authorized persisted Dataset state.

A partial physical write must not be treated as a successful logical save.

If a save spans several physical artifacts, the Product must avoid presenting a
mixed pre-save and post-save state as the completed result.

Filesystem writes, transactions, Git commits, databases, object stores, or
other persistence mechanisms are Planning choices.

The Product requirement is logical coherence.

## Save Failure

If persistence fails, the Product must not claim that the new Dataset state is
durably saved.

Accepted-but-unpersisted working state may continue to govern the current active
session if it remains available.

The persisted Dataset remains the recovery baseline for a future fresh session
unless a separately defined recovery mechanism preserves newer state.

Failure handling must preserve the distinction between operational working state
and durable persisted state.

## Session Loss

Unsaved ephemeral working state is not assumed to survive session loss.

Any candidate, production control, generated passage, reconciliation decision,
or accepted revision that must survive into a future session requires
persistence or an explicitly governed recovery mechanism.

The Product must not depend on hidden chat retention as recovery.

## Autosave

An implementation may support autosave only when its semantics are explicit.

Autosave must not silently:

- accept candidate meaning;
- grant production approval;
- change Manuscript acceptance;
- redefine the user's understood persistence boundary;
- or persist sensitive or intentionally ephemeral work contrary to governed
  policy.

Autosave changes durability, not authority.

## External Change and Concurrency

Persisted Dataset state may change after a working session begins.

The Product must not silently overwrite newer persisted state with stale working
state.

A conflicting save must be detected before successful persistence.

Resolution may involve reload, comparison, reconciliation, merge, user choice,
or another governed process.

Concurrency tokens, Git comparisons, revision identifiers, merge strategy, UI,
and recovery mechanics are Planning decisions.

## Dataset Content

A Dataset must be capable of persisting, as applicable:

- story identity and metadata;
- accepted and intentionally persisted candidate Canon;
- accepted and intentionally persisted candidate Plot;
- accepted persistent Prose guidance;
- candidate and production-approved Prose controls;
- accepted Manuscript text and ordering;
- persisted generated prose candidates;
- candidate assumptions and dependencies;
- reconciliation state;
- stable identities and material relationships;
- generation-package provenance where needed;
- generated-view preferences when intentionally durable;
- schema or format identity required to interpret the Dataset;
- and other state required for reliable session reconstruction.

The exact physical decomposition is a Planning decision.

## Durable Identity

Persistence across sessions requires durable identity where artifacts or semantic
regions participate in dependency, revision, reconciliation, ordering,
generation provenance, or cross-session targeting.

A later session must not need to infer identity solely from filename, title,
array position, conversational description, or incidental ordering when such
inference could target the wrong governed material.

Detailed identity and traceability semantics are defined by DP-175.

## Derived and Reconstructable State

Not every useful author-facing or operational representation must be persisted
directly.

The Product may reconstruct derived views, indexes, summaries, caches, or
resolved projections from persisted governed state when doing so preserves
meaning and authority classification.

A persisted derived artifact remains derived. Persistence does not grant it
semantic authority merely because recomputing it is expensive or inconvenient.

Derived reconstruction must not invent missing consequential meaning.

If reconstruction cannot be performed without choosing among materially
different interpretations, the result must be surfaced as unresolved rather
than silently synthesized.

## Dataset and Generation Packages

Generation packages defined by DP-150 are bounded execution contexts.

The Dataset need not retain every physical package forever.

It must preserve enough package provenance for any persisted generated candidate
whose later review, regeneration, or acceptance materially depends on knowing
what governed that generation attempt.

If the package itself is not retained, equivalent governing context must remain
identifiable.

## Recovery Baseline

The persisted Dataset is the ordinary fresh-session recovery baseline.

Where a separately governed recovery mechanism retains newer unsaved state, that
state must remain distinguishable from the last successful Dataset save.

Recovered accepted working state may resume operational authority at its
previous accepted scope when the recovery mechanism preserves its identity,
authority class, and dependencies reliably.

Recovered state is still not durable Dataset state until successfully persisted.

Recovered candidate and production-control material retain their prior status.

Recovery tooling must not convert recovered candidate or working material into
accepted state merely because it was recovered successfully.

## Persistence Boundary

Ordinary story persistence mutates Dataset-owned project state.

It must not silently mutate Product or Ruleset definitions, schemas owned
outside the Dataset, application configuration, construction provenance, or
other external governing definitions.

A separately governed operation may change those materials when appropriate.

Ordinary story save is not such an operation.

## Continuity Test

The Product should be able to pass the following continuity test:

1. Persist a project containing accepted story state, selected candidate work,
   production controls, and unresolved dependencies.
2. End the conversation.
3. Begin a fresh session with no prior chat history.
4. Reconstruct the project from persisted state.
5. Retrieve the dependencies for a bounded task.
6. Continue governed work without treating candidate state as accepted or
   inventing missing consequential meaning from memory.

Failure of this test indicates that durable continuity depends on conversation
rather than the Dataset.

## Simplicity Boundary

The Product requires durable, interpretable, authority-preserving persistence
and reliable fresh-session reconstruction.

It does not require elaborate startup ceremonies, proof objects, status
registries, transaction logs, hashes on every file, or persistent caches merely
because a reference implementation uses them.

Additional persistence machinery requires demonstrated value for continuity,
integrity, recovery, concurrency, or author control.

## Planning Boundary

This Design defines Dataset persistence semantics, working-state behavior,
authority-preserving save behavior, candidate continuity, session
reconstruction, retrieval expectations, and recovery boundaries.

Planning may choose file layout, database structure, transaction strategy, Git
usage, autosave implementation, indexes, caches, retrieval technology,
concurrency tokens, recovery mechanisms, revision storage, and other technical
realization.

Implementation convenience does not justify dependence on chat history,
authority loss, candidate promotion, incoherent saves, or unrecoverable
cross-session state.
