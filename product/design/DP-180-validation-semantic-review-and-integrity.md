---
doc_id: DP-180
title: Validation, Semantic Review, and Integrity
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
---

# Validation, Semantic Review, and Integrity

## Purpose

ADR Story Writer requires both mechanical validation and semantic review.

These functions protect different kinds of integrity.

Mechanical validation evaluates properties that can be decided without choosing
story meaning.

Semantic review evaluates whether governed meaning has been preserved,
respected, or realized correctly.

Neither function creates semantic authority.

Neither function may silently repair consequential story meaning merely to make a
candidate pass.

The Product uses validation and review to reduce hallucination, drift, hidden
invention, stale dependency use, and accidental corruption before candidate work
is accepted or relied upon.

## Validation Principle

Validation asks whether stated requirements, invariants, relationships, and
boundaries hold.

It does not answer what the story should mean unless that meaning has already
been established at the owning semantic surface.

A validation rule must therefore trace to:

- Product Design;
- approved Planning that realizes Product Design;
- accepted semantic state;
- approved production-control state;
- a bounded generation contract or package;
- an explicitly declared compatibility or migration requirement;
- or another governed source of requirements.

Validation must not invent requirements merely because they are easy to test.

## Mechanical Validation

Mechanical validation evaluates decidable invariants.

Examples may include:

- file or document syntax;
- Dataset schema conformance;
- required components;
- unique or non-colliding stable identities;
- resolvable durable scopes;
- valid references;
- required relationship endpoints;
- manifest and physical-file consistency;
- ordering structure;
- supported enumerated values;
- Dataset schema identity;
- Ruleset binding identity;
- compatibility declarations;
- package completeness;
- required provenance references;
- protected-text exactness where verbatim protection applies;
- bounded generation stop markers or structural boundaries;
- migration source/target metadata;
- candidate/accepted classification fields;
- or another mechanically decidable Product or Planning invariant.

Mechanical validation may use deterministic code, schemas, assertions, static
analysis, reproducible transformations, or another implementation mechanism.

A language model may assist in producing diagnostics, but a question does not
become mechanically decidable merely because a model can answer it.

## Semantic Review

Semantic review evaluates meaning against complete applicable governing context.

Examples may include whether:

- Plot preserves applicable Canon;
- lower Plot refinement preserves higher Plot intent;
- Prose controls preserve Plot meaning;
- generated prose realizes the approved bounded task;
- viewpoint access is respected;
- reveal and concealment intent is respected;
- a candidate introduces consequential meaning not authorized upstream;
- a generated detail exceeds the allowed creative freedom;
- protected material is semantically preserved where semantic protection rather
  than verbatim protection applies;
- Canon state and Events remain coherent;
- knowledge, belief, memory, and misunderstanding remain coherent;
- chronology is semantically consistent;
- a proposed revision still reflects the author's intended change;
- a migration preserves meaning;
- a derived view faithfully projects its governing sources;
- or affected downstream scopes remain aligned after an upstream revision.

Semantic review cannot be reduced to structural validation merely because review
criteria are written down.

## Review Is Context-Bound

A semantic review is meaningful only relative to the governing context against
which the candidate is evaluated.

The Product must be able to identify, as applicable:

- the reviewed candidate and scope;
- the accepted semantic sources;
- production-approved controls;
- candidate assumptions explicitly in use;
- applicable generation package or equivalent context;
- relevant revision or version identities;
- protected material;
- creative allowance;
- unresolved dependencies;
- and the review criteria applied.

A review performed against incomplete or stale governing context must not be
presented as equivalent to review against the complete applicable context.

If omitted or stale context could materially change the conclusion for a review
criterion, that criterion is indeterminate until the needed governing context is
retrieved, refreshed, or otherwise resolved.

## Review Scope

Review is scope-aware.

A review may cover:

- one semantic proposal;
- one production contract;
- one Beat;
- one near-prose unit;
- one generated paragraph;
- one scene candidate;
- one Manuscript passage;
- one migration result;
- one derived view;
- one reconciliation region;
- or another bounded governed scope.

Reviewing one scope does not review neighboring scopes merely because they share
a file or artifact.

A review result must not be broadened beyond the scope and governing context
actually evaluated.

