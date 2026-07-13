# tex-manual-translation

> An AI agent skill that translates English LaTeX documentation into Chinese — word by word, with compile-time guardrails.

## Overview

This skill guides an AI agent through translating English LaTeX user manuals into Chinese. It reads each paragraph of the English source, understands the meaning, re-expresses it in Chinese, and writes the translation via line-by-line editing. No regex substitution or automated batch tools are used for the actual translation — only for validation checks.

**Key features:**

- **7-step workflow** — from scope survey to large-document parallelism
- **Compile-first gate** — verifies the Chinese environment builds *before* translation begins
- **Three validation scripts** — automated checks for environment balance, CJK punctuation bugs, and untranslated text residue
- **Terminology management** — persistent glossary for full-document consistency
- **Domain-hardened rules** — catches real LaTeX + CJK pitfalls (e.g. `\LaTeX\，` → `Undefined control sequence`)

## Installation

```bash
npm install tex-manual-translation
```

Then copy `skills/tex-manual-translation/` into your AI agent's skills directory:

- **Claude Code**: `~/.claude/skills/tex-manual-translation/`
- **Codex**: `~/.codex/skills/tex-manual-translation/`
- **OMP**: `~/.omp/skills/tex-manual-translation/`
- **Custom**: any directory your agent scans for `SKILL.md` files

The skill auto-activates when you say "翻译 tex", "翻译 LaTeX 手册", "中文化手册", "translate LaTeX to Chinese", or "把英文文档翻译成中文".

## Workflow

```
Survey → Setup CJK Env → Terminology → Task Breakdown → Translate → Compile Check → Parallelize
```

| Step | Action | Gate |
|---|---|---|
| 1. Survey | Identify `.tex` / `.dtx` file type, grep code environment names | — |
| 2. Setup CJK | Insert `ctex`, select `fontset`, compile untranslated original | **Original compiles to PDF** |
| 3. Terminology | Create `glossary.md`, define keep-English / translate rules | — |
| 4. Breakdown | Create todo list by `\chapter` / `\section` | — |
| 5. Translate | Translate paragraph by paragraph, maintain punctuation & editing rules | — |
| 6. Verify | Compile after each chapter, run validation scripts | **Compile passes** |
| 7. Parallelize | Split large docs into sub-agents, share glossary | — |

## Validation Scripts

Three Python scripts (standard library only — no extra dependencies) assist with compile verification:

| Script | Purpose | Usage |
|---|---|---|
| `check_env_balance.py` | Counts `\begin{X}` / `\end{X}` pairs, reports unbalanced environments with line numbers | `python scripts/check_env_balance.py <file.tex>` |
| `find_backslash_before_cjk.py` | Scans for control-space backslash before Chinese punctuation (`\LaTeX\，`-type bugs) | `python scripts/find_backslash_before_cjk.py <file.tex>` |
| `find_untranslated.py` | Detects suspected untranslated English passages outside code environments | `python scripts/find_untranslated.py <file.tex>` |

**Exit codes:** `0` = no issues found, `1` = issues detected, `2` = usage error.

## Reference Documents

| File | Content |
|---|---|
| `references/punctuation.md` | Full-width/half-width punctuation rules, LaTeX mixed CJK punctuation rules with correct/incorrect examples |
| `references/editing-rules.md` | Editing golden rule (never touch `\begin`/`\end` structural lines), line-number management, common error patterns |
| `references/terminology.md` | Keep-English / translate decision rules, first-occurrence format for proper nouns, glossary template |
| `references/latex-elements.md` | Translation rules for `\index`, `\href`, `\footnote`, `\caption`, BibTeX, and other LaTeX elements |

## Core Rules

### LaTeX Mixed CJK Punctuation

A control-space backslash must **never** precede Chinese punctuation — it triggers cascading `Undefined control sequence` errors:

```latex
✗  \LaTeX\，    →  parsed as undefined control sequence \，
✓  \LaTeX，
```

**Why:** `\LaTeX\，` is parsed as the undefined control sequence `\，`. The same bug occurs across line breaks when a line ends with `\command\` and the next line starts with Chinese punctuation.

### Editing Golden Rule

When replacing text lines, if the replacement range contains `\begin{...}` or `\end{...}`, they **must be written back verbatim** in the replacement body. Otherwise the marker is permanently lost, causing dozens of cascading compilation errors.

### Engine & Font Selection

- **Engine:** Default `lualatex`; fall back to `xelatex` on `TeX capacity exceeded` or compile timeout (>120s). `pdflatex` is excluded (incompatible with CJK).
- **Fontset:** Try `fandol` → `ubuntu` → `lxgw` in order. Switch on `.log` `Missing character: There is no <glyph> in font` warnings.
- **Fallback:** If `ctex` conflicts with existing packages, switch to `xeCJK` manual loading: `\usepackage{xeCJK}` + `\setCJKmainfont{}`.

## Package Structure

```
tex-manual-translation/
├── package.json
├── LICENSE
└── skills/
    └── tex-manual-translation/
        ├── SKILL.md              ← Skill entry point (7-step workflow)
        ├── scripts/              ← Validation scripts (3)
        │   ├── check_env_balance.py
        │   ├── find_backslash_before_cjk.py
        │   └── find_untranslated.py
        └── references/           ← Reference docs (4)
            ├── punctuation.md
            ├── editing-rules.md
            ├── terminology.md
            └── latex-elements.md
```

## Requirements

- Any AI agent that supports skill-based workflows (Claude Code, Codex, Oh My Pi, etc.)
- Python 3.8+ — validation scripts (standard library only)
- LaTeX distribution (TeX Live / MiKTeX) — compile verification
- `ctex` package — Chinese typesetting support

## License

[MIT](LICENSE)
