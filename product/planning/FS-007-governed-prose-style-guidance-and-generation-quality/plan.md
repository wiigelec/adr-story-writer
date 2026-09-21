---
functional_set: FS-007
artifact: implementation-plan
title: Governed Prose Style Guidance and Generation Quality Plan
design_revision: 33fa138f69b85a15877610760006d7a98e6e376b
---

# FS-007 — Plan

## Objective

Implement persistent author-style profiles and Ruleset-owned generation-quality
guidance, resolve them with existing scene-local mode style, and freeze the
result into scene production contracts and generation packages.

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
- bounded sample provenance references.

Source samples are analysis inputs. The persistent profile stores references and
derived guidance, not a requirement to embed the full samples in every
generation package.

Candidate creation and production approval are explicit separate operations.

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

Add `product/src/style_runtime.py`.

The runtime shall:

- initialize optional FS-007 Dataset state on first style mutation;
- create candidate style profiles from normalized agent output;
- approve a profile explicitly;
- select one approved default profile;
- resolve the current generation-quality baseline, selected approved author
  profile, and supplied local scene/mode guidance into a single structured
  projection;
- preserve the three layers as distinguishable fields rather than flattening
  them into one opaque prompt string.

Material semantic conflicts that cannot be decided mechanically remain a
Semantic Review concern and must not be silently resolved by inventing author
intent.

## Scene Runtime Integration

Extend `scene_runtime.py` so:

- the tree backend optionally loads and persists FS-007 style state;
- `build_production_contract()` resolves style using the selected author profile
  plus existing applicable mode `style` entries;
- the contract includes `style_projection`;
- contract identity changes when the resolved projection changes;
- `build_generation_package()` includes the frozen `style_projection`;
- selected style-profile revision, when present, is included in
  `selected_revisions`;
- raw source sample prose is not copied into the generation package.

The existing `style_voice` field remains as a compatibility/local-mode view.

## Compatibility

Bump the Ruleset identity to `0.4.0` while retaining Dataset schema version 1.

Register meaning-preserving rebinding paths from supported earlier Rulesets,
including `0.3.0 -> 0.4.0`.

Update the Dataset initialization template to bind to `0.4.0` and initialize
empty style state.

No FS-007 Dataset migration is introduced.

## Validation

Add `product/validation/fs007_validation.py` and register it from
`validate_product.py`.

Validation shall cover:

- exact Planning Design binding;
- profile candidate/approval/selection behavior;
- sample provenance without raw-sample package injection;
- presence and shape of general generation-quality guidance;
- layered style projection;
- production-contract and generation-package integration;
- generation-package stability and style-profile revision selection;
- optional style state and fresh-session reconstruction;
- schema-v1 rebinding from Ruleset `0.3.0` to `0.4.0`;
- Dataset boundary;
- complete Requirement Evaluation Manifest bindings.

Semantic-only obligations remain for Semantic Review.

## Build Boundary

Do not add a provider SDK, style-scoring system, second persistence database,
Dataset schema v2, automatic author impersonation, or generalized style-conflict
solver.
