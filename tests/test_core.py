import pytest

from test_matrix import MatrixError, generate_matrix, validate_coverage


def test_cartesian_product_is_deterministic():
    result = generate_matrix({"python": ["3.11", "3.12"], "os": ["ubuntu", "windows"]})
    assert result.count == 4
    assert result.combinations[0] == {"python": "3.11", "os": "ubuntu"}


def test_exclude_partial_rule_and_include():
    result = generate_matrix(
        {"python": ["3.11", "3.12"], "os": ["ubuntu", "windows"]},
        exclude=[{"python": "3.11", "os": "windows"}],
        include=[{"python": "3.13", "os": "ubuntu", "experimental": True}],
    )
    assert result.count == 4
    assert {"python": "3.11", "os": "windows"} not in result.combinations
    assert result.combinations[-1]["experimental"] is True


def test_github_export_is_explicit_include():
    result = generate_matrix({"node": [20, 22]})
    assert result.as_github_matrix() == {"include": [{"node": 20}, {"node": 22}]}


def test_coverage_reports_gap():
    result = generate_matrix({"python": ["3.12"]})
    assert validate_coverage(result, {"python": ["3.12", "3.13"]}) == ["missing coverage: python='3.13'"]


def test_rejects_empty_axis_and_explosion():
    with pytest.raises(MatrixError):
        generate_matrix({"python": []})
    with pytest.raises(MatrixError):
        generate_matrix({"a": range(101), "b": range(100)}, max_combinations=10_000)
