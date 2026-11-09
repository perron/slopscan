# slopscan

Detect common AI writing tells and generic AI-looking UI patterns in text
or HTML/CSS. It is a scanner, not a rewriter: it prints hits and a score
so a skill or a review step can decide what to change.

The pattern list is original and documented in the source. It is not a
copy of any other "unslop" or "humanizer" word list.

## Install

```bash
python3 -m pip install -e .
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
