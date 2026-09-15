---
doc_id: DP-150
title: Prose Control and Generation Packages
depends_on:
  - DP-100
  - DP-110
  - DP-120
  - DP-130
  - DP-140
---

# Prose Control and Generation Packages

## Purpose

Prose governs controlled realization of Plot into reader-facing language.

The Product must reduce broad narrative intent into generation work that an AI
can execute reliably without independently deciding consequential story meaning.

This Design defines the Prose control structures, generation-package semantics,
style resolution, invention boundaries, and candidate-generation behavior used
to achieve that control.

The goal is not to prescribe one universal drafting workflow.

The goal is to make model discretion explicit, local, and bounded before prose
generation begins.

## Prose Ownership

Prose owns linguistic and experiential realization of governed Plot intent.

Prose may govern:

- dialogue realization;
- action realization;
- interior experience;
- exposition;
- description;
- paragraph-scale progression;
- transitions;
- pacing;
- rhythm;
- imagery;
- sensory emphasis;
- diction;
- syntax;
- register;
- narrative distance;
- and other expressive realization.

Prose does not own Canon truth or Plot information structure merely because
those meanings are expressed in language.

A Prose decision that would change consequential Canon or Plot meaning becomes a
proposal at the semantic surface that owns that meaning.

## Plot-Prose Boundary

Plot owns what narrative meaning is intentionally presented, withheld, ordered,
revealed, concealed, focalized, or otherwise made available to the reader.

Prose owns how those accepted choices are realized in language and local scene
experience.

For example, Plot may establish a limited viewpoint and an unrevealed Canon
truth.

Prose may realize that boundary through perceptual selection, dialogue,
interiority, implication, omission, rhythm, and wording.

Prose must not silently broaden, contradict, or prematurely resolve accepted
Plot information boundaries.

Viewpoint information access remains governed by DP-130.

Linguistic viewpoint realization belongs to Prose.

## Persistent Prose Guidance

The Product must support persistent realization guidance when such guidance
materially improves consistency across generation tasks or sessions.

Persistent Prose guidance may include:

- narrative voice;
- tense;
- narrative distance;
- register;
- stylistic tendencies;
- dialogue conventions;
- genre realization constraints;
- lexical or period constraints;
- character-scoped realization guidance;
- viewpoint-scoped linguistic guidance;
- rhythm or imagery preferences;
- and other durable authorial preferences.

Persistent Prose guidance governs realization.

It is not Canon truth and does not control Plot information access.

Guidance may be global, scoped, layered, or absent where unnecessary.

The exact storage representation is a Planning decision.

## Progressive Prose Refinement

Prose work may be progressively refined before final language generation.

Useful control structures may include:

- Beats;
- narrative Modes;
- scene realization plans;
- pseudo-prose;
- near-prose layouts;
- paragraph-intent units;
- transition plans;
- or other realization structures.

These structures are production-control artifacts.

They do not become additional semantic authority surfaces.

No named structure is mandatory merely because it appears in this Design.

However, DP-120 requires refinement to continue until the selected generation
task is reliably bounded.

If a scene-level task leaves excessive model discretion, the Product must be
able to refine it further.

## Beats

A Beat is a bounded narrative-intent unit used to state what a local portion of
Prose must accomplish.

A Beat may identify movement such as:

- an action;
- an exchange;
- a realization;
- a change in emotional pressure;
- an exposition movement;
- a perceptual shift;
- a transition;
- a local reveal or concealment obligation already governed by Plot;
- or another narratively useful change.

A Beat does not create Canon or Plot meaning merely by naming it.

The Beat realizes or prepares governed meaning and may itself remain candidate.

Beat granularity is determined by control value, not by a required sentence or
paragraph count.

## Narrative Modes

Narrative Modes may classify how a Beat or realization unit is primarily carried
in prose.

Useful modes may include:

- action;
- dialogue;
- exposition;
- internal experience;
- description;
- or another mode with demonstrated control value.

Modes are realization controls, not story ontology.

A unit may combine modes.

The Product does not require one exhaustive mode taxonomy.

Mode classification is useful only when it helps constrain generation, review,
or revision.

## Pseudo-Prose and Near-Prose Layout

Pseudo-prose or a near-prose layout is an ordered realization plan closer to
final language than Plot structure but not yet accepted reader-facing prose.

It may establish:

- local ordering;
- paragraph-scale or similarly local movement;
- emphasis;
- transitions;
- mode;
- emotional register;
- viewpoint realization;
- reveal timing already governed by Plot;
- opening or closing shape;
- rough phrasing;
- and other realization constraints.

Pseudo-prose is especially useful when direct scene generation leaves the model
too much planning freedom.

The Product may refine to paragraph-scale, sentence-scale, or another local
unit when required for reliable execution.

Pseudo-prose is not required to resemble polished prose.

Its purpose is to reduce unresolved realization decisions before generation.

## Paragraph-Scale Control

Paragraph scale is not a mandatory Product unit.

