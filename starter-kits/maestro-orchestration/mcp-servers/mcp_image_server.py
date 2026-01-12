#!/usr/bin/env python3
"""
MCP Server for Bennie Bear Image Generation Pipeline
=====================================================
Exposes image generation tools to Claude Desktop/App via MCP protocol.

Usage:
    # Stdio transport (for Claude Desktop)
    python mcp_image_server.py

    # SSE transport (for web clients)
    python mcp_image_server.py --transport sse --port 8080

Configuration:
    Add to Claude Desktop config (%APPDATA%\\Claude\\claude_desktop_config.json):
    {
        "mcpServers": {
            "bennie-image-generator": {
                "command": "python",
                "args": ["path/to/mcp_image_server.py"],
                "env": {
                    "GOOGLE_API_KEY": "your-key"
                }
            }
        }
    }
"""

import os
import sys
import json
import asyncio
import base64
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Dict, Any
from concurrent.futures import ThreadPoolExecutor

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

# Check for MCP package
try:
    from mcp.server.fastmcp import FastMCP
except ImportError:
    print("[ERROR] MCP package not found. Install with: pip install mcp", file=sys.stderr)
    print("[INFO] Or run: pip install -r requirements.txt", file=sys.stderr)
    sys.exit(1)

# Import shared image compression utilities
try:
    from mcp_image_utils import compress_image_for_mcp, verify_size_limit
except ImportError:
    print("[WARN] mcp_image_utils not found, using legacy compression", file=sys.stderr)
    compress_image_for_mcp = None
    verify_size_limit = None

# Import resilience framework
try:
    from mcp_resilience import resilient_tool, handle_large_image
except ImportError:
    print("[WARN] mcp_resilience not found, using basic error handling", file=sys.stderr)
    def resilient_tool(**kwargs):
        def decorator(func):
            return func
        return decorator
    handle_large_image = None

# Import existing pipeline functions
from generate_image import (
    generate_single,
    generate_ab_comparison as ab_compare,
    load_learnings,
    enhance_prompt,
    CONFIG,
    BENNIE_SPEC,
    LEMMINGE_SPEC,
    PROJECT_STYLE,
    PROJECT_COLORS,
    log,
    # Video generation functions
    generate_video,
    generate_video_veo,
    extend_video_veo,
    generate_video_from_frames,
)

# Import reference style for style enforcement
try:
    from reference_style import (
        REFERENCE_STYLE,
        get_reference_prompt_prefix,
        get_full_reference_context,
    )
except ImportError:
    REFERENCE_STYLE = ""
    def get_reference_prompt_prefix(character=None):
        return ""
    def get_full_reference_context():
        return ""

# =============================================================================
# SERVER CONFIGURATION
# =============================================================================

def load_config() -> dict:
    """Load configuration from file or environment."""
    config_path = Path(__file__).parent / "mcp_config.json"

    defaults = {
        "server_name": "bennie-image-generator",
        "transport": os.environ.get("MCP_TRANSPORT", "stdio"),
        "sse_port": int(os.environ.get("MCP_PORT", "8080")),
        "max_concurrent": 2,
    }

    if config_path.exists():
        try:
            with open(config_path) as f:
                file_config = json.load(f)
                defaults.update(file_config)
        except Exception as e:
            log(f"[WARN] Could not load config: {e}")

    return defaults


server_config = load_config()

# =============================================================================
# MCP SERVER INITIALIZATION
# =============================================================================

mcp = FastMCP(
    server_config["server_name"],
)

# Thread pool for blocking operations
executor = ThreadPoolExecutor(max_workers=server_config.get("max_concurrent", 2))


# =============================================================================
# IMAGE PREVIEW HELPERS
# =============================================================================

def encode_image_base64(image_path: Path, max_bytes: int = 500_000) -> Optional[str]:
    """Encode image to base64, compressed to be under max_bytes.

    Args:
        image_path: Path to image file
        max_bytes: Max size in bytes after base64 encoding (default 500KB)

    Returns:
        Base64-encoded image string (JPEG, guaranteed under max_bytes) or None if error
    """
    try:
        # Use shared compression utility if available
        if compress_image_for_mcp:
            result = compress_image_for_mcp(
                image_path=image_path,
                max_bytes=max_bytes,
                save_compressed=False  # Don't save, just return b64
            )
            if result.get("success"):
                return result["image_b64"]
            else:
                log(f"[WARN] Compression failed for {image_path}: {result.get('error')}")
                return None

        # Fallback to legacy compression
        from PIL import Image
        import io

        with Image.open(image_path) as img:
            # Resize for preview if too large
            if max(img.size) > 1024:
                img.thumbnail((1024, 1024), Image.Resampling.LANCZOS)

            # Convert to RGB if necessary (for PNG with transparency)
            if img.mode in ('RGBA', 'P'):
                img = img.convert('RGB')

            # Encode to base64
            buffer = io.BytesIO()
            img.save(buffer, format='JPEG', quality=85)
            return base64.b64encode(buffer.getvalue()).decode('utf-8')
    except Exception as e:
        log(f"[WARN] Could not encode image {image_path}: {e}")
        return None


def get_images_for_review(image_paths: List[Path], max_images: int = 4) -> List[Dict]:
    """Get image data for Claude to review.

    Returns list of dicts with path, name, and base64 preview.
    """
    results = []
    for path in image_paths[:max_images]:
        if path.exists():
            b64 = encode_image_base64(path)
            results.append({
                "path": str(path),
                "name": path.name,
                "base64": b64,
                "mime_type": "image/jpeg",
            })
    return results


# =============================================================================
# TOOLS
# =============================================================================

@mcp.tool()
async def generate_image(
    prompt: str,
    name: str,
    category: str = "characters",
    count: int = 4,
    aspect_ratio: str = "16:9",
    character: Optional[str] = None,
) -> dict:
    """
    Generate autism-friendly character art for Bennie Bear game.

    Args:
        prompt: Description of what to generate (e.g., "Bennie waving hello")
        name: Base filename for outputs (e.g., "bennie-wave")
        category: Asset category - characters, expressions, environments, items, ui
        count: Number of variations to generate (1-8, default 4)
        aspect_ratio: Image aspect ratio - 1:1, 4:3, 16:9, 3:4 (default 16:9)
        character: Apply character spec - "bennie" or "lemminge"

    Returns:
        Dictionary with generated file paths and metadata
    """
    # Validate inputs
    if count < 1 or count > 8:
        return {"success": False, "error": "count must be between 1 and 8"}

    valid_categories = ["characters", "expressions", "environments", "items", "ui", "training"]
    if category not in valid_categories:
        return {"success": False, "error": f"category must be one of: {valid_categories}"}

    # Run generation in thread pool
    loop = asyncio.get_event_loop()
    try:
        result = await loop.run_in_executor(
            executor,
            lambda: generate_single(
                prompt=prompt,
                name=name,
                category=category,
                count=count,
                aspect_ratio=aspect_ratio,
                character=character,
            )
        )
        return {
            "success": True,
            "images": result.get("generated", []),
            "category": category,
            "prompt": prompt,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


@mcp.tool()
async def generate_ab_comparison(
    prompt: str,
    name: str,
    category: str = "characters",
    aspect_ratio: str = "16:9",
    character: Optional[str] = None,
    use_learnings: bool = True,
) -> dict:
    """
    Generate A/B comparison for training style preferences.

    Creates two image variations (A and B) with learnings applied,
    plus a side-by-side comparison grid for visual review.

    Args:
        prompt: Description of what to generate
        name: Session name for outputs
        category: Asset category
        aspect_ratio: Image aspect ratio
        character: Apply character spec - "bennie" or "lemminge"
        use_learnings: Whether to apply current learnings (default True)

    Returns:
        Dictionary with option_a, option_b, grid paths and session_id
    """
    loop = asyncio.get_event_loop()
    try:
        result = await loop.run_in_executor(
            executor,
            lambda: ab_compare(
                prompt=prompt,
                name=name,
                category=category,
                aspect_ratio=aspect_ratio,
                use_learnings=use_learnings,
                character=character,
                backend="auto",
            )
        )
        return {
            "success": True,
            **result,
            "instructions": "Review option_a and option_b, then use record_feedback to store your preference"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


@mcp.tool()
async def record_feedback(
    pattern: str,
    score: int,
    source: str,
    reason: str = "",
    category: str = "general"
) -> dict:
    """
    Record preference feedback in LEARNINGS.md.

    Updates the reinforcement learning patterns for future generations.

    Args:
        pattern: The pattern/style element being scored (e.g., "softer watercolor edges")
        score: Score value: 3 (strong positive), 1 (positive), 0 (neutral), -1 (negative), -3 (strong negative)
        source: Session ID or training source identifier
        reason: Explanation of why this pattern was scored
        category: Pattern category - bennie, lemminge, environments, items, general

    Returns:
        Confirmation of recorded feedback
    """
    import re

    valid_scores = [-3, -1, 0, 1, 3]
    if score not in valid_scores:
        return {"success": False, "error": f"score must be one of: {valid_scores}"}

    # Map score to section name
    score_sections = {
        3: "STRONG POSITIVE (+3)",
        1: "POSITIVE (+1)",
        0: "NEUTRAL (0)",
        -1: "NEGATIVE (-1)",
        -3: "STRONG NEGATIVE (-3)",
    }

    section_name = score_sections[score]
    date_str = datetime.now().strftime("%Y-%m-%d")

    # Read current file
    learnings_path = CONFIG.learnings_file
    if not learnings_path.exists():
        return {"success": False, "error": "LEARNINGS.md not found"}

    try:
        content = learnings_path.read_text(encoding='utf-8')

        # Build new entry
        source_with_reason = f"{source} ({reason})" if reason else source
        new_entry = f"| {pattern} | {source_with_reason} | {date_str} |"

        # Find section header and add after table header
        section_pattern = rf"(### {re.escape(section_name)}.*?\n\|.*?\n\|[-\s|]+\n)"
        match = re.search(section_pattern, content, re.DOTALL)

        if match:
            insert_pos = match.end()
            content = content[:insert_pos] + new_entry + "\n" + content[insert_pos:]
            learnings_path.write_text(content, encoding='utf-8')

            return {
                "success": True,
                "recorded": {
                    "pattern": pattern,
                    "score": score,
                    "section": section_name,
                    "source": source
                }
            }
        else:
            return {"success": False, "error": f"Could not find section: {section_name}"}

    except Exception as e:
        return {"success": False, "error": str(e)}


@mcp.tool()
async def get_learnings(
    category: Optional[str] = None,
    score_filter: Optional[int] = None
) -> dict:
    """
    Read current learnings from LEARNINGS.md.

    Args:
        category: Filter by category (bennie, lemminge, environments, items) - not yet implemented
        score_filter: Filter by score (3, 1, 0, -1, -3)

    Returns:
        Parsed patterns organized by score level
    """
    learnings = load_learnings()

    result = {
        "strong_positive": learnings.strong_positive,
        "positive": learnings.positive,
        "neutral": learnings.neutral,
        "negative": learnings.negative,
        "strong_negative": learnings.strong_negative,
    }

    if score_filter is not None:
        score_map = {
            3: "strong_positive",
            1: "positive",
            0: "neutral",
            -1: "negative",
            -3: "strong_negative",
        }
        key = score_map.get(score_filter)
        if key:
            result = {key: result[key]}

    # Add summary stats
    result["stats"] = {
        "total_patterns": sum(len(v) for v in [
            learnings.strong_positive,
            learnings.positive,
            learnings.neutral,
            learnings.negative,
            learnings.strong_negative,
        ])
    }

    return result


@mcp.tool()
async def list_generated(
    category: str = "all",
    limit: int = 20,
    include_metadata: bool = True
) -> dict:
    """
    List previously generated images.

    Args:
        category: Filter by category or 'all'
        limit: Maximum number of results (default 20)
        include_metadata: Include file size and timestamps

    Returns:
        List of generated image files with metadata
    """
    generated_dir = CONFIG.generated_dir

    if not generated_dir.exists():
        return {"images": [], "total": 0}

    # Collect image files
    images = []

    if category == "all":
        search_dirs = [generated_dir]
    else:
        search_dirs = [generated_dir / category]

    for search_dir in search_dirs:
        if not search_dir.exists():
            continue

        for img_path in search_dir.rglob("*.png"):
            entry = {"path": str(img_path), "name": img_path.name}

            if include_metadata:
                try:
                    stat = img_path.stat()
                    entry["size_kb"] = round(stat.st_size / 1024, 1)
                    entry["created"] = datetime.fromtimestamp(stat.st_mtime).isoformat()
                    entry["category"] = img_path.parent.name
                except Exception:
                    pass

            images.append(entry)

    # Sort by creation time, newest first
    images.sort(key=lambda x: x.get("created", ""), reverse=True)

    return {
        "images": images[:limit],
        "total": len(images),
        "showing": min(limit, len(images))
    }


# =============================================================================
# VIDEO GENERATION TOOLS
# =============================================================================

@mcp.tool()
async def generate_video_reference_images(
    character: str,
    action: str,
    prompt: str,
    count: int = 4,
    aspect_ratio: str = "16:9",
) -> dict:
    """
    Generate reference images for video generation.

    Creates images in a structured folder for later video generation.
    Folder structure: public/videos/inputs/{Character}/{Action}/

    Example: generate_video_reference_images("Bennie", "Looking", "Bennie looking curiously to the side")
    Creates: public/videos/inputs/Bennie/Looking/

    Args:
        character: Character name (e.g., "Bennie", "Lemminge")
        action: Action/pose name (e.g., "Looking", "Waving", "Celebrating")
        prompt: Description of the pose/action to generate
        count: Number of variations to generate (default 4)
        aspect_ratio: Image aspect ratio (default 16:9)

    Returns:
        Dictionary with folder path. Review images, delete bad ones, then use generate_video_from_folder.
    """
    loop = asyncio.get_event_loop()

    # Create structured folder path
    output_dir = CONFIG.video_inputs_dir / character / action
    output_dir.mkdir(parents=True, exist_ok=True)

    # Apply character spec
    char_lower = character.lower()
    char_spec = "bennie" if "bennie" in char_lower else "lemminge" if "lemming" in char_lower else None

    try:
        result = await loop.run_in_executor(
            executor,
            lambda: generate_single(
                prompt=prompt,
                name=action.lower(),
                category="videos",  # Just for logging
                count=count,
                aspect_ratio=aspect_ratio,
                character=char_spec,
                output_dir=output_dir,
            )
        )

        # List generated files and get previews for review
        generated_files = sorted(output_dir.glob("*.png"))
        images_for_review = get_images_for_review(generated_files)

        return {
            "success": True,
            "folder": str(output_dir),
            "character": character,
            "action": action,
            "images": images_for_review,
            "count": len(generated_files),
            "next_step": f"Review the images above. Delete any bad ones from the folder, then call generate_video_from_folder('{character}', '{action}', 'your video prompt')",
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


@mcp.tool()
async def generate_video_from_folder(
    character: str,
    action: str,
    prompt: str,
    duration: int = 8,
    resolution: str = "720p",
    aspect_ratio: str = "16:9",
) -> dict:
    """
    Generate video using reference images from an input folder.

    Uses images from public/videos/inputs/{Character}/{Action}/ as references.
    Make sure to review and curate the reference images before calling this.

    Args:
        character: Character name (e.g., "Bennie", "Lemminge")
        action: Action/pose name (e.g., "Looking", "Waving")
        prompt: Description of the video animation
        duration: Video duration in seconds (4, 6, or 8, default 8)
        resolution: Video resolution - 720p or 1080p (default 720p)
        aspect_ratio: Aspect ratio - 16:9 or 9:16 (default 16:9)

    Returns:
        Dictionary with video file path
    """
    from pathlib import Path as PyPath

    loop = asyncio.get_event_loop()

    # Find reference images folder
    input_folder = CONFIG.video_inputs_dir / character / action

    if not input_folder.exists():
        return {
            "success": False,
            "error": f"Input folder not found: {input_folder}",
            "hint": f"First call generate_video_reference_images('{character}', '{action}', 'your prompt')"
        }

    # Get reference images (up to 3)
    ref_images = sorted(input_folder.glob("*.png"))[:3]

    if not ref_images:
        return {
            "success": False,
            "error": f"No PNG images found in {input_folder}",
            "hint": "Generate reference images first using generate_video_reference_images"
        }

    # Output folder mirrors input structure
    output_dir = CONFIG.generated_videos_dir / character / action
    output_dir.mkdir(parents=True, exist_ok=True)

    # Apply character spec
    char_lower = character.lower()
    char_spec = "bennie" if "bennie" in char_lower else "lemminge" if "lemming" in char_lower else None

    try:
        result = await loop.run_in_executor(
            executor,
            lambda: generate_video(
                prompt=prompt,
                output_dir=output_dir,
                base_name=action.lower(),
                duration=duration,
                resolution=resolution,
                aspect_ratio=aspect_ratio,
                reference_images=ref_images,
                character=char_spec,
            )
        )
        return {
            "success": True,
            "video_path": str(result),
            "filename": result.name,
            "character": character,
            "action": action,
            "reference_images_used": [str(r) for r in ref_images],
            "duration": duration,
            "resolution": resolution,
            "timestamp": datetime.now().isoformat(),
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


@mcp.tool()
async def list_video_input_folders() -> dict:
    """
    List all video input folders with their reference images.

    Shows the folder structure under public/videos/inputs/
    organized by Character/Action.

    Returns:
        Dictionary with folder structure and image counts
    """
    inputs_dir = CONFIG.video_inputs_dir

    if not inputs_dir.exists():
        return {"folders": [], "total": 0}

    folders = []

    # Walk through Character/Action structure
    for char_dir in inputs_dir.iterdir():
        if char_dir.is_dir():
            for action_dir in char_dir.iterdir():
                if action_dir.is_dir():
                    images = list(action_dir.glob("*.png"))
                    folders.append({
                        "character": char_dir.name,
                        "action": action_dir.name,
                        "path": str(action_dir),
                        "image_count": len(images),
                        "images": [f.name for f in images],
                        "ready_for_video": len(images) > 0,
                    })

    return {
        "folders": folders,
        "total": len(folders),
        "base_path": str(inputs_dir),
    }


@mcp.tool()
async def review_video_inputs(
    character: str,
    action: str,
) -> dict:
    """
    Review the reference images in a video input folder.

    Shows all images in the folder so you can evaluate them before
    generating video. Use this to check what references are available.

    Args:
        character: Character name (e.g., "Bennie")
        action: Action/pose name (e.g., "Looking")

    Returns:
        Dictionary with image previews for review
    """
    input_folder = CONFIG.video_inputs_dir / character / action

    if not input_folder.exists():
        return {
            "success": False,
            "error": f"Folder not found: {input_folder}",
            "hint": f"First call generate_video_reference_images('{character}', '{action}', 'your prompt')"
        }

    images = sorted(input_folder.glob("*.png"))

    if not images:
        return {
            "success": False,
            "error": "No images found in folder",
            "folder": str(input_folder),
        }

    # Get previews for all images
    images_for_review = get_images_for_review(images, max_images=10)

    return {
        "success": True,
        "character": character,
        "action": action,
        "folder": str(input_folder),
        "images": images_for_review,
        "count": len(images),
        "ready_for_video": len(images) > 0,
        "next_step": f"If images look good, call generate_video_from_folder('{character}', '{action}', 'your video prompt')"
    }


@mcp.tool()
async def extend_video_clip(
    video_path: str,
    prompt: str,
    name: str,
    resolution: str = "720p",
) -> dict:
    """
    Extend an existing video by 7 seconds.

    Use this to create longer sequences by continuing a previously generated video.
    The extension will maintain visual continuity with the original.

    Args:
        video_path: Path to existing video to extend
        prompt: Description of what should happen in the continuation
        name: Base filename for extended video output
        resolution: Video resolution - 720p or 1080p (default 720p)

    Returns:
        Dictionary with extended video path and metadata
    """
    from pathlib import Path as PyPath

    loop = asyncio.get_event_loop()

    try:
        output_dir = CONFIG.generated_videos_dir / "extended"
        result = await loop.run_in_executor(
            executor,
            lambda: extend_video_veo(
                video_path=PyPath(video_path),
                prompt=prompt,
                output_dir=output_dir,
                base_name=name,
                resolution=resolution,
            )
        )
        return {
            "success": True,
            "video_path": str(result),
            "filename": result.name,
            "source_video": video_path,
            "prompt": prompt,
            "timestamp": datetime.now().isoformat(),
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


@mcp.tool()
async def generate_transition_video(
    first_frame_path: str,
    last_frame_path: str,
    prompt: str,
    name: str,
    duration: int = 8,
    aspect_ratio: str = "16:9",
) -> dict:
    """
    Generate a video that transitions between two images.

    Creates smooth animation interpolating from the first frame to the last frame.
    Perfect for creating transitions between different character poses or scenes.

    Args:
        first_frame_path: Path to the starting frame image
        last_frame_path: Path to the ending frame image
        prompt: Description of the transition motion
        name: Base filename for output video
        duration: Video duration in seconds (4, 6, or 8, default 8)
        aspect_ratio: Aspect ratio - 16:9 or 9:16 (default 16:9)

    Returns:
        Dictionary with generated transition video path and metadata
    """
    from pathlib import Path as PyPath

    loop = asyncio.get_event_loop()

    try:
        output_dir = CONFIG.generated_videos_dir / "transitions"
        result = await loop.run_in_executor(
            executor,
            lambda: generate_video_from_frames(
                first_frame=PyPath(first_frame_path),
                last_frame=PyPath(last_frame_path),
                prompt=prompt,
                output_dir=output_dir,
                base_name=name,
                duration=duration,
                aspect_ratio=aspect_ratio,
            )
        )
        return {
            "success": True,
            "video_path": str(result),
            "filename": result.name,
            "first_frame": first_frame_path,
            "last_frame": last_frame_path,
            "prompt": prompt,
            "timestamp": datetime.now().isoformat(),
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


@mcp.tool()
async def list_generated_videos(
    limit: int = 20,
    include_metadata: bool = True
) -> dict:
    """
    List previously generated videos.

    Args:
        limit: Maximum number of results (default 20)
        include_metadata: Include file size and timestamps

    Returns:
        List of generated video files with metadata
    """
    videos_dir = CONFIG.generated_videos_dir

    if not videos_dir.exists():
        return {"videos": [], "total": 0}

    videos = []

    for video_path in videos_dir.rglob("*.mp4"):
        entry = {"path": str(video_path), "name": video_path.name}

        if include_metadata:
            try:
                stat = video_path.stat()
                entry["size_mb"] = round(stat.st_size / (1024 * 1024), 2)
                entry["created"] = datetime.fromtimestamp(stat.st_mtime).isoformat()
                entry["category"] = video_path.parent.name
            except Exception:
                pass

        videos.append(entry)

    # Sort by creation time, newest first
    videos.sort(key=lambda x: x.get("created", ""), reverse=True)

    return {
        "videos": videos[:limit],
        "total": len(videos),
        "showing": min(limit, len(videos))
    }


@mcp.tool()
async def get_reference_images() -> dict:
    """
    Get paths to the approved Bennie Bear reference images.

    These are the Gemini Preview 3.0 generated reference images that define
    the canonical Bennie Bear style. Use these as reference_images when
    generating new videos to maintain style consistency.

    Returns:
        Dictionary with paths to reference images
    """
    references_dir = CONFIG.project_root / "designer system" / "References"

    if not references_dir.exists():
        return {"success": False, "error": "References directory not found"}

    reference_files = []
    for img_path in references_dir.glob("*.png"):
        reference_files.append({
            "path": str(img_path),
            "name": img_path.name
        })

    # Also check for approved training images
    training_dir = CONFIG.generated_dir / "training"
    approved_training = []
    if training_dir.exists():
        for img_path in training_dir.glob("*-approved*.png"):
            approved_training.append({
                "path": str(img_path),
                "name": img_path.name
            })

    return {
        "success": True,
        "reference_images": reference_files,
        "approved_training": approved_training,
        "usage": "Pass these paths to reference_images parameter in generate_video_clip"
    }


# =============================================================================
# RESOURCES
# =============================================================================

@mcp.resource("learnings://current")
async def resource_learnings() -> str:
    """Get current LEARNINGS.md content."""
    if CONFIG.learnings_file.exists():
        return CONFIG.learnings_file.read_text(encoding='utf-8')
    return "# No learnings file found"


@mcp.resource("character://spec/bennie")
async def resource_bennie_spec() -> str:
    """Get Bennie the Bear character specification."""
    return f"# Bennie the Bear - Character Specification\n\n{BENNIE_SPEC}"


@mcp.resource("character://spec/lemminge")
async def resource_lemminge_spec() -> str:
    """Get Lemminge group character specification."""
    return f"# The Lemminge - Character Specification\n\n{LEMMINGE_SPEC}"


@mcp.resource("style://guide")
async def resource_style_guide() -> str:
    """Get project style guidelines."""
    return f"""# Bennie Bear Style Guide

## Reference Style (Gemini Preview 3.0)
{get_full_reference_context()}

## Project Style
{PROJECT_STYLE}

## Color Palette
{PROJECT_COLORS}
"""


@mcp.resource("style://reference")
async def resource_reference_style() -> str:
    """Get the definitive reference style from Gemini Preview 3.0."""
    return f"""# Bennie Bear Reference Style

{get_full_reference_context()}

CRITICAL: All generated images MUST match this style exactly.
- Clean digital illustration (NOT watercolor)
- Soft black outlines
- Smooth fur (NOT fluffy/textured)
- NO scarf or accessories
- Cream background (#FAF5EB)
- Mobile game aesthetic
"""


# =============================================================================
# SERVER ENTRY POINT
# =============================================================================

def main():
    """Run the MCP server."""
    import argparse

    parser = argparse.ArgumentParser(description="Bennie Bear Image Generation MCP Server")
    parser.add_argument("--transport", choices=["stdio", "sse"],
                       default=server_config["transport"],
                       help="Transport protocol (default: stdio)")
    parser.add_argument("--port", type=int, default=server_config["sse_port"],
                       help="Port for SSE transport (default: 8080)")

    args = parser.parse_args()

    log(f"[MCP] Starting Bennie Bear Image Generator Server")
    log(f"[MCP] Transport: {args.transport}")
    if args.transport == "sse":
        log(f"[MCP] Port: {args.port}")

    if args.transport == "sse":
        mcp.run(transport="sse", port=args.port)
    else:
        mcp.run()  # stdio is default


if __name__ == "__main__":
    main()
