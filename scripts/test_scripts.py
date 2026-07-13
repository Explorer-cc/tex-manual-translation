#!/usr/bin/env python3
"""Test harness for the three validation scripts.

Creates a fixture .tex file with known issues, runs each script,
and verifies expected exit codes and output patterns.
"""

import subprocess
import sys
import tempfile
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "skills" / "tex-manual-translation" / "scripts"

FIXTURE = r"""\documentclass{article}
\usepackage{ctex}
\begin{document}
\section{Test}

\LaTeX\，this has a backslash before CJK punctuation.

\begin{verbatim}
This code should not be flagged as untranslated content here.
\end{verbatim}

\begin{itemize}
\item First item
This is an untranslated English sentence that should be detected by the scanner.
\end{itemize}

\end{document}
"""


def run_script(name, fixture_path):
    """Run a script and return (exit_code, stdout)."""
    result = subprocess.run(
        [sys.executable, str(SCRIPTS_DIR / name), str(fixture_path)],
        capture_output=True, text=True,
    )
    return result.returncode, result.stdout + result.stderr


def test_check_env_balance(fixture_path):
    code, out = run_script("check_env_balance.py", fixture_path)
    assert code == 0, f"Expected exit 0, got {code}\n{out}"
    assert "document" in out, f"Expected 'document' in output\n{out}"
    assert "verbatim" in out, f"Expected 'verbatim' in output\n{out}"
    assert "All environments balanced" in out, f"Expected balanced message\n{out}"
    print("  PASS  check_env_balance.py")


def test_find_backslash_before_cjk(fixture_path):
    code, out = run_script("find_backslash_before_cjk.py", fixture_path)
    assert code == 1, f"Expected exit 1 (issues found), got {code}\n{out}"
    assert "LaTeX" in out, f"Expected 'LaTeX' in output\n{out}"
    assert "，" in out, f"Expected CJK comma in output\n{out}"
    print("  PASS  find_backslash_before_cjk.py")


def test_find_untranslated(fixture_path):
    code, out = run_script("find_untranslated.py", fixture_path)
    assert code == 1, f"Expected exit 1 (issues found), got {code}\n{out}"
    assert "untranslated" in out.lower(), f"Expected 'untranslated' in output\n{out}"
    assert "should not be flagged" not in out, f"Verbatim content was wrongly flagged\n{out}"
    print("  PASS  find_untranslated.py")


def test_check_env_balance_unbalanced():
    """Test with an intentionally unbalanced file."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".tex", delete=False, encoding="utf-8") as f:
        f.write("\\begin{document}\n\\begin{itemize}\n\\end{document}\n")
        path = f.name
    try:
        code, out = run_script("check_env_balance.py", path)
        assert code == 1, f"Expected exit 1 (mismatch), got {code}\n{out}"
        assert "MISMATCH" in out, f"Expected 'MISMATCH' in output\n{out}"
        assert "itemize" in out, f"Expected 'itemize' in output\n{out}"
        print("  PASS  check_env_balance.py (unbalanced case)")
    finally:
        Path(path).unlink()


def main():
    print("Running script tests...\n")

    with tempfile.NamedTemporaryFile(mode="w", suffix=".tex", delete=False, encoding="utf-8") as f:
        f.write(FIXTURE)
        fixture_path = f.name

    try:
        test_check_env_balance(fixture_path)
        test_find_backslash_before_cjk(fixture_path)
        test_find_untranslated(fixture_path)
        test_check_env_balance_unbalanced()
    finally:
        Path(fixture_path).unlink()

    print("\nAll tests passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
