# Instruction Governance

Status: Approved
Last updated: 2026-09-10

## Confirmed

### Purpose and boundary

This initiative defines two lightweight governance mechanisms for Devquitect instructions and
evaluation evidence. It changes neither a skill's product behavior nor release artifacts yet.
Its outcome is (1) a small authority map and objective checks for cross-file critical contracts,
and (2) deterministic promotion plus versioned behavior-calibration reports for model evidence.

The actors are skill maintainers, contributors, the evaluation runner, and a maintainer
who reviews a release proposal. The scope is the authority relationship among skill
instructions, reference documents, executable cases and assertions, semantic rubrics,
evaluation classification, promotion policy, and contributor guidance.

### Proposed authority and validation model

The mechanism will list only the cross-file critical contracts: authorization, scoped mutation,
durable state, approval gates, evidence classification, and promotion eligibility. Each has one
owner and may be linked, explained, or tested elsewhere. The repository validator checks objective
facts about that small map: unique contract IDs, a real owner path, permitted reference paths, and
existing local-reference integrity.

External deterministic cases own behavioral protection for each critical contract, including a
negative case where a relevant violation is observable. These checks live outside `skills/` and are
not installed with the plugin.

This is intentionally not a registry for every instruction or a linter for arbitrary prose. It
cannot prove that two unmarked Markdown sentences contradict each other; that remains a focused
review and, when needed, semantic-diagnostic concern. This boundary keeps the installed skills
short and avoids metadata on routine instruction edits.

### Current authority map

| Concern | Authoritative owner | Supporting evidence / presentation |
| --- | --- | --- |
| When a skill applies and its behavioral boundary | `skills/*/SKILL.md` | Skill-local references and `agents/openai.yaml` |
| Detailed durable-state, approval, and workflow rules | The named file in `skills/*/references/` | `SKILL.md` routes to it; `docs/contributing-skills.md` explains usage |
| Observable safety invariants | Versioned cases in `evals/cases/` plus executable assertion semantics in `src/devquitect_quality/assertions.py` | Case schema validates shape |
| Deterministic verdict precedence and inconclusive runtime handling | `src/devquitect_quality/grading.py` | Evaluation reports and unit tests |
| Semantic diagnostic dimensions | Versioned rubric in `evals/rubrics/` | The case's `semantic_rubric` reference |
| Case and report data contracts | `schemas/eval-case.schema.json` and `schemas/report.schema.json` | Loaders and report builders |
| Stable/candidate classification | `src/devquitect_quality/comparison.py` | Comparison report |
| Release-eligibility evidence and promotion proposal | `src/devquitect_quality/promotion.py` and `schemas/promotion-record.schema.json` | `docs/contributing-skills.md` operational walkthrough |

`grading.py` currently makes a critical deterministic failure a failure and infrastructure
or missing critical evidence inconclusive. Semantic grades are retained but do not alter
that classification. `promotion.py` requires passing release-eligible evaluation and a
passing clean-candidate comparison, but has no semantic-threshold owner. All present
versioned cases use one repetition; therefore no existing 15/15 rule is encoded.

### Proposed promotion policy

1. Deterministic critical assertions are the release contract: every applicable assertion
   must pass. A critical failure blocks promotion regardless of semantic grades.
2. Runtime, judge, authentication, CLI, and environment faults are **inconclusive**. They
   block satisfying the affected evidence requirement, but are neither behavioral failures
   nor a reason to edit instructions until diagnosed.
3. Promotion requires deterministic evidence only: the complete credential-free suite,
   immutable source/artifact identities, and explicit maintainer approval.
4. Model-backed scenarios produce optional behavior-calibration reports and never block
   promotion.
5. A report binds skill version, model/runtime, suite version, repetitions, observed outcomes,
   and a dimension profile; its summary score is comparable only under that configuration.

### Behavior calibration

The current evaluator executes a fresh agent run and checks observable effects, rather than
testing a model's private interpretation. That is the correct measurement surface, but the
current promotion policy treats any failed critical assertion as an absolute failure. It does not
yet distinguish a candidate-caused regression from a limitation or variance shared by the stable
model.

The evidence also shows that semantic rubrics and `forbidden_effects` are declared by cases but
not consumed by the evaluation or promotion path; all current cases run once; and comparison
currently retains only one record per case ID when repetitions exist. Therefore the current
implementation cannot support a sound threshold policy for semantic or repeated model behavior.

Calibration informs human review, model selection, and investigation. Missing calibration means
unknown behavior under that configuration, not failure. Safety needing certainty uses a
deterministic guardrail.

### Preserved behavior

- Explicit Gate 1/Gate 2 and implementation-authorization boundaries remain mandatory.
- Scoped mutation, durable-state integrity, ownership boundaries, and critical safety
  assertions remain non-overridable.
- Working-tree evidence remains diagnostic-only; promotion remains tied to an immutable
  candidate, matching snapshots, and explicit maintainer approval.
- A reviewed contract change cannot override a critical safety regression.

## Assumptions

- The policy will add no new external service or dependency.
- The affected human interaction surface is not applicable: this is an internal policy and
  CLI/report contract, not a new human-facing workflow. Existing command and report UX stays
  governed by contributor guidance and schemas.

## Open decisions

None.
