#!/usr/bin/env python3
"""
Ludo.ai Animation Processor
============================

A quick-start script that simplifies the Ludo.ai sprite sheet to Lottie workflow.

Features:
- Auto-detects new ZIPs in downloads folder
- Processes them to Lottie JSON
- Copies to BennieGame/Resources/Lottie/
- Tracks animation status

Usage:
    python process.py           # Process all new ZIPs
    python process.py --status  # Just show status
    python process.py --help    # Show help
"""

import argparse
import json
import os
import shutil
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# Import from same directory (spritesheet_processor.py is alongside process.py)
from spritesheet_processor import process_ludo_asset, detect_grid, extract_zip

# =============================================================================
# CONFIGURATION
# =============================================================================

# Directory paths (relative to this script)
SCRIPT_DIR = Path(__file__).parent.resolve()
DOWNLOADS_DIR = SCRIPT_DIR / "downloads"
OUTPUT_DIR = SCRIPT_DIR / "output"
STATUS_FILE = SCRIPT_DIR / "animation_status.json"

# Target directory for final Lottie files
LOTTIE_TARGET = SCRIPT_DIR.parent.parent / "BennieGame" / "Resources" / "Lottie"

# Required animations (from LUDO_WORKFLOW.md)
REQUIRED_ANIMATIONS = {
    "bennie": [
        "idle",
        "happy",
        "thinking",
        "encouraging",
        "celebrating",
        "waving",
        "pointing",
    ],
    "lemminge": [
        "idle",
        "curious",
        "excited",
        "celebrating",
        "hiding",
        "mischievous",
    ],
}

# Processing defaults
DEFAULT_FPS = 30
DEFAULT_FRAME_HOLD = 2

# Animation specs file for per-animation timing
ANIMATION_SPECS_FILE = SCRIPT_DIR / "config" / "animation_specs.json"


# =============================================================================
# ANIMATION TIMING
# =============================================================================

def load_animation_specs() -> Dict:
    """Load per-animation timing specifications."""
    if ANIMATION_SPECS_FILE.exists():
        with open(ANIMATION_SPECS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"defaults": {"fps": DEFAULT_FPS, "frame_count": 42, "target_duration_ms": 1400}, "characters": {}}


def calculate_frame_hold(target_ms: int, frame_count: int, fps: int) -> int:
    """
    Calculate frame_hold for target duration.

    Formula: frame_hold = round(target_seconds * fps / frame_count)

    Examples at 42 frames, 30fps:
    - 1400ms: round(1.4 * 30 / 42) = 1 -> actual 1.4s
    - 2000ms: round(2.0 * 30 / 42) = 1 -> actual 1.4s
    - 2800ms: round(2.8 * 30 / 42) = 2 -> actual 2.8s
    """
    target_seconds = target_ms / 1000
    return max(1, round(target_seconds * fps / frame_count))


def get_animation_frame_hold(character: str, animation: str, frame_count: int = 42) -> int:
    """Get optimal frame_hold for a specific animation from specs."""
    specs = load_animation_specs()
    defaults = specs.get("defaults", {})
    fps = defaults.get("fps", DEFAULT_FPS)
    default_duration = defaults.get("target_duration_ms", 1400)

    # Look up character-specific timing
    char_specs = specs.get("characters", {}).get(character.lower(), {})
    anim_spec = char_specs.get(animation.lower(), {})
    target_ms = anim_spec.get("target_duration_ms", default_duration)

    return calculate_frame_hold(target_ms, frame_count, fps)


# =============================================================================
# QA GATE
# =============================================================================

