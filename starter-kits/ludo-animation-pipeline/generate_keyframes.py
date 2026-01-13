#!/usr/bin/env python3
"""
Keyframe Generator for Ludo.ai Animation Pipeline
==================================================
Generates start and end frame images for Ludo.ai interpolation
using Gemini 3.0 Pro Image Preview.

The keyframes are used as visual references for Ludo.ai to generate
smooth sprite animations while maintaining character consistency.

Usage:
    # Generate keyframes for a single animation
    python generate_keyframes.py bennie waving

    # Generate keyframes for all emotions
    python generate_keyframes.py bennie --all

    # Custom output directory
    python generate_keyframes.py lemminge excited --output-dir ./my_keyframes

Dependencies:
    - Gemini 3.0 API (via generate_image.py)
    - Frozen character references in public/images/generated/characters/
"""

import sys
import json
import argparse
from pathlib import Path
from dataclasses import dataclass
from typing import Optional, Tuple, Dict, Any
from datetime import datetime

# Add gemini-image-pro-3 directory for imports
gemini_kit_path = Path(__file__).parent.parent / 'gemini-image-pro-3'
sys.path.insert(0, str(gemini_kit_path))

try:
    from generate_image import generate_single, CONFIG, log
    from reference_style import get_reference_prompt_prefix
except ImportError as e:
    print(f"[ERROR] Failed to import from gemini-image-pro-3: {e}", file=sys.stderr)
    print(f"[INFO] Expected path: {gemini_kit_path}", file=sys.stderr)
    sys.exit(1)


# =============================================================================
# KEYFRAME PROMPT TEMPLATES
# =============================================================================

# Each emotion has:
# - start: Initial pose description
# - end: Peak/final pose description
# - motion_hint: Description for Ludo.ai interpolation

KEYFRAME_PROMPTS = {
    "bennie": {
        "idle": {
            "start": "standing relaxed with arms at sides, eyes open, gentle smile, feet flat on ground",
            "end": "same pose, chest slightly expanded (breathing in), subtle shift in stance",
            "motion_hint": "gentle breathing cycle, calm rhythmic motion"
        },
        "happy": {
            "start": "standing with arms at sides, happy expression, feet flat on ground, slight smile",
            "end": "slight bounce up with feet lifting, arms slightly raised, eyes squinted with joy, big smile",
            "motion_hint": "gentle bounce up and down with cheerful rhythm"
        },
        "thinking": {
            "start": "standing with one paw raised near chin, eyes looking up thoughtfully, curious expression",
            "end": "head tilted slightly to other side, paw still on chin, eyes looking up-right",
            "motion_hint": "head tilting side to side while pondering"
        },
        "encouraging": {
            "start": "standing with arms close to body, supportive warm expression, slight lean forward",
            "end": "arms open wide in welcoming gesture, warm encouraging smile, slight nod",
            "motion_hint": "arms opening outward in supportive welcoming gesture"
        },
        "celebrating": {
            "start": "standing with arms at sides, excited expression, feet on ground",
            "end": "arms raised high above head in victory pose, eyes closed with joy, slight jump",
            "motion_hint": "arms raising up in celebration, controlled joyful motion"
        },
        "waving": {
            "start": "one arm raised at shoulder height, paw facing forward, friendly smile",
            "end": "same arm extended higher, paw tilted sideways in classic wave, warm expression",
            "motion_hint": "hand waving side to side in friendly greeting"
        },
        "pointing": {
            "start": "standing with arms relaxed, looking forward, alert expression",
            "end": "one arm fully extended pointing right, head turned to look at pointed direction",
            "motion_hint": "arm extending outward to point at something important"
        }
    },
    "lemminge": {
        "idle": {
            "start": "standing upright, round body slightly compressed, arms at sides, eyes looking forward",
            "end": "same pose, body slightly expanded (breathing), eyes blinking",
            "motion_hint": "subtle breathing pulse, gentle body expansion and contraction"
        },
        "curious": {
            "start": "standing upright, head straight, wide curious eyes, ears up",
            "end": "head tilted to one side, leaning forward slightly, eyes even wider",
            "motion_hint": "head tilting curiously with inquisitive lean"
        },
        "excited": {
            "start": "standing on ground, arms at sides, huge excited eyes, feet flat",
            "end": "mid-bounce with feet off ground, arms raised high, eyes sparkling",
            "motion_hint": "bouncing up and down excitedly with energetic rhythm"
        },
        "celebrating": {
            "start": "standing with arms at sides, big excited smile showing buck teeth",
            "end": "arms raised high in victory, slight jump, eyes closed with pure joy",
            "motion_hint": "jumping celebration with arms waving"
        },
        "hiding": {
            "start": "standing partially visible, paws near face, nervous eyes",
            "end": "crouched lower, paws covering more of face, body compressed into shy pose",
            "motion_hint": "shrinking motion, covering face shyly"
        },
        "mischievous": {
            "start": "standing with hands together in front, looking forward, slight grin",
            "end": "hands rubbing together, sideways glance, impish sneaky grin showing teeth",
            "motion_hint": "sneaky hand rubbing with mischievous side-to-side sway"
        }
    }
}


