---
doc_id: DP-140
title: Canon State, Events, Knowledge, and Narrative Time
depends_on:
  - DP-100
  - DP-110
  - DP-120
  - DP-130
---

# Canon State, Events, Knowledge, and Narrative Time

## Purpose

Canon represents accepted story reality through both state and occurrence.

The Product must preserve coherence between what is true, what happened, what is
known or believed, and when those meanings hold without collapsing them into one
representation.

Canon semantics must remain usable for long-form continuity, bounded generation,
and revision without requiring the Product to reconstruct story truth from
conversation history or from generated prose.

## Canon State and Occurrence

Canon includes both persistent or temporally scoped state and accepted
occurrence.

State describes what is true at a relevant time or interval.

Occurrence describes what happens, changes, begins, ends, or is established.

Neither is reducible to the other.

Current state must not erase meaningful historical occurrence.

Historical occurrence must not be inferred solely from current state.

The Product may preserve both direct state assertions and Events where doing so
improves continuity and reasoning.

## Canon Domains

Character, Setting, Events, relationships, knowledge, chronology, and other
useful categories are semantic domains or views of Canon.

They are not mandatory physical storage partitions.

A truth that spans several domains must not be duplicated into competing
authorities merely to fit an author-facing taxonomy.

Planning may choose storage organization independently from semantic ownership.

## Character State

Character Canon may include story-relevant state such as:

- identity and background;
- physical condition;
- capabilities and limitations;
- values, motives, fears, vulnerabilities, and intentions;
- relationships;
- behavioral and perceptual tendencies;
- knowledge, belief, misunderstanding, and memory;
- temporally scoped conditions;
- and accepted transformation.

Character state should be concrete enough to constrain later reasoning where
that improves continuity.

Abstract labels may be useful, but they should not be the only representation
when a concrete tendency, trigger, limit, decision pattern, or behavioral
constraint more reliably preserves accepted character meaning.

Facts about habitual speech, perception, or cognition may belong to Canon when
they are story truth.

Their linguistic realization belongs to Prose.

## Setting and World State

Setting Canon includes authoritative world truth beyond scenery.

It may include geography, environment, institutions, factions, social systems,
culture, law, technology, infrastructure, natural or supernatural rules,
objects and ownership, and other world conditions that materially constrain
story reasoning.

Setting truth may affect behavior, expectation, causality, conflict, and subtext
even when it is never explicitly explained to the reader.

This section defines semantic scope only.

It does not require a dedicated Setting storage partition.

## Events

An Event is accepted Canon occurrence whose identity or effects matter to
durable story reasoning.

An Event may:

- establish state;
- terminate state;
- transform state;
- change a relationship;
- change knowledge or belief;
- establish causality;
- create consequences;
- or provide a historical anchor for later reasoning.

Not every incidental action in prose must become a durable Canon Event.

Event granularity should follow semantic usefulness.

## State-Event Coherence

When an accepted Event materially changes Canon state, the resulting accepted
state must remain coherent with the accepted occurrence.

The Product must not knowingly preserve an accepted Event and an accepted state
that materially contradict one another.

This requirement does not imply that every state value must be mechanically
derived from a complete event history.

Likewise, storing current state directly does not eliminate the need to preserve
historically meaningful Events.

The Product may therefore use state assertions, Events, or both as long as their
accepted meanings remain coherent.

## Event Effects

An Event may have direct and indirect effects.

Direct effects are Canon changes intentionally established by the Event.

Indirect consequences may be known, unresolved, delayed, conditional, or
discovered later.

The Product must not invent consequential Event effects merely to make a state
transition appear complete.

Where an Event implies a material change but the resulting Canon meaning is not
yet resolved, that unresolved meaning remains candidate according to DP-110.

## Accepted Future Occurrence

Chronological futurity does not make accepted story meaning non-canonical.

An occurrence accepted by the author as part of story reality may be Canon even
when it:

- is future relative to current scene work;
- has not yet appeared in Plot;
- has not yet been revealed to the reader;
- has not yet been realized in Prose;
- or has not yet appeared in Manuscript.

A proposed future occurrence remains candidate Canon until accepted.

Downstream candidate work may depend on that proposal when the dependency is
declared according to DP-120.

Accepted future Canon is not a prediction.

It is author-approved story reality subject to later intentional revision.

## Historical, Current, and Future State

Canon may represent different truths at different times.

A relationship may exist, change, and end.

A character may know something later that they did not know earlier.

A location may change ownership or condition.

A person may hold one motive, belief, or capability at one time and a different
one later.

The Product must therefore support temporally scoped Canon meaning where the
distinction is material.

"Current" state is always relative to a relevant story-time reference point.

The Product must not silently treat the author's present drafting position as
the universal meaning of current Canon state.

## Knowledge and Belief

Knowledge and belief are Canon state when materially relevant.

The Product must be able to distinguish:

- objective story truth;
- what a character knows;
- what a character believes;
- what a character misunderstands;
- what a character remembers or has forgotten;
- what a group, institution, or culture knows or believes;
- and intentionally unresolved or ambiguous truth.

