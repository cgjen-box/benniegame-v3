#!/usr/bin/env python3
"""
Lottie Animation Creator
========================
Create Lottie JSON animations from PNG frames.

Usage:
    python create_lottie.py --frames ./frames/*.png --output animation.json
"""

import argparse
import base64
import json
import sys
from pathlib import Path
from typing import List, Optional

try:
    from PIL import Image
except ImportError:
    print("[ERROR] Missing pillow package", file=sys.stderr)
    print("[INFO] Install with: pip install pillow", file=sys.stderr)
    sys.exit(1)


def encode_image_base64(image_path: Path) -> str:
    """Encode image to base64 data URL."""
    with open(image_path, "rb") as f:
        data = base64.b64encode(f.read()).decode("utf-8")
    return f"data:image/png;base64,{data}"


def get_image_dimensions(image_path: Path) -> tuple:
    """Get image width and height."""
    with Image.open(image_path) as img:
        return img.size


def create_lottie_from_frames(
    frame_paths: List[Path],
    output_path: Path,
    animation_name: str = "animation",
    fps: int = 30,
    frame_hold: int = 2,
) -> dict:
    """Create Lottie JSON from a sequence of PNG frames.

    Args:
        frame_paths: List of frame image paths in order
        output_path: Output JSON file path
        animation_name: Name for the animation
        fps: Frames per second
        frame_hold: Lottie frames per sprite frame

    Returns:
        Lottie JSON dictionary
    """
    if not frame_paths:
        raise ValueError("No frame paths provided")

    # Sort frames by name
    frame_paths = sorted(frame_paths)

    # Get dimensions from first frame
    width, height = get_image_dimensions(frame_paths[0])

    # Calculate total duration
    total_frames = len(frame_paths) * frame_hold

    print(f"Creating Lottie animation:")
    print(f"  Frames: {len(frame_paths)}")
    print(f"  Dimensions: {width}x{height}")
    print(f"  FPS: {fps}")
    print(f"  Frame hold: {frame_hold}")
    print(f"  Duration: {total_frames / fps:.2f}s")

    # Build assets array
    assets = []
    for i, frame_path in enumerate(frame_paths):
        asset = {
            "id": f"frame_{i:03d}",
            "w": width,
            "h": height,
            "e": 1,  # Embedded
            "u": "",
            "p": encode_image_base64(frame_path)
        }
        assets.append(asset)
        print(f"  Embedded: {frame_path.name}")

    # Build layers array
    layers = []
    for i in range(len(frame_paths)):
        in_point = i * frame_hold
        out_point = (i + 1) * frame_hold

        layer = {
            "ddd": 0,
            "ind": i + 1,
            "ty": 2,  # Image layer
            "nm": f"Frame {i}",
            "refId": f"frame_{i:03d}",
            "ip": in_point,
            "op": out_point,
            "st": 0,
            "bm": 0,
            "sr": 1,
            "ks": {
                "o": {"a": 0, "k": 100},
                "r": {"a": 0, "k": 0},
                "p": {"a": 0, "k": [width / 2, height / 2, 0]},
                "a": {"a": 0, "k": [width / 2, height / 2, 0]},
                "s": {"a": 0, "k": [100, 100, 100]}
            }
        }
        layers.append(layer)

    # Build Lottie JSON
    lottie = {
        "v": "5.7.4",
        "fr": fps,
        "ip": 0,
        "op": total_frames,
        "w": width,
        "h": height,
        "nm": animation_name,
        "ddd": 0,
        "assets": assets,
        "layers": layers,
        "markers": []
    }

    # Write output
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(lottie, f, separators=(",", ":"))

    print(f"\nCreated: {output_path}")
    print(f"Size: {output_path.stat().st_size / 1024:.1f} KB")

    return lottie


