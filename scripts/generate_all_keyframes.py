#!/usr/bin/env python3
"""
Generate all keyframes for Ludo.ai animation pipeline using Gemini.

This script generates START and END keyframe pairs for all 13 character animations
(7 Bennie + 6 Lemminge) needed for the animation pipeline.

Usage:
    python scripts/generate_all_keyframes.py

Output:
    design/generated/Animations/keyframes/
    ├── bennie_idle/
    │   ├── start.png
    │   └── end.png
    ... (13 total directories)
"""

import os
import sys
import json
import base64
from pathlib import Path
from datetime import datetime
from typing import Optional, Tuple, List
import time

# Add path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "starter-kits" / "gemini-image-pro-3"))

try:
    from google import genai
    from google.genai import types
    from PIL import Image
except ImportError as e:
    print(f"[ERROR] Missing dependency: {e}")
    print("[INFO] Install with: pip install google-genai pillow python-dotenv")
    sys.exit(1)

# =============================================================================
# CONFIGURATION
# =============================================================================

PROJECT_ROOT = Path(__file__).parent.parent
OUTPUT_DIR = PROJECT_ROOT / "design" / "generated" / "Animations" / "keyframes"
BENNIE_REF = PROJECT_ROOT / "design" / "references" / "character" / "bennie" / "reference" / "bennie-reference.png"
LEMMINGE_REF = PROJECT_ROOT / "design" / "references" / "character" / "lemminge" / "reference" / "lemminge-reference.png"

# Characters and their emotions
ANIMATIONS = {
    "bennie": ["idle", "happy", "thinking", "encouraging", "celebrating", "waving", "pointing"],
    "lemminge": ["idle", "curious", "excited", "celebrating", "hiding", "mischievous"],
}

# =============================================================================
# KEYFRAME PROMPTS
# =============================================================================

KEYFRAME_PROMPTS = {
    "bennie": {
        "idle": {
            "start": "standing relaxed with arms at sides, eyes open, gentle smile, feet flat on ground",
            "end": "same pose, chest slightly expanded (breathing in), subtle shift in stance",
        },
        "happy": {
            "start": "standing with arms at sides, happy expression, feet flat on ground, slight smile",
            "end": "slight bounce up with feet lifting, arms slightly raised, eyes squinted with joy, big smile",
        },
        "thinking": {
            "start": "standing with one paw raised near chin, eyes looking up thoughtfully, curious expression",
            "end": "head tilted slightly to other side, paw still on chin, eyes looking up-right",
        },
        "encouraging": {
            "start": "standing with arms close to body, supportive warm expression, slight lean forward",
            "end": "arms open wide in welcoming gesture, warm encouraging smile, slight nod",
        },
        "celebrating": {
            "start": "standing with arms at sides, excited expression, feet on ground",
            "end": "arms raised high above head in victory pose, eyes closed with joy, slight jump",
        },
        "waving": {
            "start": "one arm raised at shoulder height, paw facing forward, friendly smile",
            "end": "same arm extended higher, paw tilted sideways in classic wave, warm expression",
        },
        "pointing": {
            "start": "standing with arms relaxed, looking forward, alert expression",
            "end": "one arm fully extended pointing right, head turned to look at pointed direction",
        },
    },
    "lemminge": {
        "idle": {
            "start": "standing upright, round body slightly compressed, arms at sides, eyes looking forward",
            "end": "same pose, body slightly expanded (breathing), eyes blinking",
        },
        "curious": {
            "start": "standing upright, head straight, wide curious eyes, ears up",
            "end": "head tilted to one side, leaning forward slightly, eyes even wider",
        },
        "excited": {
            "start": "standing on ground, arms at sides, huge excited eyes, feet flat",
            "end": "mid-bounce with feet off ground, arms raised high, eyes sparkling",
        },
        "celebrating": {
            "start": "standing with arms at sides, big excited smile showing buck teeth",
            "end": "arms raised high in victory, slight jump, eyes closed with pure joy",
        },
        "hiding": {
            "start": "standing partially visible, paws near face, nervous eyes",
            "end": "crouched lower, paws covering more of face, body compressed into shy pose",
        },
        "mischievous": {
            "start": "standing with hands together in front, looking forward, slight grin",
            "end": "hands rubbing together, sideways glance, impish sneaky grin showing teeth",
        },
    },
}

# =============================================================================
# STYLE TEMPLATES
# =============================================================================

