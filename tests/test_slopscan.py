from pathlib import Path
import io
import json
import pytest
import slopscan.cli as ss


def test_help_and_version():
    with pytest.raises(SystemExit) as exc:
        ss.main(["--help"])
    assert exc.value.code == 0
    with pytest.raises(SystemExit) as exc:
        ss.main(["--version"])
    assert exc.value.code == 0


def test_clean_prose(tmp_path, capsys):
    path = tmp_path / "note.md"
    path.write_text("Ship the fix on Tuesday. The timeout was coming from the refresh path.\n")
    assert ss.main([str(path)]) == 0
    assert "clean" in capsys.readouterr().out


def test_planted_writing_tells(tmp_path, capsys):
    path = tmp_path / "essay.md"
    path.write_text(
        "In today's fast-paced world, it is important to note that we must delve into the realm of design.\n"
        "Furthermore, we will unleash the potential of the stack and leverage a seamless experience.\n"
        "In conclusion, welcome to the future of notes.\n"
    )
    assert ss.main([str(path), "--json"]) == 2
    data = json.loads(capsys.readouterr().out)
    labels = {h["label"] for h in data["hits"]}
    assert "delve into" in labels
    assert "in today's fast-paced" in labels
    assert data["verdict"] == "high"


def test_ui_patterns(tmp_path, capsys):
    path = tmp_path / "page.html"
    path.write_text(
        '<body class="bg-gradient-to-r from-indigo-500 to-purple-500 rounded-3xl shadow-xl" '
        'style="font-family: Inter, sans-serif; color:#6366f1">Welcome to the future of notes</body>\n'
    )
    assert ss.main([str(path)]) == 2
    out = capsys.readouterr().out
    assert "indigo" in out or "Inter" in out
    assert "welcome to the future of" in out


def test_missing_file(tmp_path, capsys):
    assert ss.main([str(tmp_path / "nope.md")]) == 1
    assert "file not found" in capsys.readouterr().err


def test_empty_file_is_clean(tmp_path, capsys):
    path = tmp_path / "empty.md"
    path.write_text("")
    assert ss.main([str(path)]) == 0
    assert "clean" in capsys.readouterr().out


def test_stdin(monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin", io.StringIO("Ship the fix on Tuesday.\n"))
    assert ss.main(["-"]) == 0
    assert "clean" in capsys.readouterr().out


def test_em_dash_cluster(tmp_path, capsys):
    path = tmp_path / "dash.md"
    path.write_text("The result — after review — was accepted.\n")
    assert ss.main([str(path)]) == 1
    assert "em-dash cluster" in capsys.readouterr().out


def test_hedge_density(tmp_path, capsys):
    path = tmp_path / "hedge.md"
    path.write_text("It might work. It may help. It could ship. Perhaps it will. Arguably this is fine.\n")
    assert ss.main([str(path), "--json"]) == 1
    data = json.loads(capsys.readouterr().out)
    labels = {h["label"] for h in data["hits"]}
    assert "hedge density" in labels


def test_linebreak_phrase(tmp_path, capsys):
    path = tmp_path / "wrap.md"
    path.write_text("We should delve\ninto the details tomorrow.\n")
    assert ss.main([str(path), "--json"]) == 1
    data = json.loads(capsys.readouterr().out)
    labels = {h["label"] for h in data["hits"]}
    assert "delve into" in labels


def test_single_hit_is_low(tmp_path, capsys):
    path = tmp_path / "one.md"
    path.write_text("Furthermore, the tests passed on Tuesday.\n")
    assert ss.main([str(path), "--json"]) == 1
    data = json.loads(capsys.readouterr().out)
    assert data["verdict"] in {"low", "medium"}
    assert data["score"] < 50


def test_unicode_clean(tmp_path, capsys):
    path = tmp_path / "ja.md"
    path.write_text("火曜日に修正を出す。タイムアウトは refresh 経路だった。✅\n", encoding="utf-8")
    assert ss.main([str(path)]) == 0
    assert "clean" in capsys.readouterr().out


def test_score_caps_at_100():
    text = (
        "In today's fast-paced world, it's important to note we must delve into the realm of design. "
        "Furthermore, unleash the potential, leverage a seamless experience, in conclusion, "
        "welcome to the future of notes. Embark on this journey, a tapestry of robust and seamless work. "
        "Revolutionize your stack. Whether you're a beginner, not only this but also that. "
        "As an AI, utilize everything. bg-gradient-to-r from-indigo-500 to-purple-500 rounded-3xl shadow-xl "
        "font-family: Inter #6366f1 #8b5cf6"
    )
    hits = ss.scan_text(text)
    assert ss.score(hits) == 100
