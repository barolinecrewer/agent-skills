# infra

Path: `~/infra`.

## Safe categories

- **Safe docker updates**: `headRefName` is exactly `renovate/safe-docker-updates` (the grouped PR from the `safe docker updates` packageRule in `renovate.json`).
- Skip `renovate/major-docker-updates`, terraform/tofu bumps, and mixed-file PRs.

## Merge

- Merge commit (`gh pr merge <number> --merge`) to match this repo's history. Don't squash or rebase.
- Don't pass `--delete-branch`; stale renovate branches are left in place by convention.

## After merging

If any merged PR touched `stacks/**` (i.e. the safe docker updates PR), the push to `main` kicks off `deploy-docker-stacks.yml`. Find it with `gh run list --branch main --limit 1`, watch it with `gh run watch <run-id>`, and report the final status.
