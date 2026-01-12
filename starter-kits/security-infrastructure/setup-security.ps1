# Security Setup Script for Windows PowerShell
# Usage: .\setup-security.ps1

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "  SecretGuard Security Setup" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host

# Check if we're in a git repository
if (-not (Test-Path ".git")) {
    Write-Host "ERROR: Not in a git repository." -ForegroundColor Red
    Write-Host "Please run this script from your project root."
    exit 1
}

# Create hooks directory if needed
if (-not (Test-Path ".git\hooks")) {
    New-Item -ItemType Directory -Path ".git\hooks" | Out-Null
}

# Install pre-commit hook
Write-Host "Installing pre-commit hook..."
if (Test-Path "hooks\pre-commit") {
    Copy-Item "hooks\pre-commit" ".git\hooks\pre-commit" -Force
    Write-Host "  [OK] Pre-commit hook installed" -ForegroundColor Green
} else {
    Write-Host "  [X] hooks\pre-commit not found" -ForegroundColor Yellow
}

# Install pre-push hook
Write-Host "Installing pre-push hook..."
if (Test-Path "hooks\pre-push") {
    Copy-Item "hooks\pre-push" ".git\hooks\pre-push" -Force
    Write-Host "  [OK] Pre-push hook installed" -ForegroundColor Green
} else {
    Write-Host "  [X] hooks\pre-push not found" -ForegroundColor Yellow
}

# Check for gitleaks
Write-Host
Write-Host "Checking for gitleaks..."
try {
    $gitleaks = Get-Command gitleaks -ErrorAction Stop
    Write-Host "  [OK] gitleaks is installed" -ForegroundColor Green
} catch {
    Write-Host "  [X] gitleaks not found" -ForegroundColor Yellow
    Write-Host "    Install with: winget install gitleaks"
    Write-Host "    Or: https://github.com/gitleaks/gitleaks"
}

# Create .env from example if needed
Write-Host
Write-Host "Checking environment file..."
if (-not (Test-Path ".env") -and (Test-Path "config\.env.example")) {
    Copy-Item "config\.env.example" ".env"
    Write-Host "  [OK] Created .env from template" -ForegroundColor Green
    Write-Host "  [!] Remember to fill in your actual values" -ForegroundColor Yellow
} elseif (Test-Path ".env") {
    Write-Host "  [OK] .env already exists" -ForegroundColor Green
} else {
    Write-Host "  [X] No .env.example template found" -ForegroundColor Yellow
}

# Run initial scan
Write-Host
Write-Host "Running initial security scan..."
if (Test-Path "scripts\check_secrets.py") {
    python scripts\check_secrets.py
} else {
    Write-Host "  [X] check_secrets.py not found" -ForegroundColor Yellow
}

Write-Host
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "  Setup Complete!" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host
Write-Host "Next steps:"
Write-Host "  1. Edit .env with your actual API keys"
Write-Host "  2. Never commit .env to version control"
Write-Host "  3. Use SecretGuard.get() in your code"
Write-Host
