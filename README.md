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

## 30-second example

```bash
cat > draft.md << 'EOF'
In today's fast-paced world, it is important to note that we must delve into the realm of design.
Furthermore, we will unleash the potential of the stack and leverage a seamless experience.
In conclusion, welcome to the future of notes.
EOF

slopscan draft.md
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

## License

MIT. See `LICENSE`. Please read `SECURITY.md` before filing a vulnerability report.