## Candidate Validation

Candidate state may be validated without becoming accepted.

Validation of a candidate means only that the candidate satisfied the applicable
checks at the time and scope of validation.

A successful validation result does not:

- accept candidate Canon;
- accept candidate Plot;
- approve production controls;
- accept generated prose as Manuscript;
- resolve author ambiguity;
- or authorize persistence unless save authorization is separately established.

Candidate validation supports informed review and later acceptance.

It is not an authority transition.

## Production-Control Validation

Production controls may be validated for internal coherence and consistency with
their governing semantic sources.

A production contract may be checked for matters such as:

- bounded scope;
- explicit stop condition;
- required dependencies;
- viewpoint access;
- reveal limits;
- entry and exit state;
- creative allowance;
- protected material;
- style or Prose guidance;
- and sufficient refinement for reliable generation.

Mechanical checks may establish required fields or structural completeness.

Semantic review determines whether the production control actually preserves and
appropriately constrains the governing story intent.

A validated production control is not necessarily production-approved.

Production approval remains distinct under DP-110.

## Generation Readiness Validation

Before generation, the Product may evaluate whether the task is ready under
DP-120 and DP-150.

Generation readiness means the available governed context is sufficient for the
requested model task without requiring the model to independently decide
consequential narrative meaning.

Readiness evaluation may detect:

- missing material dependencies;
- unresolved viewpoint access;
- ambiguous reveal timing;
- missing stop boundaries;
- insufficient local refinement;
- conflicting production controls;
- stale upstream state;
- missing candidate assumptions;
- or other conditions that would force unsafe improvisation.

If readiness cannot be established, the Product should refine, retrieve, repair
dependencies, surface an unresolved decision, or defer generation.

It must not declare readiness by silently choosing the missing consequential
meaning.

## Generation-Package Validation

A generation package is validated against the production contract and the
governed state from which it is projected.

Validation should establish, as applicable, that:

- required governing sources are represented;
- omitted context is not materially required;
- candidate assumptions are declared;
- viewpoint restrictions are preserved;
- reveal and concealment boundaries are preserved;
- style resolution respects precedence;
- creative allowance and prohibitions are preserved;
- protected material is represented correctly;
- generation scope and stop boundaries are explicit;
- selected revisions are current for the intended attempt;
- and package provenance identifies the governing context.

A package may be mechanically complete yet semantically incomplete.

When required context is missing, validation should distinguish whether:

- the package projection omitted governed state that already exists; or
- the governing state itself is insufficient or unresolved for the intended
  task.

The first is a package-construction defect.

The second requires refinement, retrieval, author decision, or preserved
unresolved state rather than merely rebuilding the same package.

Semantic review is required where determining sufficiency or fidelity depends on
meaning rather than structure.

## Generated-Prose Validation

Generated prose remains candidate.

Validation should compare the generated candidate against the generation package
or equivalent governing context that produced it.

Review may evaluate whether the candidate:

- remains within the requested bounded scope;
- stops at the required boundary;
- realizes the required narrative movement;
- preserves viewpoint access;
- preserves reveal timing;
- respects accepted Canon;
- preserves Plot intent;
- respects persistent Prose guidance;
- respects resolved style;
- preserves protected text or meaning;
- stays within allowed creative freedom;
- avoids consequential invention;
- avoids unauthorized continuation beyond the task;
- and maintains local continuity with supplied preceding or following text where
  applicable.

The reviewer must distinguish defects in the generated text from defects or
ambiguities already present in the governing package.

Validation must not blame the candidate for obeying a defective package without
also surfacing the package defect.

## Consequential Invention Review

A primary semantic-review responsibility is detecting consequential meaning
introduced downstream without governing authority.

When generated or candidate work introduces consequential meaning not already
authorized by the applicable semantic surface:

- the invention must be identified;
- it must remain candidate;
- validation must not silently normalize it into the upstream state;
- and acceptance of downstream wording must not accept the invention upstream.

The author may choose to reject it, revise the candidate, or promote the idea as
a separate proposal at the owning semantic surface.

The review process must preserve that distinction.

## Non-Consequential Creative Detail

The Product may allow bounded non-consequential invention under DP-150.

