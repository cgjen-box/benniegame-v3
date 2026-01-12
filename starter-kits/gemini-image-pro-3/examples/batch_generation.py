#!/usr/bin/env python3
"""
Example: Batch generate multiple character variations.

Use this to generate a full set of character expressions or poses
using a frozen reference image for consistency.
"""

import subprocess
import sys
from pathlib import Path
import time

# Configuration
REFERENCE_IMAGE = "path/to/character_reference.png"  # Change this!
CHARACTER_NAME = "mycharacter"

# Define all variations to generate
VARIATIONS = [
    {"name": "idle", "prompt": "Character in relaxed neutral pose, arms at sides"},
    {"name": "happy", "prompt": "Character happy and smiling, slight bounce"},
    {"name": "thinking", "prompt": "Character thinking, hand on chin, looking up"},
    {"name": "excited", "prompt": "Character excited, arms raised slightly"},
    {"name": "waving", "prompt": "Character waving hello, one arm raised"},
    {"name": "pointing", "prompt": "Character pointing to the right"},
]

def generate_variation(name: str, prompt: str, reference: str):
    """Generate a single variation."""
    output_name = f"{CHARACTER_NAME}-{name}"
    cmd = [
        sys.executable, "generate_image.py", "generate",
        f"Same character: {prompt}",
        "--name", output_name,
        "--reference", reference,
        "--raw",
        "--count", "4"
    ]

    print(f"\nGenerating: {output_name}")
    print(f"Prompt: {prompt}")

    result = subprocess.run(cmd, capture_output=False)
    return result.returncode == 0

def main():
    """Generate all variations."""
    print("=" * 60)
    print("  Batch Generation")
    print("=" * 60)
    print(f"Reference: {REFERENCE_IMAGE}")
    print(f"Character: {CHARACTER_NAME}")
    print(f"Variations: {len(VARIATIONS)}")
    print("=" * 60)

    # Check reference exists
    if not Path(REFERENCE_IMAGE).exists():
        print(f"\nERROR: Reference image not found: {REFERENCE_IMAGE}")
        print("Please update REFERENCE_IMAGE in this script.")
        return 1

    # Generate each variation
    success = 0
    failed = 0

    for var in VARIATIONS:
        if generate_variation(var["name"], var["prompt"], REFERENCE_IMAGE):
            success += 1
        else:
            failed += 1

        # Small delay between generations to avoid rate limits
        time.sleep(2)

    # Summary
    print("\n" + "=" * 60)
    print("  Batch Complete")
    print("=" * 60)
    print(f"Success: {success}")
    print(f"Failed: {failed}")
    print(f"\nOutput in: ./generated/{CHARACTER_NAME}-*.png")

    return 0 if failed == 0 else 1

if __name__ == "__main__":
    sys.exit(main())
