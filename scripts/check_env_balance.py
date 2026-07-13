#!/usr/bin/env python3
"""Check \\begin{X} / \\end{X} balance in a LaTeX file.

Usage: python check_env_balance.py <file.tex>

Exit codes:
  0 — all environments balanced
  1 — one or more environments unbalanced
  2 — usage error
"""

import re
import sys
from collections import defaultdict
from pathlib import Path


def check_balance(filepath: str) -> int:
    text = Path(filepath).read_text(encoding="utf-8")

    begins: dict[str, list[int]] = defaultdict(list)
    ends: dict[str, list[int]] = defaultdict(list)

    for lineno, line in enumerate(text.splitlines(), 1):
        if line.lstrip().startswith("%"):
            continue
        for m in re.finditer(r"\\begin\{(\w+\*?)}", line):
            begins[m.group(1)].append(lineno)
        for m in re.finditer(r"\\end\{(\w+\*?)}", line):
            ends[m.group(1)].append(lineno)

    all_envs = set(begins) | set(ends)
    if not all_envs:
        print("No environments found.")
        return 0

    has_mismatch = False
    for env in sorted(all_envs):
        b = len(begins.get(env, []))
        e = len(ends.get(env, []))
        if b != e:
            has_mismatch = True
            print(f"MISMATCH  \\begin{{{env}}}={b}  \\end{{{env}}}={e}  (diff={b - e:+d})")
            print(f"  \\begin lines: {begins.get(env, [])}")
            print(f"  \\end   lines: {ends.get(env, [])}")
        else:
            print(f"OK        \\begin{{{env}}}={b}  \\end{{{env}}}={e}")

    if has_mismatch:
        print("\nUnbalanced environments detected. Check for lost \\begin/\\end markers.")
    else:
        print("\nAll environments balanced.")

    return 1 if has_mismatch else 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <file.tex>", file=sys.stderr)
        sys.exit(2)
    sys.exit(check_balance(sys.argv[1]))
