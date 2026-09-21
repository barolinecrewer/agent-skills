#!/usr/bin/env node

const fs = require("node:fs");
const os = require("node:os");
const path = require("node:path");

const PACKAGE_NAME = "@barolinecrewer/agent-skills";
const MARKER_FILE = ".caroline-agent-skills.json";
const sourceRoot = path.resolve(__dirname, "..", "skills");
const excluded = [];

function usage(exitCode = 0) {
  console.log(`\n${PACKAGE_NAME}\n\nUsage:\n  npx --yes ${PACKAGE_NAME} install [--all | --codex | --claude]\n  npx --yes ${PACKAGE_NAME} update  [--all | --codex | --claude]\n\nOptions:\n  --all                 Install to both agents (the default).\n  --codex               Install to $CODEX_HOME/skills or ~/.codex/skills.\n  --claude              Install to $CLAUDE_CONFIG_DIR/skills or ~/.claude/skills.\n  --codex-dir <path>    Override Codex's configuration directory.\n  --claude-dir <path>   Override Claude Code's configuration directory.\n  --exclude <path>      Skip a file or directory, relative to skills/ (repeatable), e.g. ship/repos/infra.md.\n  --force               Replace an existing skill that was not installed by this package.\n  --help                Show this help.\n\nThe update command uses the same safe installer. npx fetches the latest published package before it runs.\n`);
  process.exit(exitCode);
}

function parseArgs(argv) {
  const result = { command: "install", targets: new Set(), force: false };
  for (let index = 0; index < argv.length; index += 1) {
    const arg = argv[index];
    if (arg === "install" || arg === "update") result.command = arg;
    else if (arg === "--all") result.targets.add("all");
    else if (arg === "--codex") result.targets.add("codex");
    else if (arg === "--claude") result.targets.add("claude");
    else if (arg === "--force") result.force = true;
    else if (arg === "--exclude") {
      const value = argv[++index];
      if (!value) throw new Error("--exclude requires a path.");
      excluded.push(path.resolve(sourceRoot, value));
    }
    else if (arg === "--codex-dir" || arg === "--claude-dir") {
      const value = argv[++index];
      if (!value) throw new Error(`${arg} requires a path.`);
      result[arg.slice(2, -4).replace("-", "")] = path.resolve(value);
    } else if (arg === "--help" || arg === "-h") usage();
    else throw new Error(`Unknown option: ${arg}`);
  }
  if (!result.targets.size || result.targets.has("all")) result.targets = new Set(["codex", "claude"]);
  return result;
}

function skillNames() {
  return fs.readdirSync(sourceRoot, { withFileTypes: true })
    .filter((entry) => entry.isDirectory() && fs.existsSync(path.join(sourceRoot, entry.name, "SKILL.md")))
    .map((entry) => entry.name)
    .sort();
}

function owned(destination) {
  const markerPath = path.join(destination, MARKER_FILE);
  if (!fs.existsSync(markerPath)) return false;
  try {
    return JSON.parse(fs.readFileSync(markerPath, "utf8")).package === PACKAGE_NAME;
  } catch {
    return false;
  }
}

function installTo(agent, configDirectory, force) {
  const destinationRoot = path.join(configDirectory, "skills");
  fs.mkdirSync(destinationRoot, { recursive: true });
  const installed = [];
  const skipped = [];

  for (const name of skillNames()) {
    const source = path.join(sourceRoot, name);
    if (excluded.includes(source)) continue;
    const destination = path.join(destinationRoot, name);
    if (fs.existsSync(destination) && !owned(destination) && !force) {
      skipped.push(name);
      continue;
    }
    fs.rmSync(destination, { recursive: true, force: true });
    fs.cpSync(source, destination, {
      recursive: true,
      filter: (entry) => ![".venv", ".venv311", "__pycache__"].includes(path.basename(entry)) && !excluded.includes(entry)
    });
    fs.writeFileSync(
      path.join(destination, MARKER_FILE),
      `${JSON.stringify({ package: PACKAGE_NAME, installedAt: new Date().toISOString() }, null, 2)}\n`
    );
    installed.push(name);
  }

  console.log(`${agent}: installed/updated ${installed.length} skill(s) in ${destinationRoot}`);
  if (skipped.length) console.log(`${agent}: skipped existing unowned skill(s): ${skipped.join(", ")}. Re-run with --force to replace them.`);
}

function main() {
  const options = parseArgs(process.argv.slice(2));
  const home = os.homedir();
  if (options.targets.has("codex")) {
    installTo("Codex", options.codex || process.env.CODEX_HOME || path.join(home, ".codex"), options.force);
  }
  if (options.targets.has("claude")) {
    installTo("Claude Code", options.claude || process.env.CLAUDE_CONFIG_DIR || path.join(home, ".claude"), options.force);
  }
  console.log("Start a new Codex or Claude Code session to load the updated skills.");
}

try {
  main();
} catch (error) {
  console.error(`Error: ${error.message}`);
  process.exitCode = 1;
}
