# Registry Contributions

Use this guide when you are adding, updating, or removing registry entries.

## Ways to contribute

- Add a new library with a public `llms.txt`
- Fix an existing entry
- Remove or repair a stale entry

## Before adding a new entry

Check whether the library already exists. Search [`docs/known-libraries.json`](../docs/known-libraries.json) for the library name, package name, or a known alias.

Also check whether another entry already uses the same `llms_txt_url`. If it does, add the new packages or aliases to that existing entry instead of creating a separate record.

## Adding a library

### 1. Check eligibility

The library must have a publicly accessible `llms.txt` file.

```bash
curl -I https://docs.example.com/llms.txt
```

Expect `200 OK`. Do not add entries whose `llms_txt_url` errors or redirects to a generic page.

### 2. Add an entry to `docs/known-libraries.json`

See [registry-schema.md](../registry-schema.md) for the full field reference.

```json
{
  "id": "my-library",
  "name": "My Library",
  "description": "A brief description of what the library does.",
  "llms_txt_url": "https://docs.example.com/llms.txt",
  "aliases": ["mylib"],
  "packages": [
    {
      "ecosystem": "pypi",
      "languages": ["python"],
      "package_names": ["my-library"],
      "readme_url": "https://raw.githubusercontent.com/org/my-library/main/README.md",
      "repo_url": "https://github.com/org/my-library"
    }
  ]
}
```

Required fields:
- `id`
- `name`
- `llms_txt_url`

`id` rules:
- lowercase
- alphanumeric, hyphens, and underscores only
- must start with a letter or digit

### 3. Validate and update checksums

```bash
uv run scripts/validate.py checksum
```

Run this when you want the standard repository workflow.

You can also enable slower checks:

```bash
uv run scripts/validate.py checksum --urls
uv run scripts/validate.py checksum --pypi
uv run scripts/validate.py checksum --urls --pypi
```

## Standalone validation tools

The validators are also usable independently:

```bash
uv run scripts/validate_libraries.py
uv run scripts/validate_libraries.py checksum
uv run scripts/validate_additional_info.py
uv run scripts/validate_additional_info.py checksum
```

Custom file paths are supported:

```bash
uv run scripts/validate_libraries.py --libraries-file /tmp/known-libraries.json
uv run scripts/validate_additional_info.py --additional-info-file /tmp/registry-additional-info.json
uv run scripts/validate.py checksum \
  --libraries-file /tmp/known-libraries.json \
  --additional-info-file /tmp/registry-additional-info.json \
  --metadata-file /tmp/registry_metadata.json
```

## Grouping rules

Libraries that share the same `llms.txt` should usually be grouped into one entry.

Group them when:
- multiple packages share the exact same `llms_txt_url`
- the packages are maintained together under the same docs site

Keep them separate when:
- each library has its own distinct `llms.txt`
- the libraries come from different maintainers with different documentation

### Correct: grouped

```json
{
  "id": "langchain-python",
  "name": "LangChain (Python)",
  "llms_txt_url": "https://docs.langchain.com/llms.txt",
  "packages": [
    {
      "ecosystem": "pypi",
      "languages": ["python"],
      "package_names": ["langchain", "langchain-core", "langchain-community", "langchain-openai"],
      "repo_url": "https://github.com/langchain-ai/langchain"
    }
  ]
}
```

### Correct: separate

```json
{
  "id": "react",
  "name": "React",
  "llms_txt_url": "https://react.dev/llms.txt",
  "packages": [
    {
      "ecosystem": "npm",
      "languages": ["javascript", "typescript"],
      "package_names": ["react", "react-dom"]
    }
  ]
}
```

```json
{
  "id": "next-js",
  "name": "Next.js",
  "llms_txt_url": "https://nextjs.org/docs/llms.txt",
  "packages": [
    {
      "ecosystem": "npm",
      "languages": ["javascript", "typescript"],
      "package_names": ["next"]
    }
  ]
}
```

### Incorrect

```json
{ "id": "langchain-core", "llms_txt_url": "https://docs.langchain.com/llms.txt" }
{ "id": "langchain-openai", "llms_txt_url": "https://docs.langchain.com/llms.txt" }
```

## Per-language entries

If a project publishes separate per-language documentation, create separate entries and suffix the `id`.

Common suffixes:

| Language | Suffix |
|----------|--------|
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

Use separate entries only when the documentation is genuinely separate. If both languages are covered by one `llms.txt`, use one entry with multiple package groups.

## Updating existing entries

1. Edit the relevant record in [`docs/known-libraries.json`](../docs/known-libraries.json).
2. If you change `llms_txt_url`, verify the new URL first.
3. Run:

```bash
uv run scripts/validate.py checksum
```

## Submitting changes

1. Create a descriptive branch.
2. Make the change.
3. Run `uv run scripts/validate.py checksum`.
4. Open a pull request with a short explanation of what changed and why.