A false belief may be canonically true as a fact about the believer without
making the believed proposition objectively true.

Knowledge and belief may change over time.

Such changes may be established by Events or direct accepted state revision.

Reader-information intent remains Plot according to DP-130.

## Epistemic Change

A discovery, deception, disclosure, inference, forgetting, reinterpretation, or
other epistemic occurrence may change what a character or group knows or
believes.

The Product must preserve the distinction between:

- the underlying objective truth;
- the epistemic Event;
- the resulting knowledge or belief state;
- and whether Plot reveals any of those meanings to the reader.

A character learning a fact does not inherently reveal it to the reader.

A reader revelation does not inherently change character knowledge.

## Motive, Intention, and Internal State

Story-relevant motive, intention, emotional condition, commitment, uncertainty,
or other internal state may be Canon when the author treats it as true of the
character.

Such state may be hidden from other characters or from the reader.

Internal Canon must therefore not be exposed merely because it is available to
the authoring system.

Plot controls reader access according to DP-130.

Prose controls linguistic realization.

## Narrative Time

Canon chronology is distinct from Plot presentation order, Manuscript order,
and authoring order.

Story time may be represented as:

- exact;
- approximate;
- relative;
- interval-based;
- partially ordered;
- unknown;
- or intentionally ambiguous.

The Product must not force false temporal precision merely to satisfy a schema.

If only relative ordering is accepted, the Product must preserve that relative
meaning rather than inventing dates or durations.

## Temporal Relationships

Canon may require temporal relationships such as:

- before;
- after;
- during;
- overlaps;
- begins;
- ends;
- precedes by an approximate interval;
- or another story-relevant ordering constraint.

The Product may know some temporal relations without knowing all absolute times.

Temporal reasoning must preserve accepted constraints without manufacturing
precision that the author has not established.

## Duration and Interval State

Some Canon meaning holds over an interval rather than at a point.

Examples include residence, employment, relationship status, possession,
injury, secrecy, belief, or institutional control.

An Event may begin or end such state.

The Product should support interval meaning when point-only representation would
lose story-relevant continuity.

The exact temporal model is a Planning decision.

## Canon Ambiguity and Unknowns

Canon may intentionally contain unknown, unresolved, approximate, or ambiguous
meaning.

The Product must distinguish between:

- meaning the author has not yet decided;
- meaning the author intentionally chooses to leave unresolved;
- meaning that is objectively resolved but hidden from characters or readers;
- and meaning whose temporal precision is intentionally limited.

The Product must not convert any of these states into false certainty for
generation, validation, indexing, or schema convenience.

Where unresolved meaning materially affects downstream work, it remains
candidate or explicitly ambiguous according to DP-110 and DP-130.

## Canon Invariants and Constraints

Some Canon meaning constrains not only current state but permissible future
development.

Examples may include:

- a physical impossibility;
- a character capability limit;
- a world rule;
- an established relationship constraint;
- an irreversible Event;
- or an accepted character invariant.

Such constraints may guide Plot and Prose generation.

The AI must not violate them merely because a local continuation would be
plausible in isolation.

A proposed exception or revision remains candidate until accepted.

## Canon Revision

The author may intentionally revise accepted Canon.

Revision may affect:

- Events;
- chronology;
- relationships;
- current or historical state;
- accepted future occurrence;
- knowledge or belief;
- internal state;
- constraints;
- or other story truth.

Accepted revision supersedes prior meaning at the identified scope according to
DP-110.

It does not silently rewrite affected Plot, Prose, production-control artifacts,
or Manuscript.

Impact analysis and reconciliation follow DP-120.

## Canon and Generated Prose

Generated prose does not create Canon merely by stating something as fact.

If generated text introduces a consequential fact, Event, state change,
knowledge change, causal relationship, or other Canon meaning that was not
already governed upstream, that meaning becomes candidate Canon.

Repeated occurrence in generated or accepted Manuscript does not silently
promote it.

Acceptance closure remains governed by DP-110.

## Validation Relationship

Semantic review must be able to detect material Canon problems such as:

- contradictory state at the same relevant time;
- accepted Event/state incoherence;
- impossible chronology;
- knowledge before acquisition;
- forgotten or unknown information treated as known;
- violation of accepted world or character constraints;
- false temporal precision;
- or generated consequential Canon that lacks upstream authority.

Validation diagnoses these conditions.

It does not choose missing Canon meaning or resolve ambiguity on the author's
behalf.

Detailed validation mechanisms are defined by later Design.

## Planning Boundary

This Design defines Canon state, occurrence, Event, epistemic, and narrative-time
semantics.

DP-130 remains authoritative for the Canon/Plot boundary and reader-information
ownership.

Later Design may define identity and traceability, Prose controls,
generation-package construction, persistence, validation, generated views, and
compatibility.

Planning may choose storage layout, schemas, event representations, temporal
models, knowledge-state structures, indexes, identifiers, and derived-state
mechanisms.

Implementation convenience does not justify false temporal precision,
event/state contradiction, or silent promotion of generated meaning into Canon.
