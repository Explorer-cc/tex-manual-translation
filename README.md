# TeX Manual Translation Skill

An installable Claude, Codex, and OMP skill for translating English LaTeX documentation into Chinese.

The skill covers scope survey, CJK environment setup, terminology management, word-by-word translation, compile verification with validation scripts, and large-document parallelism. It catches real LaTeX + CJK pitfalls such as `\LaTeX\，` triggering `Undefined control sequence` errors.

## Install

Use npm without a global install:

```bash
npx tex-manual-translation install claude
npx tex-manual-translation install codex
npx tex-manual-translation install omp
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

## Manual Install

Copy `skills/tex-manual-translation` into your agent's skills directory.

Common locations:

- Claude: `~/.claude/skills/tex-manual-translation`
- Codex: `~/.codex/skills/tex-manual-translation`
- OMP: `~/.omp/skills/tex-manual-translation`

If your client uses a different skills directory, copy the folder there or use `--target`.

## Validate

```bash
npm test
npm run doctor
```

The validator checks the required `SKILL.md`, referenced files, `references/`, and `scripts/`.

## Publish

```bash
npm pack
npm publish --access public
```

Test the packed artifact before publishing:

```bash
npm pack
npx ./tex-manual-translation-1.1.0.tgz install --target ./tmp/skills --dry-run
```

## License

MIT
