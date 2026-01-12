#!/usr/bin/env python3
"""
iOS Simulator MCP Server for Bennie Bear Development
====================================================
Exposes iPad Simulator control to Claude Code via MCP protocol.
Enables recursive build-test-fix loops with full UI interaction.

Usage:
    # Stdio transport (for Claude Desktop via SSH)
    python ios_simulator_mcp.py

    # SSE transport (for web clients via SSH tunnel)
    python ios_simulator_mcp.py --transport sse --port 8765

    # Test mode (verify all tools work)
    python ios_simulator_mcp.py --test

Configuration (Claude Desktop via SSH):
    {
        "mcpServers": {
            "ios-simulator": {
                "command": "ssh",
                "args": [
                    "-i", "~/.ssh/macincloud_key",
                    "user289321@FF775.macincloud.com",
                    "cd ~/BennieGame && python3 'designer system/ios_simulator_mcp.py'"
                ]
            }
        }
    }

Requirements:
    - macOS with Xcode installed
    - iPad Simulator available
    - Python 3.9+ with mcp package
"""

import os
import sys
import json
import asyncio
import base64
import subprocess
import tempfile
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Dict, Any
from concurrent.futures import ThreadPoolExecutor

# Check for MCP package
try:
    from mcp.server.fastmcp import FastMCP
except ImportError:
    print("[ERROR] MCP package not found. Install with: pip install mcp", file=sys.stderr)
    print("[INFO] Or run: pip install fastmcp", file=sys.stderr)
    sys.exit(1)

# Import shared image compression utilities
try:
    from mcp_image_utils import compress_image_for_mcp
except ImportError:
    # Fallback if not available (shouldn't happen)
    compress_image_for_mcp = None

# Import resilience framework
try:
    from mcp_resilience import resilient_tool, handle_large_image, ResilienceConfig
except ImportError:
    # Fallback: create dummy decorator
    def resilient_tool(**kwargs):
        def decorator(func):
            return func
        return decorator
    handle_large_image = None
    ResilienceConfig = None

# =============================================================================
# CONFIGURATION
# =============================================================================

class Config:
    """iOS Simulator MCP configuration."""

    # Server settings
    server_name = "ios-simulator"
    transport = os.environ.get("MCP_TRANSPORT", "stdio")
    sse_port = int(os.environ.get("MCP_PORT", "8765"))

    # Project settings - detect Mac local vs SSH
    # On Mac: ~/app, via SSH from Windows: ~/BennieGame
    _default_path = Path.home() / "app" if (Path.home() / "app" / "BennieGame.xcodeproj").exists() else Path.home() / "BennieGame"
    project_path = _default_path
    scheme_name = "BennieGame"
    app_bundle_id = "com.bennie.BennieGame"

    # Regression testing paths
    baselines_path = Path.home() / "baselines"
    regression_path = Path.home() / "regression"

    # Simulator settings
    simulator_name = "iPad (10th generation)"
    simulator_runtime = "iOS 18.0"

    # iPad 10th gen screen dimensions (landscape)
    screen_width = 1194
    screen_height = 834

    # Timeouts (seconds)
    build_timeout = 300  # 5 minutes
    test_timeout = 600   # 10 minutes
    command_timeout = 30

    @classmethod
    def load_from_env(cls):
        """Load configuration from environment variables."""
        if os.environ.get("BENNIE_PROJECT_PATH"):
            cls.project_path = Path(os.environ["BENNIE_PROJECT_PATH"])
        if os.environ.get("BENNIE_SIMULATOR"):
            cls.simulator_name = os.environ["BENNIE_SIMULATOR"]
        if os.environ.get("BENNIE_BUNDLE_ID"):
            cls.app_bundle_id = os.environ["BENNIE_BUNDLE_ID"]


# Load config
Config.load_from_env()

# =============================================================================
# LOGGING
# =============================================================================

def log(message: str):
    """Log message to stderr (stdout reserved for MCP protocol)."""
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {message}", file=sys.stderr)

# =============================================================================
# MCP SERVER INITIALIZATION
# =============================================================================

mcp = FastMCP(Config.server_name)

# Thread pool for blocking subprocess operations
executor = ThreadPoolExecutor(max_workers=2)

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def run_command(cmd: str, timeout: int = None, cwd: Path = None) -> Dict[str, Any]:
    """
    Execute a shell command and return the result.

    Args:
        cmd: Shell command to execute
        timeout: Timeout in seconds (default: Config.command_timeout)
        cwd: Working directory (default: Config.project_path)

    Returns:
        Dict with success, stdout, stderr, return_code
    """
    timeout = timeout or Config.command_timeout
    cwd = cwd or Config.project_path

    # Environment variables to suppress all credential/keychain prompts
    env = os.environ.copy()
    env.update({
        "GIT_TERMINAL_PROMPT": "0",          # No git credential prompts
        "GIT_ASKPASS": "",                    # No git GUI credential helpers
        "SSH_ASKPASS": "",                    # No SSH password prompts
        "SUDO_ASKPASS": "",                   # No sudo GUI prompts
        "CI": "1",                            # Many tools detect CI and skip prompts
    })

    try:
        result = subprocess.run(
            cmd,
            shell=True,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=timeout,
            env=env
        )
        return {
            "success": result.returncode == 0,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "return_code": result.returncode
        }
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "error": f"Command timed out after {timeout} seconds",
            "stdout": "",
            "stderr": ""
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "stdout": "",
            "stderr": ""
        }