Semantic review may evaluate whether generated detail remains within that
allowance.

A detail does not become non-consequential merely because it is small in wording.

Materiality depends on whether later governed reasoning could be affected.

When the reviewer cannot determine confidently whether a generated detail is
consequential, the result should be surfaced for review rather than silently
classified as harmless.

## Viewpoint and Information Integrity

Semantic review should protect the distinction between:

- Canon truth;
- Character knowledge, belief, memory, and misunderstanding;
- Plot reader-information intent;
- viewpoint access;
- Prose realization;
- text actually present;
- and diagnostic reader inference.

A prose candidate can be grammatically correct and mechanically valid while
still leaking hidden Canon, revealing information too early, implying knowledge
the focal Character does not possess, or frustrating intended ambiguity.

These are semantic-review defects.

They must not be reduced to keyword or field-presence checks unless a particular
case is truly mechanically decidable.

## Canon Integrity

Canon integrity review may evaluate consistency among:

- accepted state;
- accepted Events;
- chronology;
- constitutive Event effects;
- relationships;
- Character knowledge and belief;
- Setting or world rules;
- accepted future occurrence;
- unresolved Canon questions;
- and material dependencies.

Review must preserve accepted ambiguity and unknown state.

It must not repair an apparent gap by inventing an Event, cause, motivation,
timeline value, or state transition merely to obtain completeness.

Where a real contradiction exists, review identifies it.

Resolution occurs through the appropriate semantic revision.

## Plot Integrity

Plot integrity review may evaluate whether dramatic presentation remains
consistent with applicable Canon and accepted Plot intent.

Review may detect:

- unauthorized contradiction of Canon;
- reveal timing drift;
- concealment failure;
- viewpoint-access drift;
- reordered material that changes intended dramatic meaning;
- omitted required occurrence;
- accidental resolution of intended ambiguity;
- or downstream Plot refinement that changes higher Plot intent.

Review identifies the mismatch.

It does not choose the replacement dramatic design unless acting as a separate
candidate-authoring operation.

## Prose Integrity

Prose integrity review may evaluate whether linguistic realization preserves the
governing Plot, Canon, and persistent Prose constraints.

It may also evaluate locally relevant style, voice, narrative distance,
dialogue handling, rhythm, imagery, and other accepted Prose guidance.

Literary preference is not automatically an integrity defect.

Where style criteria are subjective, the Product should distinguish:

- violation of explicit accepted guidance;
- likely mismatch requiring review;
- and optional improvement suggestion.

Review should not convert taste into hidden authority.

## Manuscript Integrity

Accepted Manuscript has its own authority over accepted final wording.

Integrity review may identify when accepted Manuscript has become materially
misaligned with revised Canon, Plot, or Prose guidance.

Such detection does not silently alter the Manuscript.

The Product must preserve the accepted text until an authorized Manuscript
revision occurs.

A downstream inconsistency may require reconciliation, but reconciliation does
not erase the distinction between accepted upstream meaning and accepted
Manuscript wording.

Accepted Manuscript may therefore become stale, misaligned, or marked as
requiring reconciliation without losing its accepted wording authority.

Only an authorized Manuscript revision changes that accepted wording authority.

## Revision Impact Review

When governed state changes, previously valid dependent state may require
review.

The Product should use material dependency and scope traceability under DP-120
and DP-175 to identify likely affected regions.

Impact analysis may classify a dependent scope as, for example:

- unaffected;
- still valid;
- mechanically invalid;
- semantically suspect;
- reconciliation required;
- unresolved;
- or requiring regeneration.

The exact vocabulary is a Planning decision.

The classification must not itself choose the semantic correction.

## Validation Freshness

Validation results are relative to the revisions and governing context reviewed.

A result may become stale when a material dependency changes.

The Product must not continue to treat a stale validation result as current
evidence when the change could affect the reviewed conclusion.

Where practical, validation provenance should permit the Product to determine
what governing revisions or scopes the result depended upon.

The exact cache-invalidation or freshness mechanism is Planning.

## Semantic Review Freshness

Semantic review can also become stale.

An upstream accepted revision, production-control change, candidate-assumption
change, or package change may invalidate a previous semantic-review conclusion.

A prior review may remain useful historical evidence.

