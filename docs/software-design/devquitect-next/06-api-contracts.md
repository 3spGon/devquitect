# Devquitect Next interfaces and contracts

Status: Approved
Last updated: 2026-09-22

## Confirmed

### QUICK selection contract

`quick-change` is eligible only when the request is authorized, local, reversible, and directly verifiable. Its skill description states those triggers and exclusions. Explicit user invocation overrides ordinary implicit selection. Evidence of a material feature decision, public interface, persistence, security-sensitive behavior, migration, cross-module change, or durable-continuity need routes work away from QUICK.

### Existing verifier contract

The distributed verifier remains the current Python 3.12+ and PyYAML implementation over the fenced YAML inventory. This initiative preserves its commands, snapshot/check/atomic-close behavior, JSON stdout, and exit codes.

```text
python <skill-root>/scripts/verify_slice.py snapshot --session <directory> --slice <SLICE-ID>
python <skill-root>/scripts/verify_slice.py check --session <directory> --slice <SLICE-ID>
python <skill-root>/scripts/verify_slice.py close --session <directory> --slice <SLICE-ID> --expected-revision <N>
```

It emits JSON on stdout and preserves exit codes: `0` valid operation, `1` evidence prevents acceptance, and `2` unsupported runtime, format, path, or revision condition.

### Prompt-change protocol contract

Before changing a prompt group, the maintainer records a baseline source identity, names the rules in scope, and selects the existing representative cases. The candidate changes one group in one skill. It must pass the same deterministic cases; an authorized behavioral comparison records one model/host configuration and is comparable only to evidence with matching configuration. A regression or inconclusive result retains the prior source and receives a ledger entry.

### Invocation and durable-root contract

`project-plan-execution` is explicit-only. Other skill metadata states its permitted implicit activation policy. Persistent workflow callers accept a configured root when supplied; otherwise they discover the repository default and previously recorded session roots. Ambiguous session discovery requires user selection rather than a silent choice.

The configured root is a single repository-relative path supplied by the caller; it is persisted as `definition_root` in `00-status.md`. The default is `docs/software-design`. A resumed session uses its recorded root first. Existing sessions without `definition_root` stay at their current path and are not migrated. Every session also records `workflow_depth` as `lightweight`, `standard`, or `rigorous`; an absent legacy value means `standard`.

### Evaluation-matrix contract

Each behavioral comparison is opt-in and separately authorized. One evidence row records one canonical model ID, host, runtime, reasoning effort where supported, case-suite revision, repetitions, and report references. The initial model IDs are `gpt-5.6-sol`, `gpt-5.6-terra`, `gpt-5.6-luna`, `gpt-6-sol`, and `gpt-6-luna`; the GPT-5.6 rows form the baseline and the GPT-6 rows are additional. Use the same prompt-change group and representative cases across rows. Use `high` reasoning effort where supported; if effort, host, or runtime differs, retain the value as part of that row's identity and do not present it as a model-only comparison. Verdicts remain independent; any release decision cites the rows that support it without combining their scores.

## Assumptions

The existing verifier contract remains adequate for the present initiative because it is explicitly out of scope.

## Open decisions

None. The verifier is intentionally preserved.
