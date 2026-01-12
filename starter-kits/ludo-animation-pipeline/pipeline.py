#!/usr/bin/env python3
"""
Ludo.ai Animation Pipeline Orchestrator
========================================
Coordinates the full animation generation workflow:
1. Generate keyframes with Gemini 3.0
2. Output MCP automation script for ludo.ai
3. Process downloaded ZIPs to Lottie
4. Validate and deploy animations

Usage:
    # Generate keyframes and get automation script
    python pipeline.py bennie waving

    # Continue after download (process ZIP to Lottie)
    python pipeline.py --continue bennie waving --zip path/to/download.zip

    # Generate all animations for a character
    python pipeline.py bennie --all

    # Show current status
    python pipeline.py --status

Dependencies:
    - generate_keyframes.py (Gemini integration)
    - ludo_automation.py (MCP sequences)
    - process.py (ZIP to Lottie conversion)
"""

import sys
import json
import argparse
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass, asdict, field
from typing import List, Optional, Dict, Any
from enum import Enum

# Local imports
try:
    from generate_keyframes import (
        generate_keyframe_pair,
        KeyframePair,
        KEYFRAME_PROMPTS,
        list_available_emotions,
    )
    from ludo_automation import (
        AnimationJob,
        create_animation_job,
        generate_automation_script,
        get_discovery_script,
    )
    from process import process_zip, show_detailed_status, load_status, save_status
except ImportError as e:
    print(f"[ERROR] Import failed: {e}", file=sys.stderr)
    print("[INFO] Ensure all modules are in starter-kits/ludo-animation-pipeline/", file=sys.stderr)
    sys.exit(1)


# =============================================================================
# PIPELINE CONFIGURATION
# =============================================================================

class PipelinePhase(Enum):
    """Phases of the animation pipeline."""
    INIT = "init"
    KEYFRAMES = "keyframes"
    BROWSER = "browser"  # MCP automation
    DOWNLOAD = "download"
    PROCESS = "process"
    VALIDATE = "validate"
    COMPLETE = "complete"
    FAILED = "failed"


PIPELINE_CONFIG = {
    "keyframes_dir": Path(__file__).parent / "keyframes",
    "downloads_dir": Path(__file__).parent / "downloads",
    "output_dir": Path(__file__).parent / "output",
    "state_file": Path(__file__).parent / "pipeline_state.json",
}


# =============================================================================
# PIPELINE JOB TRACKING
# =============================================================================

@dataclass
class PipelineJob:
    """Tracks a job through all pipeline phases."""
    character: str
    emotion: str
    phase: PipelinePhase = PipelinePhase.INIT
    keyframe_start: Optional[Path] = None
    keyframe_end: Optional[Path] = None
    motion_hint: str = ""
    download_path: Optional[Path] = None
    lottie_output: Optional[Path] = None
    started_at: str = None
    completed_at: str = None
    error: str = None

    def __post_init__(self):
        if self.started_at is None:
            self.started_at = datetime.now().isoformat()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "character": self.character,
            "emotion": self.emotion,
            "phase": self.phase.value,
            "keyframe_start": str(self.keyframe_start) if self.keyframe_start else None,
            "keyframe_end": str(self.keyframe_end) if self.keyframe_end else None,
            "motion_hint": self.motion_hint,
            "download_path": str(self.download_path) if self.download_path else None,
            "lottie_output": str(self.lottie_output) if self.lottie_output else None,
            "started_at": self.started_at,
            "completed_at": self.completed_at,
            "error": self.error,
        }


# =============================================================================
# STATE MANAGEMENT
# =============================================================================

def load_pipeline_state() -> Dict[str, Any]:
    """Load pipeline state from file."""
    state_file = PIPELINE_CONFIG["state_file"]
    if state_file.exists():
        try:
            with open(state_file) as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {"jobs": [], "last_run": None}
    return {"jobs": [], "last_run": None}


def save_pipeline_state(state: Dict[str, Any]) -> None:
    """Save pipeline state to file."""
    state["last_run"] = datetime.now().isoformat()
    with open(PIPELINE_CONFIG["state_file"], "w") as f:
        json.dump(state, f, indent=2, default=str)


def add_job_to_state(job: PipelineJob) -> None:
    """Add or update job in state file."""
    state = load_pipeline_state()
    jobs = state.get("jobs", [])

    # Remove existing job with same character/emotion
    jobs = [j for j in jobs if not (
        j.get("character") == job.character and
        j.get("emotion") == job.emotion
    )]

    jobs.append(job.to_dict())
    state["jobs"] = jobs
    save_pipeline_state(state)


