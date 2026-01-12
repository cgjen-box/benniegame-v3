#!/usr/bin/env python3
"""
Bennie Bear - Sprite Sheet Processor for Ludo.ai Assets
========================================================

Processes sprite sheet ZIPs or PNGs from Ludo.ai into Lottie animations
for use in the Bennie Bear game.

This tool:
1. Extracts sprite sheets from Ludo.ai ZIP downloads
2. Auto-detects grid dimensions by analyzing transparency gaps
3. Extracts individual frames to separate PNG files
4. Generates Lottie JSON with frame-by-frame animation (frames embedded as base64)

Usage:
    # Process a Ludo.ai ZIP download
    python spritesheet_processor.py process path/to/download.zip --output animation.json

    # Process a sprite sheet PNG directly with auto-detect
    python spritesheet_processor.py process path/to/spritesheet.png --output animation.json

    # Process with explicit grid dimensions
    python spritesheet_processor.py process spritesheet.png --output animation.json --grid 6x6

    # Customize FPS and frame hold
    python spritesheet_processor.py process spritesheet.png --output animation.json --fps 24 --frame-hold 3

Dependencies:
    pip install Pillow

Output:
    - Lottie JSON file with embedded base64 frames
    - Extracted frames in output_frames/ directory (optional)
"""

import argparse
import base64
import json
import os
import sys
import zipfile
from pathlib import Path
from typing import List, Optional, Tuple

try:
    from PIL import Image
except ImportError:
    print("[ERROR] Pillow is required. Install with: pip install Pillow", file=sys.stderr)
    sys.exit(1)


# =============================================================================
# ZIP EXTRACTION
# =============================================================================

def extract_zip(zip_path: Path, output_dir: Path) -> Path:
    """
    Extract ZIP file and return path to the sprite sheet PNG.

    Ludo.ai typically exports a ZIP containing:
    - A sprite sheet PNG (the main animation frames)
    - Sometimes a preview GIF or additional assets

    Args:
        zip_path: Path to the ZIP file
        output_dir: Directory to extract files to

    Returns:
        Path to the sprite sheet PNG file

    Raises:
        FileNotFoundError: If no PNG file is found in the ZIP
        zipfile.BadZipFile: If the file is not a valid ZIP
    """
    print(f"[INFO] Extracting ZIP: {zip_path}")

    output_dir.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(zip_path, 'r') as zf:
        # List all files in the ZIP
        file_list = zf.namelist()
        print(f"[INFO] Found {len(file_list)} file(s) in ZIP")

        # Extract all files
        zf.extractall(output_dir)

        # Find PNG files (prefer larger files as they're likely the sprite sheet)
        png_files = []
        for name in file_list:
            if name.lower().endswith('.png'):
                extracted_path = output_dir / name
                if extracted_path.exists():
                    size = extracted_path.stat().st_size
                    png_files.append((extracted_path, size))
                    print(f"  [PNG] {name} ({size:,} bytes)")

        if not png_files:
            raise FileNotFoundError(f"No PNG files found in ZIP: {zip_path}")

        # Return the largest PNG (most likely the sprite sheet)
        png_files.sort(key=lambda x: x[1], reverse=True)
        spritesheet_path = png_files[0][0]

        print(f"[OK] Selected sprite sheet: {spritesheet_path.name}")
        return spritesheet_path


# =============================================================================
# GRID DETECTION
# =============================================================================

def detect_grid(spritesheet: Image.Image) -> Tuple[int, int]:
    """
    Auto-detect grid dimensions by analyzing transparency gaps between frames.

    This works by:
    1. Summing alpha per row/column to find mostly-empty separators
    2. Ignoring edge padding gaps
    3. Using gap count to determine rows/columns

    Args:
        spritesheet: PIL Image object of the sprite sheet

    Returns:
        Tuple of (rows, columns) representing the grid dimensions

    Note:
        Falls back to common grid sizes (4x4, 6x6, etc.) if detection fails.
    """
    print("[INFO] Auto-detecting grid dimensions...")

    width, height = spritesheet.size
    print(f"[INFO] Sprite sheet size: {width}x{height}")

    # Ensure we have an alpha channel
    if spritesheet.mode != 'RGBA':
        # Try to detect grid from color uniformity instead
        print("[WARN] No alpha channel, attempting color-based detection")
        return _detect_grid_by_color(spritesheet)

    return _detect_grid_by_alpha(spritesheet)


