#!/usr/bin/env python3
"""Find backslash control-space before Chinese punctuation in a LaTeX file.

Detects patterns like \\LaTeX\\， where a control-space backslash precedes
Chinese punctuation, causing 'Undefined control sequence' errors.

Usage: python find_backslash_before_cjk.py <file.tex>

Exit codes:
  0 — no issues found
  1 — one or more issues found
  2 — usage error
"""

import re
import sys
from pathlib import Path

# Chinese punctuation that triggers the bug when preceded by \
CJK_PUNCT = "，。；：（）？！、""''……—"

# Match \ immediately followed by a Chinese punctuation character
PATTERN = re.compile(r"\\([" + re.escape(CJK_PUNCT) + r"])")


def find_issues(filepath: str) -> int:
    text = Path(filepath).read_text(encoding="utf-8")
    issues: list[tuple[int, int, str, str]] = []

    for lineno, line in enumerate(text.splitlines(), 1):
        if line.lstrip().startswith("%"):
            continue
        for m in PATTERN.finditer(line):
            issues.append((lineno, m.start() + 1, m.group(1), line.rstrip()))

    if not issues:
        print("No backslash-before-CJK-punctuation issues found.")
        return 0

    print(f"Found {len(issues)} issue(s):\n")
    for lineno, col, punct, content in issues:
        print(f"  Line {lineno}:{col}  punct='{punct}'")
        print(f"    {content}")
        print()

    print("Fix: remove the backslash before the Chinese punctuation.")
    print("Example: \\LaTeX\\， -> \\LaTeX，")
    return 1


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <file.tex>", file=sys.stderr)
        sys.exit(2)
    sys.exit(find_issues(sys.argv[1]))