It must not be represented as current review of materially changed state.

## Review Result

A semantic review may conclude, for the reviewed scope and governing context,
that the applicable criterion is:

- conforming;
- non-conforming;
- or indeterminate.

Indeterminate is not equivalent to pass or fail.

Reviewer confidence may inform escalation, additional review, or workflow policy,
but confidence does not change semantic authority, acceptance state, or the
meaning of the reviewed material.

A review result should communicate enough information for an author or later
process to understand:

- what was reviewed;
- the scope;
- the governing context;
- what criteria were applied;
- what defects or uncertainties were found;
- which findings are mechanical versus semantic;
- which findings are blocking for the intended operation;
- and what state remains unresolved.

The Product does not require one universal review-report schema.

Review results are derived evidence about identified scope and governing context.

They may be persisted, indexed, compared, or used by later workflows without
becoming story authority.

Review evidence must be sufficient for the operation that relies on it.

## Findings and Severity

Validation and review may classify findings by severity or effect.

Useful distinctions may include:

- informational observation;
- optional improvement;
- warning;
- blocking structural defect;
- blocking semantic defect;
- unresolved ambiguity;
- stale dependency;
- or another operation-relevant classification.

The exact labels are Planning decisions.

Severity must derive from the impact on the governed operation rather than from
how easy the finding is to detect.

## Known Defect Versus Unknown State

A known defect and an unresolved question are different.

A defect means applicable governed requirements are violated.

Unknown or unresolved state means the Product cannot yet establish the required
answer.

The system must not describe unresolved story meaning as invalid merely because
it has not been decided.

Likewise, it must not describe a known contradiction as harmless ambiguity when
governing meaning actually conflicts.

## Validation Failure

A validation failure must identify the violated requirement or unresolved
precondition sufficiently for governed response.

Mechanical validation failure may block an operation that requires structural
integrity.

A non-conforming semantic-review result may block acceptance, production
approval, generation, migration, rebinding, publication, or another operation
when the violated meaning is material to that operation.

An indeterminate result may also block an operation when proceeding would require
assuming the missing semantic conclusion.

Not every finding blocks every operation.

A candidate with a prose-style defect may still be persisted as candidate.

A Dataset with ambiguous identity may be inspectable while unsafe for precise
semantic revision.

Blocking behavior must be scoped to the operation and risk.

## Repair Boundary

Validation and repair are distinct operations.

A validator or reviewer may propose a repair.

Applying a repair must follow the authority and approval semantics of the thing
being changed.

Mechanical repair may be automatic only when the correct result is determined
without a consequential semantic choice.

Examples may include rebuilding a derived index or restoring a deterministic
reference representation.

A repair that changes Canon, Plot, Prose meaning, production intent, or accepted
Manuscript wording is a governed revision, not validation.

## Automatic Repair

Automatic repair is allowed only when:

- the intended result is mechanically determined;
- no unresolved consequential choice exists;
- authority classification is preserved;
- material identity and dependencies are preserved;
- and the operation does not silently accept or approve candidate meaning.

If those conditions do not hold, the Product must surface a proposed repair for
governed review.

When an automatic repair materially changes persisted representation, the Product
should preserve enough repair provenance for diagnosis, migration, or later
interpretation where that history remains material.

The Product does not require provenance for every trivial deterministic cleanup.

The fact that a model can generate a plausible correction does not make the
repair mechanical.

## Validation and Acceptance

Validation may be a prerequisite for acceptance.

Validation is not acceptance.

Semantic review may recommend acceptance.

Semantic review is not acceptance.

Acceptance remains an explicit authority transition under DP-110.

The Product must not infer acceptance from:

- a clean validation result;
- absence of findings;
- reviewer confidence;
- repeated use;
- persistence;
- generation success;
- migration success;
- or a candidate appearing in accepted context.

## Validation and Persistence

Persistence and validation are independent concerns.

Planning may require certain validations before ordinary save.

The Product may also permit persistence of known-invalid candidate or recovery
state when retaining that state is useful and its invalid status remains clear.

Persisting a failed candidate can support later repair, comparison, or
diagnosis.

Persistence must not erase validation findings or upgrade authority.

## Validation and Initialization

