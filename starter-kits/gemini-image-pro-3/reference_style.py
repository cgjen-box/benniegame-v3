#!/usr/bin/env python3
"""
Reference Style Module - Bennie Bear & Lemminge
================================================
Defines style standards for all characters with:
- Global settings (art style, quality, technique)
- Character-specific settings (Bennie vs Lemminge)

These constants are injected into image generation prompts to ensure
consistent output matching the approved reference styles.
"""

# =============================================================================
# GLOBAL STYLE SETTINGS (Apply to ALL characters)
# =============================================================================

GLOBAL_STYLE = """
GLOBAL ART STYLE REQUIREMENTS:
==============================

ART TECHNIQUE:
- Style: High-quality 2D digital vector art / cartoon illustration
- Quality: Polished clip art or video game asset look
- Line Work: Thick dark contour outlines around character
- Shading: Cel-shaded / smooth soft-shading
- Background: Cream (#FAF5EB) or transparent

COLOR GUIDELINES:
- Saturation: Keep colors soft, not oversaturated (max 35% saturation)
- Palette: Use soft, friendly tones (woodland greens, pale blues for Lemminge)
- Shadows: Use darker shades of main colors for depth
- LEMMINGE: Must be BLUE (#6FA8DC), NEVER brown or grey

AUTISM-FRIENDLY REQUIREMENTS:
- No harsh contrast or jarring colors
- No busy patterns or visual noise
- Clear, simple silhouettes
- Friendly, approachable expressions
- No scary or threatening elements
"""

GLOBAL_NEGATIVES = """
GLOBAL EXCLUSIONS (Never include for ANY character):
- Photorealistic or 3D rendered style
- Watercolor texture or effects
- Harsh neon or saturated colors
- Scary, angry, or threatening expressions
- Complex busy backgrounds
- Text or logos
- Humans or realistic animals
"""

# =============================================================================
# BENNIE THE BEAR - Character-Specific Style
# =============================================================================

BENNIE_STYLE = """
BENNIE THE BEAR - Character Reference:
======================================

CORE SUBJECT & APPEARANCE:
- Subject: Large, ADULT brown bear (NOT cute teddy, NOT chibi)
- Physique: Heavyset, sturdy, PEAR-SHAPED body
- Belly: Prominent round belly (NO separate belly patch color)
- Limbs: THICK, POWERFUL limbs with LARGE paws
- Fur: Thick and smooth texture (not scraggly, not flat vector)

FACE DETAILS:
- Eyes: SMALL, round, dark eyes with white highlights, looking slightly to side
- Nose: LARGE, dark espresso brown, TRIANGULAR shape
- Snout: Lighter tan/beige (ONLY the snout is lighter, NOT belly)
- Expression: Gentle, friendly, subtle pleasant smile, mouth closed
- Ears: Round, perched HIGH on head

POSE & ORIENTATION:
- Stance: Standing upright on hind legs (bipedal)
- Posture: Naturalistic animal posture, not human
- Angle: Three-quarter view, facing slightly right
- Arms: Hanging naturally at sides, curved around belly (NOT waving unless specified)
- Paws: Large with visible short grey/black claws
- Feet: Planted firmly on ground

COLOR PALETTE:
- Main Fur: Warm, medium-to-dark CHOCOLATE brown
- Snout Accent: Lighter tan/beige (snout area ONLY)
- Shadows: Darker shades of brown for depth
- Nose: Dark espresso brown or near-black
"""

BENNIE_ENFORCEMENT = """
BENNIE MANDATORY REQUIREMENTS:
- Adult bear proportions (tall, sturdy, NOT chibi)
- Pear-shaped body with prominent round belly
- Medium-to-dark chocolate brown fur
- SMALL round dark eyes with white highlights
- LARGE dark espresso brown triangular nose
- Lighter tan/beige snout ONLY (no belly patch)
- Thick powerful limbs with large paws
- Visible short grey/black claws
- Thick dark contour outlines
- Cel-shaded soft shading
"""

