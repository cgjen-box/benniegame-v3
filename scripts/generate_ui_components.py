#!/usr/bin/env python3
"""
UI Component Generator for Bennie Game (GSD Phase 08-01)
Uses Gemini Imagen API per playbook specifications.

Usage:
    python scripts/generate_ui_components.py
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
OUTPUT_DIR = BASE_DIR / "design" / "generated" / "UI"
API_KEY = os.environ.get("GOOGLE_API_KEY")

# Playbook color palette
COLORS = {
    "wood_light": "#C4A574",
    "wood_medium": "#A67C52",
    "wood_dark": "#6B4423",
    "success_green": "#99BF8C",
    "coin_gold": "#D9C27A",
    "cream": "#FAF5EB",
    "chain_gray": "#6B6B6B",
}

UI_COMPONENTS = {
    "buttons": [
        {
            "name": "wood_button_small",
            "prompt": """Wooden button for children's iPad game.
Wood plank with grain texture. Gradient: {wood_light} top to {wood_medium} center to {wood_dark} bottom.
Rounded rectangle, 16pt corners. Soft drop shadow.
Size: 96x60px. Clean vector style, cel-shaded. Transparent PNG background. NO text on button.""",
            "sizes": [(96, 60), (144, 90)],
        },
        {
            "name": "wood_button_medium",
            "prompt": """Medium wooden button for children's iPad game.
Wood plank with visible grain. Gradient: {wood_light} to {wood_medium} to {wood_dark}.
Rounded rectangle, 20pt corners. Soft shadow, 3D bevel effect.
Size: 192x120px. Clean vector style, cel-shaded. Transparent PNG background. NO text.""",
            "sizes": [(192, 120), (288, 180)],
        },
        {
            "name": "wood_button_large",
            "prompt": """Large wooden button for children's iPad game.
Rich wood plank with grain. Gradient: {wood_light} to {wood_medium} to {wood_dark}.
Rounded rectangle, 24pt corners. Pronounced shadow.
Size: 320x192px. Clean vector style, cel-shaded. Transparent PNG background. NO text.""",
            "sizes": [(320, 192), (480, 288)],
        },
    ],
    "signs": [
        {
            "name": "sign_unlocked",
            "prompt": """Hanging wooden sign for children's game menu.
Rectangular plank hanging from rope at top corners.
Wood: {wood_medium} base with grain texture. Rope: natural fiber {wood_light}.
Size: 400x240px. Cel-shaded style, forest game aesthetic. Transparent PNG background. NO text on sign.""",
            "sizes": [(400, 240), (600, 360)],
        },
        {
            "name": "sign_locked",
            "prompt": """Locked wooden sign for children's game.
Wooden plank with X-pattern chains across it.
Wood: dimmed {wood_dark}. Chains: gray metal {chain_gray}. Padlock at center.
Size: 400x240px. Cel-shaded style. Transparent PNG background. Shows unavailable state.""",
            "sizes": [(400, 240), (600, 360)],
        },
    ],
    "progress": [
        {
            "name": "progress_bar_empty",
            "prompt": """Empty progress bar for children's game.
Horizontal wooden trough. {wood_light} body, {wood_dark} inner channel.
Rounded ends. Size: 600x80px. Clean vector style. Transparent PNG background.""",
            "sizes": [(600, 80), (900, 120)],
        },
        {
            "name": "progress_bar_fill",
            "prompt": """Progress fill element. Glowing success indicator.
Color: {success_green} with gradient lighter at top.
Subtle inner glow effect. Size: 600x60px. Transparent PNG background.""",
            "sizes": [(600, 60), (900, 90)],
        },
        {
            "name": "gold_coin",
            "prompt": """Gold coin for children's game rewards.
Round gold coin, shiny. Color: {coin_gold} with highlights.
Embossed star pattern. Metallic shine effect. Size: 96x96px. Transparent PNG background.""",
            "sizes": [(96, 96), (144, 144)],
        },
    ],
    "treasure": [
        {
            "name": "chest_closed",
            "prompt": """Closed treasure chest for children's game.