def get_derived_data_app_path() -> Optional[Path]:
    """Find the built app in DerivedData."""
    derived_data = Path.home() / "Library/Developer/Xcode/DerivedData"

    # Find BennieGame-* directory
    for d in derived_data.glob("BennieGame-*"):
        app_path = d / "Build/Products/Debug-iphonesimulator/BennieGame.app"
        if app_path.exists():
            return app_path

    return None

# =============================================================================
# BUILD & DEPLOY TOOLS
# =============================================================================

@mcp.tool()
@resilient_tool(max_response_bytes=300_000, save_large_to_file=True)
async def build_and_deploy(
    pull_latest: bool = False,
    clean_build: bool = False
) -> dict:
    """
    Build the BennieGame app and deploy to iPad Simulator.

    This is the main build command. It will:
    1. Optionally git pull latest changes
    2. Build the Xcode project (code signing disabled for simulator)
    3. Install to the booted simulator

    Args:
        pull_latest: Git pull before building (default False to avoid credential prompts)
        clean_build: Clean build folder before building (default False)

    Returns:
        Build result with success status, output, and any errors

    Note:
        Code signing is disabled for simulator builds to avoid Keychain prompts.
        Git pull is disabled by default to avoid credential prompts.
    """
    loop = asyncio.get_event_loop()

    steps = []

    # Step 1: Git pull (with credential prompt suppression)
    if pull_latest:
        log("Git pulling latest changes...")
        # GIT_TERMINAL_PROMPT=0 prevents git from prompting for credentials
        # GIT_ASKPASS= prevents git from using GUI credential helpers
        result = await loop.run_in_executor(
            executor,
            lambda: run_command(
                "GIT_TERMINAL_PROMPT=0 GIT_ASKPASS= git pull",
                timeout=60
            )
        )
        steps.append({"step": "git_pull", **result})
        if not result["success"]:
            return {
                "success": False,
                "error": "Git pull failed",
                "steps": steps
            }

    # Step 2: Clean if requested
    if clean_build:
        log("Cleaning build folder...")
        result = await loop.run_in_executor(
            executor,
            lambda: run_command(
                f'xcodebuild -scheme {Config.scheme_name} clean',
                timeout=60
            )
        )
        steps.append({"step": "clean", **result})

    # Step 3: Build (with keychain/signing workarounds)
    log("Building Xcode project...")
    # Disable code signing for simulator (not needed, avoids keychain prompts)
    # Use GIT_TERMINAL_PROMPT=0 to prevent git credential popups
    build_cmd = (
        f'xcodebuild -scheme {Config.scheme_name} '
        f'-destination "platform=iOS Simulator,name={Config.simulator_name}" '
        f'CODE_SIGNING_ALLOWED=NO '
        f'CODE_SIGNING_REQUIRED=NO '
        f'CODE_SIGN_IDENTITY="" '
        f'build 2>&1'
    )

    result = await loop.run_in_executor(
        executor,
        lambda: run_command(build_cmd, timeout=Config.build_timeout)
    )

    # Parse build result
    build_succeeded = "BUILD SUCCEEDED" in result.get("stdout", "")
    build_failed = "BUILD FAILED" in result.get("stdout", "")

    # Extract errors and warnings
    output_lines = result.get("stdout", "").split("\n")
    errors = [l for l in output_lines if "error:" in l.lower()]
    warnings = [l for l in output_lines if "warning:" in l.lower()]

    steps.append({
        "step": "build",
        "success": build_succeeded,
        "errors": errors[:10],  # Limit to first 10
        "warnings": warnings[:10],
        "output_tail": "\n".join(output_lines[-20:])  # Last 20 lines
    })

    if not build_succeeded:
        return {
            "success": False,
            "error": "Build failed" if build_failed else "Build did not succeed",
            "errors": errors[:10],
            "steps": steps
        }

    # Step 4: Install to simulator
    log("Installing to simulator...")
    app_path = get_derived_data_app_path()

    if not app_path:
        return {
            "success": False,
            "error": "Could not find built app in DerivedData",
            "steps": steps
        }

    install_cmd = f'xcrun simctl install booted "{app_path}"'
    result = await loop.run_in_executor(
        executor,
        lambda: run_command(install_cmd, timeout=30)
    )
    steps.append({"step": "install", **result})

    if not result["success"]:
        return {
            "success": False,
            "error": "Install to simulator failed",
            "steps": steps
        }

    return {
        "success": True,
        "message": "Build and deploy successful",
        "app_path": str(app_path),
        "warnings_count": len(warnings),
        "steps": steps
    }


@mcp.tool()
@resilient_tool(max_response_bytes=100_000, save_large_to_file=True)
async def launch_app(
    wait_seconds: int = 2
) -> dict:
    """
    Launch BennieGame in the iPad Simulator.

    Args:
        wait_seconds: Seconds to wait after launch for app to initialize (default 2)

    Returns:
        Launch result with success status
    """
    loop = asyncio.get_event_loop()

    # Launch app
    result = await loop.run_in_executor(
        executor,
        lambda: run_command(
            f'xcrun simctl launch booted {Config.app_bundle_id}',
            timeout=30
        )
    )

    if not result["success"]:
        return {
            "success": False,
            "error": "Failed to launch app",
            "details": result.get("stderr", "")
        }

    # Wait for app to initialize
    if wait_seconds > 0:
        await asyncio.sleep(wait_seconds)

    return {
        "success": True,
        "message": f"App launched, waited {wait_seconds}s for initialization",
        "bundle_id": Config.app_bundle_id
    }