# =============================================================================
# CHARACTER STYLE TEMPLATES
# =============================================================================

BENNIE_STYLE = """
KEYFRAME IMAGE FOR LUDO.AI ANIMATION:

Character: Bennie the Bear
Style: 2D vector art, cartoon illustration, clean digital art
Body: Adult brown bear proportions (NOT chibi or cute), pear-shaped body
Colors: Chocolate brown fur (#8C7259), lighter tan snout area only (#FAF5EB)
Eyes: Small round dark eyes with white highlights
Nose: Large dark espresso brown triangular nose (#5A4A3A)
Outlines: Thick dark cel-shaded outlines
Background: Clean cream/off-white or transparent background

POSE FOR THIS KEYFRAME:
{pose_description}

CRITICAL REQUIREMENTS:
- EXACT same character design as reference image
- Full body visible with feet on ground
- Clean simple background (no complex scenes)
- Pose matches description precisely
- Arms clearly attached to body
- Consistent proportions throughout
"""

LEMMINGE_STYLE = """
KEYFRAME IMAGE FOR LUDO.AI ANIMATION:

Character: Single Lemming creature (NOT Bennie, NOT a bear)
Style: Flat 2D vector art, Go gopher mascot style, thick bold outlines
Body: Round blue potato-shaped blob creature (#6FA8DC soft blue)
Belly: White patch (#FFFFFF) with fuzzy edge
Eyes: Large round friendly eyes with small black pupils
Features: Prominent buck teeth ALWAYS visible, small pink nose (#E8A0A0)
Paws: Stubby nub hands and feet with pink paw pads
Ears: Two small rounded ears on top of head
Outlines: Thick bold black cel-shaded outlines
Background: Clean light grey or transparent background

POSE FOR THIS KEYFRAME:
{pose_description}

CRITICAL REQUIREMENTS:
- EXACT same character design as reference image
- ONLY ONE character (single Lemming)
- NOT a bear, NOT brown colored
- Buck teeth visible in all frames
- Full body visible
- Clean simple background
- Pose matches description precisely
"""


# =============================================================================
# KEYFRAME GENERATION
# =============================================================================

@dataclass
class KeyframePair:
    """Represents a start/end keyframe pair for animation."""
    character: str
    emotion: str
    start_frame: Path
    end_frame: Path
    prompt_start: str
    prompt_end: str
    motion_hint: str
    reference_image: Optional[Path] = None
    generated_at: str = None

    def __post_init__(self):
        if self.generated_at is None:
            self.generated_at = datetime.now().isoformat()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "character": self.character,
            "emotion": self.emotion,
            "start_frame": str(self.start_frame) if self.start_frame else None,
            "end_frame": str(self.end_frame) if self.end_frame else None,
            "motion_hint": self.motion_hint,
            "reference_image": str(self.reference_image) if self.reference_image else None,
            "generated_at": self.generated_at,
        }


