---
functional_set: FS-005
artifact: functional-set-scope
title: Governed Author Workshop and Progressive Story Development
design_revision: 21e017572c31f0aa9b95b9de0785f557511949b1
---

# FS-005 — Governed Author Workshop and Progressive Story Development

## Purpose

FS-005 realizes the majority of the remaining ordinary authoring capability
defined by Product Design so ADR Story Writer can be used primarily through an
agent conversation rather than by hand-editing Dataset JSON.

FS-001 established authority, candidate, production, review, acceptance, and
persistence semantics. FS-002 established compatibility. FS-003 established
bounded production from an already-planned scene. FS-004 established safe
accepted-upstream revision and downstream reconciliation.

FS-005 closes the ordinary author-workshop gap:

> Given a compatible persisted story Dataset that may be incomplete, partially
> developed, or already accepted, the Product can reconstruct current governed
> state; expose understandable author-facing views; create and refine candidate
> Canon, Plot, and Prose/production artifacts; explicitly accept or approve them
> with dependency closure; determine generation readiness; persist candidate and
> accepted working state coherently; revise already-accepted Canon or Plot through
> FS-004; and hand a ready scene directly into FS-003 production.

Consequential story authority remains with the author. Conversation and model
suggestion remain non-authoritative until represented by an explicit governed
candidate and accepted at its owning surface.

## Exact Design Binding

Planning consumes Product Design at repository revision:

`21e017572c31f0aa9b95b9de0785f557511949b1`

FS-005 introduces no new Product Design. It realizes already accepted obligations
from DP-100 through DP-190, especially DP-100, DP-110, DP-120, DP-130, DP-140,
DP-150, DP-160, DP-170, DP-175, DP-180, and DP-190.

## Functional Boundary

FS-005 begins with an external Story Writer Dataset, an applicable compatible
Ruleset, zero or more accepted/candidate governed artifacts, and an author
interacting through an agent or other orchestration layer.

FS-005 ends when the Product can:

1. reconstruct governed authoring state without prior-chat memory;
2. provide derived story, Canon, Plot, Prose, candidate, Manuscript, and readiness
   views without creating shadow authority;
3. create and refine new Canon and Plot candidate artifacts;
4. create Prose/production candidate artifacts for progressive refinement;
5. explicitly accept semantic candidates and approve production candidates;
6. enforce material dependency closure, including explicit coordinated acceptance;
7. withdraw pending new-artifact candidates without changing accepted work;
8. preserve pending candidates across save and fresh-session reconstruction;
9. use FS-004 for revision of already-accepted Canon or Plot artifacts;
10. determine when a scene is ready for ordinary FS-003 production;
11. hand ready work into the existing context/contract/package workflow;
12. persist coherent authoring state with stale-session conflict detection.

## Reference Demonstration

The executable demonstration shall begin from a minimally initialized external
story Dataset rather than a pre-planned production fixture. It shall create and
accept Canon, create and accept Plot, show a scene not ready before local Prose
controls, create and approve Beats/Mode/pseudo-prose, show readiness restored,
construct an FS-003 generation package, persist/reconstruct a pending candidate,
exercise one accepted-upstream FS-004 revision, prove dependency closure, and
prove stale-session conflict safety.

## Agent Boundary

FS-005 does not require a provider-specific LLM client. The agent may perform
semantic interpretation, proposal drafting, critique, refinement, and review.
The deterministic runtime owns mechanically enforceable authority transitions,
identity/revision handling, dependency closure, compatibility, readiness gating,
persistence, and reconstruction.

Natural-language conversation is input to governed operations, not a persistence
or acceptance mechanism by itself.

## Explicit Deferrals

FS-005 does not require autonomous authorship, automatic semantic acceptance,
perfect inversion of arbitrary natural-language edits, universal free-text
dependency inference, a graph database, full arbitrary split/merge lifecycle,
sophisticated editable dossiers, manuscript-wide publication tooling,
provider-specific model integrations, multi-user merge resolution, or large-story
index optimization.

## Completion Criterion

FS-005 is complete when an author can begin with an incomplete compatible Dataset
and, through governed operations suitable for an agent-driven chat UI, develop
Canon and Plot, refine a scene through Prose controls to generation readiness,
persist and reconstruct candidate and accepted state, and enter the existing
FS-003 production workflow without manually editing Dataset storage structures.
