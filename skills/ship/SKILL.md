---
name: ship
description: Commit and push a repo with a Conventional Commits + gitmoji message, then watch CI. Use when the user says "/ship <repo>", "ship it", or asks to commit and push changes. Takes a repo name (a directory under ~) and applies per-repo rules from repos/<repo>.md.
argument-hint: <repo>
---

# Ship

Ship the repo named in the arguments (a directory under `~`, so `~/<repo>`).

**No argument:** use the current working directory's repo (its top-level directory name is `<repo>`). If `repos/<repo>.md` doesn't exist, invoke the `ship-init` skill first to create it from the repo's actual ways of working, then continue. If it exists, use it.

1. Read repo-specific instructions from `repos/<repo>.md`, relative to this skill's directory, if it exists. Apply them in addition to the general steps below; where they conflict, the repo file wins. If it doesn't exist, continue with the general steps only and mention that at the end.
2. `cd` into the repo and run `git status` and `git diff`. If there are no staged or unstaged changes, stop and say so. Do not push.
3. Do any pre-commit work the repo file asks for (README updates, lint, etc.) so it lands in the same commit.
4. Group the changes into logical commits, one per concern. Split when files belong to different units of work, e.g. a service/stack change vs. DNS/terraform changes vs. CI config vs. docs for something else, or a `feat` vs. an unrelated `chore`. Signals: different top-level directories or components, different commit types, or changes that could be reverted independently. Keep together files that only make sense together (a feature and its tests/docs, a compose file and its env template). If a single file mixes concerns, use `git add -p` (or stage by hunk) to split it. If everything is one concern, make one commit; don't split for its own sake.
   Stage each group explicitly by path (never `git add -A` when splitting), excluding anything that looks like a secret (`.env`, keys, credentials); flag those instead of staging. Before committing, show the planned groups (files and message per commit) in one short list, then proceed without waiting unless the grouping is ambiguous.
5. For each group, in order, stage it and commit with a Conventional Commits message with a gitmoji prefix:

   `<gitmoji> <type>(<optional scope>): <imperative subject, lowercase, no period, <=72 chars>`

   Optional body explains why, not what. Breaking changes: `!` after type/scope plus a `BREAKING CHANGE:` footer.

   | Type | Gitmoji | Use for |
   |---|---|---|
   | feat | ✨ | new feature or capability |
   | fix | 🐛 | bug fix |
   | docs | 📝 | documentation only |
   | style | 💄 | formatting/UI, no logic change |
   | refactor | ♻️ | restructure, no behavior change |
   | perf | ⚡️ | performance |
   | test | ✅ | tests |
   | build | 📦️ | build system, dependencies |
   | ci | 👷 | CI/CD config |
   | chore | 🔧 | config, tooling, misc |
   | revert | ⏪️ | revert a commit |
   | (removal) | 🔥 | deleting code/files (use with chore/refactor) |
   | (security) | 🔒️ | security fix (use with fix) |
   | (deps bump) | ⬆️ | upgrade deps (use with build) |

   Pick the single type that best fits each commit. Never use a vague message to cover unrelated changes; that's a sign to split.
6. Push all commits to the current branch (`git push`, or `git push -u origin <branch>` if no upstream). Ask before force-pushing. Never push to a protected default branch if the repo file says to use PRs.
7. If the repo has GitHub Actions workflows (`.github/workflows`), get the latest run with `gh run list --branch $(git branch --show-current) --limit 1`, watch it with `gh run watch <run-id>`, and report the final status. Skip this if there are no workflows or the repo file says to.

## Adding a repo

Create `repos/<name>.md` with any extra rules: scopes to use, PR vs. direct push, checks to run first, files never to stage.