def get_reference_image(character: str) -> Optional[Path]:
    """Get frozen reference image for character consistency."""
    ref_dir = CONFIG.project_root / "public" / "images" / "generated" / "characters"

    if character.lower() == "bennie":
        ref_path = ref_dir / "bennie" / "reference" / "bennie-reference.png"
    else:  # lemminge
        ref_path = ref_dir / "lemminge" / "reference" / "lemminge-reference.png"

    if ref_path.exists():
        return ref_path

    # Try alternative locations
    alternatives = [
        ref_dir / character / "states" / f"{character}-idle.png",
        ref_dir / f"{character}-reference.png",
    ]

    for alt in alternatives:
        if alt.exists():
            log(f"[WARN] Using alternative reference: {alt}")
            return alt

    log(f"[WARN] No reference image found for {character}")
    return None


def build_keyframe_prompt(character: str, pose_description: str) -> str:
    """Build complete prompt for keyframe generation."""
    if character.lower() == "bennie":
        template = BENNIE_STYLE
    else:
        template = LEMMINGE_STYLE

    return template.format(pose_description=pose_description).strip()


def get_keyframe_prompts(character: str, emotion: str) -> Tuple[str, str, str]:
    """Get start and end frame prompts for a character emotion.

    Returns:
        Tuple of (start_pose, end_pose, motion_hint)
    """
    char_prompts = KEYFRAME_PROMPTS.get(character.lower(), {})
    emotion_data = char_prompts.get(emotion.lower(), {})

    if not emotion_data:
        available = list(char_prompts.keys())
        raise ValueError(
            f"No keyframe prompts for {character}/{emotion}. "
            f"Available emotions: {available}"
        )

    return (
        emotion_data["start"],
        emotion_data["end"],
        emotion_data["motion_hint"]
    )


def generate_keyframe_pair(
    character: str,
    emotion: str,
    output_dir: Path = None,
    reference_image: Path = None,
) -> KeyframePair:
    """Generate start and end keyframes for an animation.

    Args:
        character: "bennie" or "lemminge"
        emotion: Emotion state (e.g., "waving", "excited")
        output_dir: Directory to save keyframes (default: ludo/keyframes/)
        reference_image: Optional override for reference image

    Returns:
        KeyframePair with paths to generated frames
    """
    # Default output directory
    if output_dir is None:
        output_dir = Path(__file__).parent / "keyframes" / f"{character}_{emotion}"

    output_dir.mkdir(parents=True, exist_ok=True)

    # Get keyframe prompts
    start_pose, end_pose, motion_hint = get_keyframe_prompts(character, emotion)

    # Build full prompts
    prompt_start = build_keyframe_prompt(character, start_pose)
    prompt_end = build_keyframe_prompt(character, end_pose)

    # Get reference image if not provided
    if reference_image is None:
        reference_image = get_reference_image(character)

    refs = [reference_image] if reference_image and reference_image.exists() else None

    log("=" * 60)
    log(f"[KEYFRAME] Generating keyframes for {character}_{emotion}")
    log("=" * 60)

    # Generate START frame
    log(f"\n[PHASE 1] Generating START frame...")
    log(f"[POSE] {start_pose}")

    start_result = generate_single(
        prompt=prompt_start,
        name=f"{character}_{emotion}_start",
        category="keyframes",
        count=1,  # Single best frame
        aspect_ratio="1:1",  # Square for sprites
        character=character,
        output_dir=output_dir,
        raw_mode=True,  # Use exact prompt
        reference_images=refs,
    )

    start_paths = start_result.get("generated", [])
    if not start_paths:
        raise RuntimeError(f"Failed to generate START frame for {character}_{emotion}")
    start_frame = Path(start_paths[0])

    # Generate END frame
    log(f"\n[PHASE 2] Generating END frame...")
    log(f"[POSE] {end_pose}")

    end_result = generate_single(
        prompt=prompt_end,
        name=f"{character}_{emotion}_end",
        category="keyframes",
        count=1,
        aspect_ratio="1:1",
        character=character,
        output_dir=output_dir,
        raw_mode=True,
        reference_images=refs,
    )

    end_paths = end_result.get("generated", [])
    if not end_paths:
        raise RuntimeError(f"Failed to generate END frame for {character}_{emotion}")
    end_frame = Path(end_paths[0])

    # Create result
    result = KeyframePair(
        character=character,
        emotion=emotion,
        start_frame=start_frame,
        end_frame=end_frame,
        prompt_start=prompt_start,
        prompt_end=prompt_end,
        motion_hint=motion_hint,
        reference_image=reference_image,
    )

    # Save metadata
    metadata_path = output_dir / "keyframe_metadata.json"
    with open(metadata_path, "w") as f:
        json.dump(result.to_dict(), f, indent=2)

    log(f"\n[OK] Keyframes generated successfully!")
    log(f"[START] {start_frame}")
    log(f"[END] {end_frame}")
    log(f"[MOTION] {motion_hint}")
    log(f"[META] {metadata_path}")

    return result