Classic wooden chest, rounded lid. Wood: {wood_medium} and {wood_dark}.
Gold fittings {coin_gold}. Rivets at corners.
Size: 400x360px. Cel-shaded style, inviting appearance. Transparent PNG background.""",
            "sizes": [(400, 360), (600, 540)],
        },
        {
            "name": "chest_open",
            "prompt": """Open treasure chest with gold coins spilling out.
Wooden chest, lid open. Wood: {wood_medium} and {wood_dark}.
Gold coins {coin_gold} piled inside and spilling. Golden glow inside.
Size: 400x360px. Cel-shaded style, rewarding feel. Transparent PNG background.""",
            "sizes": [(400, 360), (600, 540)],
        },
        {
            "name": "chest_glow",
            "prompt": """Golden glow aura effect for treasure.
Soft radial gradient. Color: {coin_gold} fading to transparent.
Brightest at center. Size: 500x500px. Ethereal glow effect. Transparent background.""",
            "sizes": [(500, 500), (750, 750)],
        },
    ],
    "misc": [
        {
            "name": "padlock",
            "prompt": """Metal padlock for locked game items.
Classic padlock, slightly cartoonish style. Dark gray with silver highlights.
Keyhole visible. Size: 80x100px. Cel-shaded style. Transparent PNG background.""",
            "sizes": [(80, 100), (120, 150)],
        },
        {
            "name": "chain_x_pattern",
            "prompt": """X-pattern chains for locked overlay.
Two chains crossing in X shape. Color: gray {chain_gray} with highlights.
Visible chain links. Size: 200x200px. Transparent background, chains only.""",
            "sizes": [(200, 200), (300, 300)],
        },
    ],
}


def generate_component(client, component: dict, category: str) -> list:
    """Generate a UI component at all required sizes."""
    name = component["name"]
    prompt = component["prompt"].format(**COLORS)
    sizes = component["sizes"]

    output_paths = []
    output_base = OUTPUT_DIR / category
    output_base.mkdir(parents=True, exist_ok=True)

    print(f"\n  Generating: {name}")
    print(f"    Prompt: {prompt[:80]}...")

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
            # Get the image data
            generated = response.generated_images[0]

            # The image data is in generated.image._pil_image or we need to load from bytes
            if hasattr(generated.image, '_pil_image') and generated.image._pil_image:
                image = generated.image._pil_image
            elif hasattr(generated.image, 'image_bytes'):
                image = Image.open(BytesIO(generated.image.image_bytes))
            else:
                # Try to access data directly
                image_data = generated.image
                if hasattr(image_data, 'data'):
                    image = Image.open(BytesIO(image_data.data))
                else:
                    print(f"    ! Unknown image format: {type(generated.image)}")
                    return output_paths

            for idx, (width, height) in enumerate(sizes):
                scale = "@2x" if idx == 0 else "@3x"
                filename = f"{name}{scale}.png"
                output_path = output_base / filename

                resized = image.resize((width, height), Image.Resampling.LANCZOS)
                resized.save(str(output_path))
                output_paths.append(str(output_path))
                print(f"    + {filename}")
        else:
            print(f"    ! No images generated")

    except Exception as e:
        print(f"    X Error: {e}")
        import traceback
        traceback.print_exc()

    return output_paths


def main():
    print("=" * 60)
    print("GSD Phase 08-01: UI Component Generator")
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

    for category, components in UI_COMPONENTS.items():
        print(f"\n{'=' * 40}")
        print(f"Category: {category.upper()}")
        print("=" * 40)

        for component in components:
            paths = generate_component(client, component, category)
            if paths:
                total += len(paths)
            else:
                failed.append(component["name"])

    print(f"\n{'=' * 60}")
    print(f"Complete! {total} images generated.")
    print(f"Output: {OUTPUT_DIR}")

    if failed:
        print(f"\nFailed components ({len(failed)}):")
        for name in failed:
            print(f"  - {name}")

    print("=" * 60)


if __name__ == "__main__":
    main()
