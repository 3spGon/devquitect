# Contributing skills

Devquitect skills are packaged together but retain separate, focused responsibilities. Structural validation is offline and must pass before behavioral evaluation or packaging.

## Required structure

Create a skill at `skills/<skill-name>/` where `<skill-name>` is unique, kebab-case, and exactly matches the `name` in `SKILL.md` frontmatter. The frontmatter also requires a non-empty `description` that states both when to use the skill and when not to use it.

Every skill includes `agents/openai.yaml` with non-empty `interface.display_name`, `interface.short_description`, and `interface.default_prompt` values. Local resources must be linked from `SKILL.md` with relative Markdown links, must remain inside the skill directory, and must exist as regular files. Unreferenced files, escaping paths, and symlinks are not eligible plugin inputs.

The root `.codex-plugin/plugin.json` identifies the `devquitect` plugin and declares `"skills": "./skills/"`. Its name is stable kebab-case, its version follows semantic versioning, and its component paths are relative to the plugin root.

## Validate a contribution

From the repository root, run:

```text
uv run devquitect validate --source working-tree --format text
uv run devquitect validate --source working-tree --format json --report .devquitect-reports/validation.json
```

Exit `0` means every requested structural check passed. Exit `1` identifies repository quality failures such as malformed skill metadata, missing references, duplicate names, or unexpected package inputs. Exit `2` means the selected source, schema, or validator configuration is invalid or unsupported. Validation does not require credentials or network access.

JSON output and atomic report files use the versioned canonical envelope in `schemas/report.schema.json`. Paths in records are normalized and repository-relative. Text output represents the same verdict and issue records without changing exit semantics.

Behavioral evaluation, comparison, reproducible packaging, and release approval are delivered by later implementation slices. Structural success alone does not make a working-tree candidate release-eligible and does not publish or install the plugin.