@mcp.tool()
@resilient_tool(max_response_bytes=100_000, save_large_to_file=True)
async def terminate_app() -> dict:
    """
    Terminate BennieGame in the simulator.

    Returns:
        Termination result with success status
    """
    loop = asyncio.get_event_loop()

    result = await loop.run_in_executor(
        executor,
        lambda: run_command(
            f'xcrun simctl terminate booted {Config.app_bundle_id}',
            timeout=10
        )
    )

    return {
        "success": result.get("return_code", 1) == 0 or "No matching processes" in result.get("stderr", ""),
        "message": "App terminated" if result["success"] else "App was not running"
    }


# =============================================================================
# SIMULATOR CONTROL TOOLS
# =============================================================================

@mcp.tool()
@resilient_tool(max_response_bytes=100_000, save_large_to_file=True)
async def boot_simulator() -> dict:
    """
    Boot the iPad Simulator if not already running.

    Returns:
        Boot result with success status
    """
    loop = asyncio.get_event_loop()

    # Try to boot
    result = await loop.run_in_executor(
        executor,
        lambda: run_command(
            f'xcrun simctl boot "{Config.simulator_name}"',
            timeout=60
        )
    )

    # "Unable to boot device in current state: Booted" means already booted
    already_booted = "already booted" in result.get("stderr", "").lower() or \
                     "current state: Booted" in result.get("stderr", "")

    if result["success"] or already_booted:
        # Open Simulator app
        await loop.run_in_executor(
            executor,
            lambda: run_command("open -a Simulator", timeout=10)
        )

        return {
            "success": True,
            "message": "Simulator booted" if result["success"] else "Simulator was already booted",
            "simulator": Config.simulator_name
        }

    return {
        "success": False,
        "error": "Failed to boot simulator",
        "details": result.get("stderr", "")
    }


@mcp.tool()
@resilient_tool(max_response_bytes=100_000, save_large_to_file=True)
async def reset_simulator() -> dict:
    """
    Reset the iPad Simulator to clean state.

    Warning: This erases all data including the installed app.

    Returns:
        Reset result with success status
    """
    loop = asyncio.get_event_loop()

    # Shutdown first
    await loop.run_in_executor(
        executor,
        lambda: run_command("xcrun simctl shutdown all", timeout=30)
    )

    # Erase
    result = await loop.run_in_executor(
        executor,
        lambda: run_command(
            f'xcrun simctl erase "{Config.simulator_name}"',
            timeout=60
        )
    )

    if result["success"]:
        return {
            "success": True,
            "message": "Simulator reset to clean state. You'll need to rebuild and install the app.",
            "simulator": Config.simulator_name
        }

    return {
        "success": False,
        "error": "Failed to reset simulator",
        "details": result.get("stderr", "")
    }


@mcp.tool()
@resilient_tool(max_response_bytes=100_000, save_large_to_file=True)
async def get_simulator_status() -> dict:
    """
    Get current simulator status and list available simulators.

    Returns:
        Simulator status including booted device info
    """
    loop = asyncio.get_event_loop()

    result = await loop.run_in_executor(
        executor,
        lambda: run_command("xcrun simctl list devices available -j", timeout=10)
    )

    if not result["success"]:
        return {"success": False, "error": "Failed to get simulator list"}

    try:
        devices = json.loads(result["stdout"])

        # Find booted devices
        booted = []
        target_found = False

        for runtime, device_list in devices.get("devices", {}).items():
            for device in device_list:
                if device.get("state") == "Booted":
                    booted.append({
                        "name": device.get("name"),
                        "udid": device.get("udid"),
                        "runtime": runtime
                    })
                if device.get("name") == Config.simulator_name:
                    target_found = True

        return {
            "success": True,
            "target_simulator": Config.simulator_name,
            "target_available": target_found,
            "booted_devices": booted,
            "is_target_booted": any(d["name"] == Config.simulator_name for d in booted)
        }
    except json.JSONDecodeError:
        return {"success": False, "error": "Failed to parse simulator list"}


# =============================================================================
# SCREENSHOT & VISUAL INSPECTION TOOLS
# =============================================================================

