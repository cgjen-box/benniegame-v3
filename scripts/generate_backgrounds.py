#!/usr/bin/env python3
"""
Background Image Generator for Bennie Game (GSD Phase 08-02)
Uses Gemini Imagen 4.0 API to generate forest parallax layers.

Usage:
    python scripts/generate_backgrounds.py
"""

import os
import sys
from pathlib import Path
from io import BytesIO

try:
    from google import genai
    from google.genai import types
except ImportError:
    print("ERROR: google-genai package not installed.")
    print("Run: pip install google-genai")
    sys.exit(1)

try:
    from PIL import Image
except ImportError:
    print("ERROR: pillow package not installed.")
    print("Run: pip install pillow")
    sys.exit(1)

try:
    from dotenv import load_dotenv
except ImportError:
    print("ERROR: python-dotenv package not installed.")
    print("Run: pip install python-dotenv")
    sys.exit(1)

load_dotenv()

BASE_DIR = Path(__file__).parent.parent
OUTPUT_DIR = BASE_DIR / "design" / "generated" / "Backgrounds"
API_KEY = os.environ.get("GOOGLE_API_KEY")

# Playbook forest background palette
FOREST_COLORS = {
    "far_trees": "#4A6B5C",      # Misty distant trees
    "mid_trees": "#738F66",       # Sage green forest body
    "near_foliage": "#7A9973",    # Close foreground
    "light_rays": "#F5E6C8",      # Golden hour glow (30% opacity)
    "sky_warm": "#FDF5E6",        # Warm cream sky
}

# iPad landscape resolutions
# @1x: 1194x834 (not used, we generate @2x and @3x)
# @2x: 2388x1668
# @3x: 3582x2502
SIZES = {
    "@2x": (2388, 1668),
    "@3x": (3582, 2502),
}

BACKGROUND_LAYERS = [
    {
        "name": "forest_layer_far",
        "prompt": """Create a seamless horizontal parallax background layer for a children's iPad game.

LAYER TYPE: Far distant misty trees (back layer)

COLOR: Primarily {far_trees} (#4A6B5C) with soft atmospheric haze
STYLE: Cel-shaded, vector illustration, children's game aesthetic
ATMOSPHERE: Soft, dreamy, atmospheric perspective with light fog/mist
DETAILS:
- Silhouettes of pine and deciduous tree tops
- Softer edges, less detail (distance effect)
- Subtle color gradient: slightly lighter at horizon
- Misty atmosphere between tree groups
- Trees should vary in height naturally

COMPOSITION:
- Trees across full width, seamless horizontal edges
- Trees clustered naturally, some gaps showing sky
- Golden light glow from upper-left corner
- Sky visible between trees: warm cream ({sky_warm})

MUST: Seamless left-right edges for parallax scrolling
MUST NOT: Any characters, animals, or text
OUTPUT: High quality PNG, landscape orientation""",
        "transparent": False,
    },
    {
        "name": "forest_layer_mid",
        "prompt": """Create a seamless horizontal parallax background layer for a children's iPad game.

LAYER TYPE: Middle distance forest (main layer)

COLOR: Primarily {mid_trees} (#738F66) sage green tones
STYLE: Cel-shaded, vector illustration, children's game aesthetic
ATMOSPHERE: Main forest body, warm and inviting

DETAILS:
- Mix of tree types: oak, birch, pine silhouettes
- More detail than far layer, defined branches and foliage
- Natural tree groupings with depth
- Some trees overlap creating depth
- Visible trunk portions at bottom
- Leaves/needles with subtle texture

COMPOSITION:
- Trees fill middle 60% of vertical space
- Natural gaps between tree groups
- Golden sunlight filtering through from upper-left
- Light rays visible between trees
- Warm shadows on right sides of trunks

LIGHTING: Warm golden hour light from upper-left, shadows to lower-right

MUST: Seamless left-right edges for parallax scrolling
MUST NOT: Any characters, animals, or text
OUTPUT: High quality PNG with transparent sky areas""",
        "transparent": True,
    },
    {
        "name": "forest_layer_near",
        "prompt": """Create a seamless horizontal parallax background layer for a children's iPad game.

LAYER TYPE: Near foreground foliage (front layer)

COLOR: Primarily {near_foliage} (#7A9973) vibrant green
STYLE: Cel-shaded, vector illustration, children's game aesthetic
ATMOSPHERE: Close, detailed, framing the scene

DETAILS:
- Detailed grass, ferns, low bushes at bottom
- A few large tree trunk portions at edges
- Detailed leaf shapes, some catching light
- Small flowers or forest floor details
- Dappled light spots on foliage
- Rich green with yellow-green highlights

COMPOSITION:
- Foliage primarily in bottom 30% of frame
- Large leaves/branches at side edges framing view
- Clear center area for gameplay visibility
- Some tall grass or fern fronds reaching up
- Creates natural frame around center

LIGHTING: Bright golden light hitting tops of leaves, darker underneath

MUST: Seamless left-right edges for parallax scrolling
MUST: Transparent center area for gameplay
MUST NOT: Any characters, animals, or text
OUTPUT: High quality PNG with large transparent areas in center""",
        "transparent": True,
    },
    {
        "name": "forest_layer_glow",
        "prompt": """Create a light rays overlay for a children's iPad game forest scene.

LAYER TYPE: Golden hour light rays overlay

COLOR: {light_rays} (#F5E6C8) at approximately 30% opacity
STYLE: Soft, ethereal, cel-shaded illustration
ATMOSPHERE: Magical, warm, safe forest feeling

DETAILS:
- Multiple diagonal light beams from upper-left corner
- Rays spread and diffuse as they travel
- Soft feathered edges on all beams
- Varying intensities: some brighter, some fainter
- Subtle dust particles or sparkles in beams
- Warm golden-cream color throughout

COMPOSITION:
- Light source positioned at upper-left (off-canvas)
- Rays angle down-right at roughly 45 degrees
- Coverage across full image but concentrated upper-left
- Rays fade out toward lower-right
- Transparent background except for light effects

EFFECT: Creates magical golden hour ambiance when overlaid on forest layers

MUST: Fully transparent background (PNG alpha)
MUST: Rays should be semi-transparent (30-40% opacity)
MUST NOT: Any solid colors, characters, or text
OUTPUT: High quality PNG with alpha transparency""",
        "transparent": True,
    },
]


