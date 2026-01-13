#!/usr/bin/env python3
"""
Character Image Processor for Bennie Game
- Removes solid backgrounds (makes transparent)
- Crops to character bounds
- Exports at @2x and @3x sizes per playbook spec
"""

import os
from PIL import Image
import sys

# Playbook specifications
BENNIE_SIZES = {
    "@2x": (300, 450),
    "@3x": (450, 675)
}

LEMMINGE_SIZES = {
    "@2x": (80, 100),
    "@3x": (120, 150)
}

# Source and destination paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BENNIE_SOURCE = os.path.join(BASE_DIR, "design/references/character/bennie/states")
LEMMINGE_SOURCE = os.path.join(BASE_DIR, "design/references/character/lemminge/states")
OUTPUT_DIR = os.path.join(BASE_DIR, "design/processed")

# Background colors to remove (approximate - will use corner sampling)
BENNIE_BG_TOLERANCE = 30  # Color difference tolerance
LEMMINGE_BG_TOLERANCE = 30


def get_background_color(img):
    """Sample corners to determine background color."""
    pixels = [
        img.getpixel((0, 0)),
        img.getpixel((img.width - 1, 0)),
        img.getpixel((0, img.height - 1)),
        img.getpixel((img.width - 1, img.height - 1))
    ]
    # Return most common corner color (ignoring alpha if present)
    rgb_pixels = [p[:3] if len(p) > 3 else p for p in pixels]
    return max(set(rgb_pixels), key=rgb_pixels.count)


def color_distance(c1, c2):
    """Calculate Euclidean distance between two RGB colors."""
    return sum((a - b) ** 2 for a, b in zip(c1[:3], c2[:3])) ** 0.5


def remove_background(img, tolerance=30):
    """Remove solid background color, making it transparent."""
    img = img.convert("RGBA")
    bg_color = get_background_color(img)
    print(f"  Detected background color: RGB{bg_color}")

    pixels = img.load()
    width, height = img.size

    for y in range(height):
        for x in range(width):
            pixel = pixels[x, y]
            if color_distance(pixel[:3], bg_color) < tolerance:
                pixels[x, y] = (0, 0, 0, 0)  # Transparent

    return img


def get_content_bounds(img):
    """Find bounding box of non-transparent content."""
    bbox = img.getbbox()
    if bbox is None:
        return (0, 0, img.width, img.height)
    return bbox


def crop_to_content(img, padding=10):
    """Crop image to content bounds with padding."""
    bbox = get_content_bounds(img)
    # Add padding
    left = max(0, bbox[0] - padding)
    top = max(0, bbox[1] - padding)
    right = min(img.width, bbox[2] + padding)
    bottom = min(img.height, bbox[3] + padding)
    return img.crop((left, top, right, bottom))


def resize_maintain_aspect(img, target_size):
    """Resize image to fit within target size while maintaining aspect ratio."""
    target_w, target_h = target_size
    orig_w, orig_h = img.size

    # Calculate scale to fit within target
    scale = min(target_w / orig_w, target_h / orig_h)
    new_w = int(orig_w * scale)
    new_h = int(orig_h * scale)

    # Resize with high-quality resampling
    resized = img.resize((new_w, new_h), Image.Resampling.LANCZOS)

    # Create canvas at exact target size with transparent background
    canvas = Image.new("RGBA", target_size, (0, 0, 0, 0))

    # Center the resized image on canvas
    paste_x = (target_w - new_w) // 2
    paste_y = (target_h - new_h) // 2
    canvas.paste(resized, (paste_x, paste_y), resized)

    return canvas


def process_character(source_path, output_base, sizes, tolerance):
    """Process a single character image."""
    filename = os.path.basename(source_path)
    name = os.path.splitext(filename)[0]

    print(f"\nProcessing: {filename}")

    # Load image
    img = Image.open(source_path)
    print(f"  Original size: {img.size}")

    # Remove background
    img_transparent = remove_background(img, tolerance)

    # Crop to content
    img_cropped = crop_to_content(img_transparent)
    print(f"  After crop: {img_cropped.size}")

    # Export at each size
    for scale, target_size in sizes.items():
        output_filename = f"{name}{scale}.png"
        output_path = os.path.join(output_base, output_filename)

        resized = resize_maintain_aspect(img_cropped, target_size)
        resized.save(output_path, "PNG", optimize=True)
        print(f"  Exported: {output_filename} ({target_size[0]}x{target_size[1]})")

    return True


def main():
    # Create output directories
    bennie_output = os.path.join(OUTPUT_DIR, "Characters/Bennie")
    lemminge_output = os.path.join(OUTPUT_DIR, "Characters/Lemminge")

    os.makedirs(bennie_output, exist_ok=True)
    os.makedirs(lemminge_output, exist_ok=True)

    print("=" * 60)
    print("Character Image Processor - Bennie Game")
    print("=" * 60)

    # Process Bennie images
    print("\n--- Processing Bennie Images ---")
    bennie_files = [f for f in os.listdir(BENNIE_SOURCE) if f.endswith('.png')]

    for filename in sorted(bennie_files):
        source_path = os.path.join(BENNIE_SOURCE, filename)
        process_character(source_path, bennie_output, BENNIE_SIZES, BENNIE_BG_TOLERANCE)

    # Process Lemminge images
    print("\n--- Processing Lemminge Images ---")
    lemminge_files = [f for f in os.listdir(LEMMINGE_SOURCE) if f.endswith('.png')]

    for filename in sorted(lemminge_files):
        source_path = os.path.join(LEMMINGE_SOURCE, filename)
        process_character(source_path, lemminge_output, LEMMINGE_SIZES, LEMMINGE_BG_TOLERANCE)

    print("\n" + "=" * 60)
    print("Processing complete!")
    print(f"Output directory: {OUTPUT_DIR}")
    print("=" * 60)


if __name__ == "__main__":
    main()
