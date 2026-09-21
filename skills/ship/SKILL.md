---
name: ship
description: Stage, commit (Conventional Commits v1.0.0), and push a repo, then watch CI. Applies per-repo rules from repos/<repo>.md. Use for /ship, commit-and-push requests, writing or linting commit messages, or SemVer impact of a change.
argument-hint: <repo>
---

# Ship

Ship the repo named in the arguments (a directory under `~`, so `~/<repo>`).

**No argument:** ship the repo Claude/Codex was launched from: run `git rev-parse --show-toplevel` in the current directory, use its basename as `<repo>`, and run all commands there. Stop if the directory isn't a git repo. If `repos/<repo>.md` doesn't exist, invoke the `ship-init` skill first to create it from the repo's actual ways of working, then continue. If it exists, use it.

1. Read repo-specific instructions from `repos/<repo>.md`, relative to this skill's directory, if it exists. Apply them in addition to the general steps below; where they conflict, the repo file wins. If it doesn't exist, continue with the general steps only and mention that at the end.
2. `cd` into the repo (the top-level directory when no argument was given) and run `git status` and `git diff`. If there are no staged or unstaged changes, stop and say so. Do not push.
3. Do any pre-commit work the repo file asks for (README updates, lint, etc.) so it lands in the same commit.
4. Group the changes by concern, one commit per group, before writing any message. Split when files belong to different units of work (a service/stack change vs. DNS/terraform vs. CI config vs. unrelated docs, or a `feat` vs. an unrelated `chore`). Signals: different top-level directories or components, different commit types, changes that could be reverted independently. Keep together files that only make sense together (a feature and its tests/docs, a compose file and its env template). If a single file mixes concerns, split it with `git add -p`. If everything is one concern, make one commit; don't split for its own sake.
5. Stage each group explicitly by path (never `git add -A` when splitting), excluding anything that looks like a secret (`.env`, keys, credentials); flag those instead of staging. Show the planned groups (files and message per commit) in one short list, then commit each in order without waiting unless the grouping is ambiguous.
   Write each message per [Commit messages](#commit-messages) below. Never use a vague message to cover unrelated changes.
6. Push all commits to the current branch (`git push`, or `git push -u origin <branch>` if no upstream). Ask before force-pushing. Never push to a protected default branch if the repo file says to use PRs.
7. If the repo has GitHub Actions workflows (`.github/workflows`), get the latest run with `gh run list --branch $(git branch --show-current) --limit 1`, watch it with `gh run watch <run-id>`, and report the final status. Skip this if there are no workflows or the repo file says to.

## Commit messages

Follows [Conventional Commits v1.0.0](https://www.conventionalcommits.org/en/v1.0.0/). Use this section alone when the user only wants a message written or linted: output fenced code blocks, don't run git.

```
<type>[optional scope][!]: <description>

[optional body]

[optional footer(s)]
```

- **Type**: `feat` (SemVer MINOR), `fix` (PATCH), or `build`, `chore`, `ci`, `docs`, `style`, `refactor`, `perf`, `test`, `revert` (no bump). Pick the one that best fits the diff.
- **Scope**: optional noun in parens for a localized area, e.g. `fix(parser):`. Omit if broad or recurring scopes in `git log` suggest otherwise.
- **Description**: imperative, lowercase after the colon, no period, first line <=72 chars.
- **Body**: always a `- ` bullet list explaining why/specifics, never prose. Skip if the description suffices. One blank line before it.
- **Footers**: git-trailer style (`Refs: #123`, `Closes: #123`, `Reviewed-by: Z`); tokens use `-` for spaces. One blank line before them.
- **Breaking changes** (any type, SemVer MAJOR): `!` before the colon and/or a `BREAKING CHANGE: <what breaks, how to migrate>` footer. That token must be uppercase; everything else is case-insensitive.

```
fix: prevent racing of requests

- introduce a request id and a reference to the latest request
- dismiss incoming responses other than from the latest request

Refs: #123
```

```
feat(api)!: drop support for Node 6

BREAKING CHANGE: use JavaScript features not available in Node 6.
```

**Linting** an existing message: check the prefix is `type(scope)!: ` with a non-empty description, one blank line before body and footers, body is a bullet list, footer tokens are well-formed, and breaking intent appears as `!` and/or `BREAKING CHANGE:`, not just prose.

## Adding a repo

Create `repos/<name>.md` with any extra rules: scopes to use, PR vs. direct push, checks to run first, files never to stage.
