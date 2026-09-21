---
name: merge-renovate-prs
description: Merge only low-risk open Renovate PRs (grouped safe updates, GitHub Actions bumps), applying per-repo rules from repos/<repo>.md. Use for /merge-renovate-prs.
argument-hint: <repo>
---

# Merge Renovate PRs

Merge open Renovate PRs in `~/<repo>` (the argument), but only the low-risk ones. Leave everything else untouched.

**No argument:** apply this to the repo Claude/Codex was launched from: run `git rev-parse --show-toplevel` in the current directory, use its basename as `<repo>`, and run all `gh`/`git` commands there. Stop if the directory isn't a git repo.

Read `repos/<repo>.md`, relative to this skill's directory, if it exists. It defines the repo's extra "safe" PR category, merge method, branch handling, and post-merge steps. If it doesn't exist, use only the defaults below and mention that at the end.

## Find candidates

```bash
gh pr list --json number,title,headRefName,isDraft --limit 50
```

For each PR whose `headRefName` starts with `renovate/`, fetch its changed files:

```bash
gh pr view <number> --json files,mergeStateStatus,mergeable
```

Classify each PR:

- **GitHub Actions**: every changed file path is under `.github/workflows/`. Always safe.
- **Repo-defined safe categories**: whatever the repo file lists (e.g. a grouped-updates branch name).
- **Everything else** (majors, infra/terraform, mixed-file PRs, anything you're unsure about): skip. Note the PR number and why.

## Merge

For each PR in an allowed category:

- Skip it and report why if `mergeStateStatus` is `DIRTY`/`CONFLICTING` or `mergeable` is `CONFLICTING`, or if required checks are failing.
- Otherwise merge with the repo's method (default: `gh pr merge <number> --merge`; don't squash or rebase unless the repo file says so).
- Don't pass `--delete-branch` unless the repo file says to.

## After merging

Do whatever the repo file says (e.g. watch a deploy run with `gh run list --branch <branch> --limit 1` then `gh run watch <run-id>`). Skip if it says nothing.

## Report

Summarize which PRs were merged, which were skipped and why, and any post-merge status.

## Adding a repo

Create `repos/<name>.md` with: safe PR categories, merge method, branch-deletion policy, post-merge steps.
