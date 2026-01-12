#!/usr/bin/env python3
"""
Example: Run a training session with A/B comparison and feedback.

Training sessions help you build a pattern database by comparing
variations and recording which techniques work better.
"""

import subprocess
import sys

# Configuration
SESSION_NAME = "character-training"
CHARACTER = "bennie"  # or "lemminge", or None for generic
PROMPTS = [
    "Character standing in neutral pose",
    "Character happy and celebrating",
    "Character thinking with hand on chin",
]

def start_session():
    """Start a new training session."""
    cmd = [
        sys.executable, "generate_image.py", "session", "start",
        "--name", SESSION_NAME,
        "--character", CHARACTER,
    ]
    print("Starting training session...")
    subprocess.run(cmd)

def generate_round(prompt: str, round_num: int):
    """Generate A/B variations for a prompt."""
    output_name = f"{SESSION_NAME}-round{round_num}"
    cmd = [
        sys.executable, "generate_image.py", "generate",
        prompt,
        "--name", output_name,
        "--character", CHARACTER,
        "--training",  # A/B comparison mode
        "--count", "2"
    ]
    print(f"\nRound {round_num}: {prompt}")
    subprocess.run(cmd)

def main():
    """Run full training session."""
    print("=" * 60)
    print("  Training Session Example")
    print("=" * 60)

    # Start session
    start_session()

    # Generate rounds
    for i, prompt in enumerate(PROMPTS, 1):
        generate_round(prompt, i)
        print("\n" + "-" * 40)
        print("Review the A/B images and provide feedback:")
        print(f"  python generate_image.py feedback {SESSION_NAME} round{i} A")
        print(f"  python generate_image.py feedback {SESSION_NAME} round{i} B")
        print("-" * 40)

    print("\n" + "=" * 60)
    print("Session complete! To finish:")
    print(f"  python generate_image.py session complete {SESSION_NAME}")
    print("=" * 60)

if __name__ == "__main__":
    main()
