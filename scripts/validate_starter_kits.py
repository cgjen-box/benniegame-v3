#!/usr/bin/env python3
"""
Validate all starter kits are properly configured and working.

Usage:
    python scripts/validate_starter_kits.py
"""

import os
import sys
import subprocess
import json
from pathlib import Path

# Colors for output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
RESET = '\033[0m'

def check_mark(success: bool) -> str:
    return f"{GREEN}[OK]{RESET}" if success else f"{RED}[FAIL]{RESET}"

def warning_mark() -> str:
    return f"{YELLOW}[WARN]{RESET}"

def run_command(cmd: list, cwd: str = None) -> tuple[bool, str]:
    """Run a command and return (success, output)."""
    try:
        result = subprocess.run(
            cmd,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=30
        )
        return result.returncode == 0, result.stdout + result.stderr
    except Exception as e:
        return False, str(e)

def validate_env_file(project_root: Path) -> dict:
    """Check .env file for required keys."""
    env_path = project_root / '.env'
    results = {
        'exists': env_path.exists(),
        'keys': {}
    }

    required_keys = ['GOOGLE_API_KEY']
    optional_keys = ['ELEVENLABS_API_KEY', 'ANTHROPIC_API_KEY', 'REPLICATE_API_TOKEN']

    if env_path.exists():
        content = env_path.read_text()
        for key in required_keys:
            results['keys'][key] = key in content and f'{key}=' in content
        for key in optional_keys:
            results['keys'][key] = key in content and f'{key}=' in content

    return results

def validate_venv(project_root: Path) -> dict:
    """Check virtual environment exists and has required packages."""
    venv_path = project_root / '.venv'
    python_path = venv_path / 'bin' / 'python3'

    results = {
        'exists': venv_path.exists(),
        'python_works': False,
        'packages': {}
    }

    if python_path.exists():
        success, _ = run_command([str(python_path), '--version'])
        results['python_works'] = success

        # Check key packages
        packages = ['google.genai', 'PIL', 'mcp', 'requests', 'dotenv']
        for pkg in packages:
            success, _ = run_command([str(python_path), '-c', f'import {pkg}'])
            results['packages'][pkg] = success

    return results

def validate_starter_kit(project_root: Path, kit_name: str, main_script: str) -> dict:
    """Validate a starter kit can run its --help command."""
    kit_path = project_root / 'starter-kits' / kit_name
    script_path = kit_path / main_script
    python_path = project_root / '.venv' / 'bin' / 'python3'

    results = {
        'path_exists': kit_path.exists(),
        'script_exists': script_path.exists(),
        'help_works': False,
        'error': None
    }

    if script_path.exists() and python_path.exists():
        success, output = run_command([str(python_path), str(script_path), '--help'], cwd=str(kit_path))
        results['help_works'] = success
        if not success:
            results['error'] = output[:200]

    return results

def validate_git_hooks(project_root: Path) -> dict:
    """Check git hooks are installed."""
    hooks_path = project_root / '.git' / 'hooks'

    return {
        'pre-commit': (hooks_path / 'pre-commit').exists(),
        'pre-push': (hooks_path / 'pre-push').exists()
    }

def validate_skills(project_root: Path) -> dict:
    """Check skill files exist and have proper YAML frontmatter."""
    skills_path = project_root / '.claude' / 'skills'

    expected_skills = ['ios-dev', 'image-gen', 'animation', 'video-gen', 'security', 'gsd']
    results = {}

    for skill in expected_skills:
        skill_file = skills_path / skill / 'SKILL.md'
        if skill_file.exists():
            content = skill_file.read_text()
            # Check for YAML frontmatter (starts with --- and has name: and description:)
            has_frontmatter = (
                content.startswith('---') and
                'name:' in content[:500] and
                'description:' in content[:500]
            )
            results[skill] = has_frontmatter
        else:
            results[skill] = False

    return results

def validate_mcp_config() -> dict:
    """Check MCP configuration."""
    config_path = Path.home() / '.claude' / 'settings.local.json'

    results = {
        'exists': config_path.exists(),
        'ios_simulator': False,
        'image_generator': False,
        'points_to_local': False
    }

    if config_path.exists():
        try:
            config = json.loads(config_path.read_text())
            servers = config.get('mcpServers', {})
            results['ios_simulator'] = 'ios-simulator' in servers
            results['image_generator'] = 'image-generator' in servers
            if results['ios_simulator']:
                args = servers['ios-simulator'].get('args', [])
                results['points_to_local'] = any('BennieGame-v3' in str(a) for a in args)
        except:
            pass

    return results

def main():
    project_root = Path(__file__).parent.parent
    all_passed = True

    print("\n" + "="*60)
    print(" STARTER KITS VALIDATION")
    print("="*60 + "\n")

    # 1. Virtual Environment
    print("1. Virtual Environment")
    venv = validate_venv(project_root)
    print(f"   {check_mark(venv['exists'])} .venv exists")
    print(f"   {check_mark(venv['python_works'])} Python works")
    for pkg, ok in venv.get('packages', {}).items():
        print(f"   {check_mark(ok)} Package: {pkg}")
    all_passed = all_passed and venv['exists'] and venv['python_works']

    # 2. Environment File
    print("\n2. Environment File")
    env = validate_env_file(project_root)
    print(f"   {check_mark(env['exists'])} .env exists")
    for key, ok in env.get('keys', {}).items():
        mark = check_mark(ok) if 'GOOGLE' in key else (check_mark(ok) if ok else warning_mark())
        print(f"   {mark} {key}")
    all_passed = all_passed and env['exists']

    # 3. Git Hooks
    print("\n3. Git Hooks")
    hooks = validate_git_hooks(project_root)
    for hook, ok in hooks.items():
        print(f"   {check_mark(ok)} {hook}")
        all_passed = all_passed and ok

    # 4. MCP Configuration
    print("\n4. MCP Configuration")
    mcp = validate_mcp_config()
    print(f"   {check_mark(mcp['exists'])} settings.local.json exists")
    print(f"   {check_mark(mcp['ios_simulator'])} ios-simulator configured")
    print(f"   {check_mark(mcp['image_generator'])} image-generator configured")
    print(f"   {check_mark(mcp['points_to_local'])} Points to local starter-kits")
    all_passed = all_passed and mcp['exists'] and mcp['ios_simulator'] and mcp['image_generator']

    # 5. Starter Kits
    print("\n5. Starter Kits")
    kits = [
        ('gemini-image-pro-3', 'generate_image.py'),
        ('veo-video-generation', 'generate_video.py'),
        ('ludo-animation-pipeline', 'process.py'),
        ('lottie-animation-system', 'create_lottie.py'),
        ('maestro-orchestration/mcp-servers', 'ios_simulator_mcp.py'),
    ]

    for kit_name, script in kits:
        kit = validate_starter_kit(project_root, kit_name, script)
        status = check_mark(kit['help_works'])
        print(f"   {status} {kit_name}")
        if kit['error']:
            print(f"       Error: {kit['error'][:100]}...")
        all_passed = all_passed and kit['help_works']

    # 6. Skills
    print("\n6. Skills")
    skills = validate_skills(project_root)
    for skill, ok in skills.items():
        print(f"   {check_mark(ok)} {skill}")
        all_passed = all_passed and ok

    # Summary
    print("\n" + "="*60)
    if all_passed:
        print(f" {GREEN}ALL VALIDATIONS PASSED{RESET}")
    else:
        print(f" {RED}SOME VALIDATIONS FAILED{RESET}")
    print("="*60 + "\n")

    return 0 if all_passed else 1

if __name__ == '__main__':
    sys.exit(main())
