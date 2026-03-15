# Registry Schema Reference

This document describes the JSON structure of registry entries (`known-libraries.json`) and the `resolve_library` tool response.

## Registry Entry (known-libraries.json)

Each entry in the registry represents a single library, potentially spanning multiple languages and ecosystems.

```json
{
  "id": "openai",
  "name": "OpenAI",
  "description": "Official OpenAI API client libraries.",
  "llms_txt_url": "https://platform.openai.com/llms.txt",
  "aliases": ["open-ai"],
  "packages": [
    {
      "ecosystem": "pypi",
      "languages": ["python"],
      "package_names": ["openai"],
      "readme_url": "https://raw.githubusercontent.com/openai/openai-python/main/README.md",
      "repo_url": "https://github.com/openai/openai-python"
    },
    {
      "ecosystem": "npm",
      "languages": ["javascript", "typescript"],
      "package_names": ["openai"],
      "readme_url": "https://raw.githubusercontent.com/openai/openai-node/main/README.md",
      "repo_url": "https://github.com/openai/openai-node"
    }
  ]
}
```

### Library-level fields

These describe the library as a whole — identity and documentation entry point.

| Field | Type | Required | Description |
|---|---|---|---|
| `id` | string | yes | Unique lowercase identifier (`^[a-z0-9][a-z0-9_-]*$`). Used for exact ID matching in step 2 of resolution. |
| `name` | string | yes | Human-readable display name. Passed through to the agent as-is. |
| `description` | string | no | Short description of what the library does. Defaults to `""`. |
| `llms_txt_url` | string | yes | The canonical entry point — the library's documentation index. This becomes `index_url` in the response. Also used to build the SSRF domain allowlist. |
| `aliases` | list[string] | no | Alternative names for the library (e.g., `"lang-chain"` for langchain). Matched in step 3 of resolution. Defaults to `[]`. |
| `packages` | list[PackageEntry] | no | Package groups by ecosystem. This is where language-specific metadata lives. Defaults to `[]`. |

### PackageEntry fields

Each `PackageEntry` represents a group of packages within a single ecosystem, scoped to one or more languages. This is what allows a single library (e.g., OpenAI) to have separate Python and JavaScript SDKs with their own READMEs and repos under the same `id`.

| Field | Type | Required | Description |
|---|---|---|---|
| `ecosystem` | enum | yes | Package registry: `"pypi"`, `"npm"`, `"conda"`, or `"jsr"`. |
| `languages` | list[string] | no | Programming languages this group covers. Array because some ecosystems span languages (e.g., JS and TS share npm packages). Used by the `language` sort parameter. Defaults to `[]`. |
| `package_names` | list[string] | yes | Package names in this ecosystem that belong to this library. E.g., `["langchain", "langchain-core", "langchain-openai"]`. Every name here is indexed for step 1 (exact package match) and step 4 (fuzzy match) of the resolution algorithm. |
| `readme_url` | string \| null | no | README URL for this package group. Python and JS SDKs typically have separate READMEs — this field lives per-package-group to support that. |
| `repo_url` | string \| null | no | Source repository URL for this package group. Same rationale — separate repos for separate language SDKs. |

---

## resolve_library Response

The `resolve_library` tool accepts a `query` string and an optional `language` hint, and returns matching libraries from the registry.

### Input

```json
{
  "name": "resolve_library",
  "arguments": {
    "query": "openai",
    "language": "python"
  }
}
```

| Parameter | Type | Required | Description |
|---|---|---|---|
| `query` | string | yes | Library name, package specifier (e.g., `"langchain-community"`), or alias. Max 500 characters. Pip extras and version specifiers are automatically stripped. |
| `language` | string \| null | no | Optional language hint (e.g., `"python"`, `"javascript"`). Sorts matching-language packages to the top of the response. Does **not** filter — all results are always returned. |

### Output

```json
{
  "matches": [
    {
      "library_id": "openai",
      "name": "OpenAI",
      "description": "Official OpenAI API client libraries.",
      "index_url": "https://platform.openai.com/llms.txt",
      "packages": [
        {
          "ecosystem": "pypi",
          "languages": ["python"],
          "package_names": ["openai"],
          "readme_url": "https://raw.githubusercontent.com/openai/openai-python/main/README.md",
          "repo_url": "https://github.com/openai/openai-python"
        },
        {
          "ecosystem": "npm",
          "languages": ["javascript", "typescript"],
          "package_names": ["openai"],
          "readme_url": "https://raw.githubusercontent.com/openai/openai-node/main/README.md",
          "repo_url": "https://github.com/openai/openai-node"
        }
      ],
      "matched_via": "package_name",
      "relevance": 1.0
    }
  ]
}
```

### Response fields

| Field | Type | Description |
|---|---|---|
| `library_id` | string | Canonical library identifier from the registry. |
| `name` | string | Human-readable name. |
| `description` | string | Short description. |
| `index_url` | string | Documentation index URL (from `llms_txt_url`). **This is the primary output** — the agent passes it to `read_page` next. |
| `packages` | list[PackageEntry] | All package groups for this library. The agent sees the full picture — all ecosystems, all languages, all READMEs. Passed through from the registry entry. |
| `matched_via` | enum | How the match was found: `"package_name"` (step 1), `"library_id"` (step 2), `"alias"` (step 3), or `"fuzzy"` (step 4). |
| `relevance` | float | Confidence score 0.0 to 1.0. Exact matches are 1.0. Fuzzy matches are proportional to Levenshtein similarity. |

### Language sorting behavior

When `language` is provided:

1. Within each match, `packages` entries whose `languages` contain the requested language sort to the front.
2. Matches that have at least one package with the requested language sort before those that don't.
3. **Nothing is omitted** — it is a sort hint, not a filter. The agent always sees everything.
4. Whitespace-only or empty string is treated as null (no sorting applied).

For example, with `language: "python"`, the response above would have the `pypi` entry first in the packages list instead of `npm`.
