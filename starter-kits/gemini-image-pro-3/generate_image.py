#!/usr/bin/env python3
"""
Bennie Bear - Image Generation Pipeline with Reinforcement Learning
====================================================================
Generates autism-friendly character art using Gemini and learns from
user feedback to improve future generations.

Usage:
    # Training mode (A/B comparison with feedback loop)
    python generate_image.py "Bennie waving hello" --name bennie-greeting --training

    # Generate only (manual review)
    python generate_image.py "Four excited Lemminge" --name lemminge-group

Environment Variables Required:
    GOOGLE_API_KEY    - Google AI API key for image generation
    ANTHROPIC_API_KEY - Anthropic API key for auto-selection (optional)
"""

import os
import sys
import json
import base64
import argparse
import subprocess
import re
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Dict, Any, Tuple
from dataclasses import dataclass, asdict, field

# =============================================================================
# DEPENDENCIES CHECK
# =============================================================================

def check_dependencies():
    """Check required packages and provide installation instructions if missing."""
    required = {
        'google.genai': 'google-genai',
        'PIL': 'pillow',
        'anthropic': 'anthropic',
        'dotenv': 'python-dotenv',
        'requests': 'requests',
    }

    missing = []
    for module, package in required.items():
        try:
            __import__(module.split('.')[0])
        except ImportError:
            missing.append(package)

    if missing:
        print(f"[ERROR] Missing required packages: {', '.join(missing)}", file=sys.stderr)
        print(f"[INFO] Install with: pip install {' '.join(missing)}", file=sys.stderr)
        print(f"[INFO] Or run: pip install -r requirements.txt", file=sys.stderr)
        sys.exit(1)

check_dependencies()


# =============================================================================
# RETRY LOGIC
# =============================================================================

import time as _time
from functools import wraps

def retry_with_backoff(
    max_retries: int = 3,
    base_delay: float = 2.0,
    max_delay: float = 60.0,
    retryable_exceptions: tuple = (Exception,),
):
    """Decorator for retry with exponential backoff."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except retryable_exceptions as e:
                    error_str = str(e).lower()
                    # Check if error is retryable
                    is_retryable = any(x in error_str for x in [
                        'rate limit', '429', '500', '502', '503', '504',
                        'timeout', 'connection', 'temporary'
                    ])
                    if not is_retryable or attempt == max_retries:
                        raise
                    last_exception = e
                    delay = min(base_delay * (2 ** attempt), max_delay)
                    log(f"[RETRY] Attempt {attempt + 1} failed: {e}")
                    log(f"[RETRY] Retrying in {delay:.1f}s...")
                    _time.sleep(delay)
            raise last_exception
        return wrapper
    return decorator

from google import genai
from google.genai import types
from PIL import Image
import io as _io
import anthropic
from dotenv import load_dotenv

load_dotenv()


# =============================================================================
# IMAGE VALIDATION
# =============================================================================

def validate_image(image_data: bytes, min_size: int = 1024) -> Tuple[bool, str]:
    """Validate generated image data.

    Args:
        image_data: Raw image bytes
        min_size: Minimum file size in bytes

    Returns:
        Tuple of (is_valid, message)
    """
    if not image_data:
        return False, "Empty image data"

    if len(image_data) < min_size:
        return False, f"Image too small ({len(image_data)} bytes, min {min_size})"

    try:
        # Verify image can be opened
        img = Image.open(_io.BytesIO(image_data))
        img.verify()  # Verify integrity

        # Re-open for dimension check (verify() leaves file unusable)
        img = Image.open(_io.BytesIO(image_data))
        width, height = img.size

        if width < 100 or height < 100:
            return False, f"Image dimensions too small ({width}x{height})"

        if img.mode not in ('RGB', 'RGBA', 'L', 'P'):
            return False, f"Unexpected image mode: {img.mode}"

        return True, f"OK ({width}x{height}, {len(image_data)//1024}KB)"

    except Exception as e:
        return False, f"Invalid image: {e}"

# =============================================================================
# LOGGING
# =============================================================================

def log(*args, **kwargs):
    """Print to stderr to avoid conflicts with MCP JSON-RPC protocol."""
    kwargs['file'] = sys.stderr
    print(*args, **kwargs)

# =============================================================================
# CONFIGURATION - BENNIE BEAR PROJECT
# =============================================================================

def _find_project_root() -> Path:
    """Find project root by looking for marker files."""
    markers = ['CLAUDE.md', 'package.json', '.git', 'BennieGame.xcodeproj']

    # Start from script location
    current = Path(__file__).resolve().parent

    for _ in range(10):  # Max 10 levels up
        for marker in markers:
            if (current / marker).exists():
                return current
        parent = current.parent
        if parent == current:  # Reached filesystem root
            break
        current = parent

    # Fallback: use script's parent.parent
    return Path(__file__).resolve().parent.parent


from secret_guard import SecretGuard

@dataclass
class Config:
    """Pipeline configuration."""
    project_name: str = "Bennie Bear"

    # API Keys - using SecretGuard for secure access
    gemini_key: str = field(default_factory=lambda: SecretGuard.get("GEMINI_API_KEY", default="") or SecretGuard.get("GOOGLE_API_KEY", default="", required=False))
    anthropic_key: str = field(default_factory=lambda: SecretGuard.get("ANTHROPIC_API_KEY", default="", required=False))
    replicate_key: str = field(default_factory=lambda: SecretGuard.get("REPLICATE_API_TOKEN", default="", required=False))

    # Paths - use dynamic project root detection
    project_root: Path = field(default_factory=_find_project_root)
    generated_dir: Path = None
    final_dir: Path = None
    log_file: Path = None

    # RL Skill paths
    rl_skill_dir: Path = None
    learnings_file: Path = None
    training_log_file: Path = None
    style_profiles_dir: Path = None

    # Generation settings
    default_count: int = 4
    default_aspect: str = "16:9"

    # Models - configurable via environment variables
    gemini_model: str = field(default_factory=lambda: os.environ.get(
        "GEMINI_MODEL", "gemini-3-pro-image-preview"
    ))
    gemini_fallback_models: List[str] = field(default_factory=lambda: [
        "gemini-3-pro-image-preview",
        "gemini-2.5-flash-image",
        "imagen-4.0-generate-001",
    ])
    claude_model: str = field(default_factory=lambda: os.environ.get(
        "CLAUDE_MODEL", "claude-sonnet-4-20250514"
    ))
    replicate_model: str = field(default_factory=lambda: os.environ.get(
        "REPLICATE_MODEL", "black-forest-labs/flux-schnell"
    ))

    # Video generation models (Veo)
    veo_model: str = field(default_factory=lambda: os.environ.get(
        "VEO_MODEL", "veo-3.1-generate-preview"
    ))
    veo_fallback_models: List[str] = field(default_factory=lambda: [
        "veo-3.1-generate-preview",
        "veo-3.1-fast-generate-preview",
        "veo-3.0-generate-001",
    ])

    # Video generation settings
    default_video_duration: int = 8  # seconds (4, 6, or 8)
    default_video_resolution: str = "720p"  # 720p or 1080p
    default_video_aspect: str = "16:9"  # 16:9 or 9:16

    # Asset categories for Bennie Bear
    default_categories: List[str] = field(default_factory=lambda: [
        "characters",      # Bennie, Lemminge
        "expressions",     # Character expression sheets
        "environments",    # Treehouse, forest, backgrounds
        "items",           # Coins, berries, blocks
        "ui",              # Buttons, frames (if needed)
        "training",        # A/B comparison sessions
        "videos"           # Generated video clips
    ])

    # Video paths
    generated_videos_dir: Path = None
    video_inputs_dir: Path = None  # Reference images for video generation

    def __post_init__(self):
        # Normalize paths for cross-platform compatibility
        self.project_root = Path(self.project_root).resolve()

        self.generated_dir = self.project_root / "public" / "images" / "generated"
        self.generated_videos_dir = self.project_root / "public" / "videos" / "generated"
        self.video_inputs_dir = self.project_root / "public" / "videos" / "inputs"
        self.final_dir = self.project_root / "public" / "images"
        self.log_file = self.generated_dir / "generation_log.json"

        # Also check for learnings in designer system folder
        designer_learnings = self.project_root / "designer system" / "LEARNINGS.md"
        if designer_learnings.exists():
            self.learnings_file = designer_learnings
            self.rl_skill_dir = self.project_root / "designer system"
        else:
            self.rl_skill_dir = self.project_root / ".claude" / "skills" / "image-generation-rl"
            self.learnings_file = self.rl_skill_dir / "LEARNINGS.md"

        self.training_log_file = self.rl_skill_dir / "training-log.json"
        self.style_profiles_dir = self.rl_skill_dir / "style-profiles"

        # Ensure critical directories exist
        self.generated_dir.mkdir(parents=True, exist_ok=True)
        self.generated_videos_dir.mkdir(parents=True, exist_ok=True)
        self.video_inputs_dir.mkdir(parents=True, exist_ok=True)


CONFIG = Config()

# =============================================================================
# BENNIE BEAR PROJECT STYLE
# =============================================================================

PROJECT_STYLE = """
Clean digital illustration style - mobile game / children's app aesthetic.
Polished, commercial quality like Duolingo, Khan Academy Kids.
Rounded, friendly character shapes - nothing sharp or angular.
Gentle, calming visuals suitable for children on the autism spectrum.
Swiss design sensibility: clean, purposeful, high-quality.