def generate_layer(client, layer: dict) -> list:
    """Generate a background layer at @2x and @3x scales."""
    name = layer["name"]
    prompt = layer["prompt"].format(**FOREST_COLORS)

    output_paths = []
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print(f"\n  Generating: {name}")
    print(f"    Prompt: {prompt[:100]}...")

    try:
        response = client.models.generate_images(
            model='imagen-4.0-generate-001',
            prompt=prompt,
            config=types.GenerateImagesConfig(
                number_of_images=1,
                output_mime_type='image/png',
            )
        )

        if response.generated_images:
            generated = response.generated_images[0]

            # Extract PIL image from response
            if hasattr(generated.image, '_pil_image') and generated.image._pil_image:
                image = generated.image._pil_image
            elif hasattr(generated.image, 'image_bytes'):
                image = Image.open(BytesIO(generated.image.image_bytes))
            else:
                image_data = generated.image
                if hasattr(image_data, 'data'):
                    image = Image.open(BytesIO(image_data.data))
                else:
                    print(f"    ! Unknown image format: {type(generated.image)}")
                    return output_paths

            # Generate @2x and @3x versions
            for scale, (width, height) in SIZES.items():
                filename = f"{name}{scale}.png"
                output_path = OUTPUT_DIR / filename

                resized = image.resize((width, height), Image.Resampling.LANCZOS)

                # Ensure RGBA mode for transparent layers
                if layer["transparent"] and resized.mode != 'RGBA':
                    resized = resized.convert('RGBA')

                resized.save(str(output_path))
                output_paths.append(str(output_path))
                print(f"    + {filename} ({width}x{height})")
        else:
            print(f"    ! No images generated")

    except Exception as e:
        print(f"    X Error: {e}")
        import traceback
        traceback.print_exc()

    return output_paths


def main():
    print("=" * 60)
    print("GSD Phase 08-02: Background Image Generator")
    print("=" * 60)
    print(f"Output: {OUTPUT_DIR}")

    if not API_KEY:
        print("\nERROR: GOOGLE_API_KEY not found in .env")
        print("Set it with: export GOOGLE_API_KEY='your-api-key'")
        return

    print(f"API Key: {API_KEY[:10]}...{API_KEY[-4:]}")

    client = genai.Client(api_key=API_KEY)
    total = 0
    failed = []

    print(f"\n{'=' * 40}")
    print("Generating Forest Parallax Layers")
    print("=" * 40)
    print("Layers to generate:")
    for layer in BACKGROUND_LAYERS:
        print(f"  - {layer['name']}")

    for layer in BACKGROUND_LAYERS:
        paths = generate_layer(client, layer)
        if paths:
            total += len(paths)
        else:
            failed.append(layer["name"])

    print(f"\n{'=' * 60}")
    print(f"Complete! {total} images generated.")
    print(f"Expected: {len(BACKGROUND_LAYERS) * 2} (4 layers x 2 scales)")
    print(f"Output: {OUTPUT_DIR}")

    if failed:
        print(f"\nFailed layers ({len(failed)}):")
        for name in failed:
            print(f"  - {name}")

    print("=" * 60)


if __name__ == "__main__":
    main()
