#!/usr/bin/env python3
"""
Validate Lottie Animation File

Automated quality checks for Lottie animations:
- Frame count validation
- Dimension consistency
- Duration reasonableness
- Asset/layer integrity

Usage:
    python validate_lottie.py animation.json
    python validate_lottie.py --all BennieGame/Resources/Lottie/
"""

import argparse
import base64
import json
import sys
from io import BytesIO
from pathlib import Path

from PIL import Image


class ValidationResult:
    def __init__(self, name: str):
        self.name = name
        self.errors = []
        self.warnings = []
        self.info = []

    def error(self, msg: str):
        self.errors.append(msg)

    def warn(self, msg: str):
        self.warnings.append(msg)

    def add_info(self, msg: str):
        self.info.append(msg)

    @property
    def passed(self) -> bool:
        return len(self.errors) == 0

    def print_report(self):
        status = "PASS" if self.passed else "FAIL"
        print(f"\n{'='*60}")
        print(f"Validation: {self.name} - [{status}]")
        print(f"{'='*60}")

        if self.info:
            for msg in self.info:
                print(f"  [INFO] {msg}")

        if self.warnings:
            for msg in self.warnings:
                print(f"  [WARN] {msg}")

        if self.errors:
            for msg in self.errors:
                print(f"  [ERROR] {msg}")

        if self.passed and not self.warnings:
            print("  All checks passed!")


def validate_lottie(lottie_path: Path) -> ValidationResult:
    """
    Validate a Lottie animation file.

    Returns ValidationResult with errors/warnings.
    """
    result = ValidationResult(lottie_path.name)

    # Check file exists
    if not lottie_path.exists():
        result.error(f"File not found: {lottie_path}")
        return result

    # Load JSON
    try:
        with open(lottie_path, 'r') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        result.error(f"Invalid JSON: {e}")
        return result

    # Basic Lottie structure checks
    if 'v' not in data:
        result.error("Missing 'v' (version) field - not a valid Lottie file")
        return result

    result.add_info(f"Lottie version: {data.get('v', 'unknown')}")

    # Frame rate and duration
    ip = data.get('ip', 0)  # In point (start frame)
    op = data.get('op', 0)  # Out point (end frame)
    fr = data.get('fr', 30)  # Frame rate

    total_frames = op - ip
    duration = total_frames / fr if fr > 0 else 0

    result.add_info(f"Frame range: {ip} - {op} ({total_frames} frames)")
    result.add_info(f"Frame rate: {fr} fps")
    result.add_info(f"Duration: {duration:.2f} seconds")

    # Duration checks
    if duration < 0.5:
        result.warn(f"Very short duration ({duration:.2f}s) - may look choppy")
    elif duration > 10:
        result.warn(f"Long duration ({duration:.2f}s) - may be slow to load")

    # Canvas dimensions
    w = data.get('w', 0)
    h = data.get('h', 0)
    result.add_info(f"Canvas size: {w}x{h}")

    if w <= 0 or h <= 0:
        result.error(f"Invalid canvas dimensions: {w}x{h}")

    # Check assets
    assets = data.get('assets', [])
    result.add_info(f"Asset count: {len(assets)}")

    if len(assets) == 0:
        result.warn("No assets found - animation may be vector-only or empty")

    # Validate each image asset
    frame_sizes = []
    for i, asset in enumerate(assets):
        if 'p' in asset and asset.get('e', 0) == 1:
            # Embedded image
            data_uri = asset['p']
            if data_uri.startswith('data:image/png;base64,'):
                try:
                    b64_data = data_uri.split(',', 1)[1]
                    img_data = base64.b64decode(b64_data)
                    img = Image.open(BytesIO(img_data))
                    frame_sizes.append(img.size)
                except Exception as e:
                    result.error(f"Asset {i} ({asset.get('id', 'unknown')}): Invalid image data - {e}")

    # Check frame size consistency
    if frame_sizes:
        unique_sizes = set(frame_sizes)
        if len(unique_sizes) > 1:
            result.warn(f"Inconsistent frame sizes: {unique_sizes}")
        else:
            result.add_info(f"Frame dimensions: {frame_sizes[0][0]}x{frame_sizes[0][1]}")

        # Check expected frame count (Ludo.ai typically generates 42 frames)
        expected_frames = [42, 36, 24, 12, 8]  # Common frame counts
        if len(frame_sizes) not in expected_frames:
            result.warn(f"Unusual frame count ({len(frame_sizes)}) - expected one of {expected_frames}")

    # Check layers
    layers = data.get('layers', [])
    result.add_info(f"Layer count: {len(layers)}")

    if len(layers) == 0:
        result.error("No layers found - animation is empty")

    # Check for sequence layer (animated sprite)
    has_sequence = False
    for layer in layers:
        if layer.get('ty') == 2:  # Image layer
            has_sequence = True
            # Check if it references assets
            ref_id = layer.get('refId', '')
            if not any(a.get('id') == ref_id for a in assets):
                result.warn(f"Layer references missing asset: {ref_id}")

    if not has_sequence and assets:
        result.warn("Has assets but no image layers - frames may not animate")

    return result


def validate_directory(dir_path: Path) -> list[ValidationResult]:
    """Validate all Lottie files in a directory."""
    results = []
    lottie_files = list(dir_path.glob('*.json'))

    if not lottie_files:
        print(f"No .json files found in {dir_path}")
        return results

    for lottie_file in sorted(lottie_files):
        results.append(validate_lottie(lottie_file))

    return results


def main():
    parser = argparse.ArgumentParser(
        description='Validate Lottie animation files'
    )
    parser.add_argument('input', help='Input Lottie JSON file or directory')
    parser.add_argument('--all', '-a', action='store_true',
                        help='Validate all .json files in directory')

    args = parser.parse_args()

    input_path = Path(args.input)

    if args.all or input_path.is_dir():
        if not input_path.is_dir():
            print(f"[ERROR] Not a directory: {input_path}")
            sys.exit(1)

        results = validate_directory(input_path)

        # Print summary
        passed = sum(1 for r in results if r.passed)
        total = len(results)

        print(f"\n{'='*60}")
        print(f"SUMMARY: {passed}/{total} files passed validation")
        print(f"{'='*60}")

        for r in results:
            r.print_report()

        sys.exit(0 if passed == total else 1)

    else:
        result = validate_lottie(input_path)
        result.print_report()
        sys.exit(0 if result.passed else 1)


if __name__ == '__main__':
    main()