# =============================================================================
# PIPELINE PHASES
# =============================================================================

def phase_generate_keyframes(job: PipelineJob) -> PipelineJob:
    """Phase 1: Generate start/end keyframes with Gemini."""
    print()
    print("=" * 60)
    print(f"PHASE 1: KEYFRAME GENERATION")
    print(f"Character: {job.character}")
    print(f"Emotion: {job.emotion}")
    print("=" * 60)

    try:
        keyframes_dir = PIPELINE_CONFIG["keyframes_dir"]
        job_dir = keyframes_dir / f"{job.character}_{job.emotion}"

        keyframe_pair = generate_keyframe_pair(
            character=job.character,
            emotion=job.emotion,
            output_dir=job_dir,
        )

        job.keyframe_start = keyframe_pair.start_frame
        job.keyframe_end = keyframe_pair.end_frame
        job.motion_hint = keyframe_pair.motion_hint
        job.phase = PipelinePhase.BROWSER

        print()
        print("[OK] Keyframes generated successfully!")
        print(f"  Start: {job.keyframe_start}")
        print(f"  End: {job.keyframe_end}")

    except Exception as e:
        job.error = str(e)
        job.phase = PipelinePhase.FAILED
        print(f"\n[ERROR] Keyframe generation failed: {e}")

    return job


def phase_browser_automation(job: PipelineJob) -> str:
    """Phase 2: Generate MCP automation script for Claude to execute."""
    if not job.keyframe_start:
        raise ValueError("No keyframe available - run keyframe phase first")

    animation_job = create_animation_job(
        character=job.character,
        emotion=job.emotion,
        start_frame=job.keyframe_start,
        end_frame=job.keyframe_end,
    )

    script = generate_automation_script(animation_job)
    return script


def phase_process_download(job: PipelineJob, zip_path: Path) -> PipelineJob:
    """Phase 3: Process downloaded ZIP to Lottie."""
    print()
    print("=" * 60)
    print(f"PHASE 3: PROCESSING DOWNLOAD")
    print(f"ZIP: {zip_path}")
    print("=" * 60)

    if not zip_path.exists():
        job.error = f"ZIP file not found: {zip_path}"
        job.phase = PipelinePhase.FAILED
        print(f"\n[ERROR] {job.error}")
        return job

    try:
        job.download_path = zip_path

        # Use existing processor
        result = process_zip(zip_path)

        if result and result.exists():
            job.lottie_output = result
            job.phase = PipelinePhase.COMPLETE
            job.completed_at = datetime.now().isoformat()
            print(f"\n[OK] Lottie created: {result}")
        else:
            raise RuntimeError("Processing produced no output")

    except Exception as e:
        job.error = str(e)
        job.phase = PipelinePhase.FAILED
        print(f"\n[ERROR] Processing failed: {e}")

    return job


# =============================================================================
# MAIN PIPELINE FLOW
# =============================================================================

def run_pipeline(character: str, emotion: str) -> PipelineJob:
    """
    Run the pipeline for a single animation.

    Returns the job object. After keyframe generation, outputs
    the MCP automation script for Claude to execute.
    """
    job = PipelineJob(character=character, emotion=emotion, phase=PipelinePhase.INIT)

    # Phase 1: Generate keyframes
    job = phase_generate_keyframes(job)

    if job.phase == PipelinePhase.FAILED:
        add_job_to_state(job)
        return job

    # Phase 2: Output MCP automation script
    job.phase = PipelinePhase.BROWSER
    add_job_to_state(job)

    mcp_script = phase_browser_automation(job)

    print()
    print("=" * 60)
    print("PHASE 2: BROWSER AUTOMATION REQUIRED")
    print("=" * 60)
    print()
    print("Claude: Please execute the following MCP tool calls")
    print("to automate Ludo.ai animation generation.")
    print()
    print("-" * 60)
    print(mcp_script)
    print("-" * 60)
    print()
    print("After download completes, run:")
    print(f'  python pipeline.py --continue {character} {emotion} --zip <path_to_zip>')
    print()

    return job


def continue_pipeline(character: str, emotion: str, zip_path: Path) -> PipelineJob:
    """Continue pipeline after manual download."""
    job = PipelineJob(
        character=character,
        emotion=emotion,
        phase=PipelinePhase.DOWNLOAD,
    )

    # Load existing keyframe info if available
    state = load_pipeline_state()
    for j in state.get("jobs", []):
        if j.get("character") == character and j.get("emotion") == emotion:
            if j.get("keyframe_start"):
                job.keyframe_start = Path(j["keyframe_start"])
            if j.get("keyframe_end"):
                job.keyframe_end = Path(j["keyframe_end"])
            if j.get("motion_hint"):
                job.motion_hint = j["motion_hint"]

    # Phase 3: Process download
    job = phase_process_download(job, zip_path)
    add_job_to_state(job)

    if job.phase == PipelinePhase.COMPLETE:
        print()
        print("=" * 60)
        print("PIPELINE COMPLETE!")
        print("=" * 60)
        print(f"  Character: {job.character}")
        print(f"  Emotion: {job.emotion}")
        print(f"  Lottie: {job.lottie_output}")
        print()

    return job


