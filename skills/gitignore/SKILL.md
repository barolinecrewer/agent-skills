---
name: gitignore
description: Generate or update .gitignore from detected tooling via the toptal gitignore API, plus macOS, VS Code, env vars, and root temp/. Use for create/update gitignore requests.
---

# gitignore

Generates a `.gitignore` via the gitignore.io API (`https://www.toptal.com/developers/gitignore/api/<list>`).

## Steps

1. Detect tooling by checking for marker files in the project root (and one level down if root is ambiguous):
   - `package.json` → `node` (also check `package.json` deps/devDeps for `react`, `next`, `vue`, `angular` → add those templates)
   - `requirements.txt`, `pyproject.toml`, `Pipfile`, `*.py` → `python`
   - `Cargo.toml` → `rust`
   - `go.mod` → `go`
   - `Gemfile` → `ruby`
   - `pom.xml`, `build.gradle*` → `java` / `gradle` / `maven`
   - `*.xcodeproj`, `*.swift`, `Package.swift` → `swift`, `xcode`
   - `*.csproj`, `*.sln` → `visualstudio`
   - `composer.json` → `php`, `composer`
   - `Dockerfile`, `docker-compose*` → `docker`
   - `terraform` files (`*.tf`) → `terraform`
   Only include templates for tooling actually detected — don't guess.

2. Always include `macos` and `visualstudiocode` in the template list, regardless of detected tooling.

3. Fetch the combined list:
   ```
   curl -s "https://www.toptal.com/developers/gitignore/api/<comma,separated,list>"
   ```
   If a template name is invalid the API returns an error body — drop it and retry rather than writing the error into the file.

4. Prepend (or append, if `.gitignore` already exists and has other content) an env vars and root `temp/` section not covered by the API templates (always include both, and don't duplicate if already present):
   ```
   # Env vars
   .env
   .env.*
   !.env.example

   # Temp files
   /temp/
   ```

5. Write the result to `.gitignore` in the project root. If one already exists, merge: keep any existing custom entries not covered by the generated content, append the new generated block under a `# --- gitignore.io: <list> ---` comment marker so re-runs can find and replace just that block instead of duplicating it.