Ordinary session reconstruction may require mechanical integrity sufficient to
interpret the Dataset safely.

If structural interpretation cannot be established, the Product should enter
controlled recovery, migration, inspection, or refusal rather than guessing.

Semantic issues do not always prevent initialization.

A Dataset may contain known unresolved candidate or reconciliation state and
still reconstruct safely when those classifications are preserved.

## Validation and Migration

Migration under DP-170 requires validation appropriate to the migration scope.

Mechanical validation may establish target structural integrity.

Semantic review evaluates meaning preservation where the migration cannot be
proven mechanically.

A migration is not meaning-preserving merely because source and target both pass
their schemas.

A migrated candidate is not revalidated against its original generation context
merely because migration succeeds.

## Validation and Rebinding

Rebinding requires evaluation that the target Ruleset can operate on the Dataset
without semantic reinterpretation beyond the authorized transition.

Mechanical checks may confirm binding identifiers and declared compatibility.

Semantic review is required where compatibility depends on preserved meaning.

A successful rebind does not approve semantic revisions discovered during that
process.

## Validation and Derived Views

Derived views may be checked for projection fidelity.

If a dossier, report, index, or summary conflicts with current governing state,
the derived view should be refreshed, marked stale, or otherwise prevented from
being treated as current.

Repairing a derived projection does not change its source authority.

An edit to a derived view that intends to change story meaning must still map to
the owning semantic surface.

## Validation and Protected Material

Protected material may carry different protection semantics.

Mechanical validation may verify exact preservation where protection is verbatim.

Semantic review may verify meaning or structural preservation where the
protection rule allows wording changes.

A validator must not assume all protected material requires byte-for-byte or
word-for-word equality.

The protection mode is part of the governing context.

## Validation and Creative Allowance

Generation validation must evaluate creative invention against the allowance
defined by the governing production contract or package.

A reviewer should distinguish:

- expressly required content;
- permitted non-consequential invention;
- prohibited consequential invention;
- and content whose materiality is uncertain.

The last category must be surfaced rather than silently treated as permitted.

## Reviewer Information Access

The context needed to review output may differ from the context intentionally
given to the generator.

A generator may be denied hidden Canon to prevent leakage.

A reviewer may require that hidden Canon to verify that leakage, contradiction,
or accidental revelation did not occur.

The Product may therefore maintain distinct generation and review projections.

Review access does not alter Plot reveal intent or authorize generator access.

## Independent Review

Where risk justifies it, review may be performed by a different model, process,
prompt, or human than the one that generated the candidate.

Independence can reduce shared failure modes.

The Product does not require independent review for every operation.

Planning may choose where its reliability value justifies the cost.

## Model Review Limitations

Model-based semantic review is probabilistic.

A model may miss defects, invent defects, overstate confidence, or import
unstated assumptions.

The Product must not treat a model's semantic-review result as infallible simply
because it is formatted as a structured report.

Review design should reduce these risks through bounded scope, explicit governing
context, attributable criteria, targeted questions, and author escalation where
uncertainty is material.

## Human Review

Human author review remains a valid semantic-review mechanism.

The Product must not require an AI reviewer to override or reinterpret an
author's explicit governed decision.

When human review intentionally changes story meaning, that change still belongs
to the owning semantic surface and follows its acceptance semantics.

## Review Uncertainty

A semantic reviewer may be unable to determine a conclusion confidently.

Uncertainty is a valid review outcome.

The reviewer should identify the missing or conflicting context where practical.

The Product should respond through retrieval, narrower review, author decision,
refinement, or preserved unresolved state.

It must not convert uncertainty into fabricated certainty merely to complete a
workflow.

## False Positives and False Negatives

Validation strategy should consider both:

- false positives that create unnecessary author friction or pressure the author
  to "fix" valid creative choices;
- and false negatives that allow semantic drift, continuity errors, or hidden
  invention to pass unnoticed.

The Product's goal is not maximum finding count.

It is reliable protection of governed meaning with acceptable author burden.

## Validation Profiles

Different operations may require different validation profiles.

For example:

- generation readiness;
- generation package materialization;
- generated-prose review;
- semantic acceptance;
- Manuscript acceptance;
- save;
- session initialization;
- migration;
- rebinding;
- publication;
- or derived-view refresh.

