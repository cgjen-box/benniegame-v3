#!/usr/bin/env python3
"""
Generate Frame Strip from Lottie JSON

Creates a horizontal strip showing all animation frames side-by-side
for visual inspection. Helps detect jumbled/misaligned frames before deployment.

Usage:
    python generate_frame_strip.py input.json --output strip.png
    python generate_frame_strip.py input.json  # outputs to input_strip.png
"""

import argparse
import base64
import json
import sys
from io import BytesIO
from pathlib import Path

from PIL import Image


def extract_frames_from_lottie(lottie_path: Path) -> list[Image.Image]:
    """
    Extract all frames from a PNG-embedded Lottie file.

    Returns list of PIL Images in order.
    """
    with open(lottie_path, 'r') as f:
        data = json.load(f)

    frames = []

    # Lottie assets are in the "assets" array
    assets = data.get('assets', [])

    # Sort assets by ID to ensure correct order
    # Asset IDs are typically "image_0", "image_1", etc.
    def get_asset_index(asset):
        asset_id = asset.get('id', '')
        try:
            # Try to extract number from "image_N" format
            if asset_id.startswith('image_'):
                return int(asset_id.split('_')[1])
            return int(asset_id)
        except (ValueError, IndexError):
            return 0

    sorted_assets = sorted(assets, key=get_asset_index)

    for asset in sorted_assets:
        # Check if it's an image asset with embedded data
        if 'p' in asset and asset.get('e', 0) == 1:
            # Embedded image: p contains data URI
            data_uri = asset['p']
            if data_uri.startswith('data:image/png;base64,'):
                b64_data = data_uri.split(',', 1)[1]
                img_data = base64.b64decode(b64_data)
                img = Image.open(BytesIO(img_data))
                frames.append(img)

    return frames


def create_frame_strip(frames: list[Image.Image],
                       max_per_row: int = 0,
                       frame_size: tuple[int, int] = None) -> Image.Image:
    """
    Create a strip showing all frames side by side.

    Args:
        frames: List of PIL Images
        max_per_row: Max frames per row (0 = all in one row)
        frame_size: Target frame size (w, h) or None for original size

    Returns:
        Combined strip image
    """
    if not frames:
        raise ValueError("No frames to combine")

    # Resize frames if needed
    if frame_size:
        frames = [f.resize(frame_size, Image.Resampling.LANCZOS) for f in frames]

    # Get frame dimensions (assume all same size)
    fw, fh = frames[0].size

    # Calculate strip dimensions
    if max_per_row <= 0:
        cols = len(frames)
        rows = 1
    else:
        cols = min(len(frames), max_per_row)
        rows = (len(frames) + cols - 1) // cols

    strip_width = cols * fw
    strip_height = rows * fh

    # Create strip with transparent background
    strip = Image.new('RGBA', (strip_width, strip_height), (255, 255, 255, 0))

    # Paste frames
    for i, frame in enumerate(frames):
        row = i // cols
        col = i % cols
        x = col * fw
        y = row * fh

        # Ensure frame is RGBA
        if frame.mode != 'RGBA':
            frame = frame.convert('RGBA')

        strip.paste(frame, (x, y))

    return strip


def main():
    parser = argparse.ArgumentParser(
        description='Generate frame strip from Lottie JSON for visual verification'
    )
    parser.add_argument('input', help='Input Lottie JSON file')
    parser.add_argument('--output', '-o', help='Output PNG file (default: input_strip.png)')
    parser.add_argument('--max-per-row', '-r', type=int, default=14,
                        help='Max frames per row (0 for all in one row, default: 14)')
    parser.add_argument('--frame-size', '-s', type=int, nargs=2, metavar=('W', 'H'),
                        help='Resize frames to WxH (default: original size)')

    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"[ERROR] File not found: {input_path}")
        sys.exit(1)

    output_path = Path(args.output) if args.output else input_path.with_name(
        input_path.stem + '_strip.png'
    )

    print(f"[INFO] Loading Lottie: {input_path}")

    try:
        frames = extract_frames_from_lottie(input_path)
        print(f"[OK] Extracted {len(frames)} frames")

        if not frames:
            print("[ERROR] No frames found in Lottie file")
            sys.exit(1)

        frame_size = tuple(args.frame_size) if args.frame_size else None
        strip = create_frame_strip(frames, args.max_per_row, frame_size)

        # Save strip
        strip.save(output_path, 'PNG')
        print(f"[OK] Saved frame strip: {output_path}")
        print(f"[INFO] Strip size: {strip.size[0]}x{strip.size[1]} ({len(frames)} frames)")

    except Exception as e:
        print(f"[ERROR] Failed: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