def list_available_emotions(character: str) -> list:
    """List available emotions for a character."""
    return list(KEYFRAME_PROMPTS.get(character.lower(), {}).keys())


# =============================================================================
# CLI INTERFACE
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Generate keyframes for Ludo.ai animation pipeline",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Generate keyframes for single animation
    python generate_keyframes.py bennie waving

    # Generate all keyframes for a character
    python generate_keyframes.py lemminge --all

    # Custom output directory
    python generate_keyframes.py bennie celebrating --output-dir ./custom

    # List available emotions
    python generate_keyframes.py bennie --list
        """
    )

    parser.add_argument(
        "character",
        choices=["bennie", "lemminge"],
        help="Character to generate keyframes for"
    )
    parser.add_argument(
        "emotion",
        nargs="?",
        help="Emotion state (e.g., waving, excited)"
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Generate keyframes for all emotions"
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List available emotions for character"
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        help="Custom output directory"
    )
    parser.add_argument(
        "--reference",
        type=Path,
        help="Custom reference image path"
    )

    args = parser.parse_args()

    # List mode
    if args.list:
        emotions = list_available_emotions(args.character)
        print(f"\nAvailable emotions for {args.character}:")
        for e in emotions:
            prompts = KEYFRAME_PROMPTS[args.character][e]
            print(f"  - {e}")
            print(f"      Motion: {prompts['motion_hint']}")
        return 0

    # Generate all mode
    if args.all:
        emotions = list_available_emotions(args.character)
        results = []

        for emotion in emotions:
            try:
                output_dir = args.output_dir
                if output_dir:
                    output_dir = output_dir / f"{args.character}_{emotion}"

                result = generate_keyframe_pair(
                    character=args.character,
                    emotion=emotion,
                    output_dir=output_dir,
                    reference_image=args.reference,
                )
                results.append(result)
                print(f"[OK] {args.character}_{emotion}")

            except Exception as e:
                print(f"[ERROR] {args.character}_{emotion}: {e}")

        print(f"\n[SUMMARY] Generated {len(results)}/{len(emotions)} keyframe pairs")
        return 0 if len(results) == len(emotions) else 1

    # Single emotion mode
    if not args.emotion:
        print(f"Error: emotion argument required (or use --all or --list)")
        print(f"\nAvailable emotions for {args.character}:")
        for e in list_available_emotions(args.character):
            print(f"  - {e}")
        return 1

    try:
        result = generate_keyframe_pair(
            character=args.character,
            emotion=args.emotion,
            output_dir=args.output_dir,
            reference_image=args.reference,
        )

        print(f"\n[SUCCESS] Keyframes generated:")
        print(f"  Start: {result.start_frame}")
        print(f"  End:   {result.end_frame}")
        print(f"  Motion hint: {result.motion_hint}")
        return 0

    except Exception as e:
        print(f"[ERROR] {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
