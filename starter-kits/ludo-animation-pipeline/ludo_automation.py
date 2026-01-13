#!/usr/bin/env python3
"""
Ludo.ai Browser Automation Module
=================================
Provides MCP tool call sequences for automating sprite animation generation
on ludo.ai using Chrome DevTools MCP.

This module is designed to be invoked by Claude Code. It outputs the
MCP tool calls that Claude should execute to automate the browser.

Prerequisites:
    1. Chrome running in debug mode: ./scripts/launch-chrome-debug.sh
       Profile path: /Users/user289321/chrome-debug-profile (see .planning/config.json)
       Debug port: 9222
    2. Logged into ludo.ai account (session persists in debug profile)
    3. Chrome DevTools MCP server connected to localhost:9222

Usage:
    # From Claude Code, use the ludo-automation skill
    # Or manually: python ludo_automation.py bennie waving
"""

import json
import re
from pathlib import Path
from dataclasses import dataclass, asdict, field
from typing import Optional, Dict, Any, List, Tuple
from datetime import datetime


# =============================================================================
# ANIMATION JOB DEFINITION
# =============================================================================

SCRIPT_DIR = Path(__file__).parent.resolve()
DOWNLOADS_DIR = SCRIPT_DIR / "downloads"

@dataclass
class AnimationJob:
    """Represents a single animation generation job for Ludo.ai."""
    character: str
    emotion: str
    start_frame: Path
    end_frame: Optional[Path] = None
    motion_prompt: str = ""
    frame_count: int = 8
    output_name: str = ""
    status: str = "pending"
    warnings: List[str] = field(default_factory=list)
    download_path: Optional[Path] = None
    error: Optional[str] = None
    created_at: str = None

    def __post_init__(self):
        if not self.output_name:
            self.output_name = f"{self.character}_{self.emotion}"
        if self.created_at is None:
            self.created_at = datetime.now().isoformat()

    def to_dict(self) -> Dict[str, Any]:
        result = asdict(self)
        result["start_frame"] = str(self.start_frame) if self.start_frame else None
        result["end_frame"] = str(self.end_frame) if self.end_frame else None
        result["download_path"] = str(self.download_path) if self.download_path else None
        return result


# =============================================================================
# MOTION PROMPTS FOR LUDO.AI
# =============================================================================

MOTION_PROMPTS = {
    "bennie": {
        "idle": "gentle breathing cycle, chest slowly rising and falling, calm peaceful rhythmic motion, standing still",
        "happy": "gentle bounce up and down, cheerful rhythmic movement, slight hop with joy",
        "thinking": "head tilting side to side slowly, thoughtful pondering motion, hand on chin",
        "encouraging": "arms opening outward in welcoming gesture, supportive nodding movement",
        "celebrating": "arms raising up high in celebration, joyful controlled bouncing",
        "waving": "hand waving side to side smoothly, friendly greeting gesture, arm moving",
        "pointing": "arm extending outward to point, head turning to look at pointed direction"
    },
    "lemminge": {
        "idle": "subtle breathing pulse, gentle body expanding and contracting rhythmically",
        "curious": "head tilting curiously from side to side, leaning forward with interest",
        "excited": "bouncing up and down rapidly, energetic jumping motion, arms raising",
        "celebrating": "jumping with arms raised high, victory dance movement, joyful bounce",
        "hiding": "shrinking down motion, paws moving to cover face, nervous shaking",
        "mischievous": "sneaky side-to-side swaying, hands rubbing together, shifty eyes"
    }
}


# =============================================================================
# LUDO.AI URL AND SETTINGS
# =============================================================================

LUDO_CONFIG = {
    "base_url": "https://ludo.ai",
    "sprite_generator_url": "https://ludo.ai/tools/sprite-generator",
    "login_url": "https://ludo.ai/login",
    "default_frame_count": 8,
    "default_timeout": 120000,  # 2 minutes for generation
    "download_timeout": 30000,   # 30 seconds for download
    "downloads_dir": str(DOWNLOADS_DIR),
}


# =============================================================================
# KEYFRAME VALIDATION
# =============================================================================

def _token_match(name: str, token: str) -> bool:
    """Match token as a whole word segment in filenames."""
    return re.search(rf"(^|[_\\-.]){re.escape(token)}([_\\-.]|$)", name.lower()) is not None


