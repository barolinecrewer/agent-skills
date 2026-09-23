---
name: ship-init
description: Create a repo-specific repos/<repo>.md for the ship skill by inspecting how the repo is worked on. Use when /ship finds no repo file.
argument-hint: [repo]
---

# Ship Init

Write `repos/<repo>.md` in the ship skill's directory, capturing this repo's ways of working so `/ship <repo>` can follow them. `<repo>` is the argument, or the basename of the current git repo's top-level directory.

If the file already exists, show it and ask whether to update it. Don't overwrite silently.

## Inspect (read-only; never read `.env`, `stack.env`, `Caddyfile`, or other secret files)

- **Docs**: `README.md`, `CLAUDE.md`, `AGENTS.md`, `CONTRIBUTING.md`. Look for stated conventions, deploy flow, and "never do X" rules.
- **Commit style**: `git log --oneline -30`. Do commits already use conventional commits? Which scopes recur?
- **Branching**: default branch (`git symbolic-ref refs/remotes/origin/HEAD`), current branch, recent merge history (`git log --merges -10`). Direct pushes to the default branch, or PRs? Merge, squash, or rebase?
- **CI**: `.github/workflows/*` (or other CI config). What triggers on push? Is it a deploy? Which workflows are worth watching?
- **Pre-commit work**: lint/format/test scripts (`package.json`, `Makefile`, `pyproject.toml`, pre-commit config), and docs that must track the code (README sections, changelogs, generated files).
- **Never-commit files**: `.gitignore` plus anything the docs call secret or generated.
- **Remote**: `git remote -v`; is it GitHub (`gh` works) or something else?

## Write

Keep it short: bullets, only rules that differ from or add to the general `/ship` flow. Sections, omitting any that are empty:

```markdown
# <repo>

Path: `~/<repo>`. <one-line description>

- Branch/PR policy
- Pre-commit steps (README updates, lint, tests)
- Never stage: <files>
- Suggested scopes: <list>
- CI: <watch or skip, and which workflow>
```

Don't invent rules. If something is unclear from the repo, leave it out or ask one concise question.

## Finish

Show the written file. If invoked from `/ship`, continue shipping the repo using it; otherwise stop.