BENNIE_STYLE = """
KEYFRAME IMAGE FOR LUDO.AI ANIMATION:

Character: Bennie the Bear
Style: 2D vector art, cartoon illustration, clean digital art, cel-shaded
Body: Adult brown bear proportions (NOT chibi or cute), pear-shaped body
Colors: Chocolate brown fur (#8C7259), lighter tan snout area only (#FAF5EB)
Eyes: Small round dark eyes with white highlights
Nose: Large dark espresso brown triangular nose (#5A4A3A)
Outlines: Thick dark cel-shaded outlines
Background: TRANSPARENT (alpha channel)

POSE FOR THIS KEYFRAME:
{pose_description}

CRITICAL REQUIREMENTS:
- EXACT same character design as reference image
- NO CLOTHING on Bennie - never add vest, scarf, hat or any accessories
- Full body visible with feet on ground
- TRANSPARENT background (PNG alpha)
- Pose matches description precisely
- Arms clearly attached to body
- Consistent proportions throughout
"""

LEMMINGE_STYLE = """
KEYFRAME IMAGE FOR LUDO.AI ANIMATION:

Character: Single Lemming creature (NOT Bennie, NOT a bear)
Style: Flat 2D vector art, Go gopher mascot style, thick bold outlines, cel-shaded
Body: Round blue potato-shaped blob creature (#6FA8DC soft blue)
Belly: White patch (#FFFFFF) with fuzzy edge
Eyes: Large round friendly eyes with small black pupils
Features: Prominent buck teeth ALWAYS visible, small pink nose (#E8A0A0)
Paws: Stubby nub hands and feet with pink paw pads
Ears: Two small rounded ears on top of head
Outlines: Thick bold black cel-shaded outlines
Background: TRANSPARENT (alpha channel)

POSE FOR THIS KEYFRAME:
{pose_description}

CRITICAL REQUIREMENTS:
- EXACT same character design as reference image
- ONLY ONE character (single Lemming)
- NOT a bear, NOT brown colored
- Buck teeth visible in all frames
- Full body visible
- TRANSPARENT background (PNG alpha)
- Pose matches description precisely
"""

# =============================================================================
# GENERATION FUNCTIONS
# =============================================================================

def get_api_key() -> str:
    """Get Gemini API key from environment or .env file."""
    key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not key:
        # Try to load directly from .env file
        env_path = PROJECT_ROOT / ".env"
        if env_path.exists():
            for line in env_path.read_text().splitlines():
                if line.startswith("GOOGLE_API_KEY="):
                    key = line.split("=", 1)[1].strip()
                    break
    if not key:
        raise ValueError("GEMINI_API_KEY or GOOGLE_API_KEY environment variable not set")
    return key

# Gemini 3 Pro Image Preview - best for character consistency
# Supports up to 14 reference images and 4K resolution
IMAGE_MODEL = "gemini-3-pro-image-preview"


def load_reference_image(ref_path: Path) -> Optional[Image.Image]:
    """Load reference image for character consistency."""
    if ref_path.exists():
        return Image.open(ref_path)
    print(f"[WARN] Reference image not found: {ref_path}")
    return None


def generate_keyframe(
    client,
    character: str,
    emotion: str,
    pose_type: str,  # "start" or "end"
    pose_description: str,
    reference_image: Optional[Image.Image],
    output_path: Path,
    max_retries: int = 3,
) -> bool:
    """Generate a single keyframe image with retry logic."""

    # Select style template
    if character == "bennie":
        template = BENNIE_STYLE
    else:
        template = LEMMINGE_STYLE

    prompt = template.format(pose_description=pose_description)

    # Build content with reference image first
    contents = []
    if reference_image:
        contents.append(reference_image)
        prompt = f"""REFERENCE IMAGE PROVIDED - Match this character EXACTLY.

{prompt}

CRITICAL: The generated image must match the reference character design exactly.
Maintain all proportions, colors, and style details from the reference."""

    contents.append(prompt)

    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model=IMAGE_MODEL,  # Gemini 3 Pro Image Preview
                contents=contents if len(contents) > 1 else prompt,
                config=types.GenerateContentConfig(
                    response_modalities=["IMAGE", "TEXT"],
                    # Gemini 3 Pro supports image_config for resolution control
                    image_config=types.ImageConfig(
                        aspect_ratio="1:1",  # Square for animation keyframes
                        image_size="2K",     # 2K resolution for quality
                    ),
                ),
            )

            # Extract image from response
            if response.candidates:
                for part in response.candidates[0].content.parts:
                    if hasattr(part, 'inline_data') and part.inline_data:
                        if 'image' in part.inline_data.mime_type:
                            image_data = part.inline_data.data
                            if isinstance(image_data, str):
                                image_data = base64.b64decode(image_data)

                            # Save image
                            output_path.parent.mkdir(parents=True, exist_ok=True)
                            with open(output_path, 'wb') as f:
                                f.write(image_data)
                            return True

            print(f"[WARN] No image in response for {character}_{emotion}_{pose_type}")
            return False

        except Exception as e:
            error_str = str(e).lower()
            # Check if it's a rate limit error
            if '429' in str(e) or 'resource_exhausted' in error_str or 'quota' in error_str:
                wait_time = 15 * (attempt + 1)  # 15s, 30s, 45s
                print(f"[RATE LIMIT] Waiting {wait_time}s before retry {attempt + 1}/{max_retries}...")
                time.sleep(wait_time)
                continue
            else:
                print(f"[ERROR] Failed to generate {character}_{emotion}_{pose_type}: {e}")
                return False

    print(f"[ERROR] Max retries exceeded for {character}_{emotion}_{pose_type}")
    return False