def _detect_grid_by_alpha(
    spritesheet: Image.Image,
    gap_threshold: float = 0.015,  # Increased from 0.003 for anti-aliased Ludo.ai output
    edge_margin: int = 1
) -> Tuple[int, int]:
    """
    Detect grid by looking for near-transparent separator rows/columns.

    Uses alpha sum ratios so tiny stray pixels don't break gap detection.
    """
    width, height = spritesheet.size
    alpha = spritesheet.getchannel('A')
    alpha_pixels = alpha.load()

    col_sums = [0] * width
    row_sums = [0] * height

    for y in range(height):
        row_sum = 0
        for x in range(width):
            val = alpha_pixels[x, y]
            row_sum += val
            col_sums[x] += val
        row_sums[y] = row_sum

    col_threshold = height * 255 * gap_threshold
    row_threshold = width * 255 * gap_threshold

    gap_cols = [x for x, total in enumerate(col_sums) if total < col_threshold]
    gap_rows = [y for y, total in enumerate(row_sums) if total < row_threshold]

    col_groups = _group_consecutive(gap_cols)
    row_groups = _group_consecutive(gap_rows)

    # Ignore padding gaps on the outer edges
    col_groups = [
        g for g in col_groups
        if g[0] > edge_margin and g[-1] < width - 1 - edge_margin
    ]
    row_groups = [
        g for g in row_groups
        if g[0] > edge_margin and g[-1] < height - 1 - edge_margin
    ]

    print(f"[INFO] Found {len(col_groups)} vertical gaps, {len(row_groups)} horizontal gaps")

    cols = len(col_groups) + 1 if col_groups else _estimate_dimension(width)
    rows = len(row_groups) + 1 if row_groups else _estimate_dimension(height)

    frame_width = width // cols
    frame_height = height // rows

    if frame_width < 16 or frame_height < 16:
        print("[WARN] Detected frames too small, using fallback detection")
        return _fallback_grid_detection(width, height)

    if frame_width > width // 2 or frame_height > height // 2:
        print("[WARN] Detected frames too large, using fallback detection")
        return _fallback_grid_detection(width, height)

    print(f"[OK] Detected grid: {rows} rows x {cols} columns")
    print(f"[INFO] Frame size: {frame_width}x{frame_height}")

    return (rows, cols)