def qa_gate(lottie_path: Path) -> Tuple[bool, List[str]]:
    """
    Run validation and generate visual strip for QA.

    Returns:
        Tuple of (passed, issues_list)
    """
    issues = []

    try:
        # 1. Validate Lottie structure
        from validate_lottie import validate_lottie_file
        validation_result = validate_lottie_file(lottie_path)
        if not validation_result.get("valid", False):
            issues.extend(validation_result.get("errors", ["Validation failed"]))
    except ImportError:
        print("  [WARN] validate_lottie not available, skipping validation")
    except Exception as e:
        issues.append(f"Validation error: {e}")

    try:
        # 2. Generate frame strip for visual inspection
        from generate_frame_strip import create_frame_strip
        strip_path = lottie_path.with_suffix('.strip.png')
        create_frame_strip(lottie_path, strip_path)
        print(f"  [QA] Frame strip: {strip_path}")
    except ImportError:
        print("  [WARN] generate_frame_strip not available, skipping strip generation")
    except Exception as e:
        print(f"  [WARN] Frame strip generation failed: {e}")

    # 3. Duration check
    try:
        with open(lottie_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        fr = data.get("fr", 30)
        op = data.get("op", 0)
        if fr > 0:
            duration = op / fr
            if duration < 0.5:
                issues.append(f"Duration {duration:.2f}s is too short (< 0.5s)")
            elif duration > 3.0:
                issues.append(f"Duration {duration:.2f}s is too long (> 3.0s)")
            else:
                print(f"  [QA] Duration: {duration:.2f}s (OK)")
    except Exception as e:
        issues.append(f"Duration check error: {e}")

    return len(issues) == 0, issues


# =============================================================================
# STATUS TRACKING
# =============================================================================

def load_status() -> Dict:
    """Load animation status from JSON file."""
    if STATUS_FILE.exists():
        with open(STATUS_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            # Ensure processed key exists (might be legacy format)
            if "processed" not in data:
                data["processed"] = {}
            return data
    return {
        "processed": {},
        "animations": {},
        "last_updated": None,
    }


def save_status(status: Dict) -> None:
    """Save animation status to JSON file."""
    status["last_updated"] = datetime.now().isoformat()
    with open(STATUS_FILE, 'w', encoding='utf-8') as f:
        json.dump(status, f, indent=2)


def update_animation_status(status: Dict, char: str, anim: str, lottie_file: str, frame_count: int = 0) -> None:
    """Update the animation entry in status."""
    if "animations" not in status:
        status["animations"] = {}

    key = f"{char}_{anim}"
    status["animations"][key] = {
        "status": "complete",
        "lottie_file": lottie_file,
        "frames": frame_count,
    }


def get_animation_name(zip_name: str) -> Tuple[Optional[str], Optional[str]]:
    """
    Extract character and animation name from ZIP filename.

    Args:
        zip_name: Filename like 'bennie_waving.zip'

    Returns:
        Tuple of (character, animation) or (None, None) if invalid
    """
    stem = Path(zip_name).stem.lower()

    # Try to match known characters
    for char in ["bennie", "lemminge"]:
        if stem.startswith(char + "_"):
            animation = stem[len(char) + 1:]
            return (char, animation)

    # Unknown format - return the whole stem as animation name
    return (None, stem)


# =============================================================================
# PROCESSING
# =============================================================================

def scan_downloads() -> List[Path]:
    """
    Scan downloads folder for unprocessed ZIP files.

    Returns:
        List of ZIP file paths that haven't been processed yet
    """
    if not DOWNLOADS_DIR.exists():
        DOWNLOADS_DIR.mkdir(parents=True, exist_ok=True)
        return []

    status = load_status()
    processed = set(status.get("processed", {}).keys())

    zips = []
    for f in DOWNLOADS_DIR.glob("*.zip"):
        if f.name not in processed:
            zips.append(f)

    return sorted(zips)


def process_zip(
    zip_path: Path,
    fps: int = DEFAULT_FPS,
    frame_hold: int = DEFAULT_FRAME_HOLD,
    grid: Optional[Tuple[int, int]] = None,
) -> Optional[Path]:
    """
    Process a single ZIP file to Lottie JSON.

    Args:
        zip_path: Path to the ZIP file
        fps: Frames per second
        frame_hold: Frames to hold each sprite
        grid: Optional grid dimensions (rows, cols)

    Returns:
        Path to the created Lottie file, or None if failed
    """
    # Ensure output directory exists
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Determine output filename
    output_name = zip_path.stem + ".json"
    output_path = OUTPUT_DIR / output_name

    try:
        # Process using the spritesheet_processor
        result = process_ludo_asset(
            input_path=zip_path,
            output_path=output_path,
            fps=fps,
            frame_hold=frame_hold,
            grid=grid,
            keep_frames=False,
        )
        return result
    except Exception as e:
        print(f"[ERROR] Failed to process {zip_path.name}: {e}")
        return None


def copy_to_lottie_folder(lottie_path: Path) -> bool:
    """
    Copy a Lottie JSON file to the BennieGame/Resources/Lottie/ folder.

    Args:
        lottie_path: Path to the Lottie JSON file

    Returns:
        True if successful, False otherwise
    """
    if not LOTTIE_TARGET.exists():
        print(f"[WARN] Target folder does not exist: {LOTTIE_TARGET}")
        print("       Creating folder...")
        LOTTIE_TARGET.mkdir(parents=True, exist_ok=True)

    target_path = LOTTIE_TARGET / lottie_path.name

    try:
        shutil.copy2(lottie_path, target_path)
        return True
    except Exception as e:
        print(f"[ERROR] Failed to copy to Lottie folder: {e}")
        return False


def process_all(
    fps: int = DEFAULT_FPS,
    frame_hold: int = DEFAULT_FRAME_HOLD,
    grid: Optional[str] = None,
) -> int:
    """
    Process all new ZIP files in the downloads folder.

    Returns:
        Number of successfully processed files
    """
    print()
    print("Ludo.ai Animation Processor")
    print("=" * 60)
    print()

    # Scan for new ZIPs
    print("Scanning downloads folder...")
    new_zips = scan_downloads()

    if not new_zips:
        print("No new ZIP files found in downloads/")
        print()
        show_status()
        return 0

    print(f"Found {len(new_zips)} new ZIP file(s):")
    for z in new_zips:
        print(f"  - {z.name}")
    print()

    # Parse grid if provided
    grid_tuple = None
    if grid:
        parts = grid.lower().split('x')
        if len(parts) == 2:
            grid_tuple = (int(parts[0]), int(parts[1]))

    # Load status for updating
    status = load_status()
    if "processed" not in status:
        status["processed"] = {}

    # Process each ZIP
    print("Processing...")
    success_count = 0

    for i, zip_path in enumerate(new_zips, 1):
        print(f"\n[{i}/{len(new_zips)}] {zip_path.name}")

        # Detect character/animation from filename for per-animation timing
        char, anim = get_animation_name(zip_path.name)
        actual_frame_hold = frame_hold

        if char and anim:
            # Use per-animation timing from specs
            actual_frame_hold = get_animation_frame_hold(char, anim)
            if actual_frame_hold != frame_hold:
                print(f"      Using timing spec: frame_hold={actual_frame_hold}")

        # Process the ZIP
        result = process_zip(zip_path, fps, actual_frame_hold, grid_tuple)

        if result and result.exists():
            # Get file info
            file_size = result.stat().st_size

            # Try to detect grid info for display
            grid_info = "auto-detected"
            if grid_tuple:
                grid_info = f"{grid_tuple[0]}x{grid_tuple[1]}"

            print(f"      Output: {result.name}")
            print(f"      Size: {file_size:,} bytes ({file_size / 1024:.1f} KB)")

            # Run QA gate
            qa_passed, qa_issues = qa_gate(result)
            if not qa_passed:
                print(f"      [QA ISSUES]:")
                for issue in qa_issues:
                    print(f"        - {issue}")

            # Copy to Lottie folder
            if copy_to_lottie_folder(result):
                print(f"      Copied to: BennieGame/Resources/Lottie/")
                print("      [OK]")

                # Update status
                status["processed"][zip_path.name] = {
                    "character": char,
                    "animation": anim,
                    "output": result.name,
                    "processed_at": datetime.now().isoformat(),
                    "size_bytes": file_size,
                    "qa_passed": qa_passed,
                }

                # Also update the animations section
                if char and anim:
                    # Try to get frame count from the Lottie file
                    try:
                        with open(result, 'r', encoding='utf-8') as f:
                            lottie_data = json.load(f)
                            frame_count = len(lottie_data.get("assets", []))
                    except Exception:
                        frame_count = 0
                    update_animation_status(status, char, anim, result.name, frame_count)

                success_count += 1
            else:
                print("      [WARN] Copy failed")
        else:
            print("      [FAILED]")

    # Save updated status
    save_status(status)

    print()
    print("=" * 60)
    show_status()

    return success_count


def show_status() -> None:
    """Display current animation status and what's still needed."""
    status = load_status()
    processed = status.get("processed", {})

    # Check what exists in Lottie folder
    existing_lotties = set()
    if LOTTIE_TARGET.exists():
        for f in LOTTIE_TARGET.glob("*.json"):
            existing_lotties.add(f.stem)

    # Calculate completion status
    total_required = sum(len(anims) for anims in REQUIRED_ANIMATIONS.values())

    complete = {}
    missing = {}

    for char, animations in REQUIRED_ANIMATIONS.items():
        complete[char] = []
        missing[char] = []

        for anim in animations:
            lottie_name = f"{char}_{anim}"
            if lottie_name in existing_lotties:
                complete[char].append(anim)
            else:
                missing[char].append(anim)

    total_complete = sum(len(c) for c in complete.values())
    percentage = (total_complete / total_required * 100) if total_required > 0 else 0

    # Display status
    print(f"Status: {total_complete}/{total_required} animations complete ({percentage:.0f}%)")
    print()

    # Show what's missing
    has_missing = any(m for m in missing.values())
    if has_missing:
        print("Still needed:")
        for char, anims in missing.items():
            if anims:
                char_display = char.capitalize()
                anims_str = ", ".join(anims)
                print(f"  {char_display}: {anims_str}")
        print()
    else:
        print("All required animations are complete!")
        print()

    # Show recently processed
    if processed:
        recent = sorted(
            processed.items(),
            key=lambda x: x[1].get("processed_at", ""),
            reverse=True,
        )[:5]

        if recent:
            print("Recently processed:")
            for name, info in recent:
                char = info.get("character", "unknown")
                anim = info.get("animation", "unknown")
                date = info.get("processed_at", "")[:10]
                print(f"  - {char}_{anim} ({date})")
            print()


def show_detailed_status() -> None:
    """Show detailed status of all animations."""
    print()
    print("Ludo.ai Animation Status")
    print("=" * 60)
    print()

    # Check what exists in Lottie folder
    existing_lotties = {}
    if LOTTIE_TARGET.exists():
        for f in LOTTIE_TARGET.glob("*.json"):
            size = f.stat().st_size
            existing_lotties[f.stem] = {
                "path": f,
                "size": size,
            }

    # Display by character
    for char, animations in REQUIRED_ANIMATIONS.items():
        print(f"{char.upper()}")
        print("-" * 40)

        for anim in animations:
            lottie_name = f"{char}_{anim}"

            if lottie_name in existing_lotties:
                info = existing_lotties[lottie_name]
                size_kb = info["size"] / 1024
                status_mark = "[OK]"
                print(f"  {anim:15} {status_mark:8} ({size_kb:.1f} KB)")
            else:
                status_mark = "[MISSING]"
                print(f"  {anim:15} {status_mark}")

        print()

    # Summary
    total_required = sum(len(anims) for anims in REQUIRED_ANIMATIONS.values())
    total_complete = sum(
        1 for char, anims in REQUIRED_ANIMATIONS.items()
        for anim in anims
        if f"{char}_{anim}" in existing_lotties
    )
    percentage = (total_complete / total_required * 100) if total_required > 0 else 0

    print("=" * 60)
    print(f"TOTAL: {total_complete}/{total_required} complete ({percentage:.0f}%)")
    print()

    # Downloads folder status
    pending_zips = scan_downloads()
    if pending_zips:
        print(f"Pending in downloads/: {len(pending_zips)} ZIP(s)")
        for z in pending_zips[:5]:
            print(f"  - {z.name}")
        if len(pending_zips) > 5:
            print(f"  ... and {len(pending_zips) - 5} more")
        print()


# =============================================================================
# CLI
# =============================================================================

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Ludo.ai Animation Processor - Quick workflow for sprite animations",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python process.py              # Process all new ZIPs
  python process.py --status     # Just show status
  python process.py --fps 24     # Process with custom FPS
  python process.py --grid 6x6   # Force specific grid dimensions

Workflow:
  1. Download sprite animations from ludo.ai
  2. Save ZIPs to ludo-animation-pipeline/downloads/
  3. Run: python process.py
  4. Lottie files are copied to BennieGame/Resources/Lottie/
        """
    )

    parser.add_argument(
        '--status', '-s',
        action='store_true',
        help='Show animation status without processing'
    )

    parser.add_argument(
        '--detailed', '-d',
        action='store_true',
        help='Show detailed status of all animations'
    )

    parser.add_argument(
        '--fps',
        type=int,
        default=DEFAULT_FPS,
        help=f'Frames per second (default: {DEFAULT_FPS})'
    )

    parser.add_argument(
        '--frame-hold',
        type=int,
        default=DEFAULT_FRAME_HOLD,
        help=f'Lottie frames per sprite frame (default: {DEFAULT_FRAME_HOLD})'
    )

    parser.add_argument(
        '--grid', '-g',
        type=str,
        default=None,
        help='Grid dimensions as ROWSxCOLUMNS (e.g., "6x6"). Auto-detected if not specified.'
    )

    parser.add_argument(
        '--reprocess', '-r',
        action='store_true',
        help='Force reprocess all ZIPs (clear status tracking)'
    )

    args = parser.parse_args()

    # Clear status if reprocessing
    if args.reprocess:
        if STATUS_FILE.exists():
            STATUS_FILE.unlink()
            print("[INFO] Cleared animation status - will reprocess all ZIPs")

    # Handle status-only modes
    if args.detailed:
        show_detailed_status()
        return 0

    if args.status:
        print()
        show_status()
        return 0

    # Process new ZIPs
    count = process_all(
        fps=args.fps,
        frame_hold=args.frame_hold,
        grid=args.grid,
    )

    return 0 if count >= 0 else 1


if __name__ == "__main__":
    sys.exit(main())
