# Validation Rules

This page lists the validation rule numbers used by the validator scripts and the `--skip-rule` flag.

Example:

```bash
uv run scripts/validate.py checksum --skip-rule 6 --skip-rule 22
```

## Library entry rules

| Rule | Meaning |
|------|---------|
| 1 | `id` is present and a non-empty string |
| 2 | `id` matches `^[a-z0-9][a-z0-9_-]*$` |
| 3 | `name` is present and a non-empty string |
| 4 | `llms_txt_url` is present and a non-empty string |
| 5 | `llms_txt_url` starts with `https://` |
| 6 | `description`, if present, is a non-empty string |
| 7 | `aliases` is a list of strings |
| 8 | `packages` is an array |
| 9 | No unknown library-level fields are present |

## Package entry rules

| Rule | Meaning |
|------|---------|
| 10 | `ecosystem` is one of `pypi`, `npm`, `conda`, or `jsr` |
| 11 | `package_names` is a list of strings |
| 12 | `languages`, if present, is a list of strings |
| 13 | `readme_url`, if present, is a valid URL |
| 14 | `repo_url`, if present, is a valid URL |
| 15 | No unknown package-level fields are present |

## Cross-entry rules

| Rule | Meaning |
|------|---------|
| 16 | No duplicate `id` values |
| 17 | No duplicate package names within the same ecosystem |

## File-level rules

| Rule | Meaning |
|------|---------|
| 19 | `known-libraries.json` is valid JSON |
| 20 | `known-libraries.json` top-level value is an array |
| 21 | `known-libraries.json` is not empty |
| 24 | `registry-additional-info.json` is valid JSON |
| 25 | `registry-additional-info.json` top-level value is an object |
| 26 | `useful_md_probe_base_urls` is a non-empty array |
| 27 | Every `useful_md_probe_base_urls` entry is a valid URL |

## Optional slow checks

| Rule | Meaning |
|------|---------|
| 22 | `llms_txt_url` is reachable over HTTP |
| 23 | PyPI packages listed in `package_names` exist on PyPI |

## Notes

- Repeat `--skip-rule` to skip multiple rules.
- Skipping a rule suppresses reporting for that rule only.
- `scripts/validate.py checksum` still updates metadata if the remaining non-skipped rules pass.
