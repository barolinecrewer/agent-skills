#!/usr/bin/env node

/**
 * Lint skill descriptions to ensure they can be correctly parsed by Codex and other AI CLIs.
 * 
 * This script validates:
 * - SKILL.md files have valid YAML frontmatter
 * - Required fields (name, description) are present
 * - Field types are correct
 * - Skill name matches directory name (warning only)
 */

const fs = require('fs');
const path = require('path');
const yaml = require('js-yaml');

const SKILLS_DIR = path.join(__dirname, '..', 'skills');

// Known frontmatter fields
const KNOWN_FIELDS = ['name', 'description', 'argument-hint', 'version', 'author'];

function lintSkill(dirName) {
  const skillPath = path.join(SKILLS_DIR, dirName, 'SKILL.md');
  const errors = [];
  const warnings = [];

  // Check if SKILL.md exists
  if (!fs.existsSync(skillPath)) {
    warnings.push(`Missing SKILL.md in ${dirName}`);
    return { errors, warnings };
  }

  const content = fs.readFileSync(skillPath, 'utf8');

  // Check for frontmatter delimiters
  const frontmatterMatch = content.match(/^---\n(.*?)\n---/s);
  if (!frontmatterMatch) {
    errors.push(`${dirName}/SKILL.md: Missing YAML frontmatter (--- delimiters)`);
    return { errors, warnings };
  }

  let frontmatter;
  try {
    frontmatter = yaml.load(frontmatterMatch[1]);
  } catch (e) {
    errors.push(`${dirName}/SKILL.md: Invalid YAML frontmatter - ${e.message}`);
    return { errors, warnings };
  }

  if (!frontmatter || Object.keys(frontmatter).length === 0) {
    errors.push(`${dirName}/SKILL.md: Empty frontmatter`);
    return { errors, warnings };
  }

  // Check required fields
  if (!frontmatter.name) {
    errors.push(`${dirName}/SKILL.md: Missing required field 'name'`);
  } else if (typeof frontmatter.name !== 'string') {
    errors.push(`${dirName}/SKILL.md: 'name' must be a string, got ${typeof frontmatter.name}`);
  } else if (frontmatter.name.trim().length === 0) {
    errors.push(`${dirName}/SKILL.md: 'name' cannot be empty`);
  } else if (frontmatter.name !== dirName) {
    warnings.push(`${dirName}/SKILL.md: Skill name '${frontmatter.name}' does not match directory name '${dirName}'`);
  }

  if (!frontmatter.description) {
    errors.push(`${dirName}/SKILL.md: Missing required field 'description'`);
  } else if (typeof frontmatter.description !== 'string') {
    errors.push(`${dirName}/SKILL.md: 'description' must be a string, got ${typeof frontmatter.description}`);
  } else if (frontmatter.description.trim().length === 0) {
    errors.push(`${dirName}/SKILL.md: 'description' cannot be empty`);
  }

  // Check optional fields
  if (frontmatter['argument-hint'] !== undefined) {
    // argument-hint can be a string or an array (if unquoted brackets are used in YAML)
    if (typeof frontmatter['argument-hint'] === 'string') {
      if (frontmatter['argument-hint'].trim().length === 0) {
        errors.push(`${dirName}/SKILL.md: 'argument-hint' cannot be empty`);
      }
    } else if (Array.isArray(frontmatter['argument-hint'])) {
      // If it's an array, it was likely unquoted in YAML like: argument-hint: [repo]
      // Convert back to string representation
      const asString = frontmatter['argument-hint'].join(' ');
      if (asString.trim().length === 0) {
        errors.push(`${dirName}/SKILL.md: 'argument-hint' cannot be empty`);
      }
    } else {
      errors.push(`${dirName}/SKILL.md: 'argument-hint' must be a string or array, got ${typeof frontmatter['argument-hint']}`);
    }
  }

  // Check for unknown fields
  const extraFields = Object.keys(frontmatter).filter(k => !KNOWN_FIELDS.includes(k));
  if (extraFields.length > 0) {
    warnings.push(`${dirName}/SKILL.md: Unknown frontmatter fields: ${extraFields.join(', ')}`);
  }

  return { errors, warnings };
}

function main() {
  // Get all skill directories
  let skillDirs;
  try {
    skillDirs = fs.readdirSync(SKILLS_DIR).filter(d => {
      const stat = fs.statSync(path.join(SKILLS_DIR, d));
      return stat.isDirectory();
    });
  } catch (e) {
    console.error(`Error reading skills directory: ${e.message}`);
    process.exit(1);
  }

  if (skillDirs.length === 0) {
    console.warn('⚠️  No skill directories found');
    process.exit(0);
  }

  console.log(`Linting ${skillDirs.length} skill(s)...\n`);

  let allErrors = [];
  let allWarnings = [];

  for (const dir of skillDirs) {
    const { errors, warnings } = lintSkill(dir);
    allErrors = allErrors.concat(errors);
    allWarnings = allWarnings.concat(warnings);
  }

  // Output warnings
  if (allWarnings.length > 0) {
    console.warn('⚠️  WARNINGS:');
    allWarnings.forEach(w => console.warn('  -', w));
    console.log();
  }

  // Output errors
  if (allErrors.length > 0) {
    console.error('❌ LINT ERRORS:');
    allErrors.forEach(e => console.error('  -', e));
    console.error(`\nFound ${allErrors.length} error(s) in ${skillDirs.length} skill(s)`);
    process.exit(1);
  }

  console.log('✅ All skill descriptions are valid');
  console.log(`Checked ${skillDirs.length} skill(s)`);
  process.exit(0);
}

main();