BENNIE_NEGATIVES = """
BENNIE EXCLUSIONS (Never include):
- Cute teddy / chibi / kawaii proportions
- Large eyes (1/3 of face)
- Cream belly patch
- Light golden-brown fur
- Short stubby limbs
- Scarf, hat, or any accessories
- Flat vector style without shading
- Small black nose (should be large espresso brown triangular)
"""

# Copy-paste ready Bennie prompt
BENNIE_PROMPT = """A full-body 2D vector illustration of a friendly brown bear standing upright on two legs. The bear has a heavy, pear-shaped body with a round belly, thick chocolate brown fur, and a lighter tan snout. It has small round dark eyes with white highlights, and a large dark espresso brown triangular nose. It is smiling gently with a calm expression. The arms hang loosely by its sides with large paws and visible short claws. The style is clean digital art with thick dark outlines and soft cel-shading, isolated on a cream background."""

# Copy-paste ready Lemminge prompt (FROZEN v2 - 2025-12-29, improved consistency)
# Key improvements: explicit limb count, enhanced fur texture, expanded negatives for anatomy/glossy
LEMMINGE_PROMPT = """flat 2D vector art character design, round blue potato-shaped blob creature, Go gopher mascot style, soft blue body (#6FA8DC), white oval belly patch with soft fuzzy fur edge transition, SOFT MATTE FLUFFY FUR TEXTURE on body, large round friendly white eyes with small black pupils, goofy open smile showing TWO prominent white buck teeth, small pink triangular nose, TWO small stubby nub hands at sides with pink paw pads, TWO small stubby nub feet on ground with pink paw pads, two small round fuzzy ears on top of head, thick bold black outlines, cel shaded, flat matte colors, clean vector lines, neutral grey background, single character front view, full body visible head to feet, simple symmetric biped anatomy --no 3d, realistic, photorealistic, gradient, bear, brown, fur gradient, multiple characters, extra limbs, four arms, three arms, extra legs, mutated, deformed, fused, merged, extra hands, extra feet, malformed, glossy, shiny, plastic, wet, reflective, smooth skin, hairless, slick, glass-like, chrome, metallic, specular, polished, complex background, busy, cluttered"""

# =============================================================================
# THE LEMMINGE - Character-Specific Style
# =============================================================================

LEMMINGE_STYLE = """
THE LEMMINGE - Character Reference:
===================================
Based on Go gopher mascot style - friendly, round, goofy character.

CORE SUBJECT & APPEARANCE:
- Subject: Single round gopher/lemming creature
- Physique: Pear-shaped body (wider at bottom, narrower at top)
- Size: Compact, cuddly proportions
- Fur/Skin: Smooth soft BLUE or PURPLE-BLUE color (#6FA8DC or #7B8FC9)
- Belly: Large WHITE oval belly patch (prominent, takes up most of front)

FACE DETAILS:
- Eyes: LARGE round WHITE eyes with small BLACK pupils
- Eyes position: Placed close together, slightly above center of face
- Expression: Happy, friendly, goofy smile
- Mouth: Open smile showing TWO prominent buck teeth
- Teeth: White buck teeth visible in open mouth
- Nose: Small PINK nose between and below eyes

BODY DETAILS:
- Ears: TWO small rounded ears on TOP of head (like bear ears but smaller)
- Arms: Short stubby arms at sides with PINK paw pads
- Legs: Short stubby legs/feet (barely visible, wide stance)
- Overall: Round cuddly shape, no neck

ART STYLE:
- Flat 2D vector art (Go gopher mascot style)
- Cel-shaded, flat colors (NOT gradients)
- Thick bold BLACK outlines
- Clean vector lines
- Simple, readable silhouette

COLOR PALETTE:
- Body: Soft blue or purple-blue (#6FA8DC, #7B8FC9, or similar)
- Belly: Pure white oval patch
- Nose: Pink (#E8A0A0)
- Paw pads: Pink (#E8A0A0)
- Eyes: White with black pupils
- Mouth interior: Dark brown/maroon
- Teeth: White
"""

