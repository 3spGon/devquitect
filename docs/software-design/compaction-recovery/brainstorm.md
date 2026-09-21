# Compaction Recovery brainstorm

## 2026-09-19 — Seed

The initiative requests robust continuation of long `project-plan-execution` runs after one or more Codex context compactations. Its invariant is `conversation = disposable`, `checkpoint = durable`, and `repository = reality`. It explicitly excludes a second durable task-state file, general memory, Context Mode integration, multi-agent coordination, and reading the entire project after every compact.

## 2026-09-19 — Repository baseline

- `skills/project-plan-execution/references/delivery-state.md` already makes `09-delivery-status.md` the durable delivery checkpoint and defines conservative resume and repository reconciliation behavior.
- The checkpoint already owns `current_slice`, `next_action`, `required_context`, blockers, per-slice status, evidence, and a coherent-update revision protocol.
- The current contract does not explicitly model the finer execution frontier requested by the initiative and does not name compactation as a recovery event.
- `.codex/hooks.json` contains only Graphify's `PreToolUse` hook for Bash. No Devquitect compactation hook or packaged hook implementation exists.
- `.codex-plugin/plugin.json` declares only the skills root. `src/devquitect_quality/packaging.py` currently allows only that manifest and files under `skills/`, so a runtime hook cannot be shipped without an explicit package-contract change.
- Existing deterministic tests cover slice evidence and close behavior, not one, two, or four compactations.

## 2026-09-19 — External evidence

Current official OpenAI documentation confirms:

- Codex supports `PreCompact`, `PostCompact`, `SessionStart`, and `PreToolUse` lifecycle hooks.
- `SessionStart` can match `source: "compact"` and runs before the next model request after root-session compactation, including automatic compactation in the middle of a turn.
- `SessionStart` can add developer context to that immediate continuation.
- `PreToolUse` can block many local function-tool paths, but hosted tools are not covered and specialized paths may bypass the default hook route.
- Plugins can ship `hooks/hooks.json`; hook trust must be reviewed, and plugin hook commands receive `PLUGIN_ROOT`.

Source: [OpenAI Codex hooks documentation](https://developers.openai.com/codex/hooks/).

## 2026-09-19 — Direction refined

The native `SessionStart(source="compact")` boundary reaches the model before it can choose the next tool. It therefore provides the requested recovery interruption earlier and with broader coverage than a `PostCompact` marker followed by `PreToolUse` denial. The marker and tool-blocking layer were removed from the proposed first release because they duplicate runtime state and do not create an independent safety layer when hooks are disabled or untrusted.

The proposed first release instead combines:

1. a more precise execution frontier inside the existing delivery checkpoint;
2. milestone-based checkpoint freshness;
3. a compactation-as-resume skill contract;
4. a synchronous packaged `SessionStart(source="compact")` hook that injects a small recovery directive;
5. conservative checkpoint-versus-repository reconciliation before implementation resumes.

No implementation detail is assumed. Exact checkpoint schema evolution and hook/runtime packaging mechanics remain technical-design work after Gate 1.

## 2026-09-19 — Gate 1 prepared

The Change Profile is confirmed as cross-cutting/full because the change spans delivery behavior, checkpoint compatibility, plugin packaging, runtime hooks, and deterministic plus behavioral evaluation. The interaction surface is minimal: the operator must review and trust the hook, and unavailable or disabled hook states must be reported without pretending automatic recovery is active.

## 2026-09-19 — Gate 1 approved

The user explicitly approved Gate 1 in chat. The concept, requirements, `SessionStart(source="compact")` direction, full-depth Change Profile, and minimal operator interaction are now approved. Detailed architecture begins; Gate 2 and implementation remain unauthorized.

## 2026-09-19 — Gate 2 prepared

Repository evidence resolved the schema decision in favor of explicit version 3: version 2 is
already deployed for ownership, while the verifier preserves unknown fields but does not
validate schema versions. Completed legacy checkpoints stay untouched; active ones migrate
only on resume/update after repository reconciliation.

The minimal architecture is one packaged synchronous `SessionStart(source="compact")` hook,
one standard-library script, one new frontier block in the existing checkpoint, and a dedicated
App Server evaluation path for real compactation events. Packaging accepts exactly the hook
manifest and script. No marker, transcript parser, recursive scan, service, dependency, or
second execution state was added to the design. Gate 2 is awaiting explicit approval.

## 2026-09-19 — Native hook activation clarified

The user asked for activation/deactivation comparable to Graphify. Inspection showed that
Graphify's Codex `PreToolUse` handler is simply declared in `.codex/hooks.json`; its
`graphify hook install/uninstall/status` commands instead control Git hooks. Official Codex
behavior already provides the needed individual lifecycle-hook toggle through `/hooks`.

The design therefore uses native per-hook enable/disable and trust review. Disabled means
automatic compactation recovery is unavailable while manual skill recovery remains. No custom
flag, marker, environment variable, or mutable plugin configuration is introduced.

## 2026-09-19 — Gate 2 approved and plan revision 1 prepared

The user explicitly approved Gate 2 with native per-hook activation included. Technical
artifacts are approved. Planning traced the implementation through checkpoint schema, recovery
contract, hook packaging, source-correct App Server evaluation, and repository verification.

The resulting four slices preserve historical skill snapshot identities: lifecycle evaluation
freezes manifest/hook validation inputs from the same selected source and combines them only in
a disposable local marketplace with that source's frozen skills. Stable and candidate hooks
therefore cannot mix. Model-backed one/two/four compactation evidence remains separately gated.
Implementation plan revision 1 awaits explicit approval; no slice is authorized.

## 2026-09-19 — Implementation plan revision 1 approved

The user explicitly approved the implementation plan. Product behavior, technical design,
compatibility, four delivery slices, and verification inventory are now definition-complete.
No implementation slice or model-backed run was authorized. Future delivery must use
`project-plan-execution` with an explicit slice list and preserve the independent authorization
required for model-backed evaluation.
