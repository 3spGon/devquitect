# Devquitect

Devquitect packages three focused Codex skills for defining software, executing approved persistent
plans, and performing targeted behavior-preserving refactors. The repository also owns a local,
provider-neutral quality toolchain for structural validation, isolated behavioral evaluation,
stable/candidate comparison, deterministic plugin packaging, and release-eligibility review.

## Local definition of done

Install the locked development environment and run the credential-free check:

```text
uv sync --all-groups
uv run devquitect check --source working-tree --report .devquitect-reports/check.json
```

Trusted maintainers may add real Codex behavior against an exact commit:

```text
uv run devquitect check \
  --source HEAD \
  --behavioral \
  --report .devquitect-reports/full-check.json
```

Exit codes are `0` for pass, `1` for a quality or policy failure, `2` for invalid configuration,
and `3` for inconclusive infrastructure. Ordinary checks use fake runtime evidence and need no API
key or ChatGPT subscription. Real behavioral checks require explicitly trusted local authentication.

Behavioral commands default to `gpt-5.4-mini` with reasoning effort `low` to limit subscription
usage during repeated tests. A deliberate calibration run can override both with `--model` and
`--reasoning-effort`; the selected values are retained in reports. The credential-free check never
invokes a model.

See [the contributor workflow](docs/contributing-skills.md) for authoring, negative activation
boundaries, evidence review, packaging, promotion proposals, and recovery. Local commands never
install, tag, push, publish, or deploy the plugin.