def generate_animation_keyframes(
    client,
    character: str,
    emotion: str,
    reference_image: Optional[Image.Image],
) -> Tuple[Optional[Path], Optional[Path]]:
    """Generate START and END keyframes for an animation."""

    prompts = KEYFRAME_PROMPTS.get(character, {}).get(emotion)
    if not prompts:
        print(f"[ERROR] No prompts defined for {character}_{emotion}")
        return None, None

    output_dir = OUTPUT_DIR / f"{character}_{emotion}"
    start_path = output_dir / "start.png"
    end_path = output_dir / "end.png"

    print(f"\n[{character}_{emotion}] Generating keyframes...")

    # Generate START frame
    print(f"  [START] {prompts['start'][:50]}...")
    start_ok = generate_keyframe(
        client, character, emotion, "start",
        prompts["start"], reference_image, start_path
    )

    if start_ok:
        print(f"  [START] OK: {start_path.name}")
    else:
        print(f"  [START] FAILED")

    # Small delay to avoid rate limits (API allows ~10 req/min)
    time.sleep(3)

    # Generate END frame
    print(f"  [END] {prompts['end'][:50]}...")
    end_ok = generate_keyframe(
        client, character, emotion, "end",
        prompts["end"], reference_image, end_path
    )

    if end_ok:
        print(f"  [END] OK: {end_path.name}")
    else:
        print(f"  [END] FAILED")

    # Delay between animations to respect rate limits
    time.sleep(3)

    return (start_path if start_ok else None, end_path if end_ok else None)


def main():
    """Generate all keyframes for all animations."""
    print("=" * 60)
    print("BENNIE BEAR - KEYFRAME GENERATOR")
    print("=" * 60)
    print(f"Output: {OUTPUT_DIR}")
    print()

    # Initialize client
    api_key = get_api_key()
    client = genai.Client(api_key=api_key)

    # Load reference images
    bennie_ref = load_reference_image(BENNIE_REF)
    lemminge_ref = load_reference_image(LEMMINGE_REF)

    if bennie_ref:
        print(f"[REF] Loaded Bennie reference: {BENNIE_REF.name}")
    if lemminge_ref:
        print(f"[REF] Loaded Lemminge reference: {LEMMINGE_REF.name}")

    # Track results
    results = {"success": [], "failed": []}
    total = sum(len(emotions) for emotions in ANIMATIONS.values())
    current = 0

    # Generate all keyframes
    for character, emotions in ANIMATIONS.items():
        ref_image = bennie_ref if character == "bennie" else lemminge_ref

        for emotion in emotions:
            current += 1
            print(f"\n[{current}/{total}] {character}_{emotion}")

            start_path, end_path = generate_animation_keyframes(
                client, character, emotion, ref_image
            )

            if start_path and end_path:
                results["success"].append(f"{character}_{emotion}")
            else:
                results["failed"].append(f"{character}_{emotion}")

    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Success: {len(results['success'])}/{total}")
    print(f"Failed:  {len(results['failed'])}/{total}")

    if results["failed"]:
        print("\nFailed animations:")
        for name in results["failed"]:
            print(f"  - {name}")

    # Verify output
    print("\n[VERIFY] Checking output directory...")
    dirs = list(OUTPUT_DIR.glob("*/"))
    files = list(OUTPUT_DIR.glob("*/*.png"))
    print(f"  Directories: {len(dirs)}")
    print(f"  PNG files:   {len(files)}")

    if len(files) >= 26:
        print("\n[OK] All keyframes generated successfully!")
        return 0
    else:
        print(f"\n[WARN] Expected 26 files, got {len(files)}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
