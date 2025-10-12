# PowerShell script to fix common CI failures on Windows
# Usage: .\fix-ci.ps1 [command]
# Commands: fix-eslint-env, sync-frontend-lock, frontend-ci-check, audit-fix, commit, fix-all

param(
    [Parameter(Position=0)]
    [string]$Command = "fix-all"
)

$ErrorActionPreference = "Continue"
$FRONTEND = "frontend"
$CJS_FILES = @(
    "$FRONTEND\.eslintrc.cjs",
    "$FRONTEND\postcss.config.cjs",
    "$FRONTEND\tailwind.config.cjs"
)

function Fix-EslintEnv {
    Write-Host "==> Patching ESLint environment in .cjs files..." -ForegroundColor Cyan
    
    foreach ($file in $CJS_FILES) {
        if (Test-Path $file) {
            $content = Get-Content $file -Raw
            if (-not $content.StartsWith("/* eslint-env node */")) {
                $newContent = "/* eslint-env node */`n" + $content
                Set-Content $file $newContent -NoNewline
                Write-Host "    ✓ Patched: $file" -ForegroundColor Green
            } else {
                Write-Host "    ✓ OK: $file" -ForegroundColor Gray
            }
        } else {
            Write-Host "    ⚠ Missing: $file" -ForegroundColor Yellow
        }
    }
    
    git add $CJS_FILES 2>$null
}

function Sync-FrontendLock {
    Write-Host "`n==> Syncing frontend lockfile..." -ForegroundColor Cyan
    
    Push-Location $FRONTEND
    npm install
    $exitCode = $LASTEXITCODE
    Pop-Location
    
    if ($exitCode -eq 0) {
        Write-Host "    ✓ Lockfile synced successfully" -ForegroundColor Green
        git add "$FRONTEND\package-lock.json"
    } else {
        Write-Host "    ✗ Failed to sync lockfile" -ForegroundColor Red
        return $false
    }
    
    return $true
}

function Test-FrontendCI {
    Write-Host "`n==> Validating CI install (dry-run)..." -ForegroundColor Cyan
    
    Push-Location $FRONTEND
    npm ci --dry-run
    $exitCode = $LASTEXITCODE
    Pop-Location
    
    if ($exitCode -eq 0) {
        Write-Host "    ✓ CI install validation passed" -ForegroundColor Green
        return $true
    } else {
        Write-Host "    ✗ CI install validation failed" -ForegroundColor Red
        return $false
    }
}

function Fix-Audit {
    Write-Host "`n==> Attempting to fix npm audit issues..." -ForegroundColor Cyan
    
    Push-Location $FRONTEND
    npm audit fix
    $exitCode = $LASTEXITCODE
    Pop-Location
    
    if ($exitCode -eq 0) {
        Write-Host "    ✓ Audit fix completed" -ForegroundColor Green
    } else {
        Write-Host "    ⚠ Audit fix completed with warnings (this is expected)" -ForegroundColor Yellow
    }
}

function Commit-Changes {
    Write-Host "`n==> Committing staged changes..." -ForegroundColor Cyan
    
    git status --short
    
    $response = Read-Host "`nCommit these changes? (y/N)"
    if ($response -eq "y" -or $response -eq "Y") {
        git commit -m "chore: fix ESLint Node env, sync frontend lockfile"
        Write-Host "    ✓ Changes committed" -ForegroundColor Green
    } else {
        Write-Host "    ⚠ Commit skipped" -ForegroundColor Yellow
    }
}

function Fix-All {
    Write-Host "========================================" -ForegroundColor Magenta
    Write-Host "  CI Fixes - One-Shot Fixer" -ForegroundColor Magenta
    Write-Host "========================================`n" -ForegroundColor Magenta
    
    Fix-EslintEnv
    
    $lockSuccess = Sync-FrontendLock
    if (-not $lockSuccess) {
        Write-Host "`n✗ Stopping due to lockfile sync failure" -ForegroundColor Red
        return
    }
    
    $ciSuccess = Test-FrontendCI
    if (-not $ciSuccess) {
        Write-Host "`n⚠ CI validation failed, but continuing..." -ForegroundColor Yellow
    }
    
    Fix-Audit
    
    Write-Host "`n========================================" -ForegroundColor Magenta
    Write-Host "  All fixes applied!" -ForegroundColor Magenta
    Write-Host "========================================`n" -ForegroundColor Magenta
    
    Commit-Changes
}

# Main execution
switch ($Command.ToLower()) {
    "fix-eslint-env" {
        Fix-EslintEnv
    }
    "sync-frontend-lock" {
        Sync-FrontendLock
    }
    "frontend-ci-check" {
        Test-FrontendCI
    }
    "audit-fix" {
        Fix-Audit
    }
    "commit" {
        Commit-Changes
    }
    "fix-all" {
        Fix-All
    }
    default {
        Write-Host "Unknown command: $Command" -ForegroundColor Red
        Write-Host "`nAvailable commands:" -ForegroundColor Yellow
        Write-Host "  fix-eslint-env      - Patch Node.js globals in .cjs files"
        Write-Host "  sync-frontend-lock  - Sync package-lock.json"
        Write-Host "  frontend-ci-check   - Validate CI install (dry-run)"
        Write-Host "  audit-fix           - Auto-fix npm audit issues"
        Write-Host "  commit              - Commit staged changes"
        Write-Host "  fix-all             - Run all fixes (default)"
        Write-Host "`nUsage: .\fix-ci.ps1 [command]"
    }
}
