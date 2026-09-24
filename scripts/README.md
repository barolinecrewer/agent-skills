# Lint Scripts

This directory contains scripts for validating and linting skill definitions in the agent-skills repository.

## lint-skills.js

A Node.js script that validates SKILL.md files to ensure they can be correctly parsed by Codex, Claude Code, and other AI CLIs.

### What it checks

- **Required fields**: Each SKILL.md must have:
  - `name` - The skill name (string, must match directory name)
  - `description` - The skill description (non-empty string)

- **Optional fields**:
  - `argument-hint` - Usage hint for the skill argument (string or array)

- **YAML validity**: The frontmatter must be valid YAML

- **Frontmatter structure**: Must have `---` delimiters

### Usage

```bash
# Run from repository root
node scripts/lint-skills.js
```

### Exit codes

- `0` - All skills are valid
- `1` - Lint errors found (fails CI)

### Warnings vs Errors

- **Errors** cause the script to exit with code 1 and fail CI:
  - Missing required fields
  - Invalid YAML
  - Empty required fields
  - Wrong field types

- **Warnings** are logged but don't fail CI:
  - Skill name doesn't match directory name
  - Unknown frontmatter fields

### GitHub Action

This script is automatically run on:
- Pushes to main branch that modify SKILL.md files
- Pull requests targeting main branch that modify SKILL.md files

The workflow file is at `.github/workflows/lint-skill-descriptions.yml`

### Adding new skills

When creating a new skill in the `skills/` directory:

1. Create a directory named after your skill (lowercase, hyphenated)
2. Add a `SKILL.md` file with valid YAML frontmatter:

```yaml
---
name: my-skill
description: A brief description of what this skill does.
---

# My Skill

Detailed documentation...
```

3. Run `node scripts/lint-skills.js` to verify

### Known fields

The linter recognizes these frontmatter fields:
- `name` (required)
- `description` (required)
- `argument-hint` (optional)
- `version` (optional)
- `author` (optional)

Any other fields will generate a warning.