@mcp.tool()
@resilient_tool(max_response_bytes=300_000, save_large_to_file=True)
async def take_screenshot(
    save_to_file: Optional[str] = None,
    max_bytes: int = 300_000
) -> dict:
    """
    Capture the current simulator screen.

    Returns compressed screenshot as base64-encoded image (always under 500KB).
    Original full-resolution screenshot saved to disk if save_to_file specified.

    Args:
        save_to_file: Optional path to save full-resolution original (on Mac)
        max_bytes: Maximum base64 size in bytes (default 500KB)

    Returns:
        Base64-encoded compressed image data (guaranteed under max_bytes)
    """
    loop = asyncio.get_event_loop()

    # Create temp file for screenshot
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
        tmp_path = Path(tmp.name)

    try:
        # Capture screenshot
        result = await loop.run_in_executor(
            executor,
            lambda: run_command(
                f'xcrun simctl io booted screenshot "{tmp_path}"',
                timeout=10
            )
        )

        if not result["success"]:
            return {
                "success": False,
                "error": "Failed to capture screenshot",
                "details": result.get("stderr", ""),
                "hint": "Make sure simulator is booted and app is running"
            }

        # Save original to specified path if requested
        if save_to_file:
            import shutil
            shutil.copy(str(tmp_path), save_to_file)

        # Compress for MCP transport using shared utility
        if compress_image_for_mcp:
            compressed = await loop.run_in_executor(
                executor,
                lambda: compress_image_for_mcp(
                    image_path=tmp_path,
                    max_bytes=max_bytes,
                    save_compressed=True
                )
            )

            if compressed.get("success"):
                return {
                    "success": True,
                    "image": compressed["image_b64"],
                    "mime_type": compressed["mime_type"],
                    "width": compressed["dimensions"][0],
                    "height": compressed["dimensions"][1],
                    "size_bytes": compressed["size_bytes"],
                    "original_size": compressed["original_size"],
                    "compression_ratio": compressed["compression_ratio"],
                    "under_limit": compressed["under_limit"],
                    "saved_original_to": save_to_file,
                    "saved_compressed_to": compressed.get("saved_to")
                }
            else:
                return {
                    "success": False,
                    "error": f"Compression failed: {compressed.get('error')}"
                }
        else:
            # Fallback: return uncompressed (old behavior)
            with open(tmp_path, "rb") as f:
                image_data = f.read()
            b64_data = base64.b64encode(image_data).decode('utf-8')

            return {
                "success": True,
                "image": b64_data,
                "mime_type": "image/png",
                "width": Config.screen_width,
                "height": Config.screen_height,
                "size_bytes": len(b64_data.encode('utf-8')),
                "saved_to": save_to_file,
                "warning": "Compression utility not available, returning uncompressed"
            }
    finally:
        # Cleanup temp file
        try:
            os.unlink(tmp_path)
        except:
            pass


@mcp.tool()
@resilient_tool(max_response_bytes=100_000, save_large_to_file=True)
async def record_video(
    duration_seconds: int = 5,
    output_path: Optional[str] = None
) -> dict:
    """
    Record a video of the simulator screen.

    Args:
        duration_seconds: Recording duration (default 5, max 60)
        output_path: Path to save video (default: ~/simulator_recording.mp4)

    Returns:
        Path to recorded video file
    """
    loop = asyncio.get_event_loop()

    duration_seconds = min(duration_seconds, 60)
    output_path = output_path or str(Path.home() / "simulator_recording.mp4")

    # Start recording in background
    record_process = await asyncio.create_subprocess_shell(
        f'xcrun simctl io booted recordVideo "{output_path}"',
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )

    # Wait for duration
    await asyncio.sleep(duration_seconds)

    # Stop recording (send SIGINT)
    record_process.terminate()
    await record_process.wait()

    # Verify file exists
    if Path(output_path).exists():
        return {
            "success": True,
            "video_path": output_path,
            "duration": duration_seconds,
            "size_mb": round(Path(output_path).stat().st_size / (1024*1024), 2)
        }

    return {
        "success": False,
        "error": "Video recording failed or file not created"
    }


# =============================================================================
# UI INTERACTION TOOLS
# =============================================================================

@mcp.tool()
@resilient_tool(max_response_bytes=100_000, save_large_to_file=True)
async def tap(
    x: int,
    y: int
) -> dict:
    """
    Tap at specific screen coordinates.

    Coordinate system: Origin (0,0) at top-left.
    iPad 10th gen landscape: 1194 x 834 points.

    Args:
        x: X coordinate (0-1194 for iPad landscape)
        y: Y coordinate (0-834 for iPad landscape)

    Returns:
        Tap result with success status
    """
    loop = asyncio.get_event_loop()

    # Validate coordinates
    if not (0 <= x <= Config.screen_width and 0 <= y <= Config.screen_height):
        return {
            "success": False,
            "error": f"Coordinates out of bounds. Screen size: {Config.screen_width}x{Config.screen_height}"
        }

    # Use simctl ui tap (Xcode 14+, no permissions needed)
    result = await loop.run_in_executor(
        executor,
        lambda: run_command(
            f'xcrun simctl ui booted tap {x} {y}',
            timeout=5
        )
    )

    if result["success"]:
        return {
            "success": True,
            "message": f"Tapped at ({x}, {y})",
            "coordinates": {"x": x, "y": y}
        }

    # If simctl ui fails, return error (no AppleScript fallback to avoid permission prompts)
    return {
        "success": False,
        "error": "simctl ui tap failed",
        "details": result.get("stderr", ""),
        "coordinates": {"x": x, "y": y},
        "hint": "Make sure simulator is booted and in foreground. Try boot_simulator() first."
    }


