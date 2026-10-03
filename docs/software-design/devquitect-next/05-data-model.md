# Devquitect Next data model

Status: Approved
Last updated: 2026-09-22

## Confirmed

The approved delivery plan remains the source of truth for slice criteria, dependencies, declared inputs, and plan revision. The delivery checkpoint remains the source of truth for slice lifecycle and evidence. The existing fenced YAML `devquitect-verification` inventory represents the accepted concepts:

- stable `SLICE-*` identifier;
- atomic acceptance criteria;
- exact validation checks and relative working directories;
- dependencies;
- declared input paths.

The verifier retains these transitions:

```text
planned → snapshot (read-only) → check (read-only) → close (atomic) → verified
```

`close` must still reject missing approval, dependencies, criteria, current check evidence, matching fingerprints, or expected tracker revision. It re-reads its inputs before replacing the tracker atomically.

### Prompt-change ledger entry

The ledger is an append-only Markdown table or subsection with one record per evaluated change group. Each record includes:

- stable change identifier and date;
- baseline and candidate source snapshot IDs or Git references;
- affected paths and named rule group;
- disposition for each rule group: retain, move, or remove;
- deterministic case IDs and their result;
- canonical behavioral model ID, host, runtime, reasoning effort when supported, case-suite revision, repetitions, and report reference when authorized;
- verdict: retained, reverted, or inconclusive; and a short rationale.

The record contains no copied prompt body. Snapshot IDs and Git references reconstruct the original and candidate sources; authority-map entries identify the owner when the rule is critical. The initial model IDs are `gpt-5.6-sol`, `gpt-5.6-terra`, `gpt-5.6-luna`, `gpt-6-sol`, and `gpt-6-luna`; each model/host/runtime/effort combination is a separate evidence row.

### Workflow and root state

The workflow-depth record applies to all initiative contexts and records selected depth, evidence, and elevation reasons. A persistent session records its resolved root and session-relative path so discovery can find existing work after a root configuration change.

## Assumptions

The existing YAML inventory and verifier schema remain unchanged.

## Open decisions

None. The existing ledger fields represent the approved model rows without introducing another evaluator schema or changing the slice-verifier inventory.
