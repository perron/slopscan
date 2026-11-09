# slopscan

Detect common AI writing tells and generic AI-looking UI patterns in text
or HTML/CSS. It is a scanner, not a rewriter: it prints hits and a score
so a skill or a review step can decide what to change.

The pattern list is original and documented in the source. It is not a
copy of any other "unslop" or "humanizer" word list.

## Install

Python 3.10 or later.

From a checkout:

```bash
python3 -m pip install .
python3 -m pip install -e ".[dev]"  # optional, for tests
slopscan draft.md
```

## 30-second quick start

```bash
cat > draft.md << 'EOF'
In today's fast-paced world, it is important to note that we must delve into the realm of design.
Furthermore, we will unleash the potential of the stack and leverage a seamless experience.
In conclusion, welcome to the future of notes.
EOF

slopscan draft.md
```

Sample output from that exact example:

```
$ slopscan draft.md
verdict: high  score: 100
- phrase: delve into (L1) In today's fast-paced world, it is important to note that we must delve into the realm of design.
- phrase: in today's fast-paced (L1) In today's fast-paced world, it is important to note that we must delve into the realm of design.
- phrase: unleash the power/potential (L2) Furthermore, we will unleash the potential of the stack and leverage a seamless experience.
- phrase: seamless experience/integration (L2) Furthermore, we will unleash the potential of the stack and leverage a seamless experience.
- phrase: leverage (L2) Furthermore, we will unleash the potential of the stack and leverage a seamless experience.
- phrase: furthermore (L2) Furthermore, we will unleash the potential of the stack and leverage a seamless experience.
- phrase: in conclusion (L3) In conclusion, welcome to the future of notes.
- ui: welcome to the future of (L3) In conclusion, welcome to the future of notes.
exit: 2
```

Exit codes: `0` clean, `1` low/medium, `2` high.

## Credit

Motivated by the wave of anti-slop design and writing skills in late 2026.
Original patterns and scoring; no source was copied from those skills.

## Limits

- This is a scanner, not a rewriter. It prints hits and a score; it does not rewrite the file.
- The pattern list is original, documented in the source, and necessarily incomplete. Human writing can trip a pattern, and AI writing can avoid one.
- Scores are capped at 100. Exit codes: `0` clean, `1` low/medium, `2` high.

From GitHub you can also install with:

```bash
python3 -m pip install git+https://github.com/perron/slopscan.git
```

This package is not published to PyPI.

## Use it with your agent

You can point a coding agent at this repository and ask it to use the tool, adapt it, or write a small tool in the same style. That works with Claude Code, Codex, Cursor, Grok Bot, and anything else that can clone a git repo and run a Python CLI.

A short prompt you can paste:

> Clone https://github.com/perron/slopscan, install it, and scan ./draft.md. List the hits and say which ones I should actually change. Do not rewrite the file unless I ask.

If you want a new tool in this style, say so explicitly: one job, standard-library Python, pytest first, no API key, and an honest Limits section.

## Contributing / how you can help

Bug reports, tight tests, and small honest features are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md) for how to run the suite and for pull request guidelines.

Good first issues:

- Accept an optional extra patterns file so a team can add house tells without forking the defaults.
- Walk a directory of `.md` / `.html` / `.css` files and summarize by file.
- Skip fenced code blocks in Markdown so a quoted phrase in an example is not a hit.

If you are unsure whether an idea fits, open an issue before writing a large patch.

## License

MIT. See `LICENSE`. Please read `SECURITY.md` before filing a vulnerability report. Agents should also read `AGENTS.md`.
