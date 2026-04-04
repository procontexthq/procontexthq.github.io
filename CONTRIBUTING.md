# Contributing to the ProContext Registry

Contributions are welcome. This file is the contributor entrypoint and points to the right level of detail for the task at hand.

## Start here

If you are adding or updating registry data, read:

- [contributing/registry.md](contributing/registry.md)

If you are changing scripts, validation logic, or repo tooling, read:

- [contributing/code.md](contributing/code.md)

## Default workflow

For most registry changes, the main command is:

```bash
uv run scripts/validate.py checksum
```

That validates the registry files and updates [`docs/registry_metadata.json`](docs/registry_metadata.json).
