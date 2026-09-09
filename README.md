# Repository

This repository uses an installed repo-spec lifecycle framework.

## Lifecycle

Work proceeds through Design, Planning, Build, Validation, Semantic Review, and Acceptance.

`main` represents accepted repository state.

## Repository surfaces

- `repo/design/` — installed framework Design.
- `repo/specs/` — installed framework normative specifications.
- `repo/scripts/validate` — framework-owned mechanical Validation entry point.
- `scripts/validate` — repository-wide mechanical Validation entry point.
- `product/` is the product-owned domain. Product meaning is established independently through Product Design.
- `product/design/` — starting surface for Product Design.
- `user/` — user-owned operational material outside the framework.

Begin substantive product work in Product Design.

The exact repo-spec framework source revision used to initialize this repository is recorded in `repo/validation/framework-source.json`.

Validation is mechanical evaluation only. Semantic Review evaluates meaning and fidelity. Acceptance is intentional integration of a satisfactory candidate into `main`.

## App Builder runtime realization

This repo-spec-managed repository is the Ruleset product-development home for an ADR App Builder `split-git` realization. The installed lifecycle does not redefine application-owned Ruleset meaning.

## Runtime components

- application: `application.json` (file)
- ruleset: `ruleset` (tree)## Initialization inputs

`init-config/` contains immutable construction inputs and reproduces the App Builder construction invocation. It is not runtime semantic authority.



## Dataset binding boundary

This Ruleset repository is not bound to any Dataset instance. One or more independent Dataset repositories may identify this Ruleset realization through their own `binding.json` metadata. Construction provenance and retained `init-config/` inputs do not create a reverse Ruleset-to-Dataset binding.

## Provenance

`provenance.json` records ADR, App Builder, and repo-spec construction lineage and upgrade anchors. It is not a runtime component or semantic authority.