def normalize_keyframes(
    start_frame: Path,
    end_frame: Optional[Path],
) -> Tuple[Path, Optional[Path], List[str]]:
    """Detect obvious start/end swaps by filename and return warnings."""
    warnings: List[str] = []

    if not end_frame:
        return start_frame, end_frame, warnings

    start_name = start_frame.name
    end_name = end_frame.name

    start_has_start = _token_match(start_name, "start")
    start_has_end = _token_match(start_name, "end")
    end_has_start = _token_match(end_name, "start")
    end_has_end = _token_match(end_name, "end")

    if start_has_end and end_has_start and not start_has_start and not end_has_end:
        warnings.append("Detected swapped keyframes by filename; auto-swapping.")
        return end_frame, start_frame, warnings

    if start_has_end:
        warnings.append(f"Start frame filename looks like an end frame: {start_name}")
    if end_has_start:
        warnings.append(f"End frame filename looks like a start frame: {end_name}")
    if not start_has_start:
        warnings.append(f"Start frame filename does not indicate start: {start_name}")
    if not end_has_end:
        warnings.append(f"End frame filename does not indicate end: {end_name}")
    if start_frame == end_frame:
        warnings.append("Start and end frames are the same file.")

    return start_frame, end_frame, warnings


# =============================================================================
# MCP AUTOMATION SEQUENCES
# =============================================================================

def get_navigation_sequence() -> str:
    """MCP sequence to navigate to sprite generator."""
    return """
## Step 1: Navigate to Ludo.ai Sprite Generator

```
mcp__chrome-devtools__navigate_page
├── type: "url"
└── url: "https://ludo.ai/tools/sprite-generator"
```

Wait for page load:
```
mcp__chrome-devtools__wait_for
├── text: "Sprite"
└── timeout: 15000
```
"""


def get_snapshot_sequence() -> str:
    """MCP sequence to capture page state and identify elements."""
    return """
## Step 2: Capture Page Snapshot

Take accessibility snapshot to find UI elements:
```
mcp__chrome-devtools__take_snapshot
```

This returns element UIDs. Look for:
- File upload inputs (start/end keyframes)
- Prompt/description textarea
- Frame count selector
- Style/settings dropdowns
- Generate button
- Download button (after generation)

Common element patterns to look for in snapshot:
- role="textbox" → Text inputs
- role="button" → Clickable buttons
- role="combobox" → Dropdowns
- "file" or "upload" in name → File inputs
"""


def get_upload_sequence(image_path: str, label: str, uid_placeholder: str) -> str:
    """MCP sequence to upload a keyframe image."""
    return f"""
### {label} keyframe

Verify the filename matches the label before upload (start vs end).

```
mcp__chrome-devtools__upload_file
├── uid: "{uid_placeholder}"
└── filePath: "{image_path}"
```

Verify upload success by checking for:
- Image preview appearing
- Upload success message
- "Change" or "Replace" button appearing
"""


def get_upload_keyframes_sequence(start_path: str, end_path: Optional[str]) -> str:
    """MCP sequence to upload start and end keyframes."""
    sequence = f"""
## Step 3: Upload Keyframes (Start + End)

Find the START keyframe upload input (often labeled "Start" or first slot).
{get_upload_sequence(start_path, "Start", "<START_FRAME_INPUT_UID>")}
"""

    if end_path:
        sequence += f"""
Find the END keyframe upload input (often labeled "End" or second slot).
If needed, click "Add keyframe" before uploading.
{get_upload_sequence(end_path, "End", "<END_FRAME_INPUT_UID>")}
"""
    else:
        sequence += """
[WARN] End keyframe is missing. Ludo will only use the start frame.
"""

    return sequence


def get_prompt_sequence(motion_prompt: str) -> str:
    """MCP sequence to fill animation prompt."""
    return f"""
## Step 4: Set Animation Prompt

Find prompt/description textarea from snapshot.
Look for:
- Large textarea
- Placeholder text like "Describe..." or "Enter prompt..."
- Element with role="textbox" and multiline

```
mcp__chrome-devtools__fill
├── uid: "<PROMPT_TEXTAREA_UID>"
└── value: "{motion_prompt}"
```
"""


def get_settings_sequence(frame_count: int = 8) -> str:
    """MCP sequence to configure animation settings."""
    return f"""
## Step 5: Configure Animation Settings

### Frame Count (if available)
```
mcp__chrome-devtools__fill
├── uid: "<FRAME_COUNT_INPUT_UID>"
└── value: "{frame_count}"
```

### Transparent Background (if checkbox)
```
mcp__chrome-devtools__click
└── uid: "<TRANSPARENT_BG_CHECKBOX_UID>"
```

### Animation Style (if dropdown)
```
mcp__chrome-devtools__click
└── uid: "<STYLE_DROPDOWN_UID>"
```
Then:
```
mcp__chrome-devtools__click
└── uid: "<LOOP_OPTION_UID>"
```
"""


