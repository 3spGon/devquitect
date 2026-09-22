# Slice verification

`verify_slice.py` is a distributed, read-only-by-default guard for evidence attached to an
approved delivery plan. It requires Python 3.12+ and PyYAML; it never installs dependencies,
uses the network, or executes commands from YAML or evidence.

```text
python <skill-root>/scripts/verify_slice.py snapshot --session <directory> --slice <SLICE-ID>
python <skill-root>/scripts/verify_slice.py check --session <directory> --slice <SLICE-ID>
python <skill-root>/scripts/verify_slice.py close --session <directory> --slice <SLICE-ID> --expected-revision <N>
```

The plan owns the `devquitect-verification` inventory. A detail file at
`slices/<SLICE-ID>.md` owns observed criteria and check evidence. `snapshot` reports the plan
and input fingerprint without accepting anything; `check` validates current evidence without
writing; `close` is the only supported transition to `verified`, after checking authorization,
approved definition gates, non-pending acceptance, dependencies, complete criterion fields,
check timestamps/statuses/exit codes, fingerprints, and the expected tracker revision. A close
re-reads the tracker, definition, plan, detail, and declared inputs before atomic replacement and rejects
observed concurrent changes. Plan revision is read from the approved plan rather than hardcoded.

The plan format is strict and machine-readable. The header must contain the plain-text lines
`Status: Approved` and `Plan revision: <positive integer>`, followed by one fenced block named
`devquitect-verification`. Its YAML must contain `schema_version: 1` and a `slices` mapping.
Each slice must contain `depends_on` (a list of slice IDs), `criteria` (a non-empty mapping
whose entries contain `text` and `requirement`), `checks` (a non-empty mapping whose entries
contain `command` and relative `cwd`), and `inputs` (a list of relative paths). Slice IDs in
the YAML must exactly match the `SLICE-*` headings in the plan.

These machine fields are case-sensitive and must not be translated, formatted with Markdown, or
renamed. `**Estado:** Approved`, `Estado: Approved`, and `input_paths` are unsupported legacy
variants; the verifier rejects them and does not silently migrate or rewrite the plan.
Planning guidance and the canonical draft-to-approval example live in
[`implementation-planning.md`](../../software-idea-to-project/references/implementation-planning.md).

Exit codes are `0` for a valid operation, `1` when evidence prevents acceptance, and `2` for
unsupported input, runtime, format, path, or revision conditions. Output is JSON on stdout.
The tracker write is atomic and preserves its body outside the delimited close summary.