@mcp.tool()
@resilient_tool(max_response_bytes=100_000, save_large_to_file=True)
async def swipe(
    start_x: int,
    start_y: int,
    end_x: int,
    end_y: int,
    duration_ms: int = 300
) -> dict:
    """
    Perform a swipe gesture.

    Args:
        start_x: Starting X coordinate
        start_y: Starting Y coordinate
        end_x: Ending X coordinate
        end_y: Ending Y coordinate
        duration_ms: Swipe duration in milliseconds (default 300)

    Returns:
        Swipe result with success status
    """
    loop = asyncio.get_event_loop()

    # Validate coordinates
    for coord, name, max_val in [(start_x, "start_x", Config.screen_width),
                                   (start_y, "start_y", Config.screen_height),
                                   (end_x, "end_x", Config.screen_width),
                                   (end_y, "end_y", Config.screen_height)]:
        if not (0 <= coord <= max_val):
            return {"success": False, "error": f"{name} out of bounds"}

    # Try simctl ui swipe
    result = await loop.run_in_executor(
        executor,
        lambda: run_command(
            f'xcrun simctl ui booted swipe {start_x} {start_y} {end_x} {end_y}',
            timeout=5
        )
    )

    return {
        "success": result["success"],
        "message": f"Swiped from ({start_x}, {start_y}) to ({end_x}, {end_y})",
        "start": {"x": start_x, "y": start_y},
        "end": {"x": end_x, "y": end_y}
    }


@mcp.tool()
@resilient_tool(max_response_bytes=100_000, save_large_to_file=True)
async def type_text(
    text: str
) -> dict:
    """
    Type text using keyboard input.

    The simulator must have an active text field focused.

    Args:
        text: Text to type (ASCII characters only for simctl)

    Returns:
        Type result with success status
    """
    loop = asyncio.get_event_loop()

    # Escape special characters for shell
    escaped_text = text.replace('"', '\\"').replace("'", "\\'")

    result = await loop.run_in_executor(
        executor,
        lambda: run_command(
            f'xcrun simctl io booted sendtext "{escaped_text}"',
            timeout=10
        )
    )

    return {
        "success": result["success"],
        "message": f"Typed: {text[:50]}..." if len(text) > 50 else f"Typed: {text}",
        "text_length": len(text)
    }


@mcp.tool()
@resilient_tool(max_response_bytes=100_000, save_large_to_file=True)
async def press_button(
    button: str
) -> dict:
    """
    Press a physical button on the simulator.

    Args:
        button: Button to press - "home", "lock", "volumeUp", "volumeDown"

    Returns:
        Button press result
    """
    loop = asyncio.get_event_loop()

    valid_buttons = ["home", "lock", "volumeUp", "volumeDown"]
    if button not in valid_buttons:
        return {
            "success": False,
            "error": f"Invalid button. Must be one of: {valid_buttons}"
        }

    # Map button names to simctl commands
    button_map = {
        "home": "home",
        "lock": "lock",
        "volumeUp": "volumeUp",
        "volumeDown": "volumeDown"
    }

    result = await loop.run_in_executor(
        executor,
        lambda: run_command(
            f'xcrun simctl ui booted pressButton {button_map[button]}',
            timeout=5
        )
    )

    return {
        "success": result["success"],
        "message": f"Pressed {button} button",
        "button": button
    }


# =============================================================================
# LOGGING & DEBUGGING TOOLS
# =============================================================================

@mcp.tool()
@resilient_tool(max_response_bytes=300_000, save_large_to_file=True)
async def get_logs(
    lines: int = 50,
    filter_app: bool = True
) -> dict:
    """
    Get recent console logs from the simulator.

    Args:
        lines: Number of recent log lines to return (default 50)
        filter_app: Only show logs from BennieGame (default True)

    Returns:
        Log output
    """
    loop = asyncio.get_event_loop()

    if filter_app:
        cmd = (
            f'xcrun simctl spawn booted log show --last 1m '
            f'--predicate \'subsystem == "{Config.app_bundle_id}"\' 2>/dev/null | tail -{lines}'
        )
    else:
        cmd = f'xcrun simctl spawn booted log show --last 1m 2>/dev/null | tail -{lines}'

    result = await loop.run_in_executor(
        executor,
        lambda: run_command(cmd, timeout=15)
    )

    log_text = result.get("stdout", "")

    return {
        "success": True,
        "logs": log_text,
        "line_count": len(log_text.split("\n")) if log_text else 0,
        "filtered": filter_app
    }


@mcp.tool()
@resilient_tool(max_response_bytes=300_000, save_large_to_file=True)
async def get_crash_logs() -> dict:
    """
    Get recent crash logs for BennieGame.

    Returns:
        Crash log information if any crashes occurred
    """
    loop = asyncio.get_event_loop()

    # Check diagnostic reports
    crash_dir = Path.home() / "Library/Logs/DiagnosticReports"

    if not crash_dir.exists():
        return {"success": True, "crashes": [], "message": "No crash directory found"}

    # Find recent BennieGame crashes
    crashes = []
    for crash_file in crash_dir.glob("BennieGame*.crash"):
        try:
            stat = crash_file.stat()
            crashes.append({
                "file": str(crash_file),
                "date": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                "size_kb": round(stat.st_size / 1024, 1)
            })
        except:
            pass

    # Sort by date, newest first
    crashes.sort(key=lambda x: x["date"], reverse=True)

    # Read most recent crash if exists
    most_recent = None
    if crashes:
        try:
            with open(crashes[0]["file"], "r") as f:
                most_recent = f.read()[:5000]  # First 5KB
        except:
            pass

    return {
        "success": True,
        "crash_count": len(crashes),
        "crashes": crashes[:5],  # Last 5 crashes
        "most_recent_content": most_recent
    }


# =============================================================================
# TESTING TOOLS
# =============================================================================

