#!/usr/bin/env node

import { existsSync, readdirSync, readFileSync, statSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const rootDir = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const skillDir = join(rootDir, "skills", "tex-manual-translation");

if (resolve(process.argv[1] ?? "") === fileURLToPath(import.meta.url)) {
  try {
    validateSkill(skillDir);
    console.log(`OK: ${skillDir}`);
  } catch (error) {
    console.error(error.message);
    process.exit(1);
  }
}

export function validateSkill(dir) {
  // 1. SKILL.md must exist with valid frontmatter
  const skillMd = join(dir, "SKILL.md");
  assertFile(skillMd);

  const content = readFileSync(skillMd, "utf8");
  const fm = parseFrontmatter(content, skillMd);
  assertEqual(fm.name, "tex-manual-translation", "SKILL.md name must be tex-manual-translation.");
  assertPresent(fm.description, "SKILL.md description is required.");

  // 2. All referenced files in SKILL.md must exist
  const refMatches = [...content.matchAll(/\(references\/[^)]+\)/g)];
  for (const match of refMatches) {
    const refPath = match[0].slice(1, -1); // strip parens
    assertFile(join(dir, refPath));
  }

  // 3. references/ directory must exist with .md files
  const refsDir = join(dir, "references");
  assertDirectory(refsDir);
  const refFiles = readdirSync(refsDir).filter(f => f.endsWith(".md"));
  if (refFiles.length === 0) {
    throw new Error("Expected at least one references/*.md file.");
  }

  // 4. scripts/ directory must exist with .py files
  const scriptsDir = join(dir, "scripts");
  assertDirectory(scriptsDir);
  const pyFiles = readdirSync(scriptsDir).filter(f => f.endsWith(".py"));
  if (pyFiles.length === 0) {
    throw new Error("Expected at least one scripts/*.py file.");
  }

  // 5. Each script referenced in SKILL.md must exist
  const scriptMatches = [...content.matchAll(/scripts\/(\w+\.py)/g)];
  for (const match of scriptMatches) {
    assertFile(join(dir, "scripts", match[1]));
  }

  console.log(`  SKILL.md: name=${fm.name}, description=${fm.description.slice(0, 40)}...`);
  console.log(`  references/: ${refFiles.length} file(s)`);
  console.log(`  scripts/: ${pyFiles.length} file(s)`);
}

function parseFrontmatter(content, filePath) {
  const match = content.match(/^---\r?\n([\s\S]*?)\r?\n---\r?\n/);
  if (!match) {
    throw new Error(`${filePath} must start with YAML frontmatter.`);
  }
  const result = {};
  for (const line of match[1].split(/\r?\n/)) {
    const field = line.match(/^([a-zA-Z0-9_-]+):\s*(.*)$/);
    if (field) result[field[1]] = field[2].trim();
  }
  return result;
}

function assertFile(p) {
  if (!existsSync(p) || !statSync(p).isFile()) throw new Error(`Missing required file: ${p}`);
}
function assertDirectory(p) {
  if (!existsSync(p) || !statSync(p).isDirectory()) throw new Error(`Missing required directory: ${p}`);
}
function assertPresent(v, msg) { if (!v) throw new Error(msg); }
function assertEqual(a, e, msg) { if (a !== e) throw new Error(`${msg} Got "${a}", expected "${e}".`); }
