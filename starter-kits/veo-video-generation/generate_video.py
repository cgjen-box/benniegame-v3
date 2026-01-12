#!/usr/bin/env python3
"""
Veo 3.1 Video Generation - Standalone Module
=============================================
Generate AI video clips using Google's Veo 3.1 model.

Usage:
    python generate_video.py "Cartoon bear walking" --name bear-walk --duration 6

Environment Variables Required:
    GOOGLE_API_KEY - Google AI API key for video generation
"""

import os
import sys
import time
import argparse
from pathlib import Path
from datetime import datetime
from typing import Optional, List

# Load environment
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Check dependencies
try:
    from google import genai
    from google.genai import types
except ImportError:
    print("[ERROR] Missing google-genai package", file=sys.stderr)
    print("[INFO] Install with: pip install google-genai", file=sys.stderr)
    sys.exit(1)

# Import SecretGuard if available
try:
    from secret_guard import SecretGuard
    API_KEY = SecretGuard.get("GOOGLE_API_KEY", default="") or SecretGuard.get("GEMINI_API_KEY", default="", required=False)
except ImportError:
    API_KEY = os.environ.get("GOOGLE_API_KEY") or os.environ.get("GEMINI_API_KEY")


# =============================================================================
# CONFIGURATION
# =============================================================================

DEFAULT_MODEL = os.environ.get("VEO_MODEL", "veo-3.1-generate-preview")
FALLBACK_MODELS = [
    "veo-3.1-generate-preview",
    "veo-3.1-fast-generate-preview",
    "veo-3.0-generate-001",
]
OUTPUT_DIR = Path("./generated/videos")


def log(*args, **kwargs):
    """Print to stderr to avoid conflicts with JSON output."""
    kwargs['file'] = sys.stderr
    print(*args, **kwargs)


# =============================================================================
# VIDEO GENERATION
# =============================================================================

def generate_video(
    prompt: str,
    output_name: str,
    duration: int = 8,
    resolution: str = "720p",
    aspect_ratio: str = "16:9",
    reference_images: Optional[List[Path]] = None,
    negative_prompt: Optional[str] = None,
    output_dir: Path = OUTPUT_DIR,
) -> Path:
    """Generate video using Google Veo 3.1.

    Args:
        prompt: Description of the video to generate
        output_name: Base filename for output
        duration: Video duration in seconds (4, 6, or 8)
        resolution: Video resolution (720p or 1080p)
        aspect_ratio: Aspect ratio (16:9 or 9:16)
        reference_images: Optional list of reference image paths (up to 3)
        negative_prompt: Optional description of unwanted content
        output_dir: Directory to save output

    Returns:
        Path to saved video file
    """
    if not API_KEY:
        raise ValueError("GOOGLE_API_KEY environment variable not set")

    # Validate parameters
    if duration not in [4, 6, 8]:
        raise ValueError(f"Duration must be 4, 6, or 8 seconds, got {duration}")
    if resolution not in ["720p", "1080p"]:
        raise ValueError(f"Resolution must be 720p or 1080p, got {resolution}")
    if resolution == "1080p" and duration != 8:
        log("[WARN] 1080p only supports 8s duration, adjusting...")
        duration = 8
    if aspect_ratio not in ["16:9", "9:16"]:
        raise ValueError(f"Aspect ratio must be 16:9 or 9:16, got {aspect_ratio}")

    client = genai.Client(api_key=API_KEY)
    model_id = DEFAULT_MODEL

    output_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    log(f"\n[VIDEO] Generating video with Veo 3.1...")
    log(f"[MODEL] {model_id}")
    log(f"[DURATION] {duration}s @ {resolution} ({aspect_ratio})")
    log(f"[PROMPT] {prompt[:150]}...")

    # Build config
    config_params = {
        "aspect_ratio": aspect_ratio,
    }

    # Add negative prompt if provided
    if negative_prompt:
        config_params["negative_prompt"] = negative_prompt

    # Add reference images if provided
    ref_image_objects = []
    if reference_images:
        log(f"[REF] Using {len(reference_images)} reference image(s)")
        for ref_path in reference_images[:3]:  # Max 3 reference images
            ref_path = Path(ref_path)
            if ref_path.exists():
                # Read image bytes
                with open(ref_path, "rb") as f:
                    image_bytes = f.read()

                # Determine MIME type
                suffix = ref_path.suffix.lower()
                mime_type = {
                    ".png": "image/png",
                    ".jpg": "image/jpeg",
                    ".jpeg": "image/jpeg",
                    ".webp": "image/webp",
                }.get(suffix, "image/png")

                # Create reference image
                ref_image = types.VideoGenerationReferenceImage(
                    image=types.Image(
                        image_bytes=image_bytes,
                        mime_type=mime_type,
                    ),
                    reference_type="asset"
                )
                ref_image_objects.append(ref_image)
                log(f"   - {ref_path.name}")

        if ref_image_objects:
            config_params["reference_images"] = ref_image_objects

    video_config = types.GenerateVideosConfig(**config_params)

    try:
        # Start video generation (long-running operation)
        operation = client.models.generate_videos(
            model=model_id,
            prompt=prompt,
            config=video_config,
        )

        # Poll for completion
        log("[STATUS] Generation started, waiting for completion...")
        poll_count = 0
        max_polls = 120  # 20 minutes max (10s * 120)

        while not operation.done:
            poll_count += 1
            if poll_count > max_polls:
                raise TimeoutError("Video generation timed out after 20 minutes")

            if poll_count % 6 == 0:  # Log every minute
                log(f"   Still generating... ({poll_count * 10}s elapsed)")

            time.sleep(10)
            operation = client.operations.get(operation)

        # Check for errors
        if operation.error:
            raise RuntimeError(f"Video generation failed: {operation.error}")

        # Download the generated video
        video = operation.response.generated_videos[0]
        filename = f"{output_name}_{timestamp}.mp4"
        filepath = output_dir / filename

        # Download video file
        client.files.download(file=video.video)
        video.video.save(str(filepath))

        log(f"[OK] Video saved: {filename}")
        return filepath

    except Exception as e:
        log(f"[ERROR] Video generation failed: {e}")
        raise


def extend_video(
    video_path: Path,
    prompt: str,
    output_name: str,
    resolution: str = "720p",
    output_dir: Path = OUTPUT_DIR,
) -> Path:
    """Extend an existing video by 7 seconds using Veo 3.1.

    Args:
        video_path: Path to existing video to extend
        prompt: Description of the continuation
        output_name: Base filename for output
        resolution: Video resolution (720p or 1080p)
        output_dir: Directory to save output

    Returns:
        Path to extended video file
    """
    if not API_KEY:
        raise ValueError("GOOGLE_API_KEY environment variable not set")

    if not video_path.exists():
        raise FileNotFoundError(f"Video file not found: {video_path}")

    client = genai.Client(api_key=API_KEY)
    model_id = DEFAULT_MODEL

    output_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    log(f"\n[VIDEO] Extending video with Veo 3.1...")
    log(f"[SOURCE] {video_path.name}")
    log(f"[PROMPT] {prompt[:150]}...")

    try:
        # Upload the source video
        video_file = client.files.upload(file=str(video_path))

        # Start extension operation
        operation = client.models.generate_videos(
            model=model_id,
            video=video_file,
            prompt=prompt,
        )

        # Poll for completion
        log("[STATUS] Extension started, waiting for completion...")
        poll_count = 0
        max_polls = 120

        while not operation.done:
            poll_count += 1
            if poll_count > max_polls:
                raise TimeoutError("Video extension timed out after 20 minutes")

            if poll_count % 6 == 0:
                log(f"   Still extending... ({poll_count * 10}s elapsed)")

            time.sleep(10)
            operation = client.operations.get(operation)

        # Check for errors
        if operation.error:
            raise RuntimeError(f"Video extension failed: {operation.error}")

        # Download the extended video
        video = operation.response.generated_videos[0]
        filename = f"{output_name}_extended_{timestamp}.mp4"
        filepath = output_dir / filename

        client.files.download(file=video.video)
        video.video.save(str(filepath))

        log(f"[OK] Extended video saved: {filename}")
        return filepath

    except Exception as e:
        log(f"[ERROR] Video extension failed: {e}")
        raise


# =============================================================================
# CLI
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Generate AI videos using Google Veo 3.1"
    )
    subparsers = parser.add_subparsers(dest="command", help="Command")

    # Generate command
    gen_parser = subparsers.add_parser("generate", help="Generate a new video")
    gen_parser.add_argument("prompt", help="Video description")
    gen_parser.add_argument("--name", "-n", required=True, help="Output filename base")
    gen_parser.add_argument("--duration", "-d", type=int, default=8,
                           choices=[4, 6, 8], help="Duration in seconds")
    gen_parser.add_argument("--resolution", "-r", default="720p",
                           choices=["720p", "1080p"], help="Video resolution")
    gen_parser.add_argument("--aspect", "-a", default="16:9",
                           choices=["16:9", "9:16"], help="Aspect ratio")
    gen_parser.add_argument("--reference", action="append",
                           help="Reference image path (can use multiple)")
    gen_parser.add_argument("--negative", help="Negative prompt")

    # Extend command
    ext_parser = subparsers.add_parser("extend", help="Extend an existing video")
    ext_parser.add_argument("video", help="Path to video to extend")
    ext_parser.add_argument("prompt", help="Extension description")
    ext_parser.add_argument("--name", "-n", required=True, help="Output filename base")
    ext_parser.add_argument("--resolution", "-r", default="720p",
                           choices=["720p", "1080p"], help="Video resolution")

    # Default to generate if no subcommand
    args = parser.parse_args()

    if not args.command:
        # Allow direct usage without subcommand
        parser.print_help()
        return 1

    try:
        if args.command == "generate":
            ref_images = [Path(r) for r in args.reference] if args.reference else None
            result = generate_video(
                prompt=args.prompt,
                output_name=args.name,
                duration=args.duration,
                resolution=args.resolution,
                aspect_ratio=args.aspect,
                reference_images=ref_images,
                negative_prompt=args.negative,
            )
            print(str(result))

        elif args.command == "extend":
            result = extend_video(
                video_path=Path(args.video),
                prompt=args.prompt,
                output_name=args.name,
                resolution=args.resolution,
            )
            print(str(result))

        return 0

    except Exception as e:
        log(f"[ERROR] {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
