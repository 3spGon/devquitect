# Skill Change Ledger

This versioned ledger records each named prompt rule group. Baselines use immutable Git references. Candidate snapshot IDs are SHA-256 hashes of the listed worktree files; the source text is reconstructed from those paths and checked against its hash. Append new records without rewriting prior entries.

## PC-DN-001-DEF — Definition workflow and authority boundary

- **Baseline:** `git:7f7030813b7995a9a93cbf4a43cbafb9c8dddeb5` — `skills/software-idea-to-project/SKILL.md`
- **Candidate:** `worktree-sha256:6912f485c5f900737b340d5c57a88f77b3021740c0419dcec62467082897ce27` — `skills/software-idea-to-project/SKILL.md`
- **Scope:** Lean definition entrypoint; explicit gates and implementation handoff remain intact.
- **Disposition:** move
- **Deterministic cases:** `software-idea-positive`, `software-idea-negative`, `gate-one-bypass` (unchanged representative cases)
- **Behavioral configuration:** Not run; comparison requires separate authorization.
- **Evidence:** Credential-free check and command results are recorded in [SLICE-DN-001 evidence](software-design/devquitect-next/slices/SLICE-DN-001.md).
- **Verdict:** inconclusive
- **Rationale:** Detailed discovery, session-state, and planning mechanics remain in their referenced owners. No behavior comparison was authorized.

## PC-DN-001-DEL — Delivery authorization and verified close

- **Baseline:** `git:7f7030813b7995a9a93cbf4a43cbafb9c8dddeb5` — `skills/project-plan-execution/SKILL.md`, `skills/project-plan-execution/references/execution.md`
- **Candidate:** `worktree-sha256:d9a87dd0cec6e7f7e8f1d08615890fc64eeb14fff502389728ea29deb237fdca` — `skills/project-plan-execution/SKILL.md`; `worktree-sha256:607ea8e3828fb782b057da6118af1a974bb4acbc895f377ca9f4fbd937d93ae4` — `skills/project-plan-execution/references/execution.md`
- **Scope:** Lean entrypoint; authorized handoff preflight, durable delivery state, slice execution, and evidence close have canonical owners.
- **Disposition:** move
- **Deterministic cases:** `plan-execution-positive`, `plan-execution-negative`, `delivery-authorization-matching-positive`, `delivery-authorization-conflict-negative` (unchanged representative cases)
- **Behavioral configuration:** Not run; comparison requires separate authorization.
- **Evidence:** Credential-free check and command results are recorded in [SLICE-DN-001 evidence](software-design/devquitect-next/slices/SLICE-DN-001.md).
- **Verdict:** inconclusive
- **Rationale:** Authorization boundaries remain in the entrypoint and detailed execution mechanics remain in their owners. No behavior comparison was authorized.

## PC-DN-001-REF — Behavior-preserving refactor workflow

- **Baseline:** `git:7f7030813b7995a9a93cbf4a43cbafb9c8dddeb5` — `skills/targeted-refactoring/SKILL.md`
- **Candidate:** `worktree-sha256:30738c7bae7b76579e66103586dcaed1b55a54ee79282cbedbb70018230397cf` — `skills/targeted-refactoring/SKILL.md`; `worktree-sha256:fb34f0c8fbfd5f79a3ce017c3e4df3c8cbab81b4bd8eb91eea9db11163947cf5` — `skills/targeted-refactoring/references/workflow.md`
- **Scope:** Lean refactoring entrypoint and its detailed workflow owner.
- **Disposition:** move
- **Deterministic cases:** `refactoring-positive`, `refactoring-negative` (unchanged representative cases)
- **Behavioral configuration:** Not run; comparison requires separate authorization.
- **Evidence:** Credential-free check and command results are recorded in [SLICE-DN-001 evidence](software-design/devquitect-next/slices/SLICE-DN-001.md).
- **Verdict:** inconclusive
- **Rationale:** Review, authorization, behavior-preservation, and verification mechanics remain in the new workflow reference. No behavior comparison was authorized.

## BC-DN-001-001 — SLICE-DN-001 authorized behavioral comparison

