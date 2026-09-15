# FS-001 — Governed Prose Production and Acceptance

## Status

Candidate Functional Set for ADR Story Writer 0.1.

## Purpose

FS-001 defines the minimum coherent Product capability required to turn the
accepted Story Writer Product Design into an operable governed prose workflow.

The Functional Set establishes one end-to-end vertical slice:

> An author can reconstruct governed story state from a Dataset, prepare a
> bounded prose-generation task from governed Canon and Plot, generate candidate
> prose, review consequential invention and other semantic violations, accept or
> reject the result at explicit scopes, and persist the resulting state without
> confusing candidate, accepted semantic, production-approved, and accepted
> Manuscript authority.

FS-001 does not require autonomous authorship. Consequential story authority
remains with the author.

## Design Traceability

FS-001 realizes the minimum required behavior from:

- DP-100 — Story Writer Product Architecture
- DP-110 — Story State, Authority, Acceptance, and Reconciliation
- DP-120 — Workflow, Dependency, and Reconciliation
- DP-130 — Canon, Plot, Viewpoint, and Reader Information
- DP-140 — Canon State, Events, Knowledge, and Narrative Time
- DP-150 — Prose Control and Generation Packages
- DP-160 — Dataset Persistence and Session Reconstruction
- DP-175 — Artifact Identity, Semantic Scope, and Cross-Layer Traceability
- DP-180 — Validation, Semantic Review, and Integrity

DP-170 and DP-190 remain applicable Product Design but their broader migration,
rebinding, generated-view, and extensibility capabilities are not required to be
fully realized by this Functional Set unless needed to satisfy a requirement
below.

## Functional Boundary

FS-001 begins with an identified compatible Story Writer Ruleset and one story
Dataset.

FS-001 ends when a bounded prose candidate and any consequential discoveries
have been intentionally resolved at the applicable authority scopes, accepted
or rejected by the author, and the authorized resulting state has been
persisted coherently.

The implementation may support additional workflows, but those workflows must
not weaken the requirements in this Functional Set.

## Normative Requirements

### FS001-R01 — Fresh-session reconstruction

The Product shall reconstruct enough governed state from the Dataset and
applicable Ruleset to continue the requested story work without relying on prior
conversation or private model memory.

Reconstruction shall preserve, where present and relevant:

- accepted Canon;
- accepted Plot;
- persistent Prose guidance;
- accepted Manuscript;
- persisted candidate state;
- production-approved control state;
- unresolved consequential candidate dependencies;
- reconciliation state;
- and generation provenance required to interpret persisted candidates.

If authority classification or a material dependency cannot be established
reliably, the affected material shall remain unresolved rather than being
promoted by inference.

### FS001-R02 — Governed identity and authority classification

Every persisted governed artifact or durable semantic scope used by this
Functional Set shall be identifiable sufficiently to support acceptance,
dependency tracking, revision, provenance, and later reconstruction.

The Product shall distinguish at least:

- accepted semantic state;
- candidate semantic state;
- production-control candidate state;
- production-approved control state;
- candidate prose or Manuscript text;
- and accepted Manuscript state.

Persistence shall not itself change authority classification.

### FS001-R03 — Candidate dependency preservation

A candidate may depend on accepted state, candidate state, or both.

Where an unresolved consequential candidate assumption materially constrains a
downstream candidate, the Product shall preserve enough dependency information
to identify that dependency during review, acceptance, persistence, and later
session reconstruction.

Historical derivation that no longer materially constrains the current candidate
need not remain an acceptance dependency.

### FS001-R04 — Lowest-layer workflow navigation

The Product shall attempt to resolve the author's request at the lowest semantic
layer capable of preserving intended meaning.

A downstream revision shall not silently rewrite accepted upstream meaning.

When a requested downstream change requires consequential upstream revision,
the Product shall surface that revision as a proposal at the owning semantic
surface.

### FS001-R05 — Production contract

Before bounded prose generation, the Product shall establish a production
contract sufficient for the requested generation task.

The production contract shall be capable of representing, as applicable:

- generation scope;
- stopping boundary;
- intended narrative movement;
- required Beats or equivalent local realization units;
- viewpoint and information-access constraints;
- reveal and concealment obligations;
- relevant entry and exit conditions;
- applicable persistent Prose guidance;
- local style or voice constraints;
- protected wording, terminology, meaning, or structure;
- permitted creative allowance;
- prohibited consequential invention;
- accepted dependencies;
- and declared candidate dependencies.

If the task cannot be bounded reliably at the selected scope, refinement shall
continue or the unresolved decision shall be surfaced before generation.

### FS001-R06 — Generation package

Each generation attempt shall consume a task-specific generation package derived
from the applicable production contract and governed state.

The package shall contain or identify the minimum sufficient governing context
required for the task and shall exclude unrelated material where inclusion would
materially increase distraction or unsupported-inference risk.

The package shall identify enough revision or semantic-scope information to
determine what governed the generation attempt.

Once used for generation, the governing meaning of that package shall remain
stable for later review and provenance.

### FS001-R07 — Information-access safety

Generation shall preserve the distinction between objective Canon available to
the author or reviewer and information that the current viewpoint or reader may
access.

The Product shall not rely solely on unstated model memory to preserve reveal,
concealment, or viewpoint restrictions.

Where hidden Canon must constrain generation, the implementation shall
represent that constraint in a way that does not authorize disclosure.