@mcp.tool()
@resilient_tool(max_response_bytes=300_000, save_large_to_file=True)
async def run_tests(
    test_class: Optional[str] = None,
    ui_tests: bool = True
) -> dict:
    """
    Run XCUITests for BennieGame.

    Args:
        test_class: Specific test class to run (e.g., "ActivityFlowUITests")
                   If None, runs all tests in the test target
        ui_tests: Run UI tests (True) or unit tests (False)

    Returns:
        Test results with pass/fail status
    """
    loop = asyncio.get_event_loop()

    test_target = "BennieGameUITests" if ui_tests else "BennieGameTests"

    cmd = (
        f'xcodebuild test -scheme {Config.scheme_name} '
        f'-destination "platform=iOS Simulator,name={Config.simulator_name}"'
    )

    if test_class:
        cmd += f' -only-testing:{test_target}/{test_class}'

    cmd += ' 2>&1'

    log(f"Running tests: {test_class or 'all'}")

    result = await loop.run_in_executor(
        executor,
        lambda: run_command(cmd, timeout=Config.test_timeout)
    )

    output = result.get("stdout", "")

    # Parse test results
    test_succeeded = "TEST SUCCEEDED" in output or "** TEST SUCCEEDED **" in output
    test_failed = "TEST FAILED" in output or "** TEST FAILED **" in output

    # Extract failed tests
    failed_tests = []
    for line in output.split("\n"):
        if "failed" in line.lower() and ("test" in line.lower() or "✗" in line):
            failed_tests.append(line.strip())

    # Extract test counts
    import re
    counts_match = re.search(r'Executed (\d+) tests?, with (\d+) failures?', output)
    total_tests = int(counts_match.group(1)) if counts_match else 0
    failures = int(counts_match.group(2)) if counts_match else len(failed_tests)

    return {
        "success": test_succeeded,
        "test_class": test_class or f"all {test_target}",
        "total_tests": total_tests,
        "passed": total_tests - failures,
        "failed": failures,
        "failed_tests": failed_tests[:20],  # Limit to 20
        "output_tail": "\n".join(output.split("\n")[-30:])  # Last 30 lines
    }


@mcp.tool()
@resilient_tool(max_response_bytes=300_000, save_large_to_file=True)
async def verify_design_checklist() -> dict:
    """
    Run automated design verification checks.

    Captures a screenshot and runs accessibility audit tests to verify:
    - Touch targets >= 96pt
    - Approved color palette
    - German UI labels
    - Reduce motion support

    Returns:
        Checklist results with screenshot for visual inspection
    """
    loop = asyncio.get_event_loop()

    # Take screenshot first
    screenshot_result = await take_screenshot()

    if not screenshot_result.get("success"):
        return {
            "success": False,
            "error": "Could not capture screenshot for verification"
        }

    # Run accessibility audit tests
    test_result = await run_tests(test_class="AccessibilityAuditTests", ui_tests=False)

    return {
        "success": True,
        "screenshot": screenshot_result.get("image"),
        "screenshot_size": {
            "width": Config.screen_width,
            "height": Config.screen_height
        },
        "automated_checks": {
            "tests_passed": test_result.get("success", False),
            "total_tests": test_result.get("total_tests", 0),
            "failures": test_result.get("failed", 0),
            "failed_tests": test_result.get("failed_tests", [])
        },
        "manual_inspection_needed": [
            "Touch targets >= 96pt (visual inspection)",
            "No red/neon colors (visual inspection)",
            "German text throughout (visual inspection)",
            "Soft cartoon style matches reference",
            "Navigation flows correctly"
        ],
        "reference_docs": [
            "DESIGN-CHECKLIST.md",
            "public/images/generated/characters/*/reference/"
        ]
    }


# =============================================================================
# VISUAL REGRESSION TOOLS
# =============================================================================

@mcp.tool()
@resilient_tool(max_response_bytes=300_000, save_large_to_file=True)
async def save_baseline(
    screen_name: str,
    description: Optional[str] = None
) -> dict:
    """
    Save current screenshot as a baseline for regression testing.

    Baselines are stored in ~/baselines/{screen_name}.png with metadata.

    Args:
        screen_name: Unique identifier for this screen (e.g., "player_select", "home_screen")
        description: Optional description of what this screen shows

    Returns:
        Success status with baseline path
    """
    # Ensure baselines directory exists
    Config.baselines_path.mkdir(parents=True, exist_ok=True)

    baseline_path = Config.baselines_path / f"{screen_name}.png"
    metadata_path = Config.baselines_path / f"{screen_name}.json"

    # Take screenshot and save
    screenshot = await take_screenshot(save_to_file=str(baseline_path))

    if not screenshot.get("success"):
        return {
            "success": False,
            "error": "Failed to capture screenshot for baseline",
            "details": screenshot.get("error")
        }

    # Save metadata
    metadata = {
        "screen_name": screen_name,
        "description": description or f"Baseline for {screen_name}",
        "captured_at": datetime.now().isoformat(),
        "width": Config.screen_width,
        "height": Config.screen_height,
        "size_bytes": screenshot.get("size_bytes", 0)
    }

    with open(metadata_path, "w") as f:
        json.dump(metadata, f, indent=2)

    return {
        "success": True,
        "screen_name": screen_name,
        "baseline_path": str(baseline_path),
        "metadata": metadata,
        "message": f"Baseline saved for '{screen_name}'"
    }


