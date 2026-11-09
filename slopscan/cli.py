"""Detect common AI writing tells and generic AI-looking UI patterns."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, asdict
from pathlib import Path

__version__ = "0.1.1"

# Original, documented pattern list. These are common public-domain tells,
# not a copy of any commercial or open-source "unslop" word list.
PHRASES = [
    (r"\bdelve into\b", "phrase", "delve into"),
    (r"\bin today's fast-paced\b", "phrase", "in today's fast-paced"),
    (r"\bit'?s important to note\b", "phrase", "it's important to note"),
    (r"\bas an ai\b", "phrase", "as an AI"),
    (r"\bunleash( the)? (power|potential)\b", "phrase", "unleash the power/potential"),
    (r"\brobust and seamless\b", "phrase", "robust and seamless"),
    (r"\bseamless(ly)? (integrat|experience)\b", "phrase", "seamless experience/integration"),
    (r"\bin conclusion\b", "phrase", "in conclusion"),
    (r"\bembark on (a|this) journey\b", "phrase", "embark on a journey"),
    (r"\ba tapestry of\b", "phrase", "a tapestry of"),
    (r"\bin the realm of\b", "phrase", "in the realm of"),
    (r"\bleverage\b", "phrase", "leverage"),
    (r"\butilize\b", "phrase", "utilize"),
    (r"\bfurthermore\b", "phrase", "furthermore"),
    (r"\bnot only\b.{0,40}\bbut also\b", "phrase", "not only / but also"),
    (r"\bwhether you(?:'re| are) a\b", "phrase", "whether you're a"),
    (r"\bwelcome to the future of\b", "ui", "welcome to the future of"),
    (r"\brevolutionize (your|the)\b", "phrase", "revolutionize your/the"),
]

UI_PATTERNS = [
    (r"#6366f1", "ui", "Tailwind indigo-500 default"),
    (r"#8b5cf6", "ui", "Tailwind violet-500 default"),
    (r"bg-gradient-to-r\s+from-indigo-\d+\s+to-(purple|violet)-\d+", "ui", "indigo-to-purple gradient"),
    (r"font-family:\s*['\"]?Inter['\"]?", "ui", "Inter as the only font"),
    (r"rounded-3xl", "ui", "rounded-3xl card"),
    (r"shadow-xl", "ui", "shadow-xl card"),
]

EM_DASH_RE = re.compile(r"—")
HEDGE_RE = re.compile(r"\b(might|may|could|perhaps|arguably|it's worth noting)\b", re.I)


@dataclass
class Hit:
    kind: str
    label: str
    line: int
    excerpt: str


def scan_text(text: str) -> list[Hit]:
    hits: list[Hit] = []
    lines = text.splitlines() or [text]
    compiled = [(re.compile(p, re.I), kind, label) for p, kind, label in PHRASES + UI_PATTERNS]
    for i, line in enumerate(lines, 1):
        for regex, kind, label in compiled:
            if regex.search(line):
                hits.append(Hit(kind, label, i, line.strip()[:200]))
        dashes = len(EM_DASH_RE.findall(line))
        if dashes >= 2:
            hits.append(Hit("style", "em-dash cluster", i, line.strip()[:200]))
    # Re-run phrase patterns on whitespace-normalized text so a line break
    # in "delve into" still counts, without double-counting exact line hits.
    compact = re.sub(r"\s+", " ", text)
    already = {(h.kind, h.label) for h in hits}
    for regex, kind, label in compiled:
        if kind == "phrase" and (kind, label) not in already and regex.search(compact):
            hits.append(Hit(kind, label, 0, compact[:200]))
            already.add((kind, label))
    # document-level density checks
    words = re.findall(r"\S+", text)
    if words:
        hedges = len(HEDGE_RE.findall(text))
        if hedges / max(len(words), 1) >= 0.04 and hedges >= 4:
            hits.append(Hit("style", "hedge density", 0, f"{hedges} hedges in {len(words)} words"))
        dashes = len(EM_DASH_RE.findall(text))
        if dashes / max(len(words), 1) >= 0.03 and dashes >= 4:
            hits.append(Hit("style", "em-dash density", 0, f"{dashes} em dashes in {len(words)} words"))
    return hits


def score(hits: list[Hit]) -> int:
    weights = {"phrase": 2, "ui": 2, "style": 1}
    return min(100, sum(weights.get(h.kind, 1) for h in hits) * 8)


def verdict(score_value: int) -> str:
    if score_value >= 50:
        return "high"
    if score_value >= 20:
        return "medium"
    if score_value > 0:
        return "low"
    return "clean"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="slopscan",
        description="Detect common AI writing tells and generic AI-looking UI patterns.",
    )
    parser.add_argument("input", nargs="?", default="-", help="file, or '-' for stdin")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--version", action="version", version=f"slopscan {__version__}")
    args = parser.parse_args(argv)
    if args.input == "-":
        text = sys.stdin.read()
    else:
        path = Path(args.input)
        if not path.is_file():
            print(f"error: file not found: {path}", file=sys.stderr)
            return 1
        text = path.read_text(encoding="utf-8", errors="replace")
    hits = scan_text(text)
    value = score(hits)
    result = {"score": value, "verdict": verdict(value), "hits": [asdict(h) for h in hits]}
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"verdict: {result['verdict']}  score: {value}")
        if not hits:
            print("no hits")
        for h in hits:
            loc = f"L{h.line}" if h.line else "doc"
            print(f"- {h.kind}: {h.label} ({loc}) {h.excerpt}")
    if value >= 50:
        return 2
    if value > 0:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