def create_breathing_animation(
    image_path: Path,
    output_path: Path,
    animation_name: str = "breathing",
    fps: int = 30,
    duration: float = 3.0,
    scale_amount: float = 3.0,
) -> dict:
    """Create a breathing/pulsing animation from a single image.

    Args:
        image_path: Source image path
        output_path: Output JSON file path
        animation_name: Name for the animation
        fps: Frames per second
        duration: Animation duration in seconds
        scale_amount: Percentage to scale (e.g., 3.0 = 3%)

    Returns:
        Lottie JSON dictionary
    """
    width, height = get_image_dimensions(image_path)
    total_frames = int(fps * duration)
    half_frames = total_frames // 2

    print(f"Creating breathing animation:")
    print(f"  Source: {image_path.name}")
    print(f"  Scale: {scale_amount}%")
    print(f"  Duration: {duration}s")

    # Build asset
    asset = {
        "id": "character_img",
        "w": width,
        "h": height,
        "e": 1,
        "u": "",
        "p": encode_image_base64(image_path)
    }

    # Build layer with scale animation
    layer = {
        "ddd": 0,
        "ind": 1,
        "ty": 2,
        "nm": "Character",
        "refId": "character_img",
        "ip": 0,
        "op": total_frames,
        "st": 0,
        "bm": 0,
        "sr": 1,
        "ks": {
            "o": {"a": 0, "k": 100},
            "r": {"a": 0, "k": 0},
            "p": {"a": 0, "k": [width / 2, height, 0]},  # Bottom-center anchor
            "a": {"a": 0, "k": [width / 2, height, 0]},
            "s": {
                "a": 1,
                "k": [
                    {
                        "t": 0,
                        "s": [100, 100, 100],
                        "i": {"x": [0.4], "y": [0]},
                        "o": {"x": [0.6], "y": [1]}
                    },
                    {
                        "t": half_frames,
                        "s": [100 + scale_amount, 100 + scale_amount, 100],
                        "i": {"x": [0.4], "y": [0]},
                        "o": {"x": [0.6], "y": [1]}
                    },
                    {
                        "t": total_frames,
                        "s": [100, 100, 100]
                    }
                ]
            }
        }
    }

    # Build Lottie JSON
    lottie = {
        "v": "5.7.4",
        "fr": fps,
        "ip": 0,
        "op": total_frames,
        "w": width,
        "h": height,
        "nm": animation_name,
        "ddd": 0,
        "assets": [asset],
        "layers": [layer],
        "markers": []
    }

    # Write output
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(lottie, f, separators=(",", ":"))

    print(f"\nCreated: {output_path}")
    print(f"Size: {output_path.stat().st_size / 1024:.1f} KB")

    return lottie


def main():
    parser = argparse.ArgumentParser(description="Create Lottie animations")
    subparsers = parser.add_subparsers(dest="command", help="Command")

    # Frames command
    frames_parser = subparsers.add_parser("frames", help="Create from frame sequence")
    frames_parser.add_argument("--frames", "-f", nargs="+", required=True,
                               help="Frame image paths (in order)")
    frames_parser.add_argument("--output", "-o", required=True, help="Output JSON path")
    frames_parser.add_argument("--name", "-n", default="animation", help="Animation name")
    frames_parser.add_argument("--fps", type=int, default=30, help="Frames per second")
    frames_parser.add_argument("--frame-hold", type=int, default=2,
                               help="Lottie frames per sprite frame")

    # Breathing command
    breath_parser = subparsers.add_parser("breathing", help="Create breathing animation")
    breath_parser.add_argument("--image", "-i", required=True, help="Source image path")
    breath_parser.add_argument("--output", "-o", required=True, help="Output JSON path")
    breath_parser.add_argument("--name", "-n", default="breathing", help="Animation name")
    breath_parser.add_argument("--fps", type=int, default=30, help="Frames per second")
    breath_parser.add_argument("--duration", type=float, default=3.0,
                               help="Duration in seconds")
    breath_parser.add_argument("--scale", type=float, default=3.0,
                               help="Scale percentage")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    try:
        if args.command == "frames":
            frame_paths = [Path(p) for p in args.frames]
            create_lottie_from_frames(
                frame_paths=frame_paths,
                output_path=Path(args.output),
                animation_name=args.name,
                fps=args.fps,
                frame_hold=args.frame_hold,
            )

        elif args.command == "breathing":
            create_breathing_animation(
                image_path=Path(args.image),
                output_path=Path(args.output),
                animation_name=args.name,
                fps=args.fps,
                duration=args.duration,
                scale_amount=args.scale,
            )

        return 0

    except Exception as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