### FS001-R08 — Candidate-only generation

Generated prose shall begin as candidate state.

Generation shall not by itself:

- create accepted Canon;
- create accepted Plot;
- approve a production-control artifact;
- accept Manuscript text;
- or authorize persistence.

Generated content beyond the authorized stopping boundary shall remain candidate
overflow and shall not be treated as governed continuation.

### FS001-R09 — Generated-prose semantic review

Before candidate prose is accepted as Manuscript, the Product shall support
review against the governing package or equivalent complete context.

Review shall be capable of evaluating, as applicable:

- requested scope and stopping boundary;
- required narrative movement;
- Canon consistency;
- Plot fidelity;
- viewpoint access;
- reveal and concealment timing;
- applicable Prose guidance;
- protected material;
- creative allowance;
- unauthorized consequential invention;
- and local continuity with supplied accepted text.

When required governing context is incomplete or stale, the affected review
criterion shall be surfaced as unresolved or indeterminate rather than passed by
guessing.

### FS001-R10 — Consequential invention handling

Consequential meaning introduced downstream without governing authority shall be
identified as candidate meaning at the semantic surface that owns it.

The Product shall not silently promote consequential invention because it is
fluent, repeated, mechanically valid, persisted, production-approved, or
accepted as wording.

The author shall be able to reject the invention, revise the downstream
candidate to remove dependence on it, or review it as a separate proposal at its
owning semantic surface.

### FS001-R11 — Explicit acceptance operations

The Product shall preserve the semantic distinction among:

- semantic acceptance;
- production approval;
- Manuscript acceptance;
- revision acceptance where previously accepted meaning is superseded;
- and persistence authorization.

One author interaction may intentionally combine several operations, but one
operation shall not be silently inferred from another.

Acceptance shall apply to an identifiable scope.

### FS001-R12 — Acceptance closure

A downstream candidate shall not be accepted in a way that silently promotes
unresolved consequential meaning on which the accepted scope materially
depends.

Before or as part of acceptance, every unresolved consequential dependency
required by the accepted scope shall be:

- accepted at its owning semantic surface;
- revised into an accepted alternative and reconciled in the downstream result;
- explicitly excluded from the accepted scope;
- or left unresolved, in which case the dependent portion shall remain
  candidate.

### FS001-R13 — Coherent persistence

The Product shall support authorized persistence of the resulting governed state
while preserving authority classification, material dependencies, and required
generation provenance.

A persisted candidate shall remain candidate.

A partial physical write shall not be reported as a successful logical save.

If persistence fails, the Product shall not claim that the new Dataset state is
durably saved.

### FS001-R14 — Fresh-session continuation proof

A Dataset state produced through FS-001 shall contain enough persisted
information that a fresh session can reconstruct and correctly interpret the
accepted and intentionally persisted candidate state required to continue the
same work without prior-chat memory.

## Mechanical Evaluation Requirements

The Build shall provide deterministic validation for all mechanically decidable
FS-001 invariants that it represents structurally.

At minimum, mechanical validation shall cover, where structurally applicable:

- required identity fields;
- authority-class values;
- valid durable references;
- dependency endpoint resolution;
- required production-contract fields;
- generation-package completeness;
- generation-package provenance references;
- candidate-versus-accepted classification;
- explicit generation boundaries;
- and persistence structure required for fresh-session reconstruction.

Mechanical validation shall not claim to establish semantic acceptance.

## Semantic Review Requirements

The following remain semantic-review concerns where their correctness depends on
story meaning rather than structure:

- Canon/Plot fidelity;
- preservation of higher-level Plot intent;
- Prose realization fidelity;
- viewpoint and information-access correctness;
- reveal and concealment correctness;
- consequential-invention classification;
- adequacy of creative allowance;
- semantic protection of non-verbatim protected material;
- generation readiness where sufficiency depends on narrative meaning;
- and acceptance-scope fidelity to author intent.

A semantic-review result shall be interpreted only for the scope and governing
context actually reviewed.

## Required Demonstration

FS-001 is semantically satisfactory only when the implemented Product can
demonstrate this complete workflow:

1. start a fresh session with no prior-chat dependency;
2. identify the active Dataset and Ruleset;
3. reconstruct relevant governed state with authority classifications intact;
4. receive an author request for bounded prose work;
5. retrieve applicable Canon, Plot, Prose guidance, and candidate assumptions;
6. refine the task until generation-ready;
7. establish a production contract;
8. materialize a stable generation package;
9. generate candidate prose within its authorized boundary;
10. review the candidate against the governing context;
11. surface consequential invention or unresolved dependencies;
12. perform only author-authorized acceptance operations;
13. enforce acceptance closure;
14. persist an authorized coherent Dataset state; and
15. begin another fresh session and reconstruct the resulting state correctly.

## Explicit Deferrals

FS-001 does not require, except where necessary to satisfy the requirements
above:

- a complete general-purpose migration engine;
- downgrade support;
- arbitrary Ruleset rebinding workflows;
- a comprehensive generated-dossier or generated-view system;
- a universal visible artifact-status taxonomy;
- a mandatory fixed story-artifact hierarchy beyond the runtime choices needed
  for this Functional Set;
- deterministic reproduction of identical literary wording;
- or autonomous acceptance of consequential story decisions.

These capabilities may be introduced by later Functional Sets without weakening
FS-001 authority, dependency, provenance, or acceptance semantics.
