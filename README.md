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

For a GitHub-hosted, un-published release, run the same command through a GitHub package reference after replacing the repository owner:

```bash
npx --yes github:YOUR_GITHUB_USER/caroline-agent-skills install --all
```

Open a new session after installation so the agent discovers the refreshed skill set.

## Codex plugin installation

Codex plugins are installed from a marketplace rather than npm. Keep this repository in a local or remote marketplace, then use:

```bash
codex plugin add caroline-agent-skills@YOUR_MARKETPLACE
```

The npm command is the portable sync route for both Codex and Claude Code; the plugin manifest lets Codex load the same skills natively from a marketplace.

## Claude Code plugin installation

The Claude manifest uses the same `skills/` directory as Codex. Once the repository is on GitHub, add it as a Claude Code plugin marketplace or install it directly using your normal Claude Code plugin workflow; no duplicated skills or separate release process is needed.

## Publishing a release

1. Create a Git repository from this folder and push it to your GitHub account.
2. If the `@barolinecrewer` npm scope is not yours, change `package.json` to a scope you control.
3. Log in and publish:

   ```bash
   npm login
   npm publish --access public
   ```
4. For each later release, update `version` in both `package.json` and `.codex-plugin/plugin.json`, then publish again. Users update with the same `npx ... update` command.