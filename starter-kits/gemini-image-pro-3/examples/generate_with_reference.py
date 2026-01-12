#!/usr/bin/env python3
"""
Example: Generate images with reference image for character consistency.

This is the recommended approach for maintaining character identity across
multiple generations.
"""

import subprocess
import sys
from pathlib import Path

# Configuration
REFERENCE_IMAGE = "path/to/your/perfect_reference.png"  # Change this!
OUTPUT_NAME = "character-variation"
PROMPT = "Same character celebrating with arms raised, happy expression"

def main():
    """Generate images using reference image technique."""

    # Build command
    cmd = [
        sys.executable, "generate_image.py", "generate",
        PROMPT,
        "--name", OUTPUT_NAME,
        "--reference", REFERENCE_IMAGE,
        "--raw",  # Use prompt as-is
        "--count", "4"
    ]

    print(f"Generating with reference: {REFERENCE_IMAGE}")
    print(f"Prompt: {PROMPT}")
    print()

    # Run generation
    result = subprocess.run(cmd, capture_output=False)

    if result.returncode == 0:
        print(f"\nSuccess! Check output in ./generated/{OUTPUT_NAME}_*.png")
    else:
        print(f"\nGeneration failed with code {result.returncode}")

    return result.returncode

if __name__ == "__main__":
    sys.exit(main())