@mcp.tool()
@resilient_tool(max_response_bytes=300_000, save_large_to_file=True)
async def load_baseline(
    screen_name: str
) -> dict:
    """
    Load a baseline screenshot for comparison.

    Returns the baseline as base64-encoded PNG for Claude to compare with current state.

    Args:
        screen_name: Identifier of the baseline to load

    Returns:
        Base64-encoded baseline image and metadata
    """
    baseline_path = Config.baselines_path / f"{screen_name}.png"
    metadata_path = Config.baselines_path / f"{screen_name}.json"

    if not baseline_path.exists():
        return {
            "success": False,
            "error": f"Baseline '{screen_name}' not found",
            "available_baselines": [p.stem for p in Config.baselines_path.glob("*.png")]
        }

    # Read baseline image
    with open(baseline_path, "rb") as f:
        image_data = f.read()
        b64_data = base64.b64encode(image_data).decode('utf-8')

    # Read metadata if exists
    metadata = {}
    if metadata_path.exists():
        with open(metadata_path, "r") as f:
            metadata = json.load(f)

    return {
        "success": True,
        "screen_name": screen_name,
        "image": b64_data,
        "mime_type": "image/png",
        "metadata": metadata,
        "size_bytes": len(image_data)
    }


@mcp.tool()
@resilient_tool(max_response_bytes=100_000, save_large_to_file=True)
async def list_baselines() -> dict:
    """
    List all saved baselines.

    Returns:
        List of available baselines with metadata
    """
    if not Config.baselines_path.exists():
        return {
            "success": True,
            "baselines": [],
            "count": 0,
            "message": "No baselines directory found. Use save_baseline() to create baselines."
        }

    baselines = []
    for png_file in Config.baselines_path.glob("*.png"):
        screen_name = png_file.stem
        metadata_path = Config.baselines_path / f"{screen_name}.json"

        entry = {
            "screen_name": screen_name,
            "path": str(png_file),
            "size_kb": round(png_file.stat().st_size / 1024, 1)
        }

        if metadata_path.exists():
            with open(metadata_path, "r") as f:
                entry["metadata"] = json.load(f)

        baselines.append(entry)

    return {
        "success": True,
        "baselines": sorted(baselines, key=lambda x: x["screen_name"]),
        "count": len(baselines),
        "baselines_path": str(Config.baselines_path)
    }


@mcp.tool()
@resilient_tool(max_response_bytes=300_000, save_large_to_file=True)
async def compare_to_baseline(
    screen_name: str
) -> dict:
    """
    Take current screenshot and return both it and the baseline for Claude to compare.

    This is the main regression comparison tool. Claude should analyze both images
    and report ONLY meaningful changes (layout, missing elements, colors) while
    ignoring minor rendering differences.

    Args:
        screen_name: Name of the baseline to compare against

    Returns:
        Current screenshot and baseline for visual comparison
    """
    # Load baseline
    baseline = await load_baseline(screen_name)
    if not baseline.get("success"):
        return baseline

    # Take current screenshot
    current = await take_screenshot()
    if not current.get("success"):
        return {
            "success": False,
            "error": "Failed to capture current screenshot",
            "baseline_available": True
        }

    # Save current to regression folder for later reference
    Config.regression_path.mkdir(parents=True, exist_ok=True)
    current_path = Config.regression_path / f"{screen_name}_current.png"

    # Decode and save current
    with open(current_path, "wb") as f:
        f.write(base64.b64decode(current["image"]))

    return {
        "success": True,
        "screen_name": screen_name,
        "baseline": {
            "image": baseline["image"],
            "metadata": baseline.get("metadata", {})
        },
        "current": {
            "image": current["image"],
            "saved_to": str(current_path)
        },
        "comparison_prompt": f"""Compare these two screenshots for '{screen_name}'.

Report ONLY meaningful changes:
- Layout shifts (buttons moved, resized, missing)
- Missing or new UI elements
- Text content changes
- Color violations (non-BennieColor palette)
- Touch targets that appear smaller than 96pt

IGNORE these (not regressions):
- Minor antialiasing differences
- Shadow rendering variations
- Slight color temperature shifts
- Animation frame differences"""
    }