def _detect_grid_by_color(spritesheet: Image.Image) -> Tuple[int, int]:
    """
    Detect grid by looking for uniform color rows/columns (dividers).

    Used when the image doesn't have transparency.
    """
    # Convert to RGB if needed
    if spritesheet.mode != 'RGB':
        spritesheet = spritesheet.convert('RGB')

    width, height = spritesheet.size

    # Look for rows/columns with very low variance (uniform color)
    def is_uniform(pixels: List) -> bool:
        if not pixels:
            return False
        first = pixels[0]
        return all(abs(p[0] - first[0]) < 5 and
                   abs(p[1] - first[1]) < 5 and
                   abs(p[2] - first[2]) < 5 for p in pixels)

    # Sample columns
    uniform_cols = []
    for x in range(0, width, max(1, width // 200)):  # Sample every ~0.5%
        col_pixels = [spritesheet.getpixel((x, y)) for y in range(0, height, max(1, height // 100))]
        if is_uniform(col_pixels):
            uniform_cols.append(x)

    # Sample rows
    uniform_rows = []
    for y in range(0, height, max(1, height // 200)):
        row_pixels = [spritesheet.getpixel((x, y)) for x in range(0, width, max(1, width // 100))]
        if is_uniform(row_pixels):
            uniform_rows.append(y)

    col_groups = _group_consecutive(uniform_cols)
    row_groups = _group_consecutive(uniform_rows)

    cols = len(col_groups) + 1 if col_groups else _estimate_dimension(width)
    rows = len(row_groups) + 1 if row_groups else _estimate_dimension(height)

    return (max(1, rows), max(1, cols))


def _group_consecutive(numbers: List[int], gap_threshold: int = 5) -> List[List[int]]:
    """Group consecutive numbers into ranges."""
    if not numbers:
        return []

    groups = []
    current_group = [numbers[0]]

    for n in numbers[1:]:
        if n - current_group[-1] <= gap_threshold:
            current_group.append(n)
        else:
            groups.append(current_group)
            current_group = [n]

    groups.append(current_group)
    return groups


def _estimate_dimension(size: int) -> int:
    """Estimate a reasonable grid dimension based on image size."""
    # Common sprite sheet sizes
    common_grids = [2, 3, 4, 5, 6, 8, 10, 12]

    for grid in common_grids:
        if size % grid == 0:
            frame_size = size // grid
            if 32 <= frame_size <= 512:  # Reasonable frame size
                return grid

    # Fallback: try to find a dimension that gives ~256px frames
    return max(1, size // 256)


def _fallback_grid_detection(width: int, height: int) -> Tuple[int, int]:
    """
    Fallback grid detection using common sprite sheet patterns.

    Tries common grid sizes and picks one that gives reasonable frame dimensions.
    """
    print("[INFO] Using fallback grid detection...")

    # Common sprite sheet grid sizes
    common_sizes = [
        (4, 4), (6, 6), (8, 8),     # Square grids
        (4, 6), (6, 4), (4, 8),    # Rectangular
        (2, 4), (4, 2), (2, 6),    # More rectangular
        (3, 4), (4, 3), (3, 6),    # Odd columns
        (1, 8), (1, 6), (1, 4),    # Single row
        (8, 1), (6, 1), (4, 1),    # Single column
    ]

    best_match = (4, 4)  # Default
    best_score = float('inf')

    for rows, cols in common_sizes:
        frame_w = width / cols
        frame_h = height / rows

        # Score based on how "square" the frames are and if dimensions divide evenly
        aspect_diff = abs(frame_w - frame_h) / max(frame_w, frame_h)
        remainder = (width % cols) + (height % rows)

        # Prefer: even division, square frames, reasonable size
        score = remainder * 10 + aspect_diff * 100

        if 32 <= frame_w <= 1024 and 32 <= frame_h <= 1024:
            if score < best_score:
                best_score = score
                best_match = (rows, cols)

    rows, cols = best_match
    print(f"[OK] Fallback grid: {rows} rows x {cols} columns")
    return best_match


# =============================================================================
# FRAME EXTRACTION
# =============================================================================

def extract_frames(
    spritesheet_path: Path,
    grid: Tuple[int, int],
    output_dir: Path
) -> List[Path]:
    """
    Extract individual frames from a sprite sheet.

    Args:
        spritesheet_path: Path to the sprite sheet PNG
        grid: Tuple of (rows, columns)
        output_dir: Directory to save extracted frames

    Returns:
        List of paths to extracted frame PNGs (in animation order: left-to-right, top-to-bottom)
    """
    print(f"[INFO] Extracting frames from: {spritesheet_path.name}")
    print(f"[INFO] Grid: {grid[0]} rows x {grid[1]} columns")

    output_dir.mkdir(parents=True, exist_ok=True)

    with Image.open(spritesheet_path) as img:
        width, height = img.size
        rows, cols = grid

        frame_width = width // cols
        frame_height = height // rows

        print(f"[INFO] Frame size: {frame_width}x{frame_height}")

        frames = []
        skipped_count = 0

        # Validate grid divides evenly
        if width % cols != 0 or height % rows != 0:
            print(f"[WARN] Grid {rows}x{cols} doesn't divide {width}x{height} evenly!")
            print(f"       Remainder: {width % cols}px horizontal, {height % rows}px vertical")

        # Extract frames left-to-right, top-to-bottom
        # CRITICAL: Use grid position for naming to maintain sequence alignment
        for row in range(rows):
            for col in range(cols):
                # Calculate crop box
                left = col * frame_width
                top = row * frame_height
                right = left + frame_width
                bottom = top + frame_height

                # Crop the frame
                frame = img.crop((left, top, right, bottom))

                # Calculate frame index from grid position (NOT running counter)
                grid_index = row * cols + col

                # Check if frame is not empty (has non-transparent pixels)
                if _is_frame_valid(frame):
                    # Save frame using GRID POSITION index (maintains sequence)
                    frame_path = output_dir / f"frame_{grid_index:03d}.png"
                    frame.save(frame_path, 'PNG')
                    frames.append(frame_path)
                else:
                    skipped_count += 1
                    print(f"  [SKIP] Empty frame at row {row}, col {col} (index {grid_index})")

        print(f"[OK] Extracted {len(frames)} valid frames to: {output_dir}")
        if skipped_count > 0:
            print(f"[INFO] Skipped {skipped_count} empty frames")
        return frames


def _is_frame_valid(frame: Image.Image, threshold: float = 0.001) -> bool:  # Reduced from 0.01 to preserve sparse frames
    """
    Check if a frame contains meaningful content (not empty/transparent).

    Args:
        frame: PIL Image frame
        threshold: Minimum percentage of non-transparent pixels (0-1)

    Returns:
        True if the frame has content, False if mostly empty
    """
    if frame.mode != 'RGBA':
        # Non-transparent images are assumed valid
        return True

    # Count non-transparent pixels
    alpha = frame.getchannel('A')
    pixels = list(alpha.getdata())
    non_transparent = sum(1 for p in pixels if p > 10)

    ratio = non_transparent / len(pixels)
    return ratio > threshold


# =============================================================================
# LOTTIE GENERATION
# =============================================================================

def create_lottie(
    frames: List[Path],
    output_path: Path,
    fps: int = 30,
    frame_hold: int = 3
) -> Path:
    """
    Create a Lottie JSON animation from a sequence of frame images.

    The animation embeds all frames as base64-encoded images, making it
    self-contained and portable.

    Args:
        frames: List of paths to frame PNG images (in order)
        output_path: Path for the output Lottie JSON file
        fps: Frames per second for playback (default 30)
        frame_hold: Number of Lottie frames to hold each sprite frame (default 2)
                    Higher values = slower animation
                    At 30fps with frame_hold=2, each sprite frame shows for ~67ms

    Returns:
        Path to the created Lottie JSON file

    Technical Notes:
        - Uses Lottie's image sequence feature
        - Each frame is a separate asset with a separate image layer
        - Layers are timed to appear/disappear in sequence
        - frame_hold controls animation speed independent of fps
    """
    print(f"[INFO] Creating Lottie animation from {len(frames)} frames")
    print(f"[INFO] Settings: {fps} fps, {frame_hold} frame hold")

    if not frames:
        raise ValueError("No frames provided for Lottie creation")

    # Load first frame to get dimensions
    with Image.open(frames[0]) as img:
        frame_width, frame_height = img.size

    # Calculate total animation length
    total_lottie_frames = len(frames) * frame_hold
    duration_seconds = total_lottie_frames / fps

    print(f"[INFO] Canvas size: {frame_width}x{frame_height}")
    print(f"[INFO] Animation duration: {duration_seconds:.2f}s ({total_lottie_frames} frames)")

    # Build assets array (embedded base64 images)
    assets = []
    for i, frame_path in enumerate(frames):
        print(f"  [EMBED] Frame {i + 1}/{len(frames)}: {frame_path.name}")

        with open(frame_path, 'rb') as f:
            frame_data = base64.b64encode(f.read()).decode('utf-8')

        with Image.open(frame_path) as img:
            w, h = img.size

        assets.append({
            "id": f"frame_{i:03d}",
            "w": w,
            "h": h,
            "e": 1,  # 1 = embedded (base64)
            "u": "",
            "p": f"data:image/png;base64,{frame_data}"
        })

    # Build layers (one per frame, timed to show in sequence)
    layers = []
    for i in range(len(frames)):
        # Calculate timing for this frame
        in_point = i * frame_hold
        out_point = (i + 1) * frame_hold

        # Image layer
        layer = {
            "ddd": 0,
            "ind": i + 1,
            "ty": 2,  # Image layer type
            "nm": f"Frame {i + 1}",
            "refId": f"frame_{i:03d}",
            "sr": 1,
            "ks": {
                "o": {"a": 0, "k": 100},  # Opacity 100%
                "r": {"a": 0, "k": 0},    # No rotation
                # Anchor at bottom-center to keep feet planted across frames
                "a": {"a": 0, "k": [frame_width / 2, frame_height, 0]},
                "p": {"a": 0, "k": [frame_width / 2, frame_height, 0]},
                "s": {"a": 0, "k": [100, 100, 100]}  # 100% scale
            },
            "ip": in_point,   # Layer appears at this frame
            "op": out_point,  # Layer disappears at this frame
            "st": 0
        }

        layers.append(layer)

    # Build complete Lottie structure
    lottie = {
        "v": "5.7.4",
        "fr": fps,
        "ip": 0,
        "op": total_lottie_frames,
        "w": frame_width,
        "h": frame_height,
        "nm": output_path.stem,
        "ddd": 0,
        "assets": assets,
        "layers": layers,
        "markers": []
    }

    # Save to file
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(lottie, f, indent=2)

    file_size = output_path.stat().st_size
    print(f"[OK] Created Lottie: {output_path}")
    print(f"[INFO] File size: {file_size:,} bytes ({file_size / 1024:.1f} KB)")

    return output_path


# =============================================================================
# MAIN PROCESSING
# =============================================================================

def process_ludo_asset(
    input_path: Path,
    output_path: Path,
    fps: int = 30,
    frame_hold: int = 2,
    grid: Optional[Tuple[int, int]] = None,
    keep_frames: bool = False
) -> Path:
    """
    Main entry point - process a Ludo.ai ZIP or sprite sheet PNG to Lottie.

    This function handles the complete pipeline:
    1. If ZIP: extract and find the sprite sheet
    2. Detect or use provided grid dimensions
    3. Extract individual frames
    4. Generate Lottie JSON with embedded frames

    Args:
        input_path: Path to ZIP file or sprite sheet PNG
        output_path: Path for the output Lottie JSON file
        fps: Frames per second (default 30)
        frame_hold: Frames to hold each sprite (default 2)
        grid: Optional (rows, cols) tuple; auto-detected if None
        keep_frames: If True, keep extracted frames in a subdirectory

    Returns:
        Path to the created Lottie JSON file

    Example:
        >>> process_ludo_asset(
        ...     Path("character_walk.zip"),
        ...     Path("character_walk.json"),
        ...     fps=24,
        ...     frame_hold=3
        ... )
    """
    print("=" * 60)
    print("SPRITE SHEET PROCESSOR - Ludo.ai to Lottie")
    print("=" * 60)
    print(f"Input: {input_path}")
    print(f"Output: {output_path}")
    print()

    # Determine working directory for temp files
    work_dir = output_path.parent / f".{output_path.stem}_temp"
    frames_dir = output_path.parent / f"{output_path.stem}_frames"

    try:
        # Step 1: Get sprite sheet path
        if input_path.suffix.lower() == '.zip':
            spritesheet_path = extract_zip(input_path, work_dir)
        elif input_path.suffix.lower() == '.png':
            spritesheet_path = input_path
        else:
            raise ValueError(f"Unsupported input format: {input_path.suffix}")

        # Step 2: Detect grid if not provided
        with Image.open(spritesheet_path) as img:
            if grid is None:
                grid = detect_grid(img)
            else:
                print(f"[INFO] Using provided grid: {grid[0]}x{grid[1]}")

        # Step 3: Extract frames
        frames = extract_frames(spritesheet_path, grid, frames_dir)

        if not frames:
            raise ValueError("No valid frames extracted from sprite sheet")

        # Step 4: Create Lottie
        result = create_lottie(frames, output_path, fps, frame_hold)

        print()
        print("=" * 60)
        print("[DONE] Processing complete!")
        print(f"  Lottie file: {result}")
        if keep_frames:
            print(f"  Frames directory: {frames_dir}")
        print("=" * 60)

        return result

    finally:
        # Cleanup temp files
        if work_dir.exists():
            import shutil
            shutil.rmtree(work_dir, ignore_errors=True)

        # Cleanup frames unless keeping them
        if not keep_frames and frames_dir.exists():
            import shutil
            shutil.rmtree(frames_dir, ignore_errors=True)


# =============================================================================
# BATCH PROCESSING
# =============================================================================

def batch_process(
    input_dir: Path,
    output_dir: Optional[Path] = None,
    fps: int = 30,
    frame_hold: int = 2,
    grid: Optional[Tuple[int, int]] = None,
    keep_frames: bool = False,
    force: bool = False
) -> int:
    """
    Batch process all ZIP files in a directory to Lottie animations.

    Args:
        input_dir: Directory containing ZIP files to process
        output_dir: Directory for output JSON files (default: same as input)
        fps: Frames per second (default 30)
        frame_hold: Frames to hold each sprite (default 2)
        grid: Optional (rows, cols) tuple; auto-detected if None
        keep_frames: If True, keep extracted frames in subdirectories
        force: If True, reprocess files even if output exists

    Returns:
        Exit code (0 for success, 1 for errors)
    """
    # Validate input directory
    if not input_dir.exists():
        print(f"[ERROR] Input directory not found: {input_dir}", file=sys.stderr)
        return 1

    if not input_dir.is_dir():
        print(f"[ERROR] Not a directory: {input_dir}", file=sys.stderr)
        return 1

    # Default output directory is same as input
    if output_dir is None:
        output_dir = input_dir
    else:
        output_dir.mkdir(parents=True, exist_ok=True)

    # Find all ZIP files
    zip_files = sorted(input_dir.glob("*.zip"))

    if not zip_files:
        print(f"[WARN] No ZIP files found in: {input_dir}")
        return 0

    print("=" * 60)
    print("BATCH SPRITE SHEET PROCESSOR")
    print("=" * 60)
    print(f"Input directory:  {input_dir}")
    print(f"Output directory: {output_dir}")
    print(f"Settings: {fps} fps, {frame_hold} frame hold")
    if grid:
        print(f"Grid: {grid[0]}x{grid[1]} (fixed)")
    else:
        print("Grid: auto-detect")
    print(f"Force reprocess: {force}")
    print()
    print(f"Processing {len(zip_files)} ZIP file(s)...")
    print()

    # Track results
    processed = 0
    skipped = 0
    failed = 0
    results = []

    for i, zip_file in enumerate(zip_files, 1):
        # Generate output filename from input filename
        output_name = zip_file.stem + ".json"
        output_path = output_dir / output_name

        # Check if output already exists
        if output_path.exists() and not force:
            status = "SKIPPED (exists)"
            skipped += 1
            results.append((zip_file.name, output_name, status))
            print(f"[{i}/{len(zip_files)}] {zip_file.name} -> {output_name} [{status}]")
            continue

        # Process the file
        try:
            # Suppress verbose output during batch processing
            # by redirecting stdout temporarily
            process_ludo_asset(
                input_path=zip_file,
                output_path=output_path,
                fps=fps,
                frame_hold=frame_hold,
                grid=grid,
                keep_frames=keep_frames
            )
            status = "OK"
            processed += 1
        except Exception as e:
            status = f"FAILED ({e})"
            failed += 1

        results.append((zip_file.name, output_name, status))

        # Print concise status for batch mode
        if status == "OK":
            print(f"[{i}/{len(zip_files)}] {zip_file.name} -> {output_name} [OK]")
        else:
            print(f"[{i}/{len(zip_files)}] {zip_file.name} -> {output_name} [{status}]")

    # Print summary
    print()
    print("=" * 60)
    print(f"Summary: {processed} processed, {skipped} skipped, {failed} failed")
    print("=" * 60)

    # Return error code if any failures
    return 1 if failed > 0 else 0


# =============================================================================
# CLI INTERFACE
# =============================================================================

def parse_grid(grid_str: str) -> Tuple[int, int]:
    """Parse grid string like '6x6' or '4x8' into (rows, cols) tuple."""
    parts = grid_str.lower().split('x')
    if len(parts) != 2:
        raise ValueError(f"Invalid grid format: {grid_str}. Use format like '6x6'")

    rows = int(parts[0])
    cols = int(parts[1])

    if rows < 1 or cols < 1:
        raise ValueError(f"Grid dimensions must be positive: {grid_str}")

    return (rows, cols)


def main():
    """CLI entry point for sprite sheet processor."""
    parser = argparse.ArgumentParser(
        description="Process Ludo.ai sprite sheets into Lottie animations",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Process a Ludo.ai ZIP download
  python spritesheet_processor.py process download.zip --output animation.json

  # Process a sprite sheet PNG with auto-detection
  python spritesheet_processor.py process spritesheet.png --output animation.json

  # Specify grid dimensions explicitly
  python spritesheet_processor.py process spritesheet.png --output animation.json --grid 6x6

  # Customize animation timing
  python spritesheet_processor.py process spritesheet.png --output animation.json --fps 24 --frame-hold 3

  # Keep extracted frames for inspection
  python spritesheet_processor.py process spritesheet.png --output animation.json --keep-frames

  # Batch process all ZIPs in a directory
  python spritesheet_processor.py batch ludo/downloads/ --output ../BennieGame/Resources/Lottie/

  # Batch with force reprocessing
  python spritesheet_processor.py batch ludo/downloads/ --output ludo/output/ --force

Grid Format:
  Use ROWSxCOLUMNS format, e.g.:
    --grid 4x4    (4 rows, 4 columns = 16 frames)
    --grid 6x8    (6 rows, 8 columns = 48 frames)
    --grid 1x10   (1 row, 10 columns = 10 frames, horizontal strip)

Frame Hold:
  Controls animation speed. Higher values = slower animation.
  At 30fps:
    --frame-hold 1  = 33ms per frame (fast)
    --frame-hold 2  = 67ms per frame (normal)
    --frame-hold 3  = 100ms per frame (slow)
        """
    )

    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Process command
    process_parser = subparsers.add_parser(
        'process',
        help='Process a sprite sheet ZIP or PNG into Lottie'
    )
    process_parser.add_argument(
        'input',
        type=Path,
        help='Input file (ZIP from Ludo.ai or sprite sheet PNG)'
    )
    process_parser.add_argument(
        '--output', '-o',
        type=Path,
        required=True,
        help='Output Lottie JSON file path'
    )
    process_parser.add_argument(
        '--grid', '-g',
        type=str,
        default=None,
        help='Grid dimensions as ROWSxCOLUMNS (e.g., "6x6"). Auto-detected if not specified.'
    )
    process_parser.add_argument(
        '--fps',
        type=int,
        default=30,
        help='Frames per second (default: 30)'
    )
    process_parser.add_argument(
        '--frame-hold',
        type=int,
        default=2,
        help='Lottie frames per sprite frame (default: 2). Higher = slower animation.'
    )
    process_parser.add_argument(
        '--keep-frames',
        action='store_true',
        help='Keep extracted frames in a subdirectory'
    )

    # Extract command (just extract frames, no Lottie)
    extract_parser = subparsers.add_parser(
        'extract',
        help='Extract frames from sprite sheet without creating Lottie'
    )
    extract_parser.add_argument(
        'input',
        type=Path,
        help='Input sprite sheet PNG or ZIP'
    )
    extract_parser.add_argument(
        '--output-dir', '-o',
        type=Path,
        required=True,
        help='Output directory for extracted frames'
    )
    extract_parser.add_argument(
        '--grid', '-g',
        type=str,
        default=None,
        help='Grid dimensions as ROWSxCOLUMNS (auto-detected if not specified)'
    )

    # Detect command (just detect grid, for debugging)
    detect_parser = subparsers.add_parser(
        'detect',
        help='Detect grid dimensions of a sprite sheet'
    )
    detect_parser.add_argument(
        'input',
        type=Path,
        help='Input sprite sheet PNG'
    )

    # Batch command (process all ZIPs in a directory)
    batch_parser = subparsers.add_parser(
        'batch',
        help='Batch process all ZIP files in a directory'
    )
    batch_parser.add_argument(
        'input_dir',
        type=Path,
        help='Input directory containing ZIP files'
    )
    batch_parser.add_argument(
        '--output', '-o',
        type=Path,
        default=None,
        help='Output directory for Lottie JSON files (default: same as input)'
    )
    batch_parser.add_argument(
        '--grid', '-g',
        type=str,
        default=None,
        help='Grid dimensions as ROWSxCOLUMNS (auto-detected if not specified)'
    )
    batch_parser.add_argument(
        '--fps',
        type=int,
        default=30,
        help='Frames per second (default: 30)'
    )
    batch_parser.add_argument(
        '--frame-hold',
        type=int,
        default=2,
        help='Lottie frames per sprite frame (default: 2)'
    )
    batch_parser.add_argument(
        '--keep-frames',
        action='store_true',
        help='Keep extracted frames in subdirectories'
    )
    batch_parser.add_argument(
        '--force',
        action='store_true',
        help='Reprocess files even if output already exists'
    )

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        return 1

    try:
        if args.command == 'process':
            # Parse grid if provided
            grid = parse_grid(args.grid) if args.grid else None

            process_ludo_asset(
                input_path=args.input,
                output_path=args.output,
                fps=args.fps,
                frame_hold=args.frame_hold,
                grid=grid,
                keep_frames=args.keep_frames
            )

        elif args.command == 'extract':
            # Parse grid if provided
            grid = parse_grid(args.grid) if args.grid else None

            # Handle ZIP input
            if args.input.suffix.lower() == '.zip':
                work_dir = args.output_dir / '.temp_extract'
                spritesheet_path = extract_zip(args.input, work_dir)
            else:
                spritesheet_path = args.input
                work_dir = None

            # Detect grid if not provided
            with Image.open(spritesheet_path) as img:
                if grid is None:
                    grid = detect_grid(img)

            # Extract frames
            extract_frames(spritesheet_path, grid, args.output_dir)

            # Cleanup temp
            if work_dir and work_dir.exists():
                import shutil
                shutil.rmtree(work_dir, ignore_errors=True)

        elif args.command == 'detect':
            if not args.input.exists():
                print(f"[ERROR] File not found: {args.input}", file=sys.stderr)
                return 1

            with Image.open(args.input) as img:
                rows, cols = detect_grid(img)
                width, height = img.size

            print()
            print("Detected Grid Information:")
            print(f"  Image size: {width}x{height}")
            print(f"  Grid: {rows} rows x {cols} columns")
            print(f"  Frame size: {width // cols}x{height // rows}")
            print(f"  Total frames: {rows * cols}")

        elif args.command == 'batch':
            return batch_process(
                input_dir=args.input_dir,
                output_dir=args.output,
                fps=args.fps,
                frame_hold=args.frame_hold,
                grid=parse_grid(args.grid) if args.grid else None,
                keep_frames=args.keep_frames,
                force=args.force
            )

        return 0

    except FileNotFoundError as e:
        print(f"[ERROR] File not found: {e}", file=sys.stderr)
        return 1
    except ValueError as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