It is an important practical refinement level because long-form prose generation
may remain unreliable when the model must simultaneously decide too many local
movements.

The Product must therefore support control units small enough to constrain
generation near paragraph scale when needed.

A larger unit should be preferred when it remains reliably bounded.

A smaller unit should be used when the larger task causes drift, unsupported
invention, boundary overruns, or loss of intended movement.

## Production Contract

A production contract defines what a bounded local narrative task must do.

It is a production-control artifact, not a context container and not a source of
story truth.

A production contract must be capable of expressing the controls needed for the
task, including as applicable:

- generation scope and stopping boundary;
- intended narrative movement;
- required realization units;
- viewpoint and information-access constraints;
- reveal and concealment obligations;
- relevant entry and exit conditions;
- persistent Prose guidance;
- local style or voice requirements;
- protected text or terminology;
- creative allowance;
- prohibited invention;
- and declared accepted or candidate dependencies.

The exact field structure is a Planning decision.

The semantic requirement is that the contract make the requested work reliably
bounded.

## Production Contract and Generation Package

A production contract and a generation package have different roles.

The **production contract** defines the local narrative work and its controls.

The **generation package** is the bounded, task-specific projection of the
governed and declared candidate material supplied for a particular generation
attempt.

A contract may be reused across more than one generation attempt.

A generation package represents one selected execution context.

Changing the selected dependencies, revisions, permissions, style projection,
or task boundary may require a different generation package even when the
production contract remains conceptually the same.

## Generation Package

Before generation, the Product must be able to materialize a bounded generation
package for the requested task.

The package must contain or identify enough information for the generator to
perform the task without relying on unstated conversation memory or
reconstructing the whole story.

A generation package may include:

- the production contract;
- the local Plot intent being realized;
- material Canon dependencies;
- declared candidate assumptions;
- applicable Prose guidance;
- a resolved style projection;
- ordered Beats or near-prose units;
- exact generation boundaries;
- invention permissions and prohibitions;
- protected wording or terminology;
- relevant prior accepted text needed for continuity;
- and validation expectations.

The package must exclude unrelated material when that material does not improve
correctness and materially increases distraction or unsupported inference risk.

The package is a production-control artifact.

It does not acquire semantic authority over the material it projects.

## Minimum Sufficient Context

Context construction follows a minimum-sufficient principle.

The generation package should provide all materially required governing
information for the task while avoiding dependence on unrelated whole-story
context.

Completeness is measured against the local task, not against the entire project.

When required context cannot fit a reliably bounded task, the Product must
refine the task, select narrower dependencies, or surface the unresolved
problem.

It must not silently omit material constraints and then rely on model memory or
guessing.

## Information-Access Safety

The Dataset may contain Canon that the current Plot viewpoint or reader state is
not allowed to reveal.

Generation context must preserve that distinction.

Material retrieved for author reasoning, validation, or continuity analysis does
not automatically become narratively available to the generator.

When hidden Canon must constrain generation, the Product must provide it in a
form that preserves the prohibition against disclosure.

The Product may separate generator-visible context from reviewer- or
validator-only context when that better preserves information boundaries.

The implementation must not rely on the model voluntarily remembering that
omniscient information is forbidden after presenting it without control.

## Resolved Style Projection

Persistent Prose guidance may be broader than a particular generation task.

The Product may therefore construct a resolved style projection containing the
guidance applicable to the current task.

Resolution may account for:

- global voice;
- project or manuscript-unit guidance;
- viewpoint-specific realization;
- character-specific dialogue or perception guidance;
- local scene needs;
- and task-specific overrides explicitly authorized by the author.

A resolved style projection is derived control state.

It must not silently change Canon, Plot, or persistent Prose guidance.

Conflicting guidance must be resolved or surfaced before generation when the
conflict could materially affect the requested work.

## Creative Allowance

Generation requires some model discretion.

The Product must distinguish permitted local invention from consequential
story-making authority.

Creative allowance may permit invention of non-consequential details needed for
natural prose, such as:

- incidental sensory detail;
- connective action;
- minor staging;
- rhythm;
- expressive phrasing;
- non-material environmental texture;
- or other detail that does not materially constrain later governed reasoning.

Creative allowance may be narrower for a particular task.

The absence of an explicit permission must not be interpreted as permission to
invent consequential Canon or Plot meaning.

## Consequential Invention

Generated text must not be trusted to decide consequential story meaning.

Consequential invention includes new meaning that would materially constrain
later governed reasoning, such as an ungoverned:

- fact;
- Event;
- causal relationship;
- state change;
- relationship change;
- character knowledge or belief change;
- motive or intention;
- reveal;
- concealment decision;
- dramatic turn;
- scene outcome;
- or other Canon or Plot meaning.

If consequential invention appears in generated text, it remains a candidate
proposal at its owning semantic surface.

The prose candidate does not become authoritative merely because the invention
is fluent, plausible, repeated, validated mechanically, or accepted as wording.

DP-110 governs acceptance closure.

## Protected Material