- **Authorization:** Explicit user authorization received 2026-09-24.
- **Stable:** `git:7f7030813b7995a9a93cbf4a43cbafb9c8dddeb5`, snapshot `sha256:d3ae013072604f67f6f72e85c709334367134e33bdffa98e28adc6927507e359`.
- **Candidate:** `working-tree`, snapshot `sha256:1174fe6026afbcc4ca05821371a365e15962133f81e1bc513ef45d1cd1ac0073` (diagnostic-only).
- **Configuration:** `gpt-5.6-luna`, reasoning effort `high`, Codex CLI 0.154.0, devquitect-quality 0.1.0, one repetition per case. Supervised `chatgpt-cache-local` authentication was allowed and cleaned in every report.
- **Case results:** `software-idea-positive`, `software-idea-negative`, `gate-one-bypass`, `plan-execution-positive`, `plan-execution-negative`, `delivery-authorization-matching-positive`, `delivery-authorization-conflict-negative`, `refactoring-positive`, and `refactoring-negative` all returned `pass` and `equivalent`, with zero critical assertion failures.
- **Evidence:** Per-case reports are `.devquitect-reports/slice-dn-001-<case-id>.json`; the structured summary is recorded in [SLICE-DN-001 evidence](software-design/devquitect-next/slices/SLICE-DN-001.md).
- **Runtime notes:** The stable `software-idea-positive` run logged a unified exec process creation error, and the stable `plan-execution-positive` run logged a model-list refresh timeout. Both records still classified as `pass`, and both paired comparisons returned `equivalent`; the messages remain in their reports.
- **Verdict:** equivalent for the tested cases; diagnostic-only because the candidate was a working tree.
- **Rationale:** The same baseline, candidate, model, reasoning effort, and nine representative positive/negative cases were used for both sides. This follow-up supplements, and does not rewrite, the original pre-authorization PC-DN-001 records.

## PC-DN-003-WFD — Common workflow depth

- **Baseline:** `git:2a14c35e44eab2c96338b3f969d9cdfa30e5973c` — `skills/software-idea-to-project/SKILL.md`, `skills/software-idea-to-project/references/change-profile.md`, `skills/software-idea-to-project/references/discovery.md`
- **Candidate:** `worktree-sha256:e5a3626eb32efca1b6ac48dd77b026c2bfb2e7e7eb51aded98b0705d30254be6` — `skills/software-idea-to-project/SKILL.md`; `worktree-sha256:b472fbedba0caf64e83726ed0fb39e39d401c613a4a24e1152cb9ba52254180c` — `skills/software-idea-to-project/references/workflow-depth.md`; `worktree-sha256:d44eabb439adf6e9e5ae9fc135f180090869b285e3b6b087e77da34058fe9367` — `skills/software-idea-to-project/references/discovery.md`; `worktree-sha256:b5757ee892675b81fe06c17c1336029e157612681dbb300297f3b89f100b05ca` — `skills/software-idea-to-project/references/change-profile.md`
- **Scope:** Select and record common workflow depth for new-system, system-change, and hybrid initiatives while preserving Change Profile values.
- **Disposition:** move
- **Deterministic cases:** `software-idea-workflow-depth-new-system`, `software-idea-workflow-depth-system-change`, `software-idea-workflow-depth-hybrid`, `software-idea-workflow-depth-legacy`, `software-idea-positive`, `software-idea-negative`, `gate-one-bypass` (all candidate cases passed)
- **Behavioral configuration:** Candidate-only functional evaluations on `gpt-5.6-luna`, reasoning effort `high`, supervised local authentication, one repetition per case; no paired baseline comparison.
- **Evidence:** `.devquitect-reports/slice-dn-003-workflow-depth-new-system.json`, `.devquitect-reports/slice-dn-003-workflow-depth-system-change.json`, `.devquitect-reports/slice-dn-003-workflow-depth-hybrid.json`, `.devquitect-reports/slice-dn-003-workflow-depth-legacy.json`, and [SLICE-DN-003 evidence](software-design/devquitect-next/slices/SLICE-DN-003.md).
- **Verdict:** inconclusive
- **Rationale:** All candidate cases and credential-free repository checks passed. The results are diagnostic-only because they use a working tree and do not establish a paired baseline comparison.

## PC-DN-003-ROOT — Persistent definition-root continuity

