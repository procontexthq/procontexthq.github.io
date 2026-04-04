#!/usr/bin/env python3
from __future__ import annotations

"""
ProContext known-libraries validator.

Usage:
    uv run scripts/validate_libraries.py
    uv run scripts/validate_libraries.py --urls
    uv run scripts/validate_libraries.py --pypi
    uv run scripts/validate_libraries.py checksum
    uv run scripts/validate_libraries.py --libraries-file /tmp/known-libraries.json
    uv run scripts/validate_libraries.py --skip-rule 6
"""

import argparse
import sys

from registry_validation import (
    LIBRARIES_FILE,
    collect_libraries_errors,
    compute_checksum,
    display_path,
    normalize_skipped_rules,
    print_validation_result,
    resolve_cli_path,
)


def run_validation(args: argparse.Namespace) -> int:
    print(f"Validating {display_path(args.libraries_file)} ...")
    _, errors = collect_libraries_errors(
        args.libraries_file,
        check_url_reachability=args.urls,
        check_pypi_packages=args.pypi,
        skipped_rules=args.skipped_rules,
    )
    return print_validation_result(errors)


def cmd_checksum(args: argparse.Namespace) -> int:
    rc = run_validation(args)
    if rc != 0:
        print("Checksum NOT computed — fix validation errors first.")
        return rc

    print()
    checksum = compute_checksum(args.libraries_file)
    print(f"Computing checksum for {display_path(args.libraries_file)} ...")
    print(f"  checksum: {checksum}")
    return 0


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="validate_libraries.py",
        description="ProContext known-libraries validation and checksum tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
examples:
  uv run scripts/validate_libraries.py
  uv run scripts/validate_libraries.py --urls
  uv run scripts/validate_libraries.py --pypi
  uv run scripts/validate_libraries.py checksum
  uv run scripts/validate_libraries.py --libraries-file /tmp/known-libraries.json
  uv run scripts/validate_libraries.py --skip-rule 6
""",
    )
    parser.add_argument(
        "command",
        nargs="?",
        choices=("validate", "checksum"),
        default="validate",
        help="Optional command. Omit for validation; use 'checksum' to validate and print the SHA-256 checksum.",
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
    args = parser.parse_args()
    args.skipped_rules = normalize_skipped_rules(args.skipped_rules)
    args.libraries_file = resolve_cli_path(args.libraries_file, LIBRARIES_FILE)

    if args.command == "checksum":
        sys.exit(cmd_checksum(args))
    sys.exit(run_validation(args))


if __name__ == "__main__":
    main()
