---
functional_set: FS-007
artifact: functional-set-scope
title: Governed Prose Style Guidance and Generation Quality
design_revision: 08c6670ede17618f8b99c77e648168caeff1351f
---

# FS-007 — Governed Prose Style Guidance and Generation Quality

## Purpose

FS-007 realizes the persistent Prose-guidance, general realization-quality,
guidance-revision, and resolved-style-projection semantics established by
DP-150.

The Product shall let an author provide representative prose samples, derive a
compact candidate author-style profile from those samples, review and approve
that profile, combine it with Ruleset-owned generation-quality guidance and
scene-local Prose guidance, and freeze the applicable result into the generation
package.

The capability exists to make prose generation reproducible across sessions and
models without depending on conversation memory or repeatedly injecting source
manuscript samples.

## Exact Design Binding

Planning consumes Product Design at repository revision:

`08c6670ede17618f8b99c77e648168caeff1351f`

This revision explicitly establishes Ruleset-owned general realization-quality
guidance as distinct Prose production control and establishes candidate revision
semantics for previously approved persistent Prose guidance.

FS-007 selects those DP-150 obligations together with applicable authority,
persistence, compatibility, validation, and simplicity semantics from DP-110,
DP-160, DP-170, and DP-180.

## Functional Boundary

FS-007 begins with a compatible Story Writer Dataset and an author or agent
providing one or more representative prose samples or an already prepared style
analysis.

FS-007 ends when the Product can:

1. represent a candidate author-style profile as persistent Prose production
   control rather than Canon or Plot authority;
2. retain bounded provenance identifying the samples from which a profile was
   derived without requiring the source prose itself to be injected into
   ordinary generation packages;
3. support explicit approval of a candidate style profile before it becomes
   ordinary persistent generation guidance;
4. revise an approved profile under the same stable profile identity while
   creating a distinct candidate content revision that requires approval;
5. provide Ruleset-owned generation-quality guidance that applies even when no
   author style profile exists;
6. include guidance intended to reduce common model-generation artifacts such as
   unnecessary restatement, patterned contrast constructions, excessive
   micro-reactions, generic atmospheric filler, over-explanation, and
   mechanically polished dialogue;
7. keep general quality guidance, author-style guidance, and local scene/mode
   guidance distinguishable;
8. resolve the applicable guidance into one bounded style projection for a
   generation task;
9. carry author- or review-identified material style conflicts as explicit
   unresolved control state and refuse generation until they are resolved;
10. freeze a ready style projection into the production contract and generation
    package;
11. reconstruct persisted author-style state in a fresh session;
12. permit schema-v1 Datasets with no FS-007 style state to remain structurally
    valid, meaning only that no author-specific profile has been established;
13. move compatible pre-FS-007 schema-v1 Datasets to the FS-007 Ruleset through
    explicit rebinding rather than Dataset migration.

## Author-sample Analysis Boundary

Author-sample analysis is an agent-assisted interpretation step.

The analyzer should infer stable realization tendencies such as viewpoint,
tense, narrative distance, diction, dialogue behavior, description density,
interiority, sentence and paragraph behavior, pacing, and recurrent stylistic
preferences.

The analyzer must not deliberately preserve obvious spelling mistakes,
grammatical accidents, isolated drafting defects, or story facts merely because
they appear in the sample. The derived profile is a candidate until the author
approves it.

Exact provider/model invocation is outside this Functional Set.

## Generation-quality Boundary

Ruleset-owned generation-quality guidance is not an author-style profile. It is
baseline realization discipline applicable to prose generation generally.

The guidance should suppress common model defaults without banning legitimate
devices. Em dashes, fragments, rhetorical questions, repeated physical
reactions, metaphor, symmetry, and explicit interpretation may still be used
when justified by the scene or accepted author style; they must not become
automatic filler or patterned defaults.

## Style-revision Boundary

An approved profile may be revised without changing its stable profile identity.

The revision operation replaces its current content with a new candidate
revision, records the immediately superseded revision, and requires explicit
production approval before that profile can govern new generation.

FS-007 does not require concurrent active and candidate revisions of one profile.
A selected profile that has been revised back to candidate state blocks new
generation until the candidate is approved or selection is changed. Previously
frozen generation packages remain unchanged.

## Conflict Boundary

Determining that two pieces of guidance materially conflict is a semantic
author-workshop/review responsibility.

Once such a conflict is identified for a generation task, the deterministic
runtime shall preserve it as structured unresolved control state. It shall not
invent precedence, flatten the contradiction, or build a generation-ready
production contract until the conflict is resolved.

FS-007 does not introduce a generalized automatic conflict detector or solver.

## Dataset and Compatibility Boundary

FS-007 retains Dataset schema version 1.

Existing schema-v1 Datasets may omit style profile and style selection state.
Their absence means that no author-specific style profile has been established.

Because the applicable Ruleset realization changes, compatible older bindings
shall use explicit meaning-preserving rebinding. FS-007 does not require a
schema migration merely to add optional style state.

## Reference Demonstration

The executable demonstration shall:

1. construct a candidate style profile from bounded analyzed guidance and sample
   references;
2. prove it remains non-authoritative until explicitly approved;
3. approve and select the profile;
4. revise that approved profile under the same stable identity, prove the
   revision changes, and prove new generation is blocked until re-approval;
5. prove the Ruleset baseline contains general generation-quality guidance;
6. resolve baseline, author, and local style layers for a scene;
7. pass an identified material conflict into resolution and prove production
   contract construction refuses to proceed while it remains unresolved;
8. build a generation package containing a ready frozen projection;
9. prove raw source prose is not injected into the package;
10. persist and reconstruct the profile through the Dataset tree backend;
11. prove a Dataset with no style profile still resolves valid baseline guidance;
12. prove a schema-v1 Dataset bound to the prior Ruleset is rebinding-required,
    not migration-required.

## Explicit Deferrals

FS-007 does not require provider-specific LLM calls, automatic literary-quality
scoring, author impersonation, a universal style ontology, automatic semantic
conflict detection, arbitrary style conflict adjudication, multiple simultaneous
author identities, concurrent active/candidate revisions of one profile, or a
new Dataset schema version.

More elaborate viewpoint-, character-, and manuscript-unit profile precedence
may be added when concrete use demonstrates the need. Scene/mode-local guidance
already remains available as a distinct layer.

## Completion Criterion

FS-007 is complete when prose generation can rely on persistent, reviewable and
revisable author-style guidance plus Ruleset-owned generation-quality guidance,
resolve them with local Prose controls into a bounded generation-time projection,
refuse unresolved declared conflicts, and reconstruct that control state without
conversation memory or Dataset migration.