CRITICAL STYLE REQUIREMENTS (from Gemini Preview 3.0 references):
- Clean digital illustration - NOT watercolor, NOT textured
- Soft black outlines defining all shapes
- Smooth, clean fur - NOT fluffy or textured
- Simple, uncluttered compositions with clear focal points
- Large, expressive eyes (friendly, never intense)
- Warm golden lighting
- Muted but warm color palette (saturation <80%)
- Cozy, safe, inviting atmosphere
- NO textures, NO watercolor effects
- NO gradients or complex shading
- NO accessories on characters (no scarf, no hat)

References: Modern Duolingo illustrations, Khan Academy Kids,
Headspace animations - all clean digital, not watercolor.
"""

PROJECT_COLORS = """
Primary Palette:
- Woodland Sage: #738F66 (nature elements, leaves, grass)
- Warm Bark: #8C7259 (Bennie's fur, wood elements)
- Soft Sky: #B3D1E6 (accents, highlights, calm areas)
- Cream: #FAF5EB (backgrounds, Bennie's belly, light areas)

Accent Colors:
- Gentle Berry: #D9A6B0 (soft pink accents)
- Warm Sunflower: #EBD98C (golden highlights, warmth)
- Forest Moss: #7A9973 (nature, leaves)

Semantic Colors:
- Success Green: #99BF8C (celebrations, positive feedback)
- Coin Gold: #D9C27A (rewards, treasure)

Lemminge Colors:
- Lemminge Fur: #A89F96 (gray-brown, soft)
- Lemminge Blush: #D9A6B0 (cheek blush)

