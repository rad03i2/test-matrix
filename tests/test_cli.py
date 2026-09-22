import json

from test_matrix.cli import main


def test_cli_github_output(tmp_path, capsys):
    spec = tmp_path / "matrix.json"
    spec.write_text(json.dumps({"axes": {"python": ["3.11", "3.12"]}}), encoding="utf-8")
    assert main([str(spec), "--format", "github"]) == 0
    data = json.loads(capsys.readouterr().out)
    assert data["include"] == [{"python": "3.11"}, {"python": "3.12"}]


def test_cli_coverage_exit_code(tmp_path, capsys):
    spec = tmp_path / "matrix.json"
    spec.write_text(json.dumps({"axes": {"os": ["linux"]}, "required": {"os": ["linux", "windows"]}}), encoding="utf-8")
    assert main([str(spec), "--check-coverage"]) == 2
    assert "missing coverage" in capsys.readouterr().err


def test_cli_invalid_json(tmp_path, capsys):
    spec = tmp_path / "bad.json"
    spec.write_text("{bad", encoding="utf-8")
    assert main([str(spec)]) == 1
    assert "error:" in capsys.readouterr().err