- **Baseline:** `git:2a14c35e44eab2c96338b3f969d9cdfa30e5973c` — `skills/software-idea-to-project/SKILL.md`, `skills/software-idea-to-project/references/session-state.md`, `skills/software-idea-to-project/references/discovery.md`
- **Candidate:** `worktree-sha256:e5a3626eb32efca1b6ac48dd77b026c2bfb2e7e7eb51aded98b0705d30254be6` — `skills/software-idea-to-project/SKILL.md`; `worktree-sha256:3ef05fa03e53b8b7e3ace7017ddf37aa6b308baab34b07a3acb9dd3ce08aee16` — `skills/software-idea-to-project/references/session-state.md`; `worktree-sha256:d44eabb439adf6e9e5ae9fc135f180090869b285e3b6b087e77da34058fe9367` — `skills/software-idea-to-project/references/discovery.md`; `worktree-sha256:b472fbedba0caf64e83726ed0fb39e39d401c613a4a24e1152cb9ba52254180c` — `skills/software-idea-to-project/references/workflow-depth.md`
- **Scope:** Store one repository-relative definition root, resume from the recorded location, preserve legacy paths, and ask when discovery is ambiguous.
- **Disposition:** move
- **Deterministic cases:** `software-idea-definition-root-resume`, `software-idea-definition-root-ambiguity`, `software-idea-definition-root-invalid`, `software-idea-workflow-depth-legacy`, `software-idea-positive`, `software-idea-negative` (all final candidate cases passed)
- **Behavioral configuration:** Candidate-only functional evaluations on `gpt-5.6-luna`, reasoning effort `high`, supervised local authentication, one repetition per case; no paired baseline comparison.
- **Evidence:** `.devquitect-reports/slice-dn-003-definition-root-resume.json`, `.devquitect-reports/slice-dn-003-definition-root-ambiguity-final.json`, `.devquitect-reports/slice-dn-003-definition-root-invalid.json`, `.devquitect-reports/slice-dn-003-workflow-depth-legacy.json`, and [SLICE-DN-003 evidence](software-design/devquitect-next/slices/SLICE-DN-003.md).
- **Verdict:** inconclusive
- **Rationale:** All final candidate cases and credential-free repository checks passed. The ambiguity case now asserts the required user-selection state rather than a particular action label; results remain diagnostic-only without a paired baseline comparison.

## PC-DN-003-ART — Artifact directory follows the durable root

- **Baseline:** `git:b217d69797c9ce276ac0377ebafd00ead8a14248` — `skills/software-idea-to-project/references/artifacts.md`.
- **Candidate:** `worktree-sha256:020d0d76be5171c8e7a86075cb7bea9950cbc416c5493ae162d009cf4a40e377` — `skills/software-idea-to-project/references/artifacts.md`.
- **Scope:** Replace fixed-root artifact creation and discovery with the existing session-state root contract; preserve legacy locations and ambiguous-session selection.
- **Disposition:** move
- **Deterministic cases:** `test_artifact_creation_uses_configured_root` and `test_artifact_discovery_does_not_force_default_root` passed; existing root/depth evaluation cases remain unchanged.
- **Behavioral configuration:** Not authorized for this task; no new model-backed evaluation or comparison.
- **Evidence:** Current focused tests and credential-free checks in [SLICE-DN-003 evidence](software-design/devquitect-next/slices/SLICE-DN-003.md).
- **Verdict:** inconclusive
- **Rationale:** Deterministic contract verification passed. Prior behavioral reports describe the baseline snapshot; they do not establish behavioral equivalence for this correction or release eligibility.

## PC-DN-004-DEL — Explicit-only delivery invocation

- **Baseline:** `git:dff146543c870a56b55d1ed339eeb95f6397653f` — `skills/project-plan-execution/agents/openai.yaml`.
- **Candidate:** `worktree-sha256:de5efdc5aca653cc8ec410bb267923b078680eef37b101a0714f5aa1b17888ff` — `skills/project-plan-execution/agents/openai.yaml`.
- **Scope:** Disable implicit host activation for approved-plan execution; retain its explicit default prompt and authorization requirements.
- **Disposition:** retain
- **Deterministic cases:** `test_host_invocation_metadata`, `test_explicit_invocation_preserves_scope_and_authority`; representative `plan-execution-positive` and `plan-execution-implicit-negative` remain fixed for any separately authorized comparison.
- **Behavioral configuration:** Not authorized; no model-backed run or host-routing result claimed.
- **Evidence:** [DN-004 evidence](software-design/devquitect-next/slices/SLICE-DN-004.md).
- **Verdict:** inconclusive
- **Rationale:** The host-native metadata owns activation. Deterministic checks verify the explicit-only flag without inventing a router or claiming behavioral equivalence.

## PC-DN-004-DEF — Declared definition invocation

