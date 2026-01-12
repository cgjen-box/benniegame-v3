#!/usr/bin/env python3
"""
Import Generated Background Images to Xcode Assets.xcassets
GSD Phase 08-02: Background Images import step.
"""

import os
import json
import shutil
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).parent.parent
GENERATED_DIR = BASE_DIR / "design" / "generated" / "Backgrounds"
XCASSETS_DIR = BASE_DIR / "BennieGame" / "BennieGame" / "Resources" / "Assets.xcassets"


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


def import_backgrounds():
    """Import background images to xcassets."""
    if not GENERATED_DIR.exists():
        print(f"  ! Source directory not found: {GENERATED_DIR}")
        return 0

    dest_dir = XCASSETS_DIR / "Backgrounds"
    dest_dir.mkdir(parents=True, exist_ok=True)

    # Create folder Contents.json
    with open(dest_dir / "Contents.json", "w") as f:
        json.dump(create_folder_contents(), f, indent=2)

    count = 0
    # Find all unique asset names (without @2x/@3x suffix)
    assets = set()
    for file in GENERATED_DIR.glob("*.png"):
        name = file.stem.replace("@2x", "").replace("@3x", "")
        assets.add(name)

    for asset_name in sorted(assets):
        # Create imageset directory
        imageset_dir = dest_dir / f"{asset_name}.imageset"
        imageset_dir.mkdir(exist_ok=True)

        # Copy @2x and @3x images
        src_2x = GENERATED_DIR / f"{asset_name}@2x.png"
        src_3x = GENERATED_DIR / f"{asset_name}@3x.png"

        if src_2x.exists() and src_3x.exists():
            dst_2x = imageset_dir / f"{asset_name}@2x.png"
            dst_3x = imageset_dir / f"{asset_name}@3x.png"

            shutil.copy2(src_2x, dst_2x)
            shutil.copy2(src_3x, dst_3x)

            # Create Contents.json
            contents = create_imageset_contents(
                f"{asset_name}@2x.png",
                f"{asset_name}@3x.png"
            )
            with open(imageset_dir / "Contents.json", "w") as f:
                json.dump(contents, f, indent=2)

            print(f"    + {asset_name}")
            count += 1
        else:
            print(f"    ! Missing files for {asset_name}")

    return count


def main():
    print("=" * 60)
    print("GSD Phase 08-02: Import Backgrounds to Xcode")
    print("=" * 60)
    print(f"Source: {GENERATED_DIR}")
    print(f"Target: {XCASSETS_DIR / 'Backgrounds'}")

    total = import_backgrounds()

    print(f"\n{'=' * 60}")
    print(f"Complete! {total} imagesets imported to Xcode.")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Open Xcode project")
    print("2. Verify assets appear in Assets.xcassets/Backgrounds/")
    print("3. Build project to ensure no missing assets")


if __name__ == "__main__":
    main()
