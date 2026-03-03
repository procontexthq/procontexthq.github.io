# ProContext Registry

This repository hosts the library registry for [ProContext](https://github.com/procontexthq/procontext) — an MCP server that gives AI coding agents accurate, up-to-date library documentation.

## What's in here

```
docs/
├── known-libraries.json     # The registry — one entry per supported library
└── registry_metadata.json   # Version pointer + checksum, fetched by ProContext on startup
```

ProContext polls `registry_metadata.json` every 24 hours. When the `version` changes, it downloads `known-libraries.json`, verifies the SHA-256 checksum, and updates its in-memory index.

## Registry metadata format

```json
{
  "version": "YYYY-MM-DD",
  "download_url": "https://<pages-url>/docs/known-libraries.json",
  "checksum": "sha256:<hex>"
}
```

## Validation & tooling

The `scripts/validate.py` script validates `docs/known-libraries.json` and keeps `registry_metadata.json` in sync. It requires Python ≥ 3.11 and [uv](https://docs.astral.sh/uv/).

### Setup

```bash
uv sync
```

### Commands

| Command | What it does |
|---------|--------------|
| `uv run scripts/validate.py validate` | Fast schema check (rules 1–19) |
| `uv run scripts/validate.py validate --urls` | Schema check + URL reachability (rule 20) |
| `uv run scripts/validate.py validate --pypi` | Schema check + PyPI existence (rule 21) |
| `uv run scripts/validate.py checksum` | Compute SHA-256 and update `registry_metadata.json` only |
| `uv run scripts/validate.py all` | Validate then update checksum (aborts on errors) |
| `uv run scripts/validate.py all --urls --pypi` | Run all checks |

### Validation rules

#### Per-entry rules

| # | Rule |
|---|------|
| 1 | `id` is present and a non-empty string |
| 2 | `id` matches `^[a-z0-9][a-z0-9_-]*$` |
| 3 | `name` is present and a non-empty string |
| 4 | `llms_txt_url` is present and a non-empty string |
| 5 | `llms_txt_url` is a valid URL starting with `https://` |
| 6 | `docs_url`, if present, is a valid URL |
| 7 | `repo_url`, if present, is a valid URL |
| 8 | `languages` is a list of strings (not `null`, not a bare string) |
| 9 | `packages.pypi` is a list of strings |
| 10 | `packages.npm` is a list of strings |
| 11 | `aliases` is a list of strings |
| 12 | No fields outside the known set (`id`, `name`, `llms_txt_url`, `docs_url`, `repo_url`, `languages`, `packages`, `aliases`) — catches typos like `alias` instead of `aliases` |

#### Cross-entry rules

| # | Rule |
|---|------|
| 13 | No two entries share the same `id` |
| 14 | No two entries share the same PyPI package name |
| 15 | No two entries share the same npm package name |
| 16 | No two entries share the same alias |

#### File-level rules

| # | Rule |
|---|------|
| 17 | File is valid JSON |
| 18 | Top-level structure is an array |
| 19 | Array is non-empty |

#### Optional network checks (slow)

| # | Flag | Rule |
|---|------|------|
| 20 | `--urls` | `llms_txt_url` is reachable (HTTP 200) |
| 21 | `--pypi` | PyPI package names in `packages.pypi` exist on pypi.org |

## Contributing

Contributions are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for how to add or update entries, field reference, and grouping rules.

## License

This project is licensed under the [GNU General Public License v3.0](LICENSE).
