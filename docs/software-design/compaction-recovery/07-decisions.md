# Compaction Recovery decisions

Status: Approved
Last updated: 2026-09-19

## Confirmed

- Current official Codex documentation establishes `SessionStart(source="compact")` as a pre-model continuation boundary after root-session compactation.
- Current official Codex documentation establishes that `PreToolUse` is not a complete tool-control boundary.
- Current Devquitect packaging does not include plugin hooks.

## Assumptions

None.

## Open decisions

None. Gate 2 approved the technical decisions below on 2026-09-19.

## Proposed decisions for Gate 1

### DEC-CR-001 — Recover at the native compactation continuation boundary

Status: Approved at Gate 1

Use a synchronous plugin-packaged `SessionStart` hook matched to `source: "compact"` to inject the recovery directive before the next model request.

Evidence:

- The official runtime guarantee directly covers automatic compactation during a turn and delivers context before the model can choose another action: [OpenAI Codex hooks documentation](https://developers.openai.com/codex/hooks/).
- `PostCompact` is later in the same lifecycle but does not improve the point at which the model receives recovery context.
- `PreToolUse` excludes hosted tools and may be bypassed by specialized paths, so using it as the primary recovery boundary would provide weaker coverage.

Rejected alternatives:

- **`PostCompact` marker plus `PreToolUse` block:** rejected for the first release because it adds transient state, delays recovery until a supported tool path, duplicates the runtime event, and is not an independent fallback when hooks are disabled.
- **Prompt-only recovery:** rejected because it does not create a runtime compactation boundary.
- **Checkpoint-only recovery:** rejected because a compacted model must first be told to re-enter the recovery contract.

Revisit when:

- official Codex lifecycle guarantees change;
- evidence shows `SessionStart(source="compact")` can be skipped while supported tool calls still run;
- a materially independent non-hook runtime signal becomes available.

### DEC-CR-003 — Keep hook state transient

Status: Approved at Gate 1

The hook emits a bounded directive and candidate checkpoint paths but writes no task-state marker. `09-delivery-status.md` remains the only durable execution state, and repository evidence remains the source of implementation reality.

### DEC-CR-004 — Fail safe on ambiguity, not on ordinary absence

Status: Approved at Gate 1

No active delivery means silent no-op. One active candidate means explicit recovery. Multiple plausible candidates or checkpoint/repository disagreement means normal implementation does not continue until the ambiguity is resolved. This avoids both global noise and silent guessing.

## Proposed decisions for Gate 2

### DEC-CR-002 — Adopt delivery checkpoint schema version 3

Status: Approved at Gate 2

Add one `execution_frontier` mapping to schema v3. Keep v1/v2 readable; leave completed legacy
checkpoints untouched; migrate an active legacy checkpoint only during resume/update and only
after repository reconciliation. Preserve every existing field and represent unestablished
facts as empty/null, never as conversationally inferred history.

Evidence:

- schema versions 1 and 2 already coexist, and version 2 carries deployed ownership semantics;
- the verifier preserves unknown top-level fields but currently does not validate versions;
- an unversioned optional block would not distinguish legacy unknown data from a completed
  migration.

Rejected alternative: adding an optional frontier to v1/v2, because it makes enforcement and
migration state ambiguous.

### DEC-CR-005 — Use one standard-library discovery hook

Status: Approved at Gate 2

Package one synchronous `SessionStart` handler and one Python standard-library script. Scan only
the known immediate session checkpoint location, emit at most 4096 bytes, and write nothing.
Python 3.12+ is an explicit feature prerequisite; absence is an observable unsupported state.

Rejected alternatives: PyYAML in the runtime hook, transcript parsing, recursive repository
search, a daemon, and a marker file. Each adds dependency or state without strengthening the
required boundary.

### DEC-CR-006 — Exercise real compactations through a dedicated App Server adapter

Status: Approved at Gate 2

Preserve the current `codex exec` adapter for ordinary cases. Route only explicit lifecycle
scenarios through App Server, calling `thread/compact/start` and waiting for the corresponding
`contextCompaction` completion. This is the smallest interface that can prove the required one,
two, and four compactations actually occurred.

Rejected alternative: emulate compactation with concatenated prompts or a synthetic summary;
that tests prompting, not the runtime recovery boundary.

### DEC-CR-007 — Extend packaging with an exact hook allowlist

Status: Approved at Gate 2

Admit only `hooks/hooks.json` and `hooks/compaction_recovery.py` as new package inputs. Validate
their manifest linkage and handler contract, reject other hook-root inputs, and preserve current
reproducibility rules.

Rejected alternative: package the entire `hooks/` tree, because it silently broadens executable
package input.

### DEC-CR-008 — Use Codex's native per-hook enablement control

Status: Approved at Gate 2

Operators enable, disable, inspect, and re-enable the recovery handler through Codex `/hooks`.
Disabled and untrusted are explicit states in which automatic compactation recovery is
unavailable; manual skill-level recovery remains.

Evidence:

- official Codex hook documentation says `/hooks` can inspect sources, trust changed hooks, and
  disable individual non-managed hooks;
- the current Graphify Codex hook is a normal `.codex/hooks.json` handler subject to that same
  runtime control, while its separate `graphify hook install/uninstall/status` commands manage
  Git hooks rather than Codex lifecycle hooks.

Rejected alternatives: a Devquitect marker file, environment flag, mutable installed plugin
configuration, or custom enable/disable CLI. Each creates another source of state and can drift
from the runtime that actually decides whether the hook executes.
