#!/usr/bin/env python3
"""Detect potentially untranslated English sentences in a translated LaTeX file.

Scans for lines containing 5+ consecutive English words outside code
environments, which may indicate missed translations.

Usage: python find_untranslated.py <file.tex>

Exit codes:
  0 — no suspicious lines found
  1 — one or more suspicious lines found
  2 — usage error
"""

import re
import sys
from pathlib import Path

# Environments whose content should not be translated
CODE_ENVS = {
    "verbatim", "verbatim*", "lstlisting", "Verbatim", "Verbatim*",
    "minted", "alltt", "comment", "macro", "macrocode",
    "filecontents", "filecontents*",
}

# 5+ consecutive English words (2+ letters each, whitespace separated)
ENGLISH_SENTENCE = re.compile(r"\b[A-Za-z]{2,}(?:\s+[A-Za-z]{2,}){4,}\b")


def find_untranslated(filepath: str) -> int:
    text = Path(filepath).read_text(encoding="utf-8")
    lines = text.splitlines()

    code_depth = 0
    issues: list[tuple[int, str, str]] = []

    for lineno, line in enumerate(lines, 1):
        # Track code environment entry/exit
        for m in re.finditer(r"\\(begin|end)\{(\w+\*?)}", line):
            kind, env = m.group(1), m.group(2)
            if env in CODE_ENVS:
                code_depth += 1 if kind == "begin" else -1
                code_depth = max(0, code_depth)

        if code_depth > 0:
            continue
        if line.lstrip().startswith("%"):
            continue

        # Strip LaTeX commands and inline math for cleaner detection
        clean = re.sub(r"\\[A-Za-z]+\*?(?:\[[^\]]*\])?(?:\{[^}]*\})*", "", line)
        clean = re.sub(r"\$[^$]*\$", "", clean)

        for m in ENGLISH_SENTENCE.finditer(clean):
            matched = m.group().strip()
            if len(matched) < 25:
                continue
            issues.append((lineno, matched, line.rstrip()))

    if not issues:
        print("No potentially untranslated English sentences found.")
        return 0

    print(f"Found {len(issues)} potentially untranslated line(s):\n")
    for lineno, matched, content in issues:
        print(f"  Line {lineno}")
        print(f"    Matched: {matched[:80]}{'...' if len(matched) > 80 else ''}")
        print(f"    Full:    {content[:120]}")
        print()

    print("Review these lines — they may contain untranslated English text.")
    return 1


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <file.tex>", file=sys.stderr)
        sys.exit(2)
    sys.exit(find_untranslated(sys.argv[1]))