def get_generate_sequence() -> str:
    """MCP sequence to trigger generation."""
    return """
## Step 6: Start Generation

Find and click the generate button.
Look for: "Generate", "Create", "Animate" button text.

```
mcp__chrome-devtools__click
└── uid: "<GENERATE_BUTTON_UID>"
```

Expected result:
- Loading/progress indicator appears
- Generation status shown
- Wait for "Download" button to appear
"""


def get_wait_sequence() -> str:
    """MCP sequence to wait for generation completion."""
    return """
## Step 7: Wait for Generation to Complete

Poll for completion by waiting for download button:

```
mcp__chrome-devtools__wait_for
├── text: "Download"
└── timeout: 120000
```

If wait times out:
1. Take screenshot to check status
2. Look for error messages
3. If still processing, wait longer

Alternative: Check progress with evaluate_script:
```
mcp__chrome-devtools__evaluate_script
└── function: "() => {
      const progress = document.querySelector('[class*=progress]');
      return progress ? progress.textContent : 'no progress element';
    }"
```
"""


def get_download_sequence() -> str:
    """MCP sequence to download the result."""
    downloads_path = str(DOWNLOADS_DIR)
    return f"""
## Step 8: Download Animation

Click download button:
```
mcp__chrome-devtools__click
└── uid: "<DOWNLOAD_BUTTON_UID>"
```

If format selection dialog appears:
```
mcp__chrome-devtools__click
└── uid: "<PNG_SEQUENCE_OPTION_UID>"
```

Confirm download:
```
mcp__chrome-devtools__click
└── uid: "<CONFIRM_DOWNLOAD_UID>"
```

Download will be saved to:
{downloads_path}

If your browser saves elsewhere, move the ZIP into this folder before running process.py.
"""


def get_verify_sequence() -> str:
    """MCP sequence to verify download."""
    downloads_path = str(DOWNLOADS_DIR)
    return f"""
## Step 9: Verify Download

Check that ZIP file appeared in downloads folder.

On Windows:
```powershell
Get-ChildItem -Path "{downloads_path}" -Filter *.zip
```

Look for most recent file matching animation name.

If download not found:
1. Take screenshot to check page state
2. Look for download manager in browser
3. Check for popup blockers
"""


# =============================================================================
# COMPLETE AUTOMATION SCRIPT GENERATOR
# =============================================================================

def generate_automation_script(job: AnimationJob) -> str:
    """Generate complete MCP automation script for a job.

    This returns a markdown document with all MCP tool calls
    that Claude Code should execute in sequence.
    """
    warnings_block = ""
    if job.warnings:
        warning_lines = "\n".join(f"- {w}" for w in job.warnings)
        warnings_block = f"""
## Warnings
{warning_lines}

---
"""

    script = f"""
# Ludo.ai Animation Automation Script

## Job Details

| Field | Value |
|-------|-------|
| Character | {job.character} |
| Emotion | {job.emotion} |
| Motion | {job.motion_prompt} |
| Frames | {job.frame_count} |
| Start Frame | {job.start_frame} |
| End Frame | {job.end_frame or 'N/A'} |
| Downloads Dir | {DOWNLOADS_DIR} |

---

{warnings_block}

{get_navigation_sequence()}

---

{get_snapshot_sequence()}

---

{get_upload_keyframes_sequence(str(job.start_frame), str(job.end_frame) if job.end_frame else None)}

---

{get_prompt_sequence(job.motion_prompt)}

---

{get_settings_sequence(job.frame_count)}

---

{get_generate_sequence()}

---

{get_wait_sequence()}

---

{get_download_sequence()}

---

{get_verify_sequence()}

---

## Post-Download Processing

After the download completes, process the ZIP:

```bash
cd "{SCRIPT_DIR}"
python process.py
```

Or continue pipeline:

```bash
python pipeline.py --continue {job.character} {job.emotion} --zip "{DOWNLOADS_DIR}\\animation.zip"
```

---

## Error Recovery

### If upload fails:
1. Take screenshot to see page state
2. Take fresh snapshot to get new UIDs
3. Try clicking upload area first, then upload_file

### If generation times out:
1. Take screenshot to check progress
2. Wait for additional 60 seconds
3. If error shown, capture text and restart

### If download doesn't start:
1. Take fresh snapshot
2. Look for alternative download buttons
3. Check for format selection dialogs
4. Try right-click save-as via evaluate_script
"""
    return script


# =============================================================================
# ELEMENT DISCOVERY HELPER
# =============================================================================

