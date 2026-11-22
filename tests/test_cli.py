"""End-to-end tests of the pyrompt CLI: each command runs through main() against a temp base path."""

import io
import sys

import pytest

from pyrompt.cli import main


@pytest.fixture
def run(tmp_path, monkeypatch, capsys):
    def _run(*args, expect_exit=None):
        monkeypatch.setattr(sys, "argv", ["pyrompt", "--path", str(tmp_path), *args])
        if expect_exit is None:
            main()
        else:
            with pytest.raises(SystemExit) as e:
                main()
            assert e.value.code == expect_exit
        return capsys.readouterr().out

    return _run


@pytest.fixture
def demo(run):
    run("new", "demo")
    return "demo"


def test_new_list_show_stats(run, demo):
    assert "Created project 'other'" in run("new", "other")
    out = run("list", demo)
    assert "system_default: You are a helpful AI assistant." in out
    assert "=== system_default ===" in run("show", demo, "system_default")
    out = run("stats", demo)
    assert "Total prompts: 1" in out and "Average length" in out


def test_new_without_examples_gives_empty_collection(run):
    run("new", "bare", "--no-examples")
    assert "(empty)" in run("list", "bare")


def test_add_inline_file_and_stdin(run, demo, tmp_path, monkeypatch):
    assert "Added 'greet'" in run("add", demo, "greet", "Hello there")
    assert "greet: Hello there" in run("list", demo)
    f = tmp_path / "p.txt"
    f.write_text("from a file")
    run("add", demo, "fromfile", "x", "--file", str(f))
    assert "from a file" in run("show", demo, "fromfile")
    monkeypatch.setattr(sys, "stdin", io.StringIO("from stdin"))
    run("add", demo, "fromstdin")
    assert "from stdin" in run("show", demo, "fromstdin")


def test_long_prompt_is_truncated_in_list(run, demo):
    run("add", demo, "long", "word " * 40)
    line = [l for l in run("list", demo).splitlines() if "long:" in l][0]
    assert line.endswith("...")


def test_show_missing_key_exits_1(run, demo):
    out = run("show", demo, "nope", expect_exit=1)
    assert "not found" in out


def test_templates_list_and_render(run, demo):
    assert "greeting.txt" in run("list", demo, "--templates")
    out = run("render", demo, "greeting.txt", "--params", '{"name": "Ada", "project": "P"}')
    assert "Hello Ada, welcome to P!" in out
    out = run("render", demo, "greeting.txt", "--params", "name=Bo, project=Q")
    assert "Hello Bo, welcome to Q!" in out
    assert "not found" in run("render", demo, "missing.txt", expect_exit=1)


def test_engines_lists_format_engine(run):
    out = run("engines")
    assert "Available template engines:" in out and "format:" in out


def test_no_command_prints_help_and_exits_1(run):
    assert "Manage AI prompts" in run(expect_exit=1)


def test_errors_are_reported_not_raised(run):
    out = run("render", "ghost", "k", expect_exit=1)
    assert "not found" in out or "Error" in out
