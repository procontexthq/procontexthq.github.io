# ProContext Registry

This repository hosts the library registry for [ProContext](https://github.com/procontexthq/procontext) — an MCP server that gives AI coding agents accurate, up-to-date library documentation.

The live registry is published at [procontexthq.github.io](https://procontexthq.github.io/).

## What's in here

```
docs/
├── known-libraries.json          # The registry — one entry per supported library
├── registry-additional-info.json # Extra registry metadata used by probes and enrichment
└── registry_metadata.json        # Version pointer + checksums, fetched by ProContext on startup
registry-schema.md                # Canonical schema reference for registry JSON files
```

ProContext polls `registry_metadata.json` every 24 hours. When the `version` changes, it downloads `known-libraries.json` and `registry-additional-info.json`, verifies their SHA-256 checksums, and updates its in-memory index.

`registry-additional-info.json` stores supplemental data used outside the core library index. In particular, `useful_md_probe_base_urls` lists documentation URLs that should be probed by appending `.md` to determine whether they expose a valid Markdown document directly.

## Schema

See **[registry-schema.md](registry-schema.md)** for the full field reference — library-level fields, `PackageEntry` fields, `registry-additional-info.json`, and the `resolve_library` response format.

## Registry metadata format

```json
{
  "version": "YYYY-MM-DD",
  "download_url": "https://procontexthq.github.io/known-libraries.json",
  "checksum": "sha256:<hex>",
  "additional_info_download_url": "https://procontexthq.github.io/registry-additional-info.json",
  "additional_info_checksum": "sha256:<hex>"
}
```

## Validation & tooling

The primary contributor workflow is:

### Setup

```bash
uv sync
```

### Main command

```bash
uv run scripts/validate.py checksum
```

That command validates both registry JSON files, computes fresh SHA-256 checksums, and updates `docs/registry_metadata.json`.

For deeper contributor guidance, standalone validator usage, and custom file-path examples, see:

- [CONTRIBUTING.md](CONTRIBUTING.md)
- [contributing/registry.md](contributing/registry.md)
- [contributing/code.md](contributing/code.md)

## Contributing

Contributions are welcome! Start with [CONTRIBUTING.md](CONTRIBUTING.md).

## License

This project is licensed under the [MIT License](LICENSE).
