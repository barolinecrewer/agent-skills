---
name: conventional-commits
description: Guides writing git commit messages that follow the Conventional Commits v1.0.0 specification. Use this whenever the user asks to "write a commit message", "make a conventional commit", "generate a commit message", produce a changelog-friendly commit message, or review/lint an existing commit message for spec compliance. Also use when the user asks about semantic versioning implications of a change (feat/fix/BREAKING CHANGE → MINOR/PATCH/MAJOR). This skill generates commit message text only — it does not stage files or run `git commit`; do not use it for requests to actually apply/execute a commit.
---

# Conventional Commits

Reference for producing git commit messages that comply with the [Conventional Commits v1.0.0](https://www.conventionalcommits.org/en/v1.0.0/) specification.

**Scope: message generation only.** This skill produces commit message text — it does not stage files or run `git commit`, regardless of phrasing. If the user asks to actually apply/execute a commit, that's outside this skill; only fall back to running `git commit` if they explicitly and separately ask you to. Present the result(s) as fenced code block(s) so they're easy to copy (e.g. into `git commit -F -`).

## Message structure

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

## Core rules (normative)

1. The commit MUST be prefixed with a **type** — a noun (`feat`, `fix`, etc.) — followed by an OPTIONAL scope, an OPTIONAL `!`, and a REQUIRED `: ` (colon + space).
2. Use `feat` when the commit adds a new feature (correlates with SemVer **MINOR**).
3. Use `fix` when the commit patches a bug (correlates with SemVer **PATCH**).
4. A **scope** MAY follow the type: a noun describing a section of the codebase in parentheses, e.g. `fix(parser):`.
5. The **description** immediately follows `: ` — a short summary in the imperative mood, e.g. `fix: array parsing issue when multiple spaces were contained in string`.
6. An OPTIONAL longer **body** MAY follow, starting one blank line after the description. **Always write the body as a bulleted list of items (one change/point per line, `- ` prefix) rather than a prose paragraph** — even if there's only one point to make.
7. OPTIONAL **footers** MAY follow, one blank line after the body. Each footer is a token, then either `: ` or ` #`, then a value (git trailer style), e.g. `Reviewed-by: Z` or `Refs: #123`.
8. A footer token MUST use `-` instead of spaces (e.g. `Acked-by`) — except `BREAKING CHANGE`, which is the one token allowed to contain a space.
9. **Breaking changes** MUST be flagged one of two ways (or both):
   - Append `!` right before the `:` in the type/scope prefix, e.g. `feat(api)!: send an email when a product is shipped`. When `!` is used, the footer `BREAKING CHANGE:` MAY be omitted — the description itself is treated as describing the breaking change.
   - Add a footer: `BREAKING CHANGE: <description>` (uppercase, exact token — `BREAKING-CHANGE` is a synonymous token).
   - A BREAKING CHANGE can accompany *any* type, not just `feat`/`fix`. It correlates with SemVer **MAJOR**.
10. Types other than `feat`/`fix` are allowed and have no implicit SemVer effect (unless they carry a BREAKING CHANGE). Commonly used (from the Angular convention, widely adopted though not part of the core spec): `build`, `chore`, `ci`, `docs`, `style`, `refactor`, `perf`, `test`.
11. Everything is case-insensitive EXCEPT the literal footer token `BREAKING CHANGE` (or `BREAKING-CHANGE`), which MUST be uppercase.
12. **A staged diff almost always contains more than one logical change.** Never assume a single commit message covers everything staged. Before writing anything, group the changes by concern/type, and produce one commit message per group — treat this as the default expectation, not an edge case. Only skip splitting if, after reviewing the diff, every change genuinely belongs to one type/scope and one concern.

## Workflow for generating commit message(s)

### Step 1 — Determine what's actually staged, deterministically

1. Run `git status --short` to get an overview of staged, unstaged, and untracked files.
2. Run `git diff --staged` — this is the primary source of truth. Only staged content will actually be committed, so never infer messages from unstaged changes or from the user's description alone.
3. If `git diff --staged` is empty:
   - If there are unstaged or untracked changes, tell the user nothing is currently staged and ask whether to stage everything (or specific files) before proceeding. Do NOT silently describe unstaged changes as if they were staged.
   - If there's nothing to commit at all, say so and stop.
4. For large or unclear diffs, run `git diff --staged --stat` first to get a change overview before reading the full file-level diffs.

### Step 2 — Review and group the changes (do this before drafting any message)

Read through the staged diff file by file and cluster changes into groups by concern — e.g. by type (feat/fix/docs/refactor/...), by module/scope, or by unrelated purpose even within the same type. Per rule #12, expect multiple groups by default; a single-group result should be the exception, not the assumption.

For each group, note: the files involved, the type it maps to, whether it has its own scope, and whether it introduces a breaking change. This grouping is the deliverable of this step — do it explicitly (e.g. as a short list) before writing any message text, so the split is visible and the user can correct it before you draft messages.

### Step 3 — Run the message-drafting steps below for every group

For **each** group identified in Step 2, independently:

1. **Determine the type** from what that group's diff actually does (new capability → `feat`; bug fix → `fix`; otherwise pick the closest of `build`/`chore`/`ci`/`docs`/`style`/`refactor`/`perf`/`test`).
2. **Determine the scope**, if the group's changes are clearly localized to one module/package/area — omit it if broad or cross-cutting.
3. **Check for breaking changes** within that group: does it remove/rename a public API, change a default, alter a config format, etc.? If so, use `!` and/or a `BREAKING CHANGE:` footer describing what breaks and (if helpful) how to migrate.
4. **Write the description**: imperative mood ("add", not "added"/"adds"), lowercase after the colon, no trailing period, concise (aim to keep the whole first line under ~72 chars).
5. **Write the body as a bullet list** whenever the "why" or specifics aren't obvious from the description alone — one point per bullet, never a prose paragraph. Skip the body only if the description alone is fully sufficient.
6. **Add footers** as needed: `BREAKING CHANGE:`, issue references (`Refs: #123`, `Closes: #123`), `Reviewed-by:`, `Co-authored-by:`, etc.

### Step 4 — Output

Present one fenced code block per group, in the order the groups were identified, each labeled with the files it covers (since they'll need to be staged/committed separately). Do not run `git commit` — see "Scope" above.

## Examples

Simple fix:
```
fix: prevent racing of requests

- introduce a request id and a reference to the latest request
- dismiss incoming responses other than from the latest request

Reviewed-by: Z
Refs: #123
```

New feature with scope:
```
feat(lang): add Polish language
```

Breaking change via `!` only:
```
feat!: send an email to the customer when a product is shipped
```

Breaking change via `!` + scope:
```
feat(api)!: send an email to the customer when a product is shipped
```

Breaking change via footer:
```
feat: allow provided config object to extend other configs

- `extends` key in config file is now used for extending other config files

BREAKING CHANGE: `extends` key in config file is now used for extending other config files
```

Both `!` and footer together:
```
feat!: drop support for Node 6

BREAKING CHANGE: use JavaScript features not available in Node 6.
```

Docs-only, no body:
```
docs: correct spelling of CHANGELOG
```

Revert:
```
revert: let us never again speak of the noodle incident

Refs: 676104e, a215868
```

## SemVer mapping (for reasoning about release impact)

| Commit contains | SemVer bump |
|---|---|
| `fix` type | PATCH |
| `feat` type | MINOR |
| `BREAKING CHANGE` (footer or `!`), any type | MAJOR |
| any other type, no breaking change | no implicit bump |

## Linting an existing message

When asked to check/lint a commit message against the spec, verify:
- [ ] Starts with `type` (+ optional `(scope)`) (+ optional `!`) followed by `: ` (colon+space)
- [ ] Description present immediately after, non-empty
- [ ] If a body exists, exactly one blank line separates it from the description, and it's formatted as a bullet list rather than a paragraph
- [ ] If footers exist, exactly one blank line separates them from the body, and each uses `Token: value` or `Token #value` with `-` in place of spaces in the token (except `BREAKING CHANGE`)
- [ ] `BREAKING CHANGE` token is uppercase if present
- [ ] Breaking-change intent is reflected as `!` and/or a `BREAKING CHANGE:` footer, not just prose in the body
