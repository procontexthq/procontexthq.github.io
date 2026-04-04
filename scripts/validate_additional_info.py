#!/usr/bin/env python3
from __future__ import annotations

"""
ProContext registry-additional-info validator.

Usage:
    uv run scripts/validate_additional_info.py
    uv run scripts/validate_additional_info.py checksum
    uv run scripts/validate_additional_info.py --additional-info-file /tmp/registry-additional-info.json
"""

import argparse
import sys

from registry_validation import (
    ADDITIONAL_INFO_FILE,
    collect_additional_info_errors,
    compute_checksum,
    display_path,
    print_validation_result,
    resolve_cli_path,
)


def run_validation(args: argparse.Namespace) -> int:
    print(f"Validating {display_path(args.additional_info_file)} ...")
    errors = collect_additional_info_errors(args.additional_info_file)
    return print_validation_result(errors)


def cmd_checksum(args: argparse.Namespace) -> int:
    rc = run_validation(args)
    if rc != 0:
        print("Checksum NOT computed — fix validation errors first.")
        return rc

    print()
    checksum = compute_checksum(args.additional_info_file)
    print(f"Computing checksum for {display_path(args.additional_info_file)} ...")
    print(f"  checksum: {checksum}")
    return 0


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="validate_additional_info.py",
        description="ProContext registry-additional-info validation and checksum tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
examples:
  uv run scripts/validate_additional_info.py
  uv run scripts/validate_additional_info.py checksum
  uv run scripts/validate_additional_info.py --additional-info-file /tmp/registry-additional-info.json
""",
    )
    parser.add_argument(
        "command",
        nargs="?",
        choices=("validate", "checksum"),
        default="validate",
        help="Optional command. Omit for validation; use 'checksum' to validate and print the SHA-256 checksum.",
    )
    parser.add_argument(
        "--additional-info-file",
        default=None,
        help=f"Path to registry-additional-info JSON. Defaults to {display_path(ADDITIONAL_INFO_FILE)}.",
    )
    args = parser.parse_args()
    args.additional_info_file = resolve_cli_path(args.additional_info_file, ADDITIONAL_INFO_FILE)

    if args.command == "checksum":
        sys.exit(cmd_checksum(args))
    sys.exit(run_validation(args))


if __name__ == "__main__":
    main()
