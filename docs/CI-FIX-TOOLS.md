# CI/CD Maintenance Tools

This directory contains tools to help fix common CI/CD pipeline failures.

## Quick Start

### Windows (PowerShell)

```powershell
# Run all fixes at once
.\fix-ci.ps1

# Or run individual fixes
.\fix-ci.ps1 fix-eslint-env
.\fix-ci.ps1 sync-frontend-lock
.\fix-ci.ps1 frontend-ci-check
.\fix-ci.ps1 audit-fix
.\fix-ci.ps1 commit
```

### Linux/macOS/Git Bash

```bash
# Run all fixes at once
make ci-fix-all

# Or run individual fixes
make fix-eslint-env
make sync-frontend-lock
make frontend-ci-check
make audit-fix
```

## What Each Fix Does

### 1. `fix-eslint-env`
**Problem:** ESLint reports `'process' is not defined`, `'require' is not defined` in config files.

**Solution:** Adds `/* eslint-env node */` to the top of `.cjs` config files to tell ESLint these files run in Node.js environment.

**Files affected:**
- `frontend/.eslintrc.cjs`
- `frontend/postcss.config.cjs`
- `frontend/tailwind.config.cjs`

### 2. `sync-frontend-lock`
**Problem:** CI fails with "package-lock.json out of sync" or dependency resolution errors.

**Solution:** Runs `npm install` to regenerate a fresh `package-lock.json` that matches `package.json`.

**Files affected:**
- `frontend/package-lock.json`

### 3. `frontend-ci-check`
**Problem:** Want to verify CI will pass before pushing.

**Solution:** Runs `npm ci --dry-run` to simulate the CI install process locally without modifying files.

**No files modified** - validation only.

### 4. `audit-fix`
**Problem:** npm audit reports vulnerabilities in dependencies.

**Solution:** Runs `npm audit fix` to automatically update packages to non-breaking secure versions.

**Files affected:**
- `frontend/package.json`
- `frontend/package-lock.json`

⚠️ **Note:** Some vulnerabilities may require breaking changes and won't be auto-fixed. Review the output carefully.

## Common CI Failures & Solutions

### ESLint Parsing Errors

**Error:**
```
/frontend/cypress.config.js
  1:26  warning  'require' is not defined  no-undef
  3:1   warning  'module' is not defined   no-undef
```

**Fix:**
```powershell
# Windows
.\fix-ci.ps1 fix-eslint-env

# Linux/Mac
make fix-eslint-env
```

### Lockfile Out of Sync

**Error:**
```
npm ERR! `npm ci` can only install packages when your package.json and package-lock.json are in sync
```

**Fix:**
```powershell
# Windows
.\fix-ci.ps1 sync-frontend-lock

# Linux/Mac
make sync-frontend-lock
```

### TypeScript Parsing Errors

**Error:**
```
Parsing error: Unexpected token {
Parsing error: The keyword 'interface' is reserved
```

**Fix:** This was already fixed by adding `typescript-eslint` to the project. If you still see this, ensure:
1. `typescript-eslint` is in `frontend/package.json` devDependencies
2. `frontend/eslint.config.js` imports and uses TypeScript ESLint parser
3. Run `npm install` in frontend directory

### Docker Compose Command Not Found

**Error:**
```
docker-compose: command not found
```

**Fix:** This was already fixed by updating workflows to use `docker compose` (V2) instead of `docker-compose` (V1).

### Dependency Review Fails

**Error:**
```
Dependency review is not supported on this repository
```

**Fix:** This was already fixed by adding `continue-on-error: true` to the dependency-review job. This is expected on public repositories without GitHub Advanced Security.

## Manual Verification

After running fixes, verify locally:

```bash
# Check what files were changed
git status

# Review the changes
git diff

# Test frontend linting
cd frontend
npm ci
npm run lint

# Test frontend build
npm run build

# Run tests
npm test
```

## Commit & Push

After verifying fixes work:

```bash
git add .
git commit -m "chore: fix CI/CD issues - ESLint env, lockfile sync"
git push origin version2.0
```

## Troubleshooting

### "Cannot be loaded because running scripts is disabled"

**Windows PowerShell execution policy error:**

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### "make: command not found"

**Windows without Git Bash/WSL:** Use the PowerShell script instead:
```powershell
.\fix-ci.ps1
```

### "node: command not found"

**Install Node.js:** Download from https://nodejs.org/

### Script doesn't commit automatically

The PowerShell script asks for confirmation before committing. The Makefile doesn't commit automatically in `ci-fix-all`. To commit:

```bash
git add .
git commit -m "chore: fix CI issues"
```

## Files Overview

- **`fix-ci.ps1`** - PowerShell script for Windows users
- **`Makefile`** - Make targets for Linux/macOS/Git Bash users (at project root)
- **`CI-FIX-TOOLS.md`** - This documentation file

## GitHub Actions Workflow Status

Check your PR at: https://github.com/pichitchaipae/lgbtq-fluidity-analyzer/pull/2/checks

Expected results after fixes:
- ✅ CI / backend - Passing
- ✅ CI / frontend - Passing
- ✅ Docker Build - Passing
- ✅ CodeQL - Passing
- ⚠️ Dependency Review - Warning (non-blocking)
- ⚠️ NPM Security Audit - Warning (non-blocking)
- ⚠️ Docker Image Scan - Warning (may have base image vulnerabilities)
