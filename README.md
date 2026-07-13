# TeX Manual Translation Skill

An installable Claude and Codex skill for translating English LaTeX documentation into Chinese.

The skill covers scope survey, CJK environment setup, terminology management, word-by-word translation, compile verification with validation scripts, and large-document parallelism. It catches real LaTeX + CJK pitfalls such as `\LaTeX\，` triggering `Undefined control sequence` errors.

## Install

Use npm without a global install:

```bash
npx tex-manual-translation install claude
npx tex-manual-translation install codex
```

Install into an explicit skills directory:

```bash
npx tex-manual-translation install --target ~/.claude/skills
npx tex-manual-translation install --target ~/.codex/skills
```

Replace an existing install:

```bash
npx tex-manual-translation install claude --force
```

Dry-run to preview without writing:

```bash
npx tex-manual-translation install --target ./tmp/skills --dry-run
```

## Manual Install

Copy `skills/tex-manual-translation` into your agent's skills directory.

Common locations:

- Claude: `~/.claude/skills/tex-manual-translation`
- Codex: `~/.codex/skills/tex-manual-translation`

If your client uses a different skills directory, copy the folder there or use `--target`.

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
├── bin/
│   └── tex-manual-translation.mjs   ← Installer CLI
├── scripts/
│   ├── validate.mjs                  ← Skill structure validator
│   └── test_scripts.py              ← Script test harness
└── skills/
    └── tex-manual-translation/
        ├── SKILL.md                  ← Skill entry point (7-step workflow)
        ├── scripts/                  ← Validation scripts (3)
        │   ├── check_env_balance.py
        │   ├── find_backslash_before_cjk.py
        │   └── find_untranslated.py
        └── references/               ← Reference docs (4)
            ├── punctuation.md
            ├── editing-rules.md
            ├── terminology.md
            └── latex-elements.md
```

## Validate

```bash
npm test
npm run doctor
```

The validator checks the required `SKILL.md`, referenced files, `references/`, and `scripts/`.

## Requirements

- Python 3.8+ — validation scripts (standard library only)
- LaTeX distribution (TeX Live / MiKTeX) — compile verification
- `ctex` package — Chinese typesetting support

## Publish

```bash
npm pack
npm publish --access public
```

Test the packed artifact before publishing:

```bash
npm pack
npx ./tex-manual-translation-1.2.0.tgz install --target ./tmp/skills --dry-run
```

## License

MIT
