from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from .core import MatrixError, generate_matrix, validate_coverage
from . import __version__


def _load(path: str) -> dict[str, Any]:
    try:
        text = sys.stdin.read() if path == "-" else Path(path).read_text(encoding="utf-8")
        data = json.loads(text)
    except (OSError, json.JSONDecodeError) as exc:
        raise MatrixError(f"cannot read specification: {exc}") from exc
    if not isinstance(data, dict):
        raise MatrixError("specification root must be an object")
    return data


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="test-matrix", description="Generate deterministic CI test matrices from JSON.")
    p.add_argument("spec", nargs="?", help="JSON specification path, or - for stdin")
    p.add_argument("--format", choices=("rows", "github", "json"), default="rows")
    p.add_argument("--max-combinations", type=int, default=10_000)
    p.add_argument("--check-coverage", action="store_true", help="Fail when spec.required values are uncovered")
    p.add_argument("--version", action="version", version=f"test-matrix {__version__} — Radwan Abdulhadi Ahmed / @rad03i2")
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if not args.spec:
        build_parser().print_help()
        return 0
    try:
        spec = _load(args.spec)
        result = generate_matrix(spec.get("axes", {}), exclude=spec.get("exclude", []), include=spec.get("include", []), max_combinations=args.max_combinations)
        gaps = validate_coverage(result, spec.get("required", {})) if args.check_coverage else []
        if args.format == "github":
            print(json.dumps(result.as_github_matrix(), ensure_ascii=False, indent=2))
        elif args.format == "json":
            print(json.dumps({"count": result.count, "axes": list(result.axes), "combinations": result.combinations, "coverage_gaps": gaps}, ensure_ascii=False, indent=2))
        else:
            print("\t".join(result.axes))
            for row in result.combinations:
                print("\t".join(str(row.get(axis, "")) for axis in result.axes))
            print(f"\n{result.count} combination(s)", file=sys.stderr)
        if gaps:
            for gap in gaps:
                print(gap, file=sys.stderr)
            return 2
        return 0
    except MatrixError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    raise SystemExit(main())