def get_discovery_script() -> str:
    """Get script for discovering Ludo.ai UI elements."""
    return """
# Ludo.ai UI Element Discovery

Run this sequence to map the interface elements.
Execute these MCP tool calls and document the UIDs found.

## 1. Navigate to Sprite Generator

```
mcp__chrome-devtools__navigate_page
├── type: "url"
└── url: "https://ludo.ai/tools/sprite-generator"
```

```
mcp__chrome-devtools__wait_for
├── text: "Sprite"
└── timeout: 15000
```

## 2. Take Initial Snapshot

```
mcp__chrome-devtools__take_snapshot
```

## 3. Document Key Elements

From the snapshot, identify and record UIDs for:

### Upload Elements
| Element | Description | UID |
|---------|-------------|-----|
| Start keyframe | Start image upload input | |
| End keyframe | End image upload input | |
| Upload button | "Upload" or "Choose file" button | |
| Upload area | Drag-drop zone | |

### Text Inputs
| Element | Description | UID |
|---------|-------------|-----|
| Prompt textarea | Animation description input | |
| Title input | Optional name field | |

### Settings Controls
| Element | Description | UID |
|---------|-------------|-----|
| Frame count | Number of frames selector | |
| Duration | Animation length input | |
| Transparent BG | Background toggle/checkbox | |
| Style dropdown | Animation style selector | |

### Action Buttons
| Element | Description | UID |
|---------|-------------|-----|
| Generate | Main action button | |
| Preview | Optional preview button | |
| Reset | Clear/reset button | |

### Post-Generation Elements
| Element | Description | UID |
|---------|-------------|-----|
| Download | Download result button | |
| Format select | Output format dropdown | |
| Confirm | Download confirmation | |

## 4. Test Interactions

After documenting UIDs, test each critical interaction:

1. File upload
2. Text input
3. Generate click
4. Download click

## 5. Save Element Map

Save discovered UIDs to: `ludo/ui_elements.json`

```json
{
    "version": "2024-12",
    "discovered_at": "<timestamp>",
    "elements": {
        "file_upload": "<uid>",
        "prompt_textarea": "<uid>",
        "frame_count": "<uid>",
        "generate_button": "<uid>",
        "download_button": "<uid>"
    }
}
```
"""


# =============================================================================
# JOB CREATION
# =============================================================================

def create_animation_job(
    character: str,
    emotion: str,
    start_frame: Path,
    end_frame: Path = None,
    frame_count: int = 8,
) -> AnimationJob:
    """Create an animation job with appropriate motion prompt."""
    start_frame, end_frame, warnings = normalize_keyframes(start_frame, end_frame)
    char_prompts = MOTION_PROMPTS.get(character.lower(), {})
    motion_prompt = char_prompts.get(emotion.lower(), "")

    if not motion_prompt:
        motion_prompt = f"smooth animation of {character} {emotion}"

    return AnimationJob(
        character=character,
        emotion=emotion,
        start_frame=start_frame,
        end_frame=end_frame,
        motion_prompt=motion_prompt,
        frame_count=frame_count,
        warnings=warnings,
    )


# =============================================================================
# CLI INTERFACE
# =============================================================================

def main():
    import argparse
    import sys

    parser = argparse.ArgumentParser(
        description="Generate Ludo.ai automation script",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "character",
        nargs="?",
        choices=["bennie", "lemminge"],
        help="Character to animate"
    )
    parser.add_argument(
        "emotion",
        nargs="?",
        help="Emotion/animation state"
    )
    parser.add_argument(
        "--start-frame",
        type=Path,
        help="Path to start frame image"
    )
    parser.add_argument(
        "--end-frame",
        type=Path,
        help="Path to end frame image (optional)"
    )
    parser.add_argument(
        "--frames",
        type=int,
        default=8,
        help="Number of animation frames"
    )
    parser.add_argument(
        "--discover",
        action="store_true",
        help="Output UI element discovery script"
    )

    args = parser.parse_args()

    # Discovery mode
    if args.discover:
        print(get_discovery_script())
        return 0

    # Validate arguments
    if not args.character:
        parser.print_help()
        return 1

    if not args.emotion:
        print(f"\nAvailable emotions for {args.character}:")
        for e in MOTION_PROMPTS.get(args.character, {}).keys():
            print(f"  - {e}")
        return 1

    # Create job
    start_frame = args.start_frame
    if not start_frame:
        # Default location
        start_frame = Path(__file__).parent / "keyframes" / f"{args.character}_{args.emotion}" / f"{args.character}_{args.emotion}_start_v1.png"

    job = create_animation_job(
        character=args.character,
        emotion=args.emotion,
        start_frame=start_frame,
        end_frame=args.end_frame,
        frame_count=args.frames,
    )

    # Output automation script
    print(generate_automation_script(job))
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
