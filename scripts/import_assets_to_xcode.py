#!/usr/bin/env python3
"""
Asset Import Script for Bennie Game
Imports processed assets into Xcode's Assets.xcassets structure.

Creates proper .imageset directories with Contents.json files.
"""

import os
import json
import shutil
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).parent.parent
PROCESSED_DIR = BASE_DIR / "design" / "processed"
XCASSETS_DIR = BASE_DIR / "BennieGame" / "BennieGame" / "Resources" / "Assets.xcassets"

# Asset configurations
CHARACTER_ASSETS = {
    "Bennie": [
        "bennie-celebrating",
        "bennie-encouraging",
        "bennie-happy",
        "bennie-idle",
        "bennie-pointing",
        "bennie-thinking",
        "bennie-waving",
    ],
    "Lemminge": [
        "lemminge-celebrating",
        "lemminge-curious",
        "lemminge-excited",
        "lemminge-hiding",
        "lemminge-idle",
        "lemminge-mischievous",
    ],
}


def create_imageset_contents(filename_2x, filename_3x):
    """Create Contents.json for an imageset."""
    return {
        "images": [
            {
                "filename": filename_2x,
                "idiom": "universal",
                "scale": "2x"
            },
            {
                "filename": filename_3x,
                "idiom": "universal",
                "scale": "3x"
            }
        ],
        "info": {
            "author": "xcode",
            "version": 1
        }
    }


def create_folder_contents():
    """Create Contents.json for a folder."""
    return {
        "info": {
            "author": "xcode",
            "version": 1
        },
        "properties": {
            "provides-namespace": True
        }
    }


def import_character_assets():
    """Import character assets into Assets.xcassets."""
    print("=" * 60)
    print("Importing Character Assets")
    print("=" * 60)

    characters_dir = XCASSETS_DIR / "Characters"
    characters_dir.mkdir(parents=True, exist_ok=True)

    # Create Characters folder Contents.json
    with open(characters_dir / "Contents.json", "w") as f:
        json.dump(create_folder_contents(), f, indent=2)

    for character, assets in CHARACTER_ASSETS.items():
        print(f"\n--- {character} ---")

        # Create character folder
        char_dir = characters_dir / character
        char_dir.mkdir(exist_ok=True)

        # Create folder Contents.json
        with open(char_dir / "Contents.json", "w") as f:
            json.dump(create_folder_contents(), f, indent=2)

        source_dir = PROCESSED_DIR / "Characters" / character

        for asset_name in assets:
            # Create imageset directory
            # Convert filename to swift-friendly name (e.g., bennie-idle -> bennie_idle)
            swift_name = asset_name.replace("-", "_")
            imageset_dir = char_dir / f"{swift_name}.imageset"
            imageset_dir.mkdir(exist_ok=True)

            # Copy @2x and @3x images
            src_2x = source_dir / f"{asset_name}@2x.png"
            src_3x = source_dir / f"{asset_name}@3x.png"

            if src_2x.exists() and src_3x.exists():
                # Copy files
                dst_2x = imageset_dir / f"{swift_name}@2x.png"
                dst_3x = imageset_dir / f"{swift_name}@3x.png"

                shutil.copy2(src_2x, dst_2x)
                shutil.copy2(src_3x, dst_3x)

                # Create Contents.json
                contents = create_imageset_contents(
                    f"{swift_name}@2x.png",
                    f"{swift_name}@3x.png"
                )
                with open(imageset_dir / "Contents.json", "w") as f:
                    json.dump(contents, f, indent=2)

                print(f"  ✓ {swift_name}")
            else:
                print(f"  ✗ {asset_name} - source files not found")


def import_ui_components():
    """Import UI component assets (placeholder for future)."""
    print("\n" + "=" * 60)
    print("UI Components")
    print("=" * 60)

    ui_dir = XCASSETS_DIR / "UI"
    ui_dir.mkdir(parents=True, exist_ok=True)

    # Create folder Contents.json
    with open(ui_dir / "Contents.json", "w") as f:
        json.dump(create_folder_contents(), f, indent=2)

    # Create subdirectories
    for subdir in ["Buttons", "Signs", "Progress", "Treasure"]:
        sub_path = ui_dir / subdir
        sub_path.mkdir(exist_ok=True)
        with open(sub_path / "Contents.json", "w") as f:
            json.dump(create_folder_contents(), f, indent=2)
        print(f"  ✓ Created {subdir}/ folder structure")


def import_backgrounds():
    """Import background assets (placeholder for future)."""
    print("\n" + "=" * 60)
    print("Backgrounds")
    print("=" * 60)

    bg_dir = XCASSETS_DIR / "Backgrounds"
    bg_dir.mkdir(parents=True, exist_ok=True)

    # Create folder Contents.json
    with open(bg_dir / "Contents.json", "w") as f:
        json.dump(create_folder_contents(), f, indent=2)

    print("  ✓ Created Backgrounds/ folder structure")


def verify_import():
    """Verify imported assets."""
    print("\n" + "=" * 60)
    print("Verification")
    print("=" * 60)

    # Count imagesets
    imageset_count = 0
    for path in XCASSETS_DIR.rglob("*.imageset"):
        # Check if Contents.json exists and has valid images
        contents_path = path / "Contents.json"
        if contents_path.exists():
            with open(contents_path) as f:
                contents = json.load(f)
            images = contents.get("images", [])
            valid_images = sum(1 for img in images if (path / img.get("filename", "")).exists())
            if valid_images > 0:
                imageset_count += 1

    print(f"  Total imagesets with images: {imageset_count}")


def main():
    print("=" * 60)
    print("Bennie Game Asset Importer")
    print("=" * 60)
    print(f"Source: {PROCESSED_DIR}")
    print(f"Target: {XCASSETS_DIR}")

    # Import assets
    import_character_assets()
    import_ui_components()
    import_backgrounds()

    # Verify
    verify_import()

    print("\n" + "=" * 60)
    print("Import complete!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Open Xcode project")
    print("2. Verify assets appear in Assets.xcassets")
    print("3. Build project to ensure no missing assets")


if __name__ == "__main__":
    main()
