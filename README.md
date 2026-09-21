# Caroline Agent Skills

One versioned collection of reusable skills for Codex and Claude Code. The repository includes native manifests for both platforms (`.codex-plugin/plugin.json` and `.claude-plugin/plugin.json`) plus an npm package with a safe cross-agent installer.

## Install or update with npx

After publishing this folder to npm as `@barolinecrewer/agent-skills`:

```bash
npx --yes @barolinecrewer/agent-skills@latest install --all
npx --yes @barolinecrewer/agent-skills@latest update --all
```

Use one target when needed:

```bash
npx --yes @barolinecrewer/agent-skills@latest update --codex
npx --yes @barolinecrewer/agent-skills@latest update --claude
```

The installer copies top-level skills to `$CODEX_HOME/skills` (or `~/.codex/skills`) and `$CLAUDE_CONFIG_DIR/skills` (or `~/.claude/skills`). It never replaces a same-named skill it did not previously install unless you add `--force`.