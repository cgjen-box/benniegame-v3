#!/usr/bin/env python3
"""
Shared Image Compression Utilities for MCP Servers
===================================================
Ensures all images returned via MCP are under 500KB to prevent
"Tool result could not be submitted" errors.

Usage:
    from mcp_image_utils import compress_image_for_mcp, save_and_compress

    # Compress existing file
    result = compress_image_for_mcp(
        image_path="/path/to/large.png",
        output_dir="/path/to/compressed",
        max_bytes=500_000  # 500KB default
    )
    # Returns: {"success": True, "image_b64": "...", "saved_to": "...", "size_bytes": 123456}

    # Save new image and compress
    result = save_and_compress(
        image_data=raw_bytes,
        save_path="/path/to/original.png",
        compress_dir="/path/to/compressed"
    )
"""

import base64
import io
from pathlib import Path
from typing import Optional, Dict, Any
from PIL import Image

# Size limits
MAX_BASE64_BYTES = 500_000  # 500KB - safe limit for MCP transport
MAX_DIMENSION_START = 1024  # Start with this dimension
MIN_QUALITY = 20  # Don't go below this JPEG quality
QUALITY_STEP = 5  # Reduce quality by this amount per iteration


def compress_image_for_mcp(
    image_path: Path,
    output_dir: Optional[Path] = None,
    max_bytes: int = MAX_BASE64_BYTES,
    save_compressed: bool = True
) -> Dict[str, Any]:
    """
    Compress an image to be under max_bytes when base64-encoded.

    Strategy:
    1. Resize to 1024px max dimension (preserves aspect ratio)
    2. Save as JPEG with quality=85
    3. If still too large, reduce quality in steps
    4. If still too large, reduce dimensions
    5. Save compressed version to disk (original preserved)
    6. Return base64-encoded compressed version

    Args:
        image_path: Path to original image
        output_dir: Where to save compressed version (default: same dir as original with _compressed suffix)
        max_bytes: Maximum size in bytes after base64 encoding
        save_compressed: Whether to save compressed version to disk

    Returns:
        {
            "success": True,
            "image_b64": "base64-encoded compressed image",
            "mime_type": "image/jpeg",
            "size_bytes": 123456,
            "original_size": 2000000,
            "saved_to": "/path/to/compressed.jpg",
            "compression_ratio": 0.85,
            "dimensions": [width, height]
        }
    """
    image_path = Path(image_path)

    if not image_path.exists():
        return {
            "success": False,
            "error": f"Image not found: {image_path}"
        }

    try:
        # Load original
        with Image.open(image_path) as img:
            # Convert to RGB (removes alpha channel, reduces size)
            if img.mode in ('RGBA', 'P', 'LA'):
                img = img.convert('RGB')

            original_size = img.size
            current_img = img.copy()

            # Strategy: Try progressively more aggressive compression
            max_dimension = MAX_DIMENSION_START
            quality = 85
            compressed_data = None
            final_size = 0

            for attempt in range(10):  # Max 10 attempts
                # Resize if needed
                if max(current_img.size) > max_dimension:
                    current_img.thumbnail((max_dimension, max_dimension), Image.Resampling.LANCZOS)

                # Encode to JPEG
                buffer = io.BytesIO()
                current_img.save(buffer, format='JPEG', quality=quality, optimize=True)
                compressed_data = buffer.getvalue()

                # Check base64 size
                b64_data = base64.b64encode(compressed_data).decode('utf-8')
                b64_size = len(b64_data.encode('utf-8'))

                if b64_size <= max_bytes:
                    # Success!
                    final_size = b64_size
                    break

                # Too large, try more aggressive compression
                if quality > MIN_QUALITY:
                    quality -= QUALITY_STEP
                else:
                    # Reduce dimensions
                    max_dimension = int(max_dimension * 0.8)
                    quality = 85  # Reset quality

                if max_dimension < 256:
                    # Can't compress further without losing too much quality
                    final_size = b64_size
                    break

            # Save compressed version if requested
            saved_to = None
            if save_compressed and compressed_data:
                if output_dir:
                    output_dir = Path(output_dir)
                    output_dir.mkdir(parents=True, exist_ok=True)
                    compressed_path = output_dir / f"{image_path.stem}_compressed.jpg"
                else:
                    compressed_path = image_path.parent / f"{image_path.stem}_compressed.jpg"

                with open(compressed_path, 'wb') as f:
                    f.write(compressed_data)
                saved_to = str(compressed_path)

            return {
                "success": True,
                "image_b64": base64.b64encode(compressed_data).decode('utf-8'),
                "mime_type": "image/jpeg",
                "size_bytes": final_size,
                "original_size": image_path.stat().st_size,
                "saved_to": saved_to,
                "compression_ratio": round(final_size / image_path.stat().st_size, 2),
                "dimensions": list(current_img.size),
                "final_quality": quality,
                "under_limit": final_size <= max_bytes
            }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


def save_and_compress(
    image_data: bytes,
    save_path: Path,
    compress_dir: Optional[Path] = None,
    max_bytes: int = MAX_BASE64_BYTES
) -> Dict[str, Any]:
    """
    Save image data to disk, then compress for MCP transport.

    Use this when you have raw image bytes (e.g., from API response)
    and want to both save the original and return a compressed version.

    Args:
        image_data: Raw image bytes
        save_path: Where to save original image
        compress_dir: Where to save compressed version (default: same as save_path)
        max_bytes: Max size after base64 encoding

    Returns:
        Same as compress_image_for_mcp()
    """
    save_path = Path(save_path)
    save_path.parent.mkdir(parents=True, exist_ok=True)

    # Save original
    with open(save_path, 'wb') as f:
        f.write(image_data)

    # Compress for transport
    return compress_image_for_mcp(
        image_path=save_path,
        output_dir=compress_dir,
        max_bytes=max_bytes
    )


def verify_size_limit(b64_string: str, max_bytes: int = MAX_BASE64_BYTES) -> Dict[str, Any]:
    """
    Verify that a base64 string is under the size limit.

    Args:
        b64_string: Base64-encoded string to check
        max_bytes: Maximum allowed bytes

    Returns:
        {
            "under_limit": True/False,
            "size_bytes": 123456,
            "max_bytes": 500000,
            "overage": 0 or positive number if over limit
        }
    """
    size_bytes = len(b64_string.encode('utf-8'))
    under_limit = size_bytes <= max_bytes
    overage = max(0, size_bytes - max_bytes)

    return {
        "under_limit": under_limit,
        "size_bytes": size_bytes,
        "max_bytes": max_bytes,
        "overage": overage,
        "size_kb": round(size_bytes / 1024, 1),
        "max_kb": round(max_bytes / 1024, 1)
    }


# Convenience function for macOS sips compression (used by ios_simulator_mcp)
def compress_with_sips(
    input_path: Path,
    output_path: Path,
    max_dimension: int = 1024
) -> bool:
    """
    Compress using macOS sips command (faster than PIL for large images).
    Only works on macOS.

    Args:
        input_path: Source image
        output_path: Destination compressed image
        max_dimension: Max width/height

    Returns:
        True if successful
    """
    import subprocess
    import shutil

    if not shutil.which('sips'):
        return False  # sips not available (not macOS)

    try:
        subprocess.run(
            ['sips', '-Z', str(max_dimension), str(input_path), '--out', str(output_path)],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=30
        )
        return output_path.exists()
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
        return False


if __name__ == "__main__":
    # Self-test
    import sys

    print("MCP Image Compression Utilities - Self Test")
    print("=" * 60)

    # Test with a sample image if provided
    if len(sys.argv) > 1:
        test_image = Path(sys.argv[1])
        if test_image.exists():
            print(f"\nTesting compression on: {test_image}")
            result = compress_image_for_mcp(test_image)

            if result["success"]:
                print(f"✅ Compression successful!")
                print(f"   Original size: {result['original_size']:,} bytes")
                print(f"   Compressed size: {result['size_bytes']:,} bytes")
                print(f"   Compression ratio: {result['compression_ratio']:.1%}")
                print(f"   Under 500KB limit: {result['under_limit']}")
                print(f"   Dimensions: {result['dimensions'][0]}x{result['dimensions'][1]}")
                print(f"   Saved to: {result['saved_to']}")
            else:
                print(f"❌ Error: {result['error']}")
        else:
            print(f"Error: Image not found: {test_image}")
    else:
        print("\nUsage: python mcp_image_utils.py <image_path>")
        print("Example: python mcp_image_utils.py screenshot.png")
