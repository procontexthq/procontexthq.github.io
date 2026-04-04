# Code Contributions

Use this guide when you are changing repository scripts, validation logic, or tooling.

## Validation script layout

The validation tooling is split into three entrypoints plus a shared module:

- [`scripts/registry_validation.py`](../scripts/registry_validation.py)
  Shared validation, checksum, and metadata-update helpers.
- [`scripts/validate_libraries.py`](../scripts/validate_libraries.py)
  Standalone validator for `known-libraries.json`.
- [`scripts/validate_additional_info.py`](../scripts/validate_additional_info.py)
  Standalone validator for `registry-additional-info.json`.
- [`scripts/validate.py`](../scripts/validate.py)
  Combined validator that runs both flows, merges the output, and updates metadata on `checksum`.

## Behavior contract

Keep these expectations stable unless there is a strong reason to change them:

- `scripts/validate.py checksum` is the default repo workflow.
- The standalone scripts are usable on their own for external reuse.
- The standalone scripts can validate and print checksums.
- Only the combined script updates `registry_metadata.json`.
- Manual file paths are supported through CLI flags.

## Main commands

```bash
uv run scripts/validate.py checksum
uv run scripts/validate_libraries.py checksum
uv run scripts/validate_additional_info.py checksum
```

Optional slower checks for libraries:

```bash
uv run scripts/validate.py checksum --urls
uv run scripts/validate.py checksum --pypi
uv run scripts/validate_libraries.py --urls
uv run scripts/validate_libraries.py --pypi
```

Custom file-path examples:

```bash
uv run scripts/validate_libraries.py --libraries-file /tmp/known-libraries.json
uv run scripts/validate_additional_info.py --additional-info-file /tmp/registry-additional-info.json
uv run scripts/validate.py checksum \
  --libraries-file /tmp/known-libraries.json \
  --additional-info-file /tmp/registry-additional-info.json \
  --metadata-file /tmp/registry_metadata.json
```

Rule skips are also supported across all entrypoints:

```bash
uv run scripts/validate.py checksum --skip-rule 6
uv run scripts/validate_libraries.py --skip-rule 6 --libraries-file /tmp/known-libraries.json
```

Rule 6 is the optional description validation rule.

Full rule reference:

- [validation-rules.md](validation-rules.md)

## When changing validator code

Please verify at least:

```bash
python3 scripts/validate_libraries.py
python3 scripts/validate_additional_info.py
python3 scripts/validate.py
python3 scripts/validate_libraries.py checksum
python3 scripts/validate_additional_info.py checksum
```

If you change CLI behavior, also check:

```bash
python3 scripts/validate.py --help
python3 scripts/validate_libraries.py --help
python3 scripts/validate_additional_info.py --help
```

## Design intent

The split exists so the validation logic can be reused outside this repository, especially for known-library style data in other projects. Try to keep shared logic in the reusable module and keep the entrypoint scripts thin.
