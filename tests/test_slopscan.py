from pathlib import Path
import json
import slopscan.cli as ss


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