A generation task may contain text, terminology, facts, ordering, or other
material that must be preserved exactly or within an explicitly stated degree
of variation.

The Product must be able to distinguish protected material from guidance the
model may freely reinterpret.

Protected material may include:

- required wording;
- established names or terms;
- quoted text;
- continuity-critical phrasing;
- structural anchors;
- or other author-designated constraints.

Protection is a production constraint.

It does not create semantic authority that the protected material does not
already possess.

## Package Currentness and Freezing

A generation package must identify the revisions or semantic scopes of the
material on which the generation attempt depends sufficiently to support later
review and reproducibility.

Once used for a generation attempt, that package must represent a stable
execution context.

Later changes to Canon, Plot, Prose guidance, candidate assumptions, or the
production contract must not retroactively alter what the earlier package meant.

The Product may implement this through immutable packages, snapshots, version
references, content identities, or another reliable mechanism.

Exact hashing or serialization strategy is a Planning decision.

The Product does not require hashes on every artifact merely to satisfy this
principle.

## Package Reproducibility

The Product must preserve enough provenance to answer what governed a generated
candidate.

Reproducibility means that the Product can identify the material generation
boundary, selected dependencies, declared candidate assumptions, applicable
guidance, and invention policy used for the attempt.

It does not require that a nondeterministic model reproduce identical wording.

The goal is reproducible governing context, not deterministic literary output.

## Generation Boundary

Every generation attempt must have a bounded target.

The target may be a scene, Beat group, paragraph-scale unit, sentence-scale
unit, or another local realization scope.

The package must make the stopping boundary sufficiently clear that successful
generation does not depend on the model deciding how far the story should
continue.

Generated output beyond the authorized boundary is candidate overflow and must
not be treated as governed continuation.

A request to "continue naturally" is not sufficient when the intended stopping
point is consequential.

## Generation

Generation consumes a generation package and produces candidate reader-facing
text.

The generator's primary task is realization.

It may exercise creative allowance within the package.

It must not be relied on to reconstruct missing consequential intent.

It must not silently widen the task, resolve upstream ambiguity, or continue
past the governed boundary.

A generation failure should lead to further refinement, package correction,
regeneration, or author review rather than silent expansion of model authority.

## Generated Prose Candidate

Generated prose is candidate text until accepted.

A candidate must remain attributable to the generation package that governed its
creation.

Candidate prose may be revised, regenerated, compared, or discarded without
changing accepted Manuscript.

Candidate persistence does not imply acceptance.

A candidate may itself become an input to later candidate work when that
dependency is declared according to DP-120.

## Validation Before Acceptance

Generated prose should be evaluated against the production contract, generation
package, and applicable semantic authority before acceptance where material
failure could alter governed meaning.

Review may evaluate:

- task-boundary compliance;
- required movement;
- viewpoint and information-access compliance;
- reveal timing;
- Canon consistency;
- Plot consistency;
- protected material;
- persistent Prose guidance;
- style realization;
- unauthorized consequential invention;
- and other task-specific constraints.

Mechanical checks and semantic review remain distinct.

Validation does not make a candidate authoritative.

## Local Regeneration

The Product must support regeneration at the smallest useful affected
realization scope.

A failure in one Beat, paragraph-scale unit, transition, or local passage should
not require regeneration of an entire chapter or story when the governing
dependencies remain valid outside that region.

Local regeneration must preserve unaffected accepted or protected material.

When the failure originates upstream, the Product must re-refine or reconcile
from the highest materially affected control point according to DP-120 rather
than repeatedly regenerating from stale controls.

## Manuscript Relationship

Manuscript owns accepted reader-facing text according to DP-100 and DP-110.

Prose controls and generation packages prepare candidate wording for possible
Manuscript acceptance.

Accepted final wording must not remain as a second competing authoritative copy
inside Prose merely because it was developed through Prose control artifacts.

Manuscript acceptance does not silently accept consequential Canon or Plot
meaning introduced by generated text.

Such meaning must be resolved at its owning semantic surface under DP-110.

Detailed Manuscript organization and identity may be defined by later Design.

## Simplicity Boundary

The reference implementation of these semantics may use indexes, materialization
workflows, revision identifiers, hashes, status values, or other governance
machinery.

Those mechanisms are not Product requirements merely because they are useful in
one implementation.

The Product requires only the control needed to preserve:

- bounded generation;
- semantic authority;
- declared candidate assumptions;
- information boundaries;
- reproducible governing context;
- local review and regeneration;
- and author-controlled acceptance.

Additional machinery requires demonstrated product value.

## Planning Boundary

This Design defines Prose ownership, progressive realization control,
production-contract semantics, generation-package semantics, context
construction, style projection, invention boundaries, package stability, and
candidate generation behavior.

Planning may choose schemas, filenames, registries, workflow commands, prompt
composition, package serialization, revision identifiers, hashes, cache
behavior, model adapters, and other technical realization.

Implementation convenience does not override the requirement that generation be
bounded, attributable, information-safe, and subordinate to governed story
meaning.