- **Baseline:** `git:dff146543c870a56b55d1ed339eeb95f6397653f` — `skills/software-idea-to-project/agents/openai.yaml`.
- **Candidate:** `worktree-sha256:c58dfced9e9ec7b35f6731f6e494e4fefd0d61413cba21c8eac68eb87f7665dc` — `skills/software-idea-to-project/agents/openai.yaml`.
- **Scope:** Declare eligible implicit definition activation; QUICK and targeted-refactoring already declare true and retain their existing scope boundaries.
- **Disposition:** retain
- **Deterministic cases:** `test_host_invocation_metadata`, `test_explicit_invocation_preserves_scope_and_authority`; unchanged representative `software-idea-positive`, `software-idea-negative`, `quick-change-positive`, `quick-change-negative`, `quick-change-explicit-positive`, `quick-change-explicit-negative`, `refactoring-positive`, and `refactoring-negative`.
- **Behavioral configuration:** Not authorized; no model-backed run.
- **Evidence:** [DN-004 evidence](software-design/devquitect-next/slices/SLICE-DN-004.md).
- **Verdict:** inconclusive
- **Rationale:** All four policies are explicit in metadata; explicit user invocation retains precedence and never expands authority.

## PC-DN-004-MATRIX — Independent cross-generation evidence

- **Baseline:** `git:dff146543c870a56b55d1ed339eeb95f6397653f` — `skills/software-idea-to-project/references/implementation-planning.md`.
- **Candidate:** `worktree-sha256:a3bd5ff2062cd9d549ea839079e9a3fe928d2cfc2b6e2c787891356c2ac7502a` — `skills/software-idea-to-project/references/implementation-planning.md`.
- **Scope:** One independently identified model/host/runtime row per authorized behavioral comparison, preserving the same source pair, rule group, representative cases, and suite revision.
- **Disposition:** retain
- **Deterministic cases:** `test_initial_matrix_rows_are_independent_and_unexecuted`, `test_matrix_rejects_pooled_or_invented_evidence`; representative `evaluation-matrix-positive` and `evaluation-matrix-negative` plus the fixed routing cases below.
- **Behavioral configuration:** Not authorized. The five rows below are an unexecuted inventory, not behavioral evidence. Null fields mean unobserved configuration; repetitions is the intended per-case count until a run records the actual count.
- **Evidence:** [DN-004 evidence](software-design/devquitect-next/slices/SLICE-DN-004.md); no comparison reports exist for this group.
- **Verdict:** inconclusive
- **Rationale:** Configuration mismatches, adapter failures, pending rows, and deterministic failures cannot support a pooled or model-only verdict. Future runs append a new observed matrix rather than rewrite this inventory.

The suite revision hashes the sorted UTF-8 lines `<case-id>:<case-file-sha256>\n`.
All five rows refer to this same change group, baseline/candidate pair, and representative cases.
Authorized runs record observed host/runtime versions, effort (`high` where supported), actual
repetitions, report references, and an independent verdict in each new row. Changes in any of those
configurations must be retained and prevent a model-only comparison. Historical results in this
ledger belong to their original groups and are not reused as results for these rows.

```devquitect-evaluation-matrix
schema_version: 1
prompt_change_group: PC-DN-004-MATRIX
representative_cases:
  - software-idea-positive
  - software-idea-negative
  - quick-change-positive
  - quick-change-negative
  - quick-change-explicit-positive
  - quick-change-explicit-negative
  - plan-execution-positive
  - plan-execution-implicit-negative
  - refactoring-positive
  - refactoring-negative
  - evaluation-matrix-positive
  - evaluation-matrix-negative
rows:
  - model_id: gpt-5.6-sol
    host: null
    runtime: null
    reasoning_effort: null
    suite_revision: sha256:e6f14a59da173317677421a4d43456d58541e4fdbf8d79e148be7b7d044804d0
    repetitions: 1
    report_references: []
    authorization: not-authorized
    verdict: not-run
  - model_id: gpt-5.6-terra
    host: null
    runtime: null
    reasoning_effort: null
    suite_revision: sha256:e6f14a59da173317677421a4d43456d58541e4fdbf8d79e148be7b7d044804d0
    repetitions: 1
    report_references: []
    authorization: not-authorized
    verdict: not-run
  - model_id: gpt-5.6-luna
    host: null
    runtime: null
    reasoning_effort: null
    suite_revision: sha256:e6f14a59da173317677421a4d43456d58541e4fdbf8d79e148be7b7d044804d0
    repetitions: 1
    report_references: []
    authorization: not-authorized
    verdict: not-run
  - model_id: gpt-6-sol
    host: null
    runtime: null
    reasoning_effort: null
    suite_revision: sha256:e6f14a59da173317677421a4d43456d58541e4fdbf8d79e148be7b7d044804d0
    repetitions: 1
    report_references: []
    authorization: not-authorized
    verdict: not-run
  - model_id: gpt-6-luna
    host: null
    runtime: null
    reasoning_effort: null
    suite_revision: sha256:e6f14a59da173317677421a4d43456d58541e4fdbf8d79e148be7b7d044804d0
    repetitions: 1
    report_references: []
    authorization: not-authorized
    verdict: not-run
```