def show_pipeline_status() -> None:
    """Show pipeline and animation status."""
    print()
    print("=" * 60)
    print("PIPELINE STATUS")
    print("=" * 60)

    state = load_pipeline_state()
    jobs = state.get("jobs", [])

    if jobs:
        print(f"\nLast run: {state.get('last_run', 'Never')}")
        print(f"Jobs tracked: {len(jobs)}")
        print()

        # Group by status
        by_phase = {}
        for j in jobs:
            phase = j.get("phase", "unknown")
            by_phase.setdefault(phase, []).append(j)

        for phase, phase_jobs in sorted(by_phase.items()):
            print(f"\n{phase.upper()}:")
            for j in phase_jobs:
                char = j.get("character", "?")
                emotion = j.get("emotion", "?")
                lottie = j.get("lottie_output", "")
                error = j.get("error", "")

                if lottie:
                    print(f"  {char}_{emotion}: {Path(lottie).name}")
                elif error:
                    print(f"  {char}_{emotion}: ERROR - {error[:50]}")
                else:
                    print(f"  {char}_{emotion}")
    else:
        print("\nNo pipeline jobs recorded yet.")

    # Also show process.py status
    print()
    show_detailed_status()


def discover_ui() -> None:
    """Output UI discovery script."""
    print(get_discovery_script())


# =============================================================================
# CLI
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Ludo.ai Animation Pipeline",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Start pipeline for single animation
    python pipeline.py bennie waving

    # Continue after download
    python pipeline.py --continue bennie waving --zip downloads/animation.zip

    # Generate all animations for character
    python pipeline.py bennie --all

    # Show status
    python pipeline.py --status

    # UI element discovery
    python pipeline.py --discover
        """
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
        "--all",
        action="store_true",
        help="Generate all emotions for character"
    )
    parser.add_argument(
        "--continue",
        dest="continue_job",
        action="store_true",
        help="Continue job after download"
    )
    parser.add_argument(
        "--zip",
        type=Path,
        help="Path to downloaded ZIP (with --continue)"
    )
    parser.add_argument(
        "--status",
        action="store_true",
        help="Show pipeline status"
    )
    parser.add_argument(
        "--discover",
        action="store_true",
        help="Output UI element discovery script"
    )

    args = parser.parse_args()

    # Status mode
    if args.status:
        show_pipeline_status()
        return 0

    # Discovery mode
    if args.discover:
        discover_ui()
        return 0

    # Validate character
    if not args.character:
        parser.print_help()
        return 1

    # Continue mode
    if args.continue_job:
        if not args.emotion:
            print("Error: --continue requires emotion argument")
            return 1
        if not args.zip:
            print("Error: --continue requires --zip argument")
            return 1

        job = continue_pipeline(args.character, args.emotion, args.zip)
        return 0 if job.phase == PipelinePhase.COMPLETE else 1

    # All emotions mode
    if args.all:
        emotions = list_available_emotions(args.character)
        print(f"\nGenerating keyframes for {len(emotions)} animations...")
        print("Note: Each animation requires manual browser automation step.\n")

        for i, emotion in enumerate(emotions, 1):
            print(f"\n[{i}/{len(emotions)}] Starting {args.character}_{emotion}...")
            job = run_pipeline(args.character, emotion)

            if job.phase == PipelinePhase.FAILED:
                print(f"[SKIP] Failed: {job.error}")
                continue

            if i < len(emotions):
                print("\n" + "-" * 40)
                response = input("Press Enter to continue to next animation, or 'q' to quit: ")
                if response.lower() == 'q':
                    break

        print("\n[DONE] Keyframe generation complete for all animations.")
        print("Execute the MCP scripts above to complete generation.")
        return 0

    # Single emotion mode
    if not args.emotion:
        print(f"\nAvailable emotions for {args.character}:")
        for e in list_available_emotions(args.character):
            print(f"  - {e}")
        return 1

    job = run_pipeline(args.character, args.emotion)
    return 0 if job.phase != PipelinePhase.FAILED else 1


if __name__ == "__main__":
    sys.exit(main())