@mcp.tool()
@resilient_tool(max_response_bytes=300_000, save_large_to_file=True)
async def run_regression_flow(
    flow_file: Optional[str] = None
) -> dict:
    """
    Run full visual regression test flow.

    Executes a series of navigation actions and compares each screen to baseline.
    Uses regression_flow.json in project root or designer system folder.

    Args:
        flow_file: Optional path to custom flow definition JSON

    Returns:
        Regression results for each screen
    """
    loop = asyncio.get_event_loop()

    # Find flow definition
    flow_path = None
    if flow_file:
        flow_path = Path(flow_file)
    else:
        # Check default locations
        for path in [
            Config.project_path / "regression_flow.json",
            Config.project_path / "designer system" / "regression_flow.json"
        ]:
            if path.exists():
                flow_path = path
                break

    if not flow_path or not flow_path.exists():
        return {
            "success": False,
            "error": "No regression_flow.json found",
            "hint": "Create regression_flow.json with screen definitions",
            "example": {
                "screens": [
                    {"name": "player_select", "actions": []},
                    {"name": "home_screen", "actions": [{"tap": [400, 350]}]}
                ]
            }
        }

    # Load flow
    with open(flow_path, "r") as f:
        flow = json.load(f)

    screens = flow.get("screens", [])
    if not screens:
        return {
            "success": False,
            "error": "No screens defined in regression_flow.json"
        }

    results = []
    all_passed = True

    for screen in screens:
        screen_name = screen.get("name")
        actions = screen.get("actions", [])

        log(f"Regression: Testing '{screen_name}'...")

        # Execute actions to navigate to this screen
        for action in actions:
            if "tap" in action:
                x, y = action["tap"]
                await tap(x, y)
                await asyncio.sleep(0.5)  # Wait for UI update
            elif "swipe" in action:
                coords = action["swipe"]
                await swipe(coords[0], coords[1], coords[2], coords[3])
                await asyncio.sleep(0.5)
            elif "wait" in action:
                await asyncio.sleep(action["wait"])

        # Wait for screen to stabilize
        await asyncio.sleep(1)

        # Compare to baseline
        comparison = await compare_to_baseline(screen_name)

        if comparison.get("success"):
            results.append({
                "screen_name": screen_name,
                "status": "captured",
                "has_baseline": True,
                "comparison": comparison
            })
        else:
            # No baseline - just capture current
            screenshot = await take_screenshot()
            results.append({
                "screen_name": screen_name,
                "status": "no_baseline",
                "has_baseline": False,
                "current_screenshot": screenshot.get("image") if screenshot.get("success") else None,
                "hint": f"Run save_baseline('{screen_name}') to create baseline"
            })
            all_passed = False

    return {
        "success": True,
        "all_baselines_exist": all_passed,
        "screens_tested": len(results),
        "results": results,
        "message": "Regression flow complete. Claude should analyze each comparison."
    }


# =============================================================================
# RESOURCES
# =============================================================================

@mcp.resource("config://current")
async def resource_config() -> str:
    """Get current server configuration."""
    return json.dumps({
        "project_path": str(Config.project_path),
        "scheme_name": Config.scheme_name,
        "app_bundle_id": Config.app_bundle_id,
        "simulator_name": Config.simulator_name,
        "screen_size": f"{Config.screen_width}x{Config.screen_height}",
        "baselines_path": str(Config.baselines_path),
        "regression_path": str(Config.regression_path)
    }, indent=2)


@mcp.resource("design://checklist")
async def resource_design_checklist() -> str:
    """Get design checklist for visual verification."""
    return """# Bennie Bear Design Checklist

## Critical Rules (Non-Negotiable)

1. **Touch targets >= 96pt**
   - All buttons and interactive elements must be at least 96x96 points

2. **No red/neon/bright colors**
   - Use BennieColor palette only (Woodland, Bark, Sky, Cream, Success, CoinGold)
   - Saturation must be < 80%

3. **No flashing/shaking**
   - All animations must be smooth, no rapid changes

4. **German UI only**
   - All text and voice must be in German

5. **Never say "wrong"**
   - Only positive reinforcement

6. **Independent audio channels**
   - Music, voice, effects must have separate volume controls

7. **Reduce motion support**
   - Every animation needs a static fallback

8. **Same greeting every time**
   - Predictable welcome message

## Color Palette (Safe)
- Woodland: #738F66 (Primary)
- Bark: #8C7259 (Secondary)
- Sky: #B3D1E6 (Accents)
- Cream: #FAF5EB (Backgrounds)
- Success: #99BF8C (Positive feedback)
- CoinGold: #D9C27A (Rewards)
"""


# =============================================================================
# SERVER ENTRY POINT
# =============================================================================

def run_self_test():
    """Run self-test to verify all tools work."""
    import asyncio

    async def test():
        print("Running iOS Simulator MCP self-test...\n")

        # Test 1: Simulator status
        print("1. Checking simulator status...")
        result = await get_simulator_status()
        print(f"   Target simulator: {result.get('target_simulator')}")
        print(f"   Available: {result.get('target_available')}")
        print(f"   Booted: {result.get('is_target_booted')}")

        if not result.get("is_target_booted"):
            print("\n2. Booting simulator...")
            result = await boot_simulator()
            print(f"   {result.get('message')}")

        # Test 2: Screenshot
        print("\n3. Taking screenshot...")
        result = await take_screenshot()
        if result.get("success"):
            print(f"   Screenshot captured: {result.get('size_bytes')} bytes")
        else:
            print(f"   Failed: {result.get('error')}")

        print("\nSelf-test complete!")

    asyncio.run(test())


def main():
    """Run the MCP server."""
    import argparse

    parser = argparse.ArgumentParser(description="iOS Simulator MCP Server")
    parser.add_argument("--transport", choices=["stdio", "sse"],
                       default=Config.transport,
                       help="Transport protocol (default: stdio)")
    parser.add_argument("--port", type=int, default=Config.sse_port,
                       help="Port for SSE transport (default: 8765)")
    parser.add_argument("--test", action="store_true",
                       help="Run self-test and exit")

    args = parser.parse_args()

    if args.test:
        run_self_test()
        return

    log(f"Starting iOS Simulator MCP Server")
    log(f"Transport: {args.transport}")
    log(f"Project: {Config.project_path}")
    log(f"Simulator: {Config.simulator_name}")

    if args.transport == "sse":
        log(f"Port: {args.port}")
        mcp.run(transport="sse", port=args.port)
    else:
        mcp.run()  # stdio is default


if __name__ == "__main__":
    main()
