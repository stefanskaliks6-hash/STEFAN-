"""CLI entrypoint for the student housing accelerator."""

from __future__ import annotations

import argparse
import json
import sys

from .builder import build_housing_brief, build_profile


def _parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate a student housing research brief from a JSON profile.",
    )
    parser.add_argument(
        "--input",
        "-i",
        required=True,
        help="Path to a JSON file describing the student housing profile.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv or sys.argv[1:])
    try:
        with open(args.input, "r", encoding="utf-8") as handle:
            payload = json.load(handle)
    except FileNotFoundError as exc:
        print(f"Input file not found: {exc}", file=sys.stderr)
        return 1
    except json.JSONDecodeError as exc:
        print(f"Input file is not valid JSON: {exc}", file=sys.stderr)
        return 1

    profile = build_profile(payload)
    brief = build_housing_brief(profile)
    print(brief)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