A validation profile may compose mechanical checks and semantic-review steps.

A profile may select or compose established requirements and gates.

It must not turn an advisory criterion into a Product-blocking requirement unless
that blocking behavior is grounded in Product Design or approved Planning that
realizes Product semantics.

The exact profile representation is Planning.

Profiles must not invent new semantic authority.

## Blocking Gates

A governed workflow may define blocking validation or review gates.

A gate is justified when proceeding despite failure would materially risk:

- corrupt interpretation;
- authority confusion;
- semantic drift;
- unbounded model invention;
- loss of accepted state;
- invalid migration;
- or another Product integrity requirement.

Gates should not be added merely because additional checks are possible.

A blocking gate applies only to the operation and scope for which its requirement
is material.

A finding that blocks generation, acceptance, migration, or publication does not
therefore automatically block candidate persistence, inspection, export, or
unrelated governed work.

Overvalidation can reduce author control by turning implementation preferences
into hidden policy.

## Integrity Invariant

At every stage, the Product should preserve the distinction between:

- what is accepted;
- what is candidate;
- what is production-approved;
- what is generated;
- what is derived;
- what is unresolved;
- what has been validated;
- what has been semantically reviewed;
- and what has been persisted.

These states may overlap.

They are not interchangeable.

For example, material can be accepted but not yet persisted, persisted but
candidate, validated but unaccepted, reviewed but unresolved, or generated and
persisted while still failing semantic review.

## Fail-Safe Principle

When the Product cannot establish structural safety, it should fail, restrict
operation, or enter controlled recovery rather than silently guess.

When the Product cannot establish semantic fidelity, it should preserve the
candidate or unresolved state and surface the uncertainty rather than silently
choose a story interpretation.

When the Product detects a contradiction, it should identify the conflict rather
than invent a reconciliation.

Fail-safe behavior protects author authority.

## Validation Test

The Product should support at least these scenarios:

1. A generated scene is mechanically well-formed but leaks hidden Canon; semantic
   review rejects the candidate without changing Canon.
2. A prose candidate introduces a consequential new motive; review identifies the
   invention and keeps it candidate rather than promoting it.
3. A generation package omits a material reveal constraint; package validation
   blocks generation readiness or marks the package insufficient.
4. An upstream Plot revision makes a previously reviewed prose candidate stale;
   the old review is not treated as current.
5. A mechanically valid migration changes candidate material into accepted state;
   semantic review identifies the authority violation.
6. A Dataset with a broken durable identity reference is safe for inspection but
   blocked from precise governed revision until repaired.
7. A derived dossier becomes stale after Canon changes; refreshing the dossier
   changes the projection, not Canon.
8. A candidate fails style review but may still be persisted as a failed
   candidate for later repair.
9. A reviewer cannot establish whether an invented detail is consequential;
   uncertainty is surfaced instead of silently permitting it.
10. A repair is mechanically determined and non-semantic; the Product may apply
    it without inventing or accepting story meaning.

Failure to distinguish these cases risks collapsing validation, authority,
persistence, and semantic authorship into one unsafe mechanism.

## Simplicity Boundary

The Product does not require:

- validation of every artifact after every keystroke;
- one global validation status;
- giant issue registries;
- proof objects for every operation;
- model review of every mechanical invariant;
- independent reviewers for all generation;
- exhaustive quality scoring;
- or validation logs for every transient intermediate.

Validation infrastructure should exist where it materially improves correctness,
continuity, safe generation, acceptance, migration, recovery, or author
confidence.

## Planning Boundary

This Design defines the distinction between mechanical validation and semantic
review, context-bound and scope-bound review, candidate and generation
validation, freshness, findings, repair boundaries, acceptance boundaries,
fail-safe behavior, and Product integrity requirements.

Planning may choose schemas, validators, review prompts, review models,
deterministic checks, severity labels, validation profiles, caching, freshness
tracking, report formats, CI integration, save gates, migration gates, and other
technical realization.

Implementation convenience does not justify turning mechanical checks into story
meaning, treating model review as infallible, silently repairing consequential
semantics, accepting candidate state through validation, or relying on stale
review results after material dependencies change.
