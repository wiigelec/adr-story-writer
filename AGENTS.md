# Agent Guidance

This file provides operational guidance and does not independently define normative meaning.

## Default operating mode: ADR Story Writer

Unless the user explicitly asks to inspect, modify, validate, review, or otherwise work on the ADR Story Writer repository itself, operate in **Story Writer application mode**.

In Story Writer application mode:

- the chat Agent is the transient ADR Agent;
- `application.json` defines application initialization instructions;
- the local `ruleset/` is the applicable Story Writer governing semantics;
- the selected external Dataset is the authoritative committed state of one story instance;
- the Story Writer runtime realization mechanically executes applicable governed operations against that Dataset;
- conversation and model-local memory are transient and must not substitute for committed Dataset state.

Read `application.json` and apply its initialization instructions before ordinary story work.

Identify the selected story Dataset and its Ruleset binding, establish compatibility for the requested operation, reconstruct the relevant current Dataset state, and use applicable Story Writer runtime operations rather than manually recreating their mechanics in conversation.

Runtime responsibilities include Dataset reconstruction, compatibility checks, governed artifact and dependency resolution, production-contract and generation-package construction, revision impact analysis, reconciliation mechanics, validation, and Dataset persistence.

The runtime implements Ruleset-owned behavior; it does not replace the Ruleset as semantic authority. The Agent reasons and orchestrates; the Ruleset governs meaning and valid transitions; the Dataset owns committed story state.

Ordinary Dataset saves belong in the Dataset repository being operated and must not mutate this Ruleset repository.

## Repository-governance mode

Enter repository-governance mode only when the user explicitly asks to work on ADR Story Writer itself, such as changing Product Design, Planning, implementation, validation, Ruleset realization, repository structure, or lifecycle state.

When repository-governance mode is active, apply the following repository lifecycle and ownership guidance.

### Lifecycle ownership

A missing consequential semantic decision → **Design**.

A Functional Set, Plan, normative requirement, scope, or evaluation-classification defect → **Planning**.

An implementation or mechanical-enforcement-construction defect → **Build**.

Validation does not create Design meaning or normative requirements.

### Repository ownership

`repo/` is the reusable repository-development framework.

`product/` is the generic product-owned domain. Do not assume Product meaning before Product Design establishes it.

`scripts/` is the narrow repository-wide operational composition role.

`user/` is user-owned operational material outside the framework.

Closed architectural boundaries are default-deny. Do not add new direct children or files where the accepted architecture does not allow them.

### Build discipline

Consume reviewed Design and Planning. Prefer the simplest implementation that preserves their meaning and satisfies applicable normative requirements.

Do not infer normative intent from implementation behavior.

### Validation

Use `scripts/validate` as the repository-wide mechanical Validation entry point. `repo/scripts/validate` remains authoritative for framework mechanical checks.

Mechanical Validation passing does not establish semantic acceptance.

### Semantic Review and Acceptance

Semantic Review evaluates the realized candidate against the complete applicable Design and Planning result.

`main` represents accepted state. Acceptance occurs only through intentional integration of a satisfactory candidate into `main`.

## Runtime realization boundary

Preserve runtime `application.json`, runtime Ruleset material, `provenance.json`, and `init-config/` as distinct roles.

This Ruleset repository is not bound to any Dataset instance; Dataset repositories carry their own Ruleset binding metadata.

The local runtime Ruleset is the accepted operational realization. `product/` is the development domain for later Story Writer product work and must not be treated as ordinary runtime story state.

Do not invent application-specific Product Design, Dataset schema, compatibility, migration, or validation meaning from the generic initialized scaffold.
