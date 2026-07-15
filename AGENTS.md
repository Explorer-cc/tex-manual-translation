# Repository Guidelines

## Project Overview

**tex-manual-translation** is an npm package that ships a single skill for translating English LaTeX documentation into Chinese. The skill works with any AI coding agent and guides it through a 7-step workflow — from scope survey to large-document parallelism — with compile-time gate conditions and three Python validation scripts that catch common LaTeX + CJK pitfalls.

Published to npm as `tex-manual-translation`. Install with `npx tex-manual-translation install claude` (or `codex`), or copy the skill folder into any agent's skills directory.

## Architecture & Data Flow

```
package.json (npm manifest)
  └── skills/tex-manual-translation/     ← agents discover skills one level under skills/
       ├── SKILL.md                       ← Controller: 7-step workflow, gates, reference links
       ├── scripts/                       ← Layered linters (called during step 6)
       │   ├── check_env_balance.py       ← \begin{}/\end{} pair checker
       │   ├── find_backslash_before_cjk.py ← CJK punctuation backslash scanner
       │   └── find_untranslated.py       ← Untranslated English passage detector
       └── references/                    ← Convention sources (loaded on demand during step 5)
           ├── punctuation.md
           ├── editing-rules.md
           ├── terminology.md
           └── latex-elements.md
```

**Data flow:** SKILL.md is the entry point. It drives the AI agent linearly through 7 steps. Reference files are loaded on demand (progressive disclosure) — the agent reads `references/punctuation.md` only when handling punctuation, not at startup. Python scripts are invoked as CLI tools during step 6 (compile verification), each taking a `.tex` file path and returning an exit code.

**Gate conditions** block progress at two points:
- Step 2: untranslated Chinese-version original must compile to PDF before translation begins
- Step 6: each chapter must compile after translation

## Key Directories

| Directory | Purpose |
|---|---|
| `skills/tex-manual-translation/` | The skill itself — agents discover it via a one-level scan of `skills/<name>/SKILL.md` |
| `skills/.../scripts/` | Three standalone Python linters (stdlib only, no dependencies) |
| `skills/.../references/` | Four Markdown convention docs loaded on demand by the AI agent |
| `scripts/` | Package-level tooling: `validate.mjs` (skill structure validator) and `test_scripts.py` (test harness). Not published to npm. |
| `.github/workflows/` | CI workflow |

## Development Commands

```bash
# Validate skill structure (frontmatter, file existence, directory layout)
npm run validate

# Run full test suite (structure validator + Python script tests)
npm test

# Run Python script tests only
python scripts/test_scripts.py

# Verify npm packaging (dry run, no publish)
npm pack --dry-run

# Publish to npm (requires npm login + OTP)
npm publish --otp=<code>
```

## Code Conventions & Common Patterns

### Python Scripts (skills/.../scripts/)

All three scripts share a **uniform calling convention** and **identical error-handling shape**:

```python
# Usage: python <script>.py <file.tex>
# Exit codes: 0 = no issues, 1 = issues found, 2 = usage error

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <file.tex>", file=sys.stderr)
        sys.exit(2)
    sys.exit(main_function(sys.argv[1]))
```

- **Dependencies**: stdlib only (`re`, `sys`, `pathlib`, `collections`). Never add external deps.
- **Comment skipping**: all scripts skip lines starting with `%` (LaTeX comments).
- **Code environment tracking**: `find_untranslated.py` tracks `code_depth` to skip `verbatim`, `lstlisting`, `minted`, etc.
- **Output format**: human-readable with line numbers, not machine-parseable JSON.

### Node.js Scripts (scripts/)

- **ESM only**: `"type": "module"` in package.json. Use `import` syntax, `.mjs` extension.
- `validate.mjs` serves dual duty: CLI entry point and importable module (exports `validateSkill()`).
- Frontmatter parsing is manual regex (no YAML library dependency).

### SKILL.md Conventions

- Frontmatter: `name` and `description` only (no extra fields).
- Reference links use relative paths: `[references/punctuation.md](references/punctuation.md)`.
- Script invocations use relative paths: `python scripts/check_env_balance.py <file.tex>`.
- Workflow steps are numbered (`## 1.` through `## 7.`) with gate conditions in **bold**.

## Important Files

| File | Role |
|---|---|
| `package.json` | npm manifest. `files` controls what gets published (`bin/`, `scripts/`, `skills/`, README, LICENSE). |
| `skills/tex-manual-translation/SKILL.md` | Skill entry point — the 7-step workflow. The agent reads this when the skill triggers. |
| `skills/.../references/punctuation.md` | LaTeX mixed CJK punctuation rules with correct/incorrect code examples. |
| `skills/.../references/editing-rules.md` | Editing golden rule: never lose `\begin{}`/`\end{}` markers during line replacement. |
| `skills/.../references/terminology.md` | Keep-English vs translate decision rules, glossary template. |
| `skills/.../references/latex-elements.md` | Per-element translation rules (`\index`, `\href`, `\footnote`, `\caption`, BibTeX, etc.). |
| `scripts/validate.mjs` | Skill structure validator — checks frontmatter, referenced files, directory layout. |
| `scripts/test_scripts.py` | Test harness — creates fixture .tex, runs all 3 scripts, asserts exit codes and output. |
| `.github/workflows/ci.yml` | CI: validate structure → test scripts → verify npm pack. |

## Runtime/Tooling Preferences

| Tool | Requirement | Notes |
|---|---|---|
| Node.js | ≥18 | Required for ESM (`"type": "module"`) and `validate.mjs` |
| Python | ≥3.8 | Required for the 3 validation scripts (stdlib only, no pip install needed) |
| npm | ≥10 | Package management and publishing |
| LaTeX | TeX Live / MiKTeX | Required at runtime for compile verification (user's environment, not CI) |
| `ctex` | LaTeX package | Chinese typesetting support (user's environment) |

**No build step.** The package is pure data — Markdown, Python scripts, and JSON. No compilation, no bundling, no transpilation.

## Testing & QA

### CI Pipeline (`.github/workflows/ci.yml`)

Runs on every push to `main` and every PR:

1. **Validate skill structure** — `node scripts/validate.mjs` checks SKILL.md frontmatter (`name`, `description`), verifies all referenced files exist, confirms `references/` has `.md` files and `scripts/` has `.py` files.
2. **Test validation scripts** — `python scripts/test_scripts.py` creates a fixture `.tex` file with known issues (unbalanced env, backslash before CJK, untranslated English), runs all 3 scripts, and asserts exit codes + output patterns. Also tests the unbalanced environment case separately.
3. **Verify npm pack** — `npm pack --dry-run` ensures the tarball builds with correct file list.

### Local Testing

```bash
npm test    # runs both validate.mjs and test_scripts.py
```

### Test Coverage

The test harness covers:
- ✅ Environment balance detection (balanced + unbalanced cases)
- ✅ Backslash-before-CJK-punctuation detection
- ✅ Untranslated English passage detection
- ✅ Code environment content correctly skipped (not flagged as untranslated)
- ✅ Skill structure validation (frontmatter, file references, directory layout)

No coverage thresholds — this is a data package, not an application. Tests guard against structural breakage, not runtime behavior.
