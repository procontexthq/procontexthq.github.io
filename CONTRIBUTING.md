# Contributing to the ProContext Registry

Thanks for helping improve the registry! Before contributing, please read the [README.md](README.md) for an overview of the project.

## Ways to Contribute

- **Add a new library** — a library you use that has a public `llms.txt` file
- **Fix an existing entry** — correct a URL, name, alias, or package name
- **Remove a stale entry** — a library whose `llms_txt_url` is no longer reachable

---

## Before You Add a New Entry

**Check whether the library already exists.** Search `docs/known-libraries.json` for the library name, package name, or a known alias. If an entry already exists, update it instead of creating a new one.

Also check whether another library in the registry **shares the same `llms_txt_url`**. If it does, add your library's packages and aliases to that existing entry rather than creating a separate one (see [Grouping rules](#grouping-libraries-under-one-entry) below).

---

## Adding a Library

### 1. Check eligibility

The library must have a publicly accessible `llms.txt` file. Verify it is reachable before submitting:

```bash
curl -I https://docs.example.com/llms.txt
```

Expect a `200 OK` response. Do not add entries whose `llms_txt_url` returns an error or redirects to a generic page.

### 2. Add an entry to `docs/known-libraries.json`

Append your entry to the JSON array:

```json
{
  "id": "my-library",
  "name": "My Library",
  "docs_url": "https://docs.example.com",
  "repo_url": "https://github.com/org/my-library",
  "languages": ["python"],
  "packages": {
    "pypi": ["my-library"],
    "npm": []
  },
  "aliases": ["mylib"],
  "llms_txt_url": "https://docs.example.com/llms.txt"
}
```

**Required fields:** `id`, `name`, `llms_txt_url`

**`id` rules:** lowercase, alphanumeric, hyphens and underscores only, must start with a letter or digit — e.g. `langchain`, `openai`, `react`

### 3. Validate and update the checksum

```bash
uv run scripts/validate.py all
```

This validates the file structure and updates `registry_metadata.json` with a fresh checksum. Run `--urls` to also verify the URL is reachable:

```bash
uv run scripts/validate.py all --urls
```

---

## Field Reference

### `docs_url`
The standard documentation URL for the library — the human-readable docs site provided by the maintainers. This is **not** the `llms.txt` URL.

```json
"docs_url": "https://docs.pydantic.dev"
```

### `repo_url`
The URL of the library's **source code repository** (e.g. GitHub, GitLab).

```json
"repo_url": "https://github.com/pydantic/pydantic"
```

### `languages`
List only the languages relevant to the **content of the `llms_txt_url`** — not every language the library might support in theory.

- If the `llms.txt` covers Python usage → `["python"]`
- If the `llms.txt` covers both JavaScript and TypeScript → `["javascript", "typescript"]`
- Do not add a language just because a binding or wrapper exists elsewhere

```json
// Python library
"languages": ["python"]

// JS/TS library
"languages": ["javascript", "typescript"]
```

### `packages`
List the installable package names users would use to install the library. Only include packages that are genuinely part of this entry's `llms.txt` coverage.

**Package names must exactly match the name on the package host** — use the name as it appears on [pypi.org](https://pypi.org) for `pypi` entries and on [npmjs.com](https://npmjs.com) for `npm` entries. Do not use import names, aliases, or shorthand.

```json
// PyPI only — names must match pypi.org exactly
"packages": { "pypi": ["langchain", "langchain-core", "langchain-community"], "npm": [] }

// npm only — names must match npmjs.com exactly (including scope)
"packages": { "pypi": [], "npm": ["react", "react-dom"] }

// scoped npm package
"packages": { "pypi": [], "npm": ["@anthropic-ai/sdk"] }

// both registries
"packages": { "pypi": ["grpcio"], "npm": ["@grpc/grpc-js"] }
```

---

## Grouping Libraries Under One Entry

**Libraries that share the same `llms.txt` should be grouped into a single entry.**

A single `llms.txt` often covers an entire ecosystem of related packages (e.g. a core library and its official plugins). Creating separate entries for each package would point ProContext to the same documentation file, which is redundant.

**Group them when:**
- Multiple packages share the exact same `llms_txt_url`
- The packages are maintained together under the same docs site

**Keep them separate when:**
- Each library has its own distinct `llms.txt`
- The libraries are from different maintainers and have genuinely different documentation

### Examples

**Correct — grouped (same `llms.txt`):**
```json
{
  "id": "langchain",
  "name": "LangChain",
  "llms_txt_url": "https://docs.langchain.com/llms.txt",
  "packages": {
    "pypi": ["langchain", "langchain-core", "langchain-community", "langchain-openai"],
    "npm": []
  },
  "languages": ["python"]
}
```

`langchain-core` and `langchain-openai` are not separate entries — they share the same `llms.txt` as `langchain`.

---

**Correct — separate (different `llms.txt`):**
```json
{
  "id": "react",
  "name": "React",
  "llms_txt_url": "https://react.dev/llms.txt",
  "languages": ["javascript", "typescript"]
}
```
```json
{
  "id": "nextjs",
  "name": "Next.js",
  "llms_txt_url": "https://nextjs.org/docs/llms.txt",
  "languages": ["javascript", "typescript"]
}
```

React and Next.js each have their own `llms.txt`, so they get their own entries.

---

**Incorrect — do not do this:**
```json
{ "id": "langchain-core", "llms_txt_url": "https://docs.langchain.com/llms.txt" }
{ "id": "langchain-openai", "llms_txt_url": "https://docs.langchain.com/llms.txt" }
```

These duplicate the same `llms.txt` and should instead be listed as packages under the `langchain` entry.

---

### Same library, separate per-language documentation

Some libraries publish independent `llms.txt` files for each language (e.g. a Python SDK and a JavaScript SDK with separate docs sites). In that case, create one entry per language and append a language shorthand to the `id`:

| Language | Shorthand |
|----------|-----------|
| Python | `-python` |
| JavaScript | `-js` |
| TypeScript | `-ts` |
| Go | `-go` |
| Rust | `-rust` |
| Java | `-java` |
| Ruby | `-rb` |
| Kotlin | `-kt` |
| Swift | `-swift` |
| .NET / C# | `-dotnet` |
| PHP | `-php` |

**Example — a library with distinct Python and JS docs:**
```json
{
  "id": "langchain-python",
  "name": "LangChain (Python)",
  "llms_txt_url": "https://docs.langchain.com/llms.txt",
  "languages": ["python"],
  "packages": { "pypi": ["langchain", "langchain-core"], "npm": [] },
  "aliases": ["langchain"]
}
```
```json
{
  "id": "langchain-js",
  "name": "LangChain (JS)",
  "llms_txt_url": "https://js.langchain.com/llms.txt",
  "languages": ["javascript", "typescript"],
  "packages": { "pypi": [], "npm": ["langchain"] },
  "aliases": []
}
```

Do **not** use this pattern when both languages are covered by the same `llms.txt` — use a single entry with both languages listed instead.

---

## Making Changes to Existing Entries

1. Edit the relevant entry in `docs/known-libraries.json`.
2. If you are fixing a broken `llms_txt_url`, verify the new URL is reachable before submitting.
3. Run validation and update the checksum:

```bash
uv run scripts/validate.py all
```

---

## Submitting Your Changes

1. Fork this repository and create a branch with a descriptive name (e.g. `add-langchain`, `fix-openai-url`).
2. Make your changes following the steps above.
3. Run `uv run scripts/validate.py all` and confirm it exits cleanly.
4. Open a pull request with a short description of what you added or changed and why.

