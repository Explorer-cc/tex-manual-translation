#!/usr/bin/env node

import { existsSync, mkdirSync, readdirSync, rmSync, copyFileSync } from "node:fs";
import { homedir } from "node:os";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { validateSkill } from "../scripts/validate.mjs";

const rootDir = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const skillName = "tex-manual-translation";
const skillDir = join(rootDir, "skills", skillName);

main().catch((error) => {
  console.error(error.message);
  process.exit(1);
});

async function main() {
  const [command, ...args] = process.argv.slice(2);

  switch (command) {
    case "install":
      install(args);
      break;
    case "doctor":
    case "validate":
      validateSkill(skillDir);
      console.log(`OK: ${skillName} skill is valid.`);
      break;
    case "help":
    case "--help":
    case "-h":
    case undefined:
      printHelp();
      break;
    default:
      throw new Error(`Unknown command: ${command}\nRun "tex-manual-translation help".`);
  }
}

function install(args) {
  const options = parseInstallArgs(args);
  validateSkill(skillDir);

  const baseDir = options.target
    ? resolve(options.target)
    : defaultSkillsDir(options.client);
  const destination = join(baseDir, skillName);

  if (options.dryRun) {
    console.log(`Would install ${skillName} to ${destination}`);
    return;
  }

  if (existsSync(destination)) {
    if (!options.force) {
      throw new Error(`Destination already exists: ${destination}\nRe-run with --force to replace it.`);
    }
    rmSync(destination, { recursive: true, force: true });
  }

  mkdirSync(baseDir, { recursive: true });
  copyDirectory(skillDir, destination);
  console.log(`Installed ${skillName} to ${destination}`);
}

function parseInstallArgs(args) {
  const options = {
    client: "claude",
    target: undefined,
    force: false,
    dryRun: false
  };

  for (let index = 0; index < args.length; index += 1) {
    const arg = args[index];
    if (arg === "codex" || arg === "claude" || arg === "omp") {
      options.client = arg;
    } else if (arg === "--target") {
      const value = args[index + 1];
      if (!value) {
        throw new Error("--target requires a directory path.");
      }
      options.target = value;
      index += 1;
    } else if (arg === "--force") {
      options.force = true;
    } else if (arg === "--dry-run") {
      options.dryRun = true;
    } else {
      throw new Error(`Unknown install option: ${arg}`);
    }
  }

  return options;
}

function defaultSkillsDir(client) {
  if (client === "codex") {
    return join(homedir(), ".codex", "skills");
  }
  if (client === "claude") {
    return join(homedir(), ".claude", "skills");
  }
  if (client === "omp") {
    return join(homedir(), ".omp", "skills");
  }
  throw new Error(`Unsupported client: ${client}`);
}

function copyDirectory(source, destination) {
  mkdirSync(destination, { recursive: true });

  for (const entry of readdirSync(source, { withFileTypes: true })) {
    const sourcePath = join(source, entry.name);
    const destinationPath = join(destination, entry.name);

    if (entry.isDirectory()) {
      copyDirectory(sourcePath, destinationPath);
    } else if (entry.isFile()) {
      mkdirSync(dirname(destinationPath), { recursive: true });
      copyFileSync(sourcePath, destinationPath);
    } else {
      throw new Error(`Unsupported filesystem entry in skill package: ${sourcePath}`);
    }
  }
}

function printHelp() {
  console.log(`tex-manual-translation

Usage:
  tex-manual-translation install [claude|codex|omp] [--target <dir>] [--force] [--dry-run]
  tex-manual-translation doctor
  tex-manual-translation help

Examples:
  tex-manual-translation install claude
  tex-manual-translation install codex --target ~/.codex/skills
  tex-manual-translation install omp --force
  tex-manual-translation install --target /tmp/skills --dry-run
`);
}
