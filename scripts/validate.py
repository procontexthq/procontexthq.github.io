#!/usr/bin/env python3
from __future__ import annotations

"""
ProContext Registry — combined validation and checksum management.

Usage:
    uv run scripts/validate.py                       # fast schema and cross-entry validation
    uv run scripts/validate.py --urls               # + URL reachability (rule 22)
    uv run scripts/validate.py --pypi               # + PyPI package existence (rule 23)
    uv run scripts/validate.py checksum              # validate, then update both checksums
    uv run scripts/validate.py checksum --urls --pypi  # validation + optional network checks
    uv run scripts/validate.py --libraries-file /tmp/known-libraries.json
    uv run scripts/validate.py checksum --metadata-file /tmp/registry_metadata.json
    uv run scripts/validate.py --skip-rule 6
"""

import argparse
import sys

from registry_validation import (
    ADDITIONAL_INFO_FILE,
    LIBRARIES_FILE,
    METADATA_FILE,
    collect_additional_info_errors,
    collect_libraries_errors,
    compute_checksum,
    display_path,
    normalize_skipped_rules,
    print_validation_result,
    resolve_cli_path,
    update_metadata,
)


def run_validation(args: argparse.Namespace) -> int:
    print(f"Validating {display_path(args.libraries_file)} ...")
    _, library_errors = collect_libraries_errors(
        args.libraries_file,
        check_url_reachability=args.urls,
        check_pypi_packages=args.pypi,
        skipped_rules=args.skipped_rules,
    )

    print(f"Validating {display_path(args.additional_info_file)} ...")
    additional_info_errors = collect_additional_info_errors(
        args.additional_info_file,
        skipped_rules=args.skipped_rules,
    )
    return print_validation_result(library_errors + additional_info_errors)


def cmd_checksum(args: argparse.Namespace) -> int:
    rc = run_validation(args)
    if rc != 0:
        print("Checksum NOT updated — fix validation errors first.")
        return rc

    print()
    libraries_checksum = compute_checksum(args.libraries_file)
    additional_info_checksum = compute_checksum(args.additional_info_file)
    print(f"Computing checksum for {display_path(args.libraries_file)} ...")
    print(f"Computing checksum for {display_path(args.additional_info_file)} ...")
    update_metadata(libraries_checksum, additional_info_checksum, args.metadata_file)
    return 0


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="validate.py",
        description="ProContext Registry — combined validation and checksum management",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
examples:
  uv run scripts/validate.py                       fast schema and cross-entry validation
  uv run scripts/validate.py --urls               + URL reachability (rule 22)
  uv run scripts/validate.py --pypi               + PyPI package existence (rule 23)
  uv run scripts/validate.py checksum              validate, then update both checksums
  uv run scripts/validate.py checksum --urls       + URL reachability before checksum update
  uv run scripts/validate.py checksum --pypi       + PyPI package existence before checksum update
  uv run scripts/validate.py --libraries-file /tmp/known-libraries.json
  uv run scripts/validate.py checksum --metadata-file /tmp/registry_metadata.json
  uv run scripts/validate.py --skip-rule 6
""",
    )
    parser.add_argument(
        "command",
        nargs="?",
        choices=("validate", "checksum"),
        default="validate",
        help="Optional command. Omit for validation; use 'checksum' to validate and update registry_metadata.json.",
    )
    parser.add_argument("--urls", action="store_true", help="Also check URL reachability (rule 22, slow)")
    parser.add_argument("--pypi", action="store_true", help="Also verify PyPI packages exist (rule 23, slow)")
    parser.add_argument(
        "--skip-rule",
        dest="skipped_rules",
        action="append",
        type=int,
        default=None,
        help="Skip a specific validation rule. Repeat to skip multiple rules, e.g. --skip-rule 6 --skip-rule 22.",
    )
    parser.add_argument(
        "--libraries-file",
        default=None,
        help=f"Path to known-libraries JSON. Defaults to {display_path(LIBRARIES_FILE)}.",
    )
    parser.add_argument(
        "--additional-info-file",
        default=None,
        help=f"Path to registry-additional-info JSON. Defaults to {display_path(ADDITIONAL_INFO_FILE)}.",
    )
    parser.add_argument(
        "--metadata-file",
        default=None,
        help=f"Path to registry metadata JSON for checksum updates. Defaults to {display_path(METADATA_FILE)}.",
    )
    args = parser.parse_args()
    args.skipped_rules = normalize_skipped_rules(args.skipped_rules)
    args.libraries_file = resolve_cli_path(args.libraries_file, LIBRARIES_FILE)
    args.additional_info_file = resolve_cli_path(args.additional_info_file, ADDITIONAL_INFO_FILE)
    args.metadata_file = resolve_cli_path(args.metadata_file, METADATA_FILE)

    if args.command == "checksum":
        sys.exit(cmd_checksum(args))
    sys.exit(run_validation(args))


if __name__ == "__main__":
    main()
