# Devquitect Next architecture

Status: Approved
Last updated: 2026-09-22

## Confirmed

### Current architecture

Devquitect currently distributes three skills with distinct entrypoints and a Python quality package. `project-plan-execution` delegates accepted-slice state transitions to the distributed `verify_slice.py` guard, which reads a YAML inventory and requires Python 3.12+ plus PyYAML.

### Proposed architecture

| Component | Responsibility | Preserved boundary |
| --- | --- | --- |
| Lean skill entrypoints | State each entrypoint's outcome, authorization, escalation, and completion policy once. | References retain detailed mechanics and canonical state rules. |
| `quick-change` skill | Execute an authorized, localized change after focused discovery and relevant verification. | It escalates rather than deciding product, architecture, migration, or durable-work questions. |
| Existing definition, refactoring, and delivery skills | Own their current domains. | No skill silently assumes another skill's authority. |
| Existing `verify_slice.py` | Preserve the current Python/PyYAML, YAML-inventory, snapshot/check/close verification boundary. | This initiative neither changes nor migrates it. |

The host may choose `quick-change` implicitly from its description. There is no universal router skill in 0.7.0. A consumer may add a short `AGENTS.md` routing convention if it needs local enforcement beyond normal skill selection.

### Expanded v2 components

| Component | Responsibility | Boundary |
| --- | --- | --- |
| Workflow-depth selector | Select lightweight, standard, or rigorous depth for every initiative from observable impact and risk. | It replaces no approval boundary and does not authorize implementation. |
| Durable-root resolver | Resolve an explicitly configured definition root; otherwise use the detected repository default while discovering existing sessions in both locations. | It preserves existing session paths and never silently migrates them. |
| Invocation policy | Declare implicit activation per skill: definition, QUICK, and refactoring may be eligible; approved-plan execution requires explicit invocation. | Host matching remains advisory; explicit user invocation takes precedence. |
| Prompt-change ledger | Record the disposition and evidence for every staged change group. | Snapshot and Git identities own exact source text; comparison and calibration reports own observed evidence. |
| Evaluation matrix | Run each authorized behavioral comparison with one declared model/host configuration at a time. | Results from differing models, hosts, suite versions, or repetitions are not merged into one verdict. |

### Resolved operating design

- **Workflow depth:** retain `change_profile` for compatibility and add one optional `workflow_depth` field to every persistent session. Its values are `lightweight`, `standard`, and `rigorous`; omitted legacy values mean `standard`. A system-change profile records the same selected depth rather than replacing its existing classification fields.
- **Durable root:** the current `docs/software-design` remains the default. A caller may explicitly provide one repository-relative definition root; the resolver stores that root in the session, checks the recorded root first on resume, and searches the default only for legacy discovery. A collision between viable sessions is surfaced for user selection. No session is moved automatically.
- **Invocation:** definition, QUICK, and targeted-refactoring may opt into host implicit matching through their metadata; `project-plan-execution` is explicit-only. An explicit skill mention wins over matching.
- **Prompt changes:** a change group has an immutable baseline snapshot, one named rule group, the unchanged representative deterministic cases, and—only when separately authorized—a comparison on one declared model/host configuration. A regression or inconclusive result retains the prior wording.
- **Evidence matrix:** initial rows use canonical model IDs `gpt-5.6-sol`, `gpt-5.6-terra`, `gpt-5.6-luna`, `gpt-6-sol`, and `gpt-6-luna`. GPT-5.6 rows are the prior-generation baseline; GPT-6 Sol/Luna are additive rows. Every row fixes and records model ID, host, runtime, reasoning effort (`high` where supported), case-suite revision, repetitions, and report references. Comparisons reuse the same prompt-change group and representative cases. Each row has its own verdict; results are never pooled. If host/runtime/effort differ or cannot be matched, record the difference and do not claim a direct model-only comparison. Behavioral runs remain separately authorized.

### Delivery flow

```text
authorized local change → quick-change → focused inspection → edit → relevant validation → result
                                      │
                                      └─ material complexity → appropriate existing skill

approved plan → existing verify_slice.py → snapshot / check / atomic close → verified tracker state
```

## Assumptions

The existing skill packaging can distribute an additional skill and compatibility helper without adding a new host integration.

The repository can store the ledger as a versioned Markdown document without adding a new runtime parser; immutable snapshots and existing reports provide reproducibility.

## Open decisions

None. The initial matrix and ledger schema are deliberately minimal and can be extended only after evidence demonstrates a need.

## Requirement traceability

| Requirement | Technical treatment |
| --- | --- |
| R-01 | Component ownership table and preserved boundaries. |
| R-02 | Lean skill-entrypoint component. |
| R-03, R-04 | `quick-change` component and escalation flow. |
| R-05, R-06 | Preserved verify_slice contract and staged delivery flow. |
| R-07, R-08 | Staged prompt-change protocol and append-only, snapshot-referencing ledger. |
| R-09 | Shared workflow-depth state and durable-root resolver with legacy discovery. |
| R-10 | Per-skill invocation metadata and non-pooled model/host evaluation matrix. |