FORBIDDEN Colors:
- Pure white (#FFFFFF) - use Cream instead
- Pure black (#000000) - use dark brown #4A4036
- Bright red - too stimulating
- Neon colors - overstimulating
- High saturation (>80%) - use muted tones
"""

PROJECT_AVOID = """
NEVER include (autism-friendly requirements):
- Harsh lighting or strong shadows
- Sharp angles or aggressive shapes
- Scary or threatening expressions
- Cluttered, busy backgrounds
- Flashing or high-contrast patterns
- Realistic style (keep it illustrated)
- Complex textures that could be overwhelming
- Multiple competing focal points

NEVER include (brand consistency):
- Puzzle piece symbols (autism speaks association)
- Religious symbols
- Real-world brand logos
- Text or words in images
- Modern technology
- Urban environments

NEVER include (child safety):
- Anything scary or threatening
- Weapons or violence
- Adult themes
- Sad or crying characters (Bennie is always patient)
- Frustrated or angry expressions on Bennie
"""

# =============================================================================
# CHARACTER SPECIFICATIONS
# =============================================================================

BENNIE_SPEC = """
BENNIE THE BEAR - Main Character (Gemini 3.0 Preview Reference)

CRITICAL: Match the Gemini reference EXACTLY.

Physical Description:
- Species: Large ADULT brown bear (NOT cute teddy, NOT chibi)
- Physique: Heavyset, sturdy, PEAR-SHAPED body
- Body: Narrow shoulders, wide hips, prominent round belly
- Fur color: Warm medium-to-dark CHOCOLATE brown
- Fur texture: Thick and smooth (not scraggly, not flat vector)
- Limbs: THICK, POWERFUL limbs with LARGE paws
- Claws: Visible short grey/black claws
- NO belly patch - uniform brown body with shading only
- NO accessories: No scarf, no hat, no clothing

Face (CRITICAL):
- Eyes: SMALL, round, dark eyes with white highlights
- Eye direction: Looking slightly to the side
- Nose: LARGE, dark espresso brown, TRIANGULAR shape
- Snout: Lighter tan/beige color (ONLY the snout is lighter)
- Expression: Gentle, friendly, subtle pleasant smile, mouth closed
- Ears: Round, perched HIGH on head

Pose & Orientation:
- Stance: Standing upright on hind legs (bipedal)
- Posture: Naturalistic animal posture, not human
- Angle: Three-quarter view, facing slightly right
- Arms: Hanging naturally at sides, curved around belly (NOT waving)
- Feet: Planted firmly on ground

Art Style:
- Style: High-quality 2D digital vector art / cartoon illustration
- Quality: Polished clip art or video game asset look
- Line Work: THICK dark brown/black contour outlines
- Shading: Cel-shaded / smooth soft-shading
- Shadow Areas: Under chin (neck ruff), under belly, inner legs

NEVER:
- Chibi/kawaii/cute teddy proportions
- Large eyes
- Cream belly patch
- Light fur color
- Short stubby limbs
- Arms raised or waving
- Scarf or accessories
"""

LEMMINGE_SPEC = """
THE LEMMINGE - Supporting Characters (Group of 4-6)

Physical Description:
- Species: Stylized lemming-like creatures
- Body: Extremely round, almost spherical
- Fur color: Gray-brown (#A89F96)
- Size: About 1/4 of Bennie's size
- Legs: Tiny, often hidden under body
- Arms: Small, stubby

Face (CRITICAL):
- Eyes: HUGE, take up 50%+ of face
- Eye style: Round, excited, always looking at something
- Blush: Permanent pink circles on cheeks (#D9A6B0)
- Mouth: Small, usually open in wonder or mischief
- No visible nose (too small)

Group Behavior:
- Always appear in groups (4-6)
- Slightly staggered positions (not perfectly aligned)
- Each one slightly different pose/expression
- Move together but with individual timing
"""

EVALUATION_CRITERIA = """
Evaluate each image on these criteria for Bennie Bear (score 1-10 each):

1. AUTISM-FRIENDLY (weight: 35%)
   - Calm, non-overwhelming visuals
   - Simple, clear composition
   - Muted but warm colors
   - No harsh elements

2. CHARACTER ACCURACY (weight: 25%)
   - Matches Bennie/Lemminge specifications exactly
   - Correct proportions and colors
   - NO scarf or accessories on Bennie
   - Smooth fur (NOT fluffy/textured)
   - Large eyes (~1/3 face), small black nose

3. STYLE CONSISTENCY (weight: 20%)
   - Clean digital illustration style (NOT watercolor)
   - Mobile game aesthetic (Duolingo-like)
   - Soft black outlines on all shapes
   - Warm, cozy atmosphere
   - Cream background (#FAF5EB)

4. TECHNICAL QUALITY (weight: 10%)
   - Clean execution
   - No artifacts
   - Appropriate detail level

5. EMOTIONAL WARMTH (weight: 10%)
   - Feels safe and inviting
   - Would appeal to children
   - Encourages engagement

CRITICAL: Reject any image with:
- Watercolor textures or effects
- Scarf or other accessories on Bennie
- Fluffy or textured fur
- Complex backgrounds
- High saturation colors

Return your evaluation as JSON:
{
  "rankings": [
    {"image": 1, "score": 8.5, "strengths": "...", "weaknesses": "..."},
    ...
  ],
  "selected": 1,
  "reasoning": "Image 1 best because..."
}
"""

# =============================================================================
# REINFORCEMENT LEARNING DATA MODELS
# =============================================================================

@dataclass
class Learnings:
    """Parsed learnings from LEARNINGS.md"""
    strong_positive: List[str] = field(default_factory=list)
    positive: List[str] = field(default_factory=list)
    neutral: List[str] = field(default_factory=list)
    negative: List[str] = field(default_factory=list)
    strong_negative: List[str] = field(default_factory=list)


@dataclass
class FeedbackRound:
    """Single A/B comparison round within a session."""
    round_id: str
    timestamp: str
    prompt_base: str
    prompt_a: str
    prompt_b: str
    image_a_path: str
    image_b_path: str
    grid_path: Optional[str] = None
    winner: Optional[str] = None  # "A", "B", "NEITHER", "BOTH"
    feedback_notes: str = ""
    patterns_tested: List[str] = field(default_factory=list)
    patterns_confirmed: List[str] = field(default_factory=list)
    patterns_rejected: List[str] = field(default_factory=list)


@dataclass
class TrainingSession:
    """Represents a training session with multiple rounds."""
    session_id: str
    name: str
    category: str  # "bennie", "lemminge", "environments", "items"
    character: Optional[str]
    created_at: str
    status: str  # "active", "completed", "abandoned"
    rounds: List[FeedbackRound] = field(default_factory=list)
    notes: str = ""


@dataclass
class PatternVote:
    """Tracks votes for a pattern to enable promotion/demotion."""
    pattern: str
    current_score: int  # -3 to +3
    positive_votes: int = 0
    negative_votes: int = 0
    total_appearances: int = 0
    last_voted: Optional[str] = None
    category: str = "general"


@dataclass
class ImageAnnotation:
    """Metadata and tags for a generated image."""
    image_path: str
    session_id: str
    round_id: str
    variant: str  # "A" or "B"
    tags: List[str] = field(default_factory=list)
    quality_score: Optional[float] = None
    autism_friendly_score: Optional[float] = None
    character_accuracy_score: Optional[float] = None
    notes: str = ""
    is_approved: bool = False
    approved_for: List[str] = field(default_factory=list)  # ["reference", "game", "video"]


# =============================================================================
# SESSION STORAGE
# =============================================================================

def _get_sessions_file() -> Path:
    """Get path to training sessions storage file."""
    return CONFIG.rl_skill_dir / "training-sessions.json"


def _get_votes_file() -> Path:
    """Get path to pattern votes storage file."""
    return CONFIG.rl_skill_dir / "pattern-votes.json"


def _get_annotations_file() -> Path:
    """Get path to image annotations storage file."""
    return CONFIG.rl_skill_dir / "image-annotations.json"


def _load_all_sessions() -> Dict[str, TrainingSession]:
    """Load all sessions from storage."""
    sessions_file = _get_sessions_file()
    if not sessions_file.exists():
        return {}
    try:
        data = json.loads(sessions_file.read_text(encoding='utf-8'))
        return {
            k: TrainingSession(
                session_id=v['session_id'],
                name=v['name'],
                category=v['category'],
                character=v.get('character'),
                created_at=v['created_at'],
                status=v['status'],
                notes=v.get('notes', ''),
                rounds=[FeedbackRound(**r) for r in v.get('rounds', [])]
            )
            for k, v in data.items()
        }
    except Exception as e:
        log(f"[WARN] Could not load sessions: {e}")
        return {}


def _save_session(session: TrainingSession):
    """Save a session to storage."""
    sessions = _load_all_sessions()
    sessions[session.session_id] = session

    sessions_file = _get_sessions_file()
    sessions_file.parent.mkdir(parents=True, exist_ok=True)

    data = {
        k: {
            'session_id': v.session_id,
            'name': v.name,
            'category': v.category,
            'character': v.character,
            'created_at': v.created_at,
            'status': v.status,
            'notes': v.notes,
            'rounds': [asdict(r) for r in v.rounds]
        }
        for k, v in sessions.items()
    }
    sessions_file.write_text(json.dumps(data, indent=2), encoding='utf-8')


def _load_pattern_votes() -> Dict[str, PatternVote]:
    """Load pattern votes from storage."""
    votes_file = _get_votes_file()
    if not votes_file.exists():
        return {}
    try:
        data = json.loads(votes_file.read_text(encoding='utf-8'))
        return {k: PatternVote(**v) for k, v in data.items()}
    except Exception as e:
        log(f"[WARN] Could not load votes: {e}")
        return {}


def _save_pattern_votes(votes: Dict[str, PatternVote]):
    """Save pattern votes to storage."""
    votes_file = _get_votes_file()
    votes_file.parent.mkdir(parents=True, exist_ok=True)
    data = {k: asdict(v) for k, v in votes.items()}
    votes_file.write_text(json.dumps(data, indent=2), encoding='utf-8')


# =============================================================================
# SESSION MANAGEMENT FUNCTIONS
# =============================================================================

def create_session(name: str, category: str, character: Optional[str] = None) -> TrainingSession:
    """Start a new training session."""
    session_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{name}"
    session = TrainingSession(
        session_id=session_id,
        name=name,
        category=category,
        character=character,
        created_at=datetime.now().isoformat(),
        status="active",
        rounds=[],
        notes=""
    )
    _save_session(session)
    log(f"[SESSION] Created: {session_id}")
    return session


def get_session(session_id: str) -> Optional[TrainingSession]:
    """Load an existing session by ID."""
    sessions = _load_all_sessions()
    return sessions.get(session_id)


def list_sessions(status: Optional[str] = None, category: Optional[str] = None) -> List[TrainingSession]:
    """List sessions, optionally filtered by status or category."""
    sessions = _load_all_sessions()
    results = list(sessions.values())
    if status:
        results = [s for s in results if s.status == status]
    if category:
        results = [s for s in results if s.category == category]
    return sorted(results, key=lambda s: s.created_at, reverse=True)


def continue_session(session_id: str) -> TrainingSession:
    """Resume an active session."""
    session = get_session(session_id)
    if not session:
        raise ValueError(f"Session not found: {session_id}")
    if session.status != "active":
        raise ValueError(f"Session is {session.status}, cannot continue")
    return session


def complete_session(session_id: str, notes: str = "") -> TrainingSession:
    """Mark a session as completed."""
    session = get_session(session_id)
    if not session:
        raise ValueError(f"Session not found: {session_id}")
    session.status = "completed"
    session.notes = notes
    _save_session(session)
    log(f"[SESSION] Completed: {session_id}")
    return session


# =============================================================================
# FEEDBACK AND PATTERN EVOLUTION
# =============================================================================

# Evolution thresholds
PROMOTION_THRESHOLD = 5      # Positive votes needed to promote
DEMOTION_THRESHOLD = 3       # Negative votes needed to demote
MIN_APPEARANCES = 3          # Minimum tests before evolution


def record_feedback(
    session_id: str,
    round_id: str,
    winner: str,  # "A", "B", "NEITHER", "BOTH"
    notes: str = "",
    patterns_confirmed: List[str] = None,
    patterns_rejected: List[str] = None
) -> FeedbackRound:
    """Record user feedback for an A/B comparison round."""
    session = get_session(session_id)
    if not session:
        raise ValueError(f"Session not found: {session_id}")

    # Find the round
    round_data = None
    for r in session.rounds:
        if r.round_id == round_id:
            round_data = r
            break

    if not round_data:
        raise ValueError(f"Round not found: {round_id}")

    # Update the round
    round_data.winner = winner
    round_data.feedback_notes = notes
    round_data.patterns_confirmed = patterns_confirmed or []
    round_data.patterns_rejected = patterns_rejected or []

    # Process pattern votes
    _process_pattern_votes(round_data, winner)

    # Save
    _save_session(session)

    log(f"[FEEDBACK] Recorded: {winner} for round {round_id}")
    return round_data


def _process_pattern_votes(round_data: FeedbackRound, winner: str):
    """Update pattern vote counts based on feedback."""
    # Extract patterns unique to each prompt variation
    patterns_a = set(round_data.patterns_tested[:len(round_data.patterns_tested)//2])
    patterns_b = set(round_data.patterns_tested[len(round_data.patterns_tested)//2:])

    # If we have confirmed/rejected patterns, use those
    if round_data.patterns_confirmed or round_data.patterns_rejected:
        votes = _load_pattern_votes()
        for p in round_data.patterns_confirmed:
            _increment_vote(votes, p, positive=True)
        for p in round_data.patterns_rejected:
            _increment_vote(votes, p, positive=False)
        _save_pattern_votes(votes)
        _check_pattern_evolution(votes)
        return

    # Otherwise infer from winner
    unique_a = patterns_a - patterns_b
    unique_b = patterns_b - patterns_a

    votes = _load_pattern_votes()

    if winner == "A":
        for p in unique_a:
            _increment_vote(votes, p, positive=True)
        for p in unique_b:
            _increment_vote(votes, p, positive=False)
    elif winner == "B":
        for p in unique_b:
            _increment_vote(votes, p, positive=True)
        for p in unique_a:
            _increment_vote(votes, p, positive=False)
    elif winner == "BOTH":
        for p in unique_a | unique_b:
            _increment_vote(votes, p, positive=True)
    # NEITHER: no votes recorded

    _save_pattern_votes(votes)
    _check_pattern_evolution(votes)


def _increment_vote(votes: Dict[str, PatternVote], pattern: str, positive: bool):
    """Increment vote count for a pattern."""
    if pattern not in votes:
        votes[pattern] = PatternVote(pattern=pattern, current_score=0)

    vote = votes[pattern]
    vote.total_appearances += 1
    vote.last_voted = datetime.now().isoformat()

    if positive:
        vote.positive_votes += 1
    else:
        vote.negative_votes += 1


def _check_pattern_evolution(votes: Dict[str, PatternVote]):
    """Check if any patterns should be promoted or demoted."""
    changes_made = False

    for pattern, vote_data in votes.items():
        if vote_data.total_appearances < MIN_APPEARANCES:
            continue

        net_score = vote_data.positive_votes - vote_data.negative_votes
        current = vote_data.current_score

        # Promotion logic
        if net_score >= PROMOTION_THRESHOLD:
            new_score = min(current + 2, 3)  # Jump by 2, cap at +3
            if new_score != current:
                log(f"[EVOLVE] Promoting '{pattern}' from {current} to {new_score}")
                vote_data.current_score = new_score
                vote_data.positive_votes = 0  # Reset after promotion
                vote_data.negative_votes = 0
                changes_made = True

        # Demotion logic
        elif net_score <= -DEMOTION_THRESHOLD:
            new_score = max(current - 2, -3)  # Drop by 2, floor at -3
            if new_score != current:
                log(f"[EVOLVE] Demoting '{pattern}' from {current} to {new_score}")
                vote_data.current_score = new_score
                vote_data.positive_votes = 0
                vote_data.negative_votes = 0
                changes_made = True

    if changes_made:
        _save_pattern_votes(votes)


# =============================================================================
# TRAINING REPORTS
# =============================================================================

def generate_training_report(
    session_id: str = None,
    category: str = None,
) -> Dict[str, Any]:
    """Generate a report of training progress and learnings."""
    sessions = list_sessions()

    # Filter
    if session_id:
        sessions = [s for s in sessions if s.session_id == session_id]
    if category:
        sessions = [s for s in sessions if s.category == category]

    # Aggregate stats
    total_rounds = sum(len(s.rounds) for s in sessions)
    total_feedback = sum(1 for s in sessions for r in s.rounds if r.winner)

    winner_counts = {"A": 0, "B": 0, "NEITHER": 0, "BOTH": 0}
    for s in sessions:
        for r in s.rounds:
            if r.winner and r.winner in winner_counts:
                winner_counts[r.winner] += 1

    # Pattern evolution
    votes = _load_pattern_votes()
    trending_positive = [(p, v.positive_votes - v.negative_votes)
                         for p, v in votes.items()
                         if v.positive_votes > v.negative_votes]
    trending_negative = [(p, v.negative_votes - v.positive_votes)
                         for p, v in votes.items()
                         if v.negative_votes > v.positive_votes]

    # Current learnings
    learnings = load_learnings()

    report = {
        "summary": {
            "total_sessions": len(sessions),
            "completed_sessions": sum(1 for s in sessions if s.status == "completed"),
            "total_rounds": total_rounds,
            "feedback_recorded": total_feedback,
            "feedback_rate": f"{(total_feedback/total_rounds*100):.1f}%" if total_rounds else "N/A"
        },
        "winner_distribution": winner_counts,
        "pattern_trends": {
            "trending_positive": sorted(trending_positive, key=lambda x: x[1], reverse=True)[:5],
            "trending_negative": sorted(trending_negative, key=lambda x: x[1], reverse=True)[:5],
        },
        "current_learnings": {
            "strong_positive": len(learnings.strong_positive),
            "positive": len(learnings.positive),
            "neutral": len(learnings.neutral),
            "negative": len(learnings.negative),
            "strong_negative": len(learnings.strong_negative),
        },
        "sessions": [
            {
                "id": s.session_id,
                "name": s.name,
                "category": s.category,
                "status": s.status,
                "rounds": len(s.rounds),
                "created": s.created_at
            }
            for s in sessions[:10]  # Last 10
        ]
    }

    return report


def print_training_report(report: Dict[str, Any]):
    """Pretty-print a training report."""
    print("\n" + "=" * 60)
    print("BENNIE BEAR - TRAINING REPORT")
    print("=" * 60)

    s = report["summary"]
    print(f"\nSessions: {s['total_sessions']} ({s['completed_sessions']} completed)")
    print(f"Total A/B Rounds: {s['total_rounds']}")
    print(f"Feedback Recorded: {s['feedback_recorded']} ({s['feedback_rate']})")

    print("\nWinner Distribution:")
    for winner, count in report["winner_distribution"].items():
        print(f"  {winner}: {count}")

    print("\nPattern Trends:")
    print("  Trending Positive:")
    for pattern, net in report["pattern_trends"]["trending_positive"][:3]:
        print(f"    + {pattern} (net +{net})")

    print("  Trending Negative:")
    for pattern, net in report["pattern_trends"]["trending_negative"][:3]:
        print(f"    - {pattern} (net -{net})")

    print("\nCurrent Learnings:")
    l = report["current_learnings"]
    print(f"  +3: {l['strong_positive']} | +1: {l['positive']} | 0: {l['neutral']}")
    print(f"  -1: {l['negative']} | -3: {l['strong_negative']}")

    print("\n" + "=" * 60)


# =============================================================================
# REINFORCEMENT LEARNING FUNCTIONS
# =============================================================================


def load_learnings() -> Learnings:
    """Load and parse learnings from LEARNINGS.md file."""
    learnings = Learnings()

    if not CONFIG.learnings_file.exists():
        log("[INFO] No learnings file found, using defaults")
        return learnings

    try:
        content = CONFIG.learnings_file.read_text(encoding='utf-8')

        sections = {
            'strong_positive': r'### STRONG POSITIVE \(\+3\).*?(?=###|\Z)',
            'positive': r'### POSITIVE \(\+1\).*?(?=###|\Z)',
            'neutral': r'### NEUTRAL \(0\).*?(?=###|\Z)',
            'negative': r'### NEGATIVE \(-1\).*?(?=###|\Z)',
            'strong_negative': r'### STRONG NEGATIVE \(-3\).*?(?=###|\Z)',
        }

        for key, pattern in sections.items():
            match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
            if match:
                section_text = match.group(0)
                patterns = re.findall(r'\|\s*([^|]+?)\s*\|', section_text)
                patterns = [p.strip() for p in patterns
                           if p.strip() and not p.strip().startswith('Pattern')
                           and not p.strip().startswith('---')
                           and not p.strip().startswith('Source')
                           and not p.strip().startswith('Date')
                           and not p.strip().startswith('Reason')
                           and not p.strip().startswith('Notes')
                           and len(p.strip()) > 3]
                setattr(learnings, key, patterns)

        log(f"[RL] Loaded learnings: +3:{len(learnings.strong_positive)}, +1:{len(learnings.positive)}, -1:{len(learnings.negative)}, -3:{len(learnings.strong_negative)}")

    except Exception as e:
        log(f"[WARNING] Could not parse learnings: {e}")

    return learnings


def apply_learnings_to_prompt(base_prompt: str, learnings: Learnings) -> Tuple[str, str]:
    """Apply learnings to create A/B prompt variations."""
    enhancements = []
    if learnings.strong_positive:
        enhancements.extend(learnings.strong_positive[:5])
    if learnings.positive:
        enhancements.extend(learnings.positive[:3])

    exclusions = []
    if learnings.strong_negative:
        exclusions.extend([f"NO {p}" for p in learnings.strong_negative])
    if learnings.negative:
        exclusions.extend([f"Avoid {p}" for p in learnings.negative[:3]])

    # CRITICAL ANCHOR - prevents drift to cute/chibi proportions
    anchor = """CRITICAL - MAINTAIN EXACT PROPORTIONS:
- TALL ADULT bear (NOT cute teddy, NOT chibi, NOT short)
- PEAR-SHAPED body, prominent round belly
- THICK POWERFUL limbs with large paws (NOT short stubby limbs)
- SMALL round dark eyes (NOT large eyes)
- Same height and proportions as reference"""

    prompt_a = f"""{base_prompt}

{anchor}

Style enhancements (from learnings):
{chr(10).join(['- ' + e for e in enhancements[:5]])}

{chr(10).join(exclusions)}
"""

    # Option B: ONLY color variation - NEVER shape/edge modifiers
    # "Softer edges" causes proportion drift - REMOVED
    prompt_b = f"""{base_prompt}

{anchor}

Style enhancements (from learnings):
{chr(10).join(['- ' + e for e in enhancements[:5]])}
- Slightly warmer color temperature (proportions unchanged)

{chr(10).join(exclusions)}
"""

    return prompt_a, prompt_b


def enhance_prompt(base_prompt: str, character: str = None) -> str:
    """Add project style guidelines and character specs to prompt.

    Injects reference style requirements from Gemini Preview 3.0 references
    to ensure consistent output matching the approved style.
    """
    # Import reference style module
    try:
        from reference_style import get_reference_prompt_prefix, REFERENCE_STYLE
        reference_prefix = get_reference_prompt_prefix(character)
    except ImportError:
        reference_prefix = ""

    char_spec = ""
    if character:
        if "bennie" in character.lower():
            char_spec = BENNIE_SPEC
        elif "lemming" in character.lower():
            char_spec = LEMMINGE_SPEC

    # Build enhanced prompt with reference style as PRIMARY guidance
    return f"""CRITICAL: Follow this reference style EXACTLY.

{reference_prefix}

{base_prompt}

{char_spec}

Style: {PROJECT_STYLE}

Color palette: {PROJECT_COLORS}

{PROJECT_AVOID}

REMINDER: Clean digital illustration style - NOT watercolor. No scarf on Bennie.
"""


# =============================================================================
# IMAGE GENERATION
# =============================================================================

@retry_with_backoff(max_retries=3, base_delay=2.0)
def _call_gemini_api(
    client,
    model_id: str,
    prompt: str,
    image_size: str = None,
    aspect_ratio: str = None,
    reference_images: List[Path] = None,
) -> Any:
    """Make Gemini API call with retry logic and resolution control.

    Uses generate_content for Gemini image generation models (Nano Banana).
    Imagen models use separate generate_images API.

    Args:
        client: Gemini client
        model_id: Model identifier
        prompt: Generation prompt
        image_size: Resolution tier - "1K", "2K", or "4K" (optional)
        aspect_ratio: Aspect ratio like "16:9" (optional)
        reference_images: List of paths to reference images for character consistency (max 6)
    """
    # Imagen models use dedicated generate_images API (no reference support)
    if 'imagen' in model_id.lower():
        if reference_images:
            log("[WARN] Imagen models don't support reference images, ignoring")
        return client.models.generate_images(
            model=model_id,
            prompt=prompt,
            config=types.GenerateImagesConfig(
                number_of_images=1,
            )
        )
    else:
        # Gemini image models (gemini-3-pro-image-preview, gemini-2.5-flash-image)
        # use generate_content with response_modalities

        # Build content list: reference images FIRST, then prompt
        # This is critical for character consistency
        contents = []

        if reference_images:
            loaded_refs = []
            for ref_path in reference_images[:6]:  # Max 6 object references
                ref_path = Path(ref_path)
                if ref_path.exists():
                    try:
                        ref_img = Image.open(ref_path)
                        loaded_refs.append(ref_img)
                        log(f"[REF] Loaded: {ref_path.name}")
                    except Exception as e:
                        log(f"[WARN] Could not load reference {ref_path}: {e}")

            if loaded_refs:
                # Add reference images to contents
                contents.extend(loaded_refs)

                # Enhance prompt with reference labeling
                ref_labels = "\n".join([
                    f"- Image {i+1}: Reference for character consistency (MATCH EXACTLY)"
                    for i in range(len(loaded_refs))
                ])
                prompt = f"""REFERENCE IMAGES PROVIDED:
{ref_labels}

GENERATION INSTRUCTIONS:
{prompt}

CRITICAL: Match the character design from the reference image(s) EXACTLY.
Preserve all visual details: proportions, colors, line thickness, style, paw pads."""

        # Add prompt as final element
        contents.append(prompt)

        # If no images, just use string prompt directly
        if len(contents) == 1:
            contents = prompt

        # Build config with optional image settings
        config_params = {
            "response_modalities": ["IMAGE", "TEXT"],
        }

        # Add image config for resolution control if specified
        if image_size or aspect_ratio:
            image_config_params = {}
            if image_size:
                image_config_params["image_size"] = image_size
            if aspect_ratio:
                image_config_params["aspect_ratio"] = aspect_ratio
            config_params["image_config"] = types.ImageConfig(**image_config_params)

        return client.models.generate_content(
            model=model_id,
            contents=contents,
            config=types.GenerateContentConfig(**config_params),
        )


def generate_images_gemini(
    prompt: str,
    output_dir: Path,
    base_name: str,
    count: int = 4,
    aspect_ratio: str = "16:9",
    reference_images: List[Path] = None,
) -> List[Path]:
    """Generate images using Gemini with retry logic and validation.

    Args:
        prompt: Generation prompt
        output_dir: Directory to save images
        base_name: Base filename for outputs
        count: Number of variations to generate
        aspect_ratio: Output aspect ratio
        reference_images: Optional list of reference image paths for character consistency
    """

    if not CONFIG.gemini_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set")

    client = genai.Client(api_key=CONFIG.gemini_key)
    model_id = CONFIG.gemini_model

    output_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    saved_paths = []

    log(f"\n[GEN] Generating {count} images...")
    log(f"[MODEL] {model_id}")
    if reference_images:
        log(f"[REF] Using {len(reference_images)} reference image(s)")
    log(f"[PROMPT] {prompt[:150]}...")

    for i in range(count):
        log(f"   Generating variation {i+1}/{count}...", end=" ", flush=True)

        try:
            variation_prompt = f"""{prompt}

Variation {i+1}: Create a unique interpretation while maintaining the core concept and style."""

            # Use retry-enabled API call with reference images
            response = _call_gemini_api(
                client, model_id, variation_prompt,
                reference_images=reference_images
            )

            image_saved = False
            if response.candidates:
                for part in response.candidates[0].content.parts:
                    if hasattr(part, 'inline_data') and part.inline_data:
                        if 'image' in part.inline_data.mime_type:
                            image_data = part.inline_data.data
                            if isinstance(image_data, str):
                                image_data = base64.b64decode(image_data)

                            # Validate image before saving
                            is_valid, validation_msg = validate_image(image_data)
                            if not is_valid:
                                log(f"[WARN] Invalid image: {validation_msg}")
                                continue

                            filename = f"{base_name}_{timestamp}_v{i+1}.png"
                            filepath = output_dir / filename

                            with open(filepath, 'wb') as f:
                                f.write(image_data)

                            saved_paths.append(filepath)
                            log(f"[OK] {filename} - {validation_msg}")
                            image_saved = True
                            break

            if not image_saved:
                for part in response.candidates[0].content.parts:
                    if hasattr(part, 'image') and part.image:
                        img = part.image
                        filename = f"{base_name}_{timestamp}_v{i+1}.png"
                        filepath = output_dir / filename

                        if hasattr(img, 'save'):
                            img.save(str(filepath))
                        elif hasattr(img, 'image_bytes'):
                            # Validate before saving
                            is_valid, validation_msg = validate_image(img.image_bytes)
                            if not is_valid:
                                log(f"[WARN] Invalid image: {validation_msg}")
                                continue
                            with open(filepath, 'wb') as f:
                                f.write(img.image_bytes)

                        saved_paths.append(filepath)
                        log(f"[OK] {filename}")
                        image_saved = True
                        break

            if not image_saved:
                log("[WARNING] No valid image in response")

        except Exception as e:
            log(f"[ERROR] Failed: {e}")
            import traceback
            traceback.print_exc()

    if not saved_paths:
        raise RuntimeError("No images were generated successfully")

    return saved_paths


def generate_images_replicate(
    prompt: str,
    output_dir: Path,
    base_name: str,
    count: int = 4,
    aspect_ratio: str = "16:9",
) -> List[Path]:
    """Generate images using Replicate API (Flux model)."""
    import requests
    import time

    if not CONFIG.replicate_key:
        raise ValueError("REPLICATE_API_TOKEN environment variable not set")

    output_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    saved_paths = []

    log(f"\n[GEN] Generating {count} images with Replicate (Flux)...")

    headers = {
        "Authorization": f"Bearer {CONFIG.replicate_key}",
        "Content-Type": "application/json",
        "Prefer": "wait=60",
    }

    for i in range(count):
        log(f"   Generating variation {i+1}/{count}...", end=" ", flush=True)

        try:
            variation_prompt = f"{prompt}\n\nVariation {i+1}: Create a unique interpretation."

            response = requests.post(
                f"https://api.replicate.com/v1/models/{CONFIG.replicate_model}/predictions",
                headers=headers,
                json={
                    "input": {
                        "prompt": variation_prompt,
                        "aspect_ratio": aspect_ratio,
                        "output_format": "png",
                        "output_quality": 90,
                    }
                },
                timeout=120,
            )

            if response.status_code not in [200, 201]:
                log(f"[ERROR] API error: {response.status_code}")
                continue

            result = response.json()

            if result.get("status") in ["starting", "processing"]:
                prediction_url = result.get("urls", {}).get("get")
                if prediction_url:
                    for _ in range(30):
                        time.sleep(2)
                        poll_response = requests.get(prediction_url, headers=headers)
                        if poll_response.status_code == 200:
                            result = poll_response.json()
                            if result.get("status") == "succeeded":
                                break
                            elif result.get("status") == "failed":
                                break

            output = result.get("output")
            if output:
                image_urls = output if isinstance(output, list) else [output]
                for image_url in image_urls:
                    img_response = requests.get(image_url, timeout=30)
                    if img_response.status_code == 200:
                        filename = f"{base_name}_{timestamp}_v{i+1}.png"
                        filepath = output_dir / filename
                        with open(filepath, 'wb') as f:
                            f.write(img_response.content)
                        saved_paths.append(filepath)
                        log(f"[OK] {filename}")
                        break

        except Exception as e:
            log(f"[ERROR] Failed: {e}")

    if not saved_paths:
        raise RuntimeError("No images were generated successfully")

    return saved_paths


# =============================================================================
# VIDEO GENERATION (Veo 3.1)
# =============================================================================

def generate_video_veo(
    prompt: str,
    output_dir: Path,
    base_name: str,
    duration: int = 8,
    resolution: str = "720p",
    aspect_ratio: str = "16:9",
    reference_images: Optional[List[Path]] = None,
    negative_prompt: Optional[str] = None,
) -> Path:
    """Generate video using Google Veo 3.1.

    Args:
        prompt: Description of the video to generate
        output_dir: Directory to save output
        base_name: Base filename for output
        duration: Video duration in seconds (4, 6, or 8)
        resolution: Video resolution (720p or 1080p)
        aspect_ratio: Aspect ratio (16:9 or 9:16)
        reference_images: Optional list of reference image paths (up to 3)
        negative_prompt: Optional description of unwanted content

    Returns:
        Path to saved video file
    """
    import time

    if not CONFIG.gemini_key:
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

    client = genai.Client(api_key=CONFIG.gemini_key)
    model_id = CONFIG.veo_model

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

                # Create reference image with raw bytes and mime type
                ref_image = types.VideoGenerationReferenceImage(
                    image=types.Image(
                        image_bytes=image_bytes,
                        mime_type=mime_type,
                    ),
                    reference_type="asset"  # Use as asset/character reference
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
        filename = f"{base_name}_{timestamp}.mp4"
        filepath = output_dir / filename

        # Download video file
        client.files.download(file=video.video)
        video.video.save(str(filepath))

        log(f"[OK] Video saved: {filename}")
        return filepath

    except Exception as e:
        log(f"[ERROR] Video generation failed: {e}")
        raise


def extend_video_veo(
    video_path: Path,
    prompt: str,
    output_dir: Path,
    base_name: str,
    resolution: str = "720p",
) -> Path:
    """Extend an existing video by 7 seconds using Veo 3.1.

    Args:
        video_path: Path to existing video to extend
        prompt: Description of the continuation
        output_dir: Directory to save output
        base_name: Base filename for output
        resolution: Video resolution (720p or 1080p)

    Returns:
        Path to extended video file
    """
    import time

    if not CONFIG.gemini_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set")

    if not video_path.exists():
        raise FileNotFoundError(f"Video file not found: {video_path}")

    client = genai.Client(api_key=CONFIG.gemini_key)
    model_id = CONFIG.veo_model

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
            config=types.GenerateVideosConfig(resolution=resolution),
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
                log(f"   Still processing... ({poll_count * 10}s elapsed)")

            time.sleep(10)
            operation = client.operations.get(operation)

        if operation.error:
            raise RuntimeError(f"Video extension failed: {operation.error}")

        # Download extended video
        video = operation.response.generated_videos[0]
        filename = f"{base_name}_extended_{timestamp}.mp4"
        filepath = output_dir / filename

        client.files.download(file=video.video)
        video.video.save(str(filepath))

        log(f"[OK] Extended video saved: {filename}")
        return filepath

    except Exception as e:
        log(f"[ERROR] Video extension failed: {e}")
        raise


def generate_video_from_frames(
    first_frame: Path,
    last_frame: Path,
    prompt: str,
    output_dir: Path,
    base_name: str,
    duration: int = 8,
    aspect_ratio: str = "16:9",
) -> Path:
    """Generate video by interpolating between first and last frames.

    Args:
        first_frame: Path to first frame image
        last_frame: Path to last frame image
        prompt: Description of the transition
        output_dir: Directory to save output
        base_name: Base filename for output
        duration: Video duration in seconds (4, 6, or 8)
        aspect_ratio: Aspect ratio (16:9 or 9:16)

    Returns:
        Path to generated video file
    """
    import time

    if not CONFIG.gemini_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set")

    if not first_frame.exists():
        raise FileNotFoundError(f"First frame not found: {first_frame}")
    if not last_frame.exists():
        raise FileNotFoundError(f"Last frame not found: {last_frame}")

    client = genai.Client(api_key=CONFIG.gemini_key)
    model_id = CONFIG.veo_model

    output_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    log(f"\n[VIDEO] Generating frame interpolation video...")
    log(f"[FIRST] {first_frame.name}")
    log(f"[LAST] {last_frame.name}")
    log(f"[PROMPT] {prompt[:150]}...")

    try:
        # Upload first frame
        first_file = client.files.upload(file=str(first_frame))

        # Upload last frame
        last_file = client.files.upload(file=str(last_frame))

        # Start generation with frame interpolation
        operation = client.models.generate_videos(
            model=model_id,
            prompt=prompt,
            image=first_file,
            config=types.GenerateVideosConfig(
                last_frame=last_file,
                aspect_ratio=aspect_ratio,
            ),
        )

        # Poll for completion
        log("[STATUS] Frame interpolation started...")
        poll_count = 0
        max_polls = 120

        while not operation.done:
            poll_count += 1
            if poll_count > max_polls:
                raise TimeoutError("Video generation timed out after 20 minutes")

            if poll_count % 6 == 0:
                log(f"   Still processing... ({poll_count * 10}s elapsed)")

            time.sleep(10)
            operation = client.operations.get(operation)

        if operation.error:
            raise RuntimeError(f"Video generation failed: {operation.error}")

        # Download video
        video = operation.response.generated_videos[0]
        filename = f"{base_name}_interpolated_{timestamp}.mp4"
        filepath = output_dir / filename

        client.files.download(file=video.video)
        video.video.save(str(filepath))

        log(f"[OK] Interpolated video saved: {filename}")
        return filepath

    except Exception as e:
        log(f"[ERROR] Frame interpolation failed: {e}")
        raise


def generate_video(
    prompt: str,
    output_dir: Path,
    base_name: str,
    duration: int = None,
    resolution: str = None,
    aspect_ratio: str = None,
    reference_images: Optional[List[Path]] = None,
    negative_prompt: Optional[str] = None,
    character: Optional[str] = None,
) -> Path:
    """Generate video with Bennie Bear style enforcement.

    Main entry point for video generation with automatic style injection.

    Args:
        prompt: Description of the video to generate
        output_dir: Directory to save output
        base_name: Base filename for output
        duration: Video duration (4, 6, or 8 seconds)
        resolution: Video resolution (720p or 1080p)
        aspect_ratio: Aspect ratio (16:9 or 9:16)
        reference_images: Optional reference image paths
        negative_prompt: Optional description of unwanted content
        character: Apply character spec ("bennie" or "lemminge")

    Returns:
        Path to saved video file
    """
    # Apply defaults
    duration = duration or CONFIG.default_video_duration
    resolution = resolution or CONFIG.default_video_resolution
    aspect_ratio = aspect_ratio or CONFIG.default_video_aspect

    # Enhance prompt with style (same as images)
    enhanced_prompt = enhance_prompt(prompt, character)

    return generate_video_veo(
        prompt=enhanced_prompt,
        output_dir=output_dir,
        base_name=base_name,
        duration=duration,
        resolution=resolution,
        aspect_ratio=aspect_ratio,
        reference_images=reference_images,
        negative_prompt=negative_prompt,
    )


def generate_images(
    prompt: str,
    output_dir: Path,
    base_name: str,
    count: int = 4,
    aspect_ratio: str = "16:9",
    backend: str = "auto",
    reference_images: List[Path] = None,
) -> List[Path]:
    """Generate images using best available backend.

    Args:
        prompt: Generation prompt
        output_dir: Directory to save images
        base_name: Base filename for outputs
        count: Number of variations to generate
        aspect_ratio: Output aspect ratio
        backend: Which backend to use ("auto", "gemini", "replicate")
        reference_images: Optional list of reference image paths for character consistency
    """

    if backend == "replicate" or (backend == "auto" and CONFIG.replicate_key and not CONFIG.gemini_key):
        if reference_images:
            log("[WARN] Replicate backend doesn't support reference images, ignoring")
        return generate_images_replicate(prompt, output_dir, base_name, count, aspect_ratio)

    if backend == "gemini" or backend == "auto":
        try:
            return generate_images_gemini(
                prompt, output_dir, base_name, count, aspect_ratio,
                reference_images=reference_images
            )
        except Exception as e:
            error_str = str(e).lower()
            if "not available in your country" in error_str or "failed_precondition" in error_str:
                log("\n[INFO] Gemini blocked, falling back to Replicate...")
                if CONFIG.replicate_key:
                    return generate_images_replicate(prompt, output_dir, base_name, count, aspect_ratio)
            raise

    raise ValueError(f"Unknown backend: {backend}")


def create_ab_comparison_grid(image_a: Path, image_b: Path, output_dir: Path, base_name: str) -> Path:
    """Create side-by-side A|B comparison grid."""
    try:
        img_a = Image.open(image_a)
        img_b = Image.open(image_b)

        max_w = max(img_a.width, img_b.width)
        max_h = max(img_a.height, img_b.height)

        padding = 20
        label_height = 50
        divider_width = 10

        grid_w = 2 * max_w + 3 * padding + divider_width
        grid_h = max_h + label_height + 2 * padding

        grid = Image.new('RGB', (grid_w, grid_h), '#FAF5EB')  # Cream background

        img_a_resized = img_a.copy()
        img_a_resized.thumbnail((max_w, max_h), Image.Resampling.LANCZOS)

        img_b_resized = img_b.copy()
        img_b_resized.thumbnail((max_w, max_h), Image.Resampling.LANCZOS)

        x_a = padding
        x_b = padding + max_w + divider_width + padding
        y_img = padding + label_height

        paste_x_a = x_a + (max_w - img_a_resized.width) // 2
        paste_y_a = y_img + (max_h - img_a_resized.height) // 2
        grid.paste(img_a_resized, (paste_x_a, paste_y_a))

        paste_x_b = x_b + (max_w - img_b_resized.width) // 2
        paste_y_b = y_img + (max_h - img_b_resized.height) // 2
        grid.paste(img_b_resized, (paste_x_b, paste_y_b))

        try:
            from PIL import ImageDraw, ImageFont
            draw = ImageDraw.Draw(grid)
            try:
                font = ImageFont.truetype("arial.ttf", 36)
            except:
                font = ImageFont.load_default()

            label_y = padding + 5
            # Use Bennie Bear palette colors
            draw.text((x_a + max_w//2 - 60, label_y), "OPTION A", fill='#738F66', font=font)
            draw.text((x_b + max_w//2 - 60, label_y), "OPTION B", fill='#8C7259', font=font)

            divider_x = padding + max_w + padding // 2
            draw.line([(divider_x, padding), (divider_x, grid_h - padding)], fill='#D9C27A', width=3)

        except Exception as e:
            log(f"[INFO] Could not add labels: {e}")

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        grid_path = output_dir / f"{base_name}_AB_GRID_{timestamp}.png"
        grid.save(grid_path)

        return grid_path

    except Exception as e:
        log(f"[ERROR] Could not create comparison grid: {e}")
        return None


# =============================================================================
# MAIN PIPELINE
# =============================================================================

def generate_ab_comparison(
    prompt: str,
    name: str,
    category: str = "characters",
    aspect_ratio: str = "16:9",
    use_learnings: bool = True,
    character: str = None,
    backend: str = "auto",
) -> Dict[str, Any]:
    """Generate A/B comparison with learnings applied."""
    
    output_dir = CONFIG.generated_dir / "training" / name
    output_dir.mkdir(parents=True, exist_ok=True)

    log("=" * 60)
    log(f"[RL] BENNIE BEAR A/B IMAGE GENERATION")
    log("=" * 60)

    learnings = load_learnings() if use_learnings else Learnings()
    prompt_a, prompt_b = apply_learnings_to_prompt(prompt, learnings)

    log(f"\n[A] Generating Option A...")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    images_a = generate_images(
        prompt=enhance_prompt(prompt_a, character),
        output_dir=output_dir,
        base_name=f"{name}_A",
        count=1,
        aspect_ratio=aspect_ratio,
        backend=backend,
    )

    log(f"\n[B] Generating Option B...")

    images_b = generate_images(
        prompt=enhance_prompt(prompt_b, character),
        output_dir=output_dir,
        base_name=f"{name}_B",
        count=1,
        aspect_ratio=aspect_ratio,
        backend=backend,
    )

    if not images_a or not images_b:
        raise RuntimeError("Failed to generate both options")

    image_a = images_a[0]
    image_b = images_b[0]

    log(f"\n[GRID] Creating comparison grid...")
    grid_path = create_ab_comparison_grid(image_a, image_b, output_dir, name)

    result = {
        "option_a": str(image_a),
        "option_b": str(image_b),
        "grid": str(grid_path) if grid_path else None,
        "prompt_a": prompt_a,
        "prompt_b": prompt_b,
        "session_id": f"session_{timestamp}",
    }

    log("\n" + "=" * 60)
    log("[SUCCESS] A/B COMPARISON READY")
    log("=" * 60)
    log(f"Option A: {image_a}")
    log(f"Option B: {image_b}")
    if grid_path:
        log(f"Grid:     {grid_path}")

    return result


def generate_single(
    prompt: str,
    name: str,
    category: str = "characters",
    count: int = 4,
    aspect_ratio: str = "16:9",
    character: str = None,
    output_dir: Path = None,
    raw_mode: bool = False,
    reference_images: List[Path] = None,
) -> Dict[str, Any]:
    """Generate images without A/B comparison.

    Args:
        prompt: Generation prompt
        name: Base name for output files
        category: Asset category (characters, environments, etc.)
        count: Number of variations to generate
        aspect_ratio: Output aspect ratio
        character: Character spec to apply ("bennie" or "lemminge")
        output_dir: Custom output directory (optional)
        raw_mode: If True, use prompt exactly as-is without enhancement
        reference_images: Optional list of reference image paths for character consistency
    """

    if output_dir is None:
        output_dir = CONFIG.generated_dir / category

    log("=" * 60)
    log(f"[GEN] BENNIE BEAR IMAGE GENERATION")
    log("=" * 60)

    # Use raw prompt or enhance it
    if raw_mode:
        final_prompt = prompt
        log("[MODE] RAW - Using prompt exactly as provided")
    else:
        final_prompt = enhance_prompt(prompt, character)

    # Log the actual prompt being sent
    log(f"[MODEL] {CONFIG.gemini_model}")
    if reference_images:
        log(f"[REF] Using {len(reference_images)} reference image(s) for consistency")
        for ref in reference_images:
            log(f"   - {Path(ref).name}")
    log(f"[PROMPT] {final_prompt[:100]}...")

    # Save full prompt to log file
    log_file = output_dir / f"{name}_prompt_log.txt"
    try:
        with open(log_file, 'w', encoding='utf-8') as f:
            f.write(f"Generated: {name}\n")
            f.write(f"Raw Mode: {raw_mode}\n")
            f.write(f"Character: {character}\n")
            if reference_images:
                f.write(f"Reference Images: {', '.join(str(r) for r in reference_images)}\n")
            f.write(f"=" * 60 + "\n")
            f.write(f"FULL PROMPT SENT TO GEMINI:\n")
            f.write(f"=" * 60 + "\n")
            f.write(final_prompt)
        log(f"[LOG] Prompt saved to: {log_file}")
    except Exception as e:
        log(f"[WARN] Could not save prompt log: {e}")

    image_paths = generate_images(
        prompt=final_prompt,
        output_dir=output_dir,
        base_name=name,
        count=count,
        aspect_ratio=aspect_ratio,
        backend="auto",
        reference_images=reference_images,
    )

    result = {
        "generated": [str(p) for p in image_paths],
        "category": category,
    }

    log("\n" + "=" * 60)
    log("[SUCCESS] GENERATION COMPLETE")
    log("=" * 60)
    log(f"Generated: {len(image_paths)} images")

    return result


# =============================================================================
# CLI
# =============================================================================

def cmd_generate(args):
    """Handle generate command."""
    if not args.prompt:
        print("[ERROR] Prompt is required", file=sys.stderr)
        sys.exit(1)

    # Parse reference images if provided
    reference_images = None
    if hasattr(args, 'reference') and args.reference:
        reference_images = [Path(p) for p in args.reference]
        # Validate paths exist
        for ref in reference_images:
            if not ref.exists():
                print(f"[ERROR] Reference image not found: {ref}", file=sys.stderr)
                sys.exit(1)

    try:
        if args.training:
            result = generate_ab_comparison(
                prompt=args.prompt,
                name=args.name,
                category=args.category,
                aspect_ratio=args.aspect,
                use_learnings=not args.no_learnings,
                character=args.character,
                backend=args.backend,
            )
        else:
            result = generate_single(
                prompt=args.prompt,
                name=args.name,
                category=args.category,
                count=args.count,
                aspect_ratio=args.aspect,
                character=args.character,
                raw_mode=getattr(args, 'raw', False),
                reference_images=reference_images,
            )

        if args.output_json:
            print(json.dumps(result, indent=2))

    except Exception as e:
        log(f"\n[ERROR] {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


def cmd_session(args):
    """Handle session subcommands."""
    if args.session_cmd == "start":
        session = create_session(
            name=args.name,
            category=args.category,
            character=args.character
        )
        print(f"[SESSION] Created: {session.session_id}")
        print(f"[INFO] Use --session {session.session_id} with generate command")

    elif args.session_cmd == "list":
        sessions = list_sessions(status=args.status, category=args.category)
        if not sessions:
            print("[INFO] No sessions found")
            return

        print(f"\n{'ID':<45} {'Name':<20} {'Status':<10} {'Rounds':<8} {'Created'}")
        print("-" * 100)
        for s in sessions[:20]:
            print(f"{s.session_id:<45} {s.name:<20} {s.status:<10} {len(s.rounds):<8} {s.created_at[:10]}")

    elif args.session_cmd == "continue":
        try:
            session = continue_session(args.session_id)
            print(f"[SESSION] Resumed: {session.session_id}")
            print(f"[INFO] Rounds completed: {len(session.rounds)}")
        except ValueError as e:
            print(f"[ERROR] {e}", file=sys.stderr)
            sys.exit(1)

    elif args.session_cmd == "complete":
        try:
            session = complete_session(args.session_id, notes=args.notes or "")
            print(f"[SESSION] Completed: {session.session_id}")
            print(f"[INFO] Total rounds: {len(session.rounds)}")
        except ValueError as e:
            print(f"[ERROR] {e}", file=sys.stderr)
            sys.exit(1)

    else:
        print("[ERROR] Unknown session command", file=sys.stderr)
        sys.exit(1)


def cmd_feedback(args):
    """Handle feedback command."""
    try:
        round_data = record_feedback(
            session_id=args.session_id,
            round_id=args.round_id,
            winner=args.winner,
            notes=args.notes or "",
            patterns_confirmed=args.confirm or [],
            patterns_rejected=args.reject or []
        )
        print(f"[FEEDBACK] Recorded: {args.winner} for round {args.round_id}")
        if round_data.patterns_confirmed:
            print(f"[INFO] Confirmed patterns: {', '.join(round_data.patterns_confirmed)}")
        if round_data.patterns_rejected:
            print(f"[INFO] Rejected patterns: {', '.join(round_data.patterns_rejected)}")
    except ValueError as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        sys.exit(1)


def cmd_report(args):
    """Handle report command."""
    report = generate_training_report(
        session_id=args.session,
        category=args.category
    )

    if args.output == "json":
        print(json.dumps(report, indent=2))
    else:
        print_training_report(report)


def main():
    parser = argparse.ArgumentParser(
        description="Bennie Bear Image Generation Pipeline with RL Training",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Commands:
  generate    Generate images (default if no command given)
  session     Manage training sessions
  feedback    Record feedback for A/B comparisons
  report      Generate training reports

Examples:
  # Generate images
  %(prog)s "Bennie waving hello" --name bennie-greeting --training --character bennie

  # Session management
  %(prog)s session start --name bennie-eyes --category characters --character bennie
  %(prog)s session list --status active
  %(prog)s session complete SESSION_ID --notes "Established eye style"

  # Record feedback
  %(prog)s feedback SESSION_ID ROUND_ID A --notes "Better proportions"

  # View reports
  %(prog)s report --category characters
        """
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # === GENERATE COMMAND ===
    gen_parser = subparsers.add_parser("generate", help="Generate images")
    gen_parser.add_argument("prompt", nargs="?", help="Image generation prompt")
    gen_parser.add_argument("--name", "-n", required=True, help="Output name")
    gen_parser.add_argument("--category", "-c", default="characters",
                           help="Category: characters, expressions, environments, items, training")
    gen_parser.add_argument("--count", type=int, default=4, help="Number of variations")
    gen_parser.add_argument("--aspect", "-a", default="16:9", help="Aspect ratio")
    gen_parser.add_argument("--training", "-t", action="store_true",
                           help="Generate A/B comparison for training")
    gen_parser.add_argument("--character", choices=["bennie", "lemminge"],
                           help="Add character specification to prompt")
    gen_parser.add_argument("--no-learnings", action="store_true",
                           help="Skip applying learnings")
    gen_parser.add_argument("--raw", action="store_true",
                           help="Use prompt exactly as-is, skip all enhancement")
    gen_parser.add_argument("--reference", "-r", nargs="+", metavar="IMAGE",
                           help="Reference image(s) for character consistency (max 6)")
    gen_parser.add_argument("--backend", "-b", default="auto",
                           choices=["auto", "gemini", "replicate"])
    gen_parser.add_argument("--output-json", "-j", action="store_true",
                           help="Output result as JSON")

    # === SESSION COMMAND ===
    session_parser = subparsers.add_parser("session", help="Manage training sessions")
    session_sub = session_parser.add_subparsers(dest="session_cmd", help="Session commands")

    # session start
    start_parser = session_sub.add_parser("start", help="Start new training session")
    start_parser.add_argument("--name", "-n", required=True, help="Session name")
    start_parser.add_argument("--category", "-c", default="characters",
                             help="Category: characters, expressions, environments, items")
    start_parser.add_argument("--character", choices=["bennie", "lemminge"],
                             help="Character focus")

    # session list
    list_parser = session_sub.add_parser("list", help="List training sessions")
    list_parser.add_argument("--status", "-s", choices=["active", "completed", "abandoned"],
                            help="Filter by status")
    list_parser.add_argument("--category", "-c", help="Filter by category")

    # session continue
    cont_parser = session_sub.add_parser("continue", help="Continue a session")
    cont_parser.add_argument("session_id", help="Session ID to continue")

    # session complete
    comp_parser = session_sub.add_parser("complete", help="Complete a session")
    comp_parser.add_argument("session_id", help="Session ID to complete")
    comp_parser.add_argument("--notes", help="Session notes/learnings")

    # === FEEDBACK COMMAND ===
    fb_parser = subparsers.add_parser("feedback", help="Record A/B comparison feedback")
    fb_parser.add_argument("session_id", help="Session ID")
    fb_parser.add_argument("round_id", help="Round ID")
    fb_parser.add_argument("winner", choices=["A", "B", "NEITHER", "BOTH"],
                          help="Which option won")
    fb_parser.add_argument("--notes", help="Feedback notes")
    fb_parser.add_argument("--confirm", nargs="*", default=[],
                          help="Patterns to confirm as positive")
    fb_parser.add_argument("--reject", nargs="*", default=[],
                          help="Patterns to reject as negative")

    # === REPORT COMMAND ===
    report_parser = subparsers.add_parser("report", help="Generate training report")
    report_parser.add_argument("--session", help="Filter by session ID")
    report_parser.add_argument("--category", "-c", help="Filter by category")
    report_parser.add_argument("--output", "-o", choices=["text", "json"], default="text",
                              help="Output format")

    # Parse args
    args = parser.parse_args()

    # Handle commands
    if args.command == "session":
        cmd_session(args)
    elif args.command == "feedback":
        cmd_feedback(args)
    elif args.command == "report":
        cmd_report(args)
    elif args.command == "generate":
        cmd_generate(args)
    else:
        # Default: treat as generate command for backwards compatibility
        # Re-parse with generate-style arguments
        gen_parser_compat = argparse.ArgumentParser()
        gen_parser_compat.add_argument("prompt", nargs="?", help="Image generation prompt")
        gen_parser_compat.add_argument("--name", "-n", help="Output name")
        gen_parser_compat.add_argument("--category", "-c", default="characters")
        gen_parser_compat.add_argument("--count", type=int, default=4)
        gen_parser_compat.add_argument("--aspect", "-a", default="16:9")
        gen_parser_compat.add_argument("--training", "-t", action="store_true")
        gen_parser_compat.add_argument("--character", choices=["bennie", "lemminge"])
        gen_parser_compat.add_argument("--no-learnings", action="store_true")
        gen_parser_compat.add_argument("--raw", action="store_true")
        gen_parser_compat.add_argument("--reference", "-r", nargs="+", metavar="IMAGE",
                                       help="Reference image(s) for character consistency")
        gen_parser_compat.add_argument("--backend", "-b", default="auto",
                                       choices=["auto", "gemini", "replicate"])
        gen_parser_compat.add_argument("--output-json", "-j", action="store_true")

        args = gen_parser_compat.parse_args()

        if not args.prompt or not args.name:
            parser.print_help()
            sys.exit(1)

        cmd_generate(args)


if __name__ == "__main__":
    main()