LEMMINGE_ENFORCEMENT = """
LEMMINGE MANDATORY REQUIREMENTS:
- Pear-shaped round body (wider bottom)
- LARGE round white eyes with small black pupils
- Happy goofy expression with open smile
- TWO visible white buck teeth
- Small pink nose
- Large white oval belly patch
- Two small rounded ears on top of head
- Short stubby arms with pink paw pads
- Soft BLUE or purple-blue body color (#6FA8DC) - NEVER brown/grey
- Flat 2D vector style with cel-shading
- THICK BOLD BLACK outlines
- SINGLE character only
- Light grey background (NO yellow/warm tint)
"""

LEMMINGE_NEGATIVES = """
LEMMINGE EXCLUSIONS (Never include):
- ANY bear or brown animal (NOT Bennie, NOT a bear)
- Brown coloring or brown fur
- Small realistic eyes
- Long limbs or defined arms/legs
- Serious or angry expressions
- Realistic animal anatomy
- Large triangular nose (use small pink nose)
- Multiple characters (ONLY ONE blue lemming)
- Grizzy (the bear character)
- Extra limbs, four arms, three arms, extra legs
- Mutated, deformed, fused, merged anatomy
- Extra hands, extra feet, malformed proportions
- Glossy, shiny, plastic appearance
- Wet, reflective, slick surface
- Smooth skin, hairless (should have soft fur)
- Glass-like, chrome, metallic, specular, polished finish
"""

# =============================================================================
# API FUNCTIONS
# =============================================================================

def get_reference_prompt_prefix(character: str = None) -> str:
    """Get the reference style prefix for prompt enhancement.

    Args:
        character: Optional character name ("bennie" or "lemminge")

    Returns:
        String to prepend to generation prompts
    """
    # Start with global style
    prefix = "CRITICAL: Follow this reference style EXACTLY.\n\n"
    prefix += GLOBAL_STYLE + "\n"

    # Add character-specific style
    if character:
        char_lower = character.lower()
        if "bennie" in char_lower or "bear" in char_lower:
            prefix += BENNIE_STYLE + "\n"
            prefix += BENNIE_ENFORCEMENT + "\n"
            prefix += BENNIE_NEGATIVES + "\n"
        elif "lemming" in char_lower:
            prefix += LEMMINGE_STYLE + "\n"
            prefix += LEMMINGE_ENFORCEMENT + "\n"
            prefix += LEMMINGE_NEGATIVES + "\n"

    # Add global negatives
    prefix += GLOBAL_NEGATIVES

    return prefix


def get_style_for_character(character: str) -> dict:
    """Get all style components for a specific character.

    Args:
        character: Character name ("bennie" or "lemminge")

    Returns:
        Dictionary with style, enforcement, negatives, and prompt keys
    """
    char_lower = character.lower() if character else ""

    if "bennie" in char_lower or "bear" in char_lower:
        return {
            "style": BENNIE_STYLE,
            "enforcement": BENNIE_ENFORCEMENT,
            "negatives": BENNIE_NEGATIVES,
            "prompt": BENNIE_PROMPT,
            "global_style": GLOBAL_STYLE,
            "global_negatives": GLOBAL_NEGATIVES,
        }
    elif "lemming" in char_lower:
        return {
            "style": LEMMINGE_STYLE,
            "enforcement": LEMMINGE_ENFORCEMENT,
            "negatives": LEMMINGE_NEGATIVES,
            "prompt": LEMMINGE_PROMPT,
            "global_style": GLOBAL_STYLE,
            "global_negatives": GLOBAL_NEGATIVES,
        }
    else:
        # Return global only for unknown characters
        return {
            "style": "",
            "enforcement": "",
            "negatives": "",
            "prompt": None,
            "global_style": GLOBAL_STYLE,
            "global_negatives": GLOBAL_NEGATIVES,
        }


def get_full_reference_context() -> str:
    """Get the complete reference style context (Bennie).

    Returns:
        Complete Bennie reference style documentation
    """
    return BENNIE_STYLE


def get_bennie_prompt() -> str:
    """Get the copy-paste ready Bennie prompt.

    Returns:
        The definitive Bennie generation prompt
    """
    return BENNIE_PROMPT


def get_lemminge_prompt() -> str:
    """Get a base Lemminge generation prompt.

    Returns:
        The definitive Lemminge generation prompt (FROZEN - iter-09 v1 approved 2025-12-29)
    """
    return LEMMINGE_PROMPT
