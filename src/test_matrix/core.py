from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from typing import Any, Iterable, Mapping


class MatrixError(ValueError):
    """Raised for invalid matrix specifications."""


@dataclass(frozen=True)
class MatrixResult:
    combinations: tuple[dict[str, Any], ...]
    axes: tuple[str, ...]

    @property
    def count(self) -> int:
        return len(self.combinations)

    def as_github_matrix(self) -> dict[str, Any]:
        """Return a GitHub Actions compatible explicit include matrix."""
        return {"include": [dict(item) for item in self.combinations]}


def _validate_axes(axes: Mapping[str, Iterable[Any]]) -> dict[str, tuple[Any, ...]]:
    if not isinstance(axes, Mapping) or not axes:
        raise MatrixError("axes must be a non-empty object")
    normalized: dict[str, tuple[Any, ...]] = {}
    for name, values in axes.items():
        if not isinstance(name, str) or not name.strip():
            raise MatrixError("axis names must be non-empty strings")
        if isinstance(values, (str, bytes, Mapping)):
            raise MatrixError(f"axis '{name}' must be an array")
        try:
            vals = tuple(values)
        except TypeError as exc:
            raise MatrixError(f"axis '{name}' must be iterable") from exc
        if not vals:
            raise MatrixError(f"axis '{name}' cannot be empty")
        normalized[name] = vals
    return normalized


def _matches(combo: Mapping[str, Any], rule: Mapping[str, Any]) -> bool:
    return bool(rule) and all(combo.get(k) == v for k, v in rule.items())


def generate_matrix(
    axes: Mapping[str, Iterable[Any]], *, exclude: Iterable[Mapping[str, Any]] = (),
    include: Iterable[Mapping[str, Any]] = (), max_combinations: int = 10_000,
) -> MatrixResult:
    """Generate a deterministic Cartesian test matrix with include/exclude rules."""
    normalized = _validate_axes(axes)
    if max_combinations < 1:
        raise MatrixError("max_combinations must be at least 1")
    names = tuple(normalized)
    theoretical = 1
    for values in normalized.values():
        theoretical *= len(values)
        if theoretical > max_combinations:
            raise MatrixError(f"matrix expands to {theoretical}+ combinations; limit is {max_combinations}")

    exclusions = tuple(exclude)
    additions = tuple(include)
    for rule in (*exclusions, *additions):
        if not isinstance(rule, Mapping):
            raise MatrixError("include/exclude entries must be objects")

    rows = [dict(zip(names, values)) for values in product(*(normalized[n] for n in names))]
    rows = [row for row in rows if not any(_matches(row, rule) for rule in exclusions)]
    for addition in additions:
        candidate = dict(addition)
        if candidate not in rows:
            rows.append(candidate)
    if len(rows) > max_combinations:
        raise MatrixError(f"final matrix exceeds limit of {max_combinations}")
    return MatrixResult(tuple(rows), names)


def validate_coverage(result: MatrixResult, required: Mapping[str, Iterable[Any]]) -> list[str]:
    """Return human-readable coverage gaps for required axis values."""
    gaps: list[str] = []
    for axis, values in required.items():
        present = {row.get(axis) for row in result.combinations if axis in row}
        for value in values:
            if value not in present:
                gaps.append(f"missing coverage: {axis}={value!r}")
    return gaps
