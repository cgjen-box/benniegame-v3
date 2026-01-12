# =============================================================================
# Maestro Orchestration - Windows Setup Script
# =============================================================================
# Usage: .\scripts\setup-maestro.ps1

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Maestro Orchestration Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RootDir = Split-Path -Parent $ScriptDir

# Step 1: Check Python
Write-Host "[1/5] Checking Python..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "  [OK] $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "  [ERROR] Python not found. Please install Python 3.11+" -ForegroundColor Red
    exit 1
}

# Step 2: Create .env from template
Write-Host "[2/5] Setting up environment..." -ForegroundColor Yellow
$envFile = Join-Path $RootDir ".env"
$envExample = Join-Path $RootDir "config\.env.example"

if (-not (Test-Path $envFile)) {
    if (Test-Path $envExample) {
        Copy-Item $envExample $envFile
        Write-Host "  [OK] Created .env from template" -ForegroundColor Green
        Write-Host "  [!] Edit .env with your API keys" -ForegroundColor Yellow
    } else {
        Write-Host "  [WARN] No .env.example found" -ForegroundColor Yellow
    }
} else {
    Write-Host "  [OK] .env already exists" -ForegroundColor Green
}

# Step 3: Install Python dependencies
Write-Host "[3/5] Installing dependencies..." -ForegroundColor Yellow
$reqFile = Join-Path $RootDir "requirements.txt"
if (Test-Path $reqFile) {
    pip install -r $reqFile --quiet
    Write-Host "  [OK] Dependencies installed" -ForegroundColor Green
} else {
    Write-Host "  [WARN] requirements.txt not found" -ForegroundColor Yellow
}

# Step 4: Check SSH key
Write-Host "[4/5] Checking SSH key..." -ForegroundColor Yellow
$sshKey = "$env:USERPROFILE\.ssh\macincloud_key"
if (Test-Path $sshKey) {
    Write-Host "  [OK] SSH key found at $sshKey" -ForegroundColor Green
} else {
    Write-Host "  [WARN] SSH key not found at $sshKey" -ForegroundColor Yellow
    Write-Host "  Generate with: ssh-keygen -t ed25519 -f $sshKey"
}

# Step 5: Create Claude settings
Write-Host "[5/5] Setting up Claude Code..." -ForegroundColor Yellow
$claudeDir = "$env:USERPROFILE\.claude"
if (-not (Test-Path $claudeDir)) {
    New-Item -ItemType Directory -Path $claudeDir -Force | Out-Null
}

$settingsTemplate = Join-Path $RootDir "config\settings.local.json.template"
$settingsTarget = Join-Path $claudeDir "settings.local.json"

if (Test-Path $settingsTemplate) {
    if (-not (Test-Path $settingsTarget)) {
        Write-Host "  [INFO] Copy and customize settings.local.json.template to:" -ForegroundColor Yellow
        Write-Host "         $settingsTarget"
    } else {
        Write-Host "  [OK] Claude settings already configured" -ForegroundColor Green
    }
}

Write-Host
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Setup Complete!" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host
Write-Host "Next steps:"
Write-Host "  1. Edit .env with your API keys"
Write-Host "  2. Configure settings.local.json with your SSH host"
Write-Host "  3. Test: python scripts\test-mcp-connection.py"
Write-Host
