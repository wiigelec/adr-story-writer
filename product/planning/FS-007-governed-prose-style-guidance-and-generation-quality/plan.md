---
functional_set: FS-007
artifact: implementation-plan
title: Governed Prose Style Guidance and Generation Quality Plan
design_revision: 08c6670ede17618f8b99c77e648168caeff1351f
---

# FS-007 — Plan

## Objective

Implement persistent and revisable author-style profiles plus Ruleset-owned
generation-quality guidance, resolve them with existing scene-local mode style,
surface declared material style conflicts, and freeze only ready projections
into scene production contracts and generation packages.

## Dataset Representation

Dataset schema remains `adr-story-writer.dataset` version `1`.

Under `prose`, FS-007 adds optional state:

```json
{
  "style_profiles": {},
  "style_selection": {
    "default_profile": null
  }
}
```

An absent `style_profiles` or `style_selection` member is valid and means no
author-specific FS-007 state has yet been established.

For the split/tree Dataset backend, persist these optional members as:

- `dataset/prose/style-profiles.json`
- `dataset/prose/style-selection.json`

Do not require these files for older schema-v1 Datasets.

## Style Profile

A style profile is Prose production-control state. It is not Canon, Plot, or
Manuscript authority.

A profile records:

- stable profile identity;
- `surface: prose.style_profile`;
- production candidate/approved authority class;
- durable content revision;
- normalized guidance;
- bounded sample provenance references;
- the immediately superseded revision when the profile is a revision of prior
  approved guidance.

Source samples are analysis inputs. Persistent provenance is limited to bounded
reference metadata rather than arbitrary source sample content.

Candidate creation and production approval are explicit separate operations.

## Stable Profile Revision

Add a deterministic `revise_style_profile()` operation.

The operation shall:

- require an existing `production_approved` profile;
- preserve the profile's stable `id`;
- replace normalized guidance and bounded provenance with the proposed revision;
- compute a new durable revision identity;
- record the prior durable revision as `supersedes_revision`;
- set the profile back to `production_candidate`;
- leave a default selection that names that profile intact, but make the
  selected candidate unusable for new generation until re-approved.

Approval returns the revised profile to `production_approved`.

FS-007 intentionally does not maintain concurrent approved and candidate
versions for the same stable profile. Previously materialized generation
packages remain stable because they contain the frozen earlier projection and
selected revision.

## Sample Analysis

The author-workshop agent performs prose-sample interpretation and supplies the
normalized candidate guidance to the deterministic runtime.

The runtime does not make provider-specific model calls.

The agent shall distinguish stable realization tendencies from obvious errors,
isolated scene facts, and accidental draft artifacts. This is a Semantic Review
obligation; deterministic validation shall not pretend to prove literary
inference quality.

## General Generation-quality Guidance

Store baseline generation-quality guidance in `ruleset/prose.json`.

The baseline shall include mechanically inspectable categories covering at
least:

- semantic restraint and avoidance of redundant interpretation;
- repetition/restatement restraint;
- patterned-construction restraint;
- physical micro-reaction restraint;
- concrete description over generic atmospheric filler;
- dialogue variation and avoidance of uniformly polished exchanges;
- selective figurative language;
- natural sentence/paragraph variation.

Guidance is phrased as defaults and restraint, not categorical bans on valid
literary devices.

## Style Resolution

`product/src/style_runtime.py` shall:

- initialize optional FS-007 Dataset state on first style mutation;
- create candidate style profiles from normalized agent output;
- revise an approved profile under stable identity into a new candidate revision;
- approve a profile explicitly;
- select one approved default profile;
- resolve the current generation-quality baseline, selected approved author
  profile, and supplied local scene/mode guidance into one structured projection;
- accept an optional structured list of material conflicts identified by the
  author-workshop or Semantic Review;
- mark the projection `ready` when no declared conflict exists and `unresolved`
  when one or more material conflicts are declared;
- preserve general, author, and local guidance as distinguishable layers.

A material conflict record shall be bounded diagnostic control state, not a
semantic decision. At minimum it contains a non-empty `description`; it may also
identify involved layers or references.

The deterministic runtime does not infer literary conflict from arbitrary prose
guidance and does not solve conflicts.

## Scene Runtime Integration

Extend `scene_runtime.py` so:

- the tree backend optionally loads and persists FS-007 style state;
- `build_production_contract()` resolves style using the selected author profile
  plus existing applicable mode `style` entries;
- callers may provide declared material style conflicts for the current task;
- production-contract construction refuses to proceed if the resolved projection
  is `unresolved`;
- a ready contract includes `style_projection`;
- contract identity changes when the ready resolved projection changes;
- `build_generation_package()` includes the frozen ready `style_projection`;
- selected style-profile revision, when present, is included in
  `selected_revisions`;
- raw source sample prose is not copied into the generation package.

The existing `style_voice` field remains as a compatibility/local-mode view.

## Compatibility

Ruleset identity remains `0.4.0`; Dataset schema remains version 1.

Meaning-preserving rebinding paths from supported earlier Rulesets, including
`0.3.0 -> 0.4.0`, remain applicable.

The Dataset initialization template remains bound to `0.4.0` and initializes
empty style state.

No FS-007 Dataset migration is introduced.

## Validation

`product/validation/fs007_validation.py` shall cover:

- exact Planning Design binding;
- profile candidate/approval/selection behavior;
- bounded sample provenance without raw-sample package injection;
- stable-identity profile revision, changed content revision, supersession
  provenance, and required re-approval;
- selected candidate profile blocking new style resolution;
- presence and shape of general generation-quality guidance;
- layered ready style projection;
- preservation of declared conflict diagnostics;
- refusal to construct a production contract while a declared material conflict
  remains unresolved;
- production-contract and generation-package integration;
- generation-package stability and selected style-profile revision;
- optional style state and fresh-session reconstruction;
- schema-v1 rebinding from Ruleset `0.3.0` to `0.4.0`;
- Dataset boundary;
- complete Requirement Evaluation Manifest bindings.

Semantic-only obligations remain for Semantic Review, including whether sample
analysis normalized stable tendencies correctly and whether a declared conflict
is materially meaningful.

## Build Boundary

Do not add a provider SDK, style-scoring system, second persistence database,
Dataset schema v2, automatic author impersonation, generalized semantic
conflict detector/solver, or concurrent active/candidate history store.
