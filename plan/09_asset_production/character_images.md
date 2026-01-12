# Character Image Production

## Purpose

Complete specification for generating all character images using Gemini Image Generation API.

## Bennie der Bär - All Poses

### Core Specifications (ALL POSES)

```
CRITICAL RULES (NEVER VIOLATE):
❌ NO vest, NO clothing, NO accessories whatsoever
❌ NO separate belly patch - body is uniform brown
✅ Main fur: #8C7259 (warm chocolate brown)
✅ Snout ONLY: #C4A574 (lighter tan)
✅ Nose: #3D2B1F (dark espresso triangle)
✅ Adult brown bear (NOT teddy, NOT cub)
✅ Pear-shaped body: narrow shoulders, wide hips
✅ Cel-shaded style, bold black outlines, flat colors
✅ Transparent background
✅ High resolution for @3x export
```

### 1. bennie_idle.png

**Prompt:**
```
Generate Bennie the Bear in the "idle" pose for a children's game.

CHARACTER SPECIFICATIONS:
- Adult brown bear, NOT teddy bear, NOT cub
- Pear-shaped body: narrow shoulders, wide hips, round belly
- Main fur color: #8C7259 (warm chocolate brown)
- Snout ONLY lighter tan: #C4A574
- NO separate belly patch - body is uniform brown
- Dark espresso nose: #3D2B1F
- Small, round, kind eyes with white highlight
- Style: Cel-shaded, bold black outlines, flat colors
- Transparent background

POSE DETAILS:
- Standing upright, calm stance
- Arms relaxed at sides
- Gentle smile
- Slightly tilted head (friendly)
- Front-facing, slight 3/4 angle
- Breathing animation-ready (subtle stance)

CRITICAL RULES:
❌ NO vest, NO clothing, NO accessories whatsoever
✅ Clean vector art style
✅ 16:9 aspect ratio
✅ High resolution (1350x759 minimum)
```

**Expected Output:** 300×450pt (@2x = 600×900px, @3x = 900×1350px)

**QA Checklist:**
- [ ] No clothing/vest/accessories?
- [ ] Fur is #8C7259 brown (uniform across body)?
- [ ] ONLY snout is tan #C4A574?
- [ ] No belly patch?
- [ ] Pear-shaped body?
- [ ] Adult bear proportions?
- [ ] Transparent background?
- [ ] Cel-shaded with bold outlines?

---

### 2. bennie_waving.png

**Prompt:**
```
Generate Bennie the Bear in the "waving" pose for a children's game.

CHARACTER SPECIFICATIONS:
[Same as idle - copy from above]

POSE DETAILS:
- Right arm raised up high
- Paw waving (palm facing forward)
- Big friendly smile
- Eyes squinted slightly from smile
- Left arm at side or on hip
- Leaning slightly toward the wave

CRITICAL RULES:
❌ NO vest, NO clothing, NO accessories whatsoever
✅ Clean vector art style
✅ 16:9 aspect ratio
✅ High resolution
```

---

### 3. bennie_pointing.png

**Prompt:**
```
Generate Bennie the Bear in the "pointing" pose for a children's game.

CHARACTER SPECIFICATIONS:
[Same as idle]

POSE DETAILS:
- Left arm extended, pointing to the right
- Index claw extended, other claws curled
- Head turned slightly in pointing direction
- Encouraging smile
- Right arm relaxed at side
- Body angled toward pointing direction

CRITICAL RULES:
[Same as idle]
```

---

### 4. bennie_thinking.png

**Prompt:**
```
Generate Bennie the Bear in the "thinking" pose for a children's game.

CHARACTER SPECIFICATIONS:
[Same as idle]

POSE DETAILS:
- Right paw on chin in thinking gesture
- Head tilted slightly up and to the side
- Eyes looking up (thoughtful)
- Gentle smile
- Left arm relaxed
- Contemplative expression

CRITICAL RULES:
[Same as idle]
```

---

### 5. bennie_encouraging.png

**Prompt:**
```
Generate Bennie the Bear in the "encouraging" pose for a children's game.

CHARACTER SPECIFICATIONS:
[Same as idle]

POSE DETAILS:
- Both arms slightly forward, palms up (inviting gesture)
- Leaning forward slightly
- Soft, kind eyes
- Warm smile
- Open, welcoming body language
- Supportive expression

CRITICAL RULES:
[Same as idle]
```

---

### 6. bennie_celebrating.png

**Prompt:**
```
Generate Bennie the Bear in the "celebrating" pose for a children's game.

CHARACTER SPECIFICATIONS:
[Same as idle]

POSE DETAILS:
- Both arms raised up high in celebration
- Slight jumping pose (one foot slightly lifted)
- Big smile, eyes squeezed happy
- Body facing forward
- Joyful, energetic expression
- Dynamic pose (but not mid-motion blur)

CRITICAL RULES:
[Same as idle]
```

---

## Die Lemminge - All Expressions

### Core Specifications (ALL EXPRESSIONS)

```
CRITICAL RULES (NEVER VIOLATE):
🔵 Body MUST be #6FA8DC (soft blue)
❌ NEVER green, NEVER brown, NEVER any other color
✅ Belly: #FAF5EB (cream/white) with fuzzy edge
✅ Pink nose: #E8A0A0
✅ Pink paw pads: #E8A0A0
✅ Buck teeth (2 white, always visible)
✅ Go gopher style (round potato blob)
✅ Cel-shaded, thick black outlines
✅ Transparent background
```

### 1. lemminge_idle.png

**Prompt:**
```
Generate a Lemminge character in the "idle" pose for a children's game.

CHARACTER SPECIFICATIONS:
- Round potato blob shape (Go gopher mascot style)
- Body color: #6FA8DC (soft blue) - ABSOLUTELY NOT GREEN OR BROWN
- Belly: #FAF5EB (cream/white) with fuzzy edge transition
- Large round eyes with white sclera, small dark pupils
- Prominent white buck teeth (2 teeth), always visible
- Small pink nose: #E8A0A0
- Stubby pink paw nubs: #E8A0A0
- Two small round ears on top, same blue as body
- Style: Cel-shaded, thick black outlines, flat colors
- Transparent background

POSE DETAILS:
- Standing upright
- Gentle swaying stance
- Neutral expression
- Eyes looking forward
- Arms at sides
- Calm, relaxed

CRITICAL RULES:
🔵 Body MUST be #6FA8DC blue
❌ NEVER green, NEVER brown, NEVER any other color
✅ Clean vector art style
✅ 16:9 aspect ratio
```

**Expected Output:** 80×100pt (@2x = 160×200px, @3x = 240×300px)

---

### 2. lemminge_curious.png

**Prompt:**
```
[Same CHARACTER SPECIFICATIONS as idle]

POSE DETAILS:
- Head tilted to one side (curious)
- Wide eyes looking at something interesting
- Ears perked up
- Body in standing position, slight lean forward
- One paw raised slightly (questioning gesture)
- Inquisitive expression

CRITICAL RULES:
[Same as idle]
```

---

### 3. lemminge_excited.png

**Prompt:**
```
[Same CHARACTER SPECIFICATIONS as idle]

POSE DETAILS:
- Bouncing stance (slight crouch, ready to jump)
- Eyes wide and sparkly
- Big grin showing buck teeth
- Arms slightly raised
- Energetic, happy expression
- Body leaning forward slightly

CRITICAL RULES:
[Same as idle]
```

---

### 4. lemminge_celebrating.png

**Prompt:**
```
[Same CHARACTER SPECIFICATIONS as idle]

POSE DETAILS:
- Jumping pose (both feet off ground)
- Arms raised up high
- Eyes squeezed shut from happiness
- Huge smile showing buck teeth
- Body fully extended
- Joyful, triumphant expression

CRITICAL RULES:
[Same as idle]
```

---

### 5. lemminge_hiding.png

**Prompt:**
```
[Same CHARACTER SPECIFICATIONS as idle]

POSE DETAILS:
- Peeking pose (half hidden)
- One eye visible, one eye hidden
- Shy smile
- Arms pulled close to body
- Leaning to one side (peeking around corner)
- Playful, mischievous expression

CRITICAL RULES:
[Same as idle]
```

---

### 6. lemminge_mischievous.png

**Prompt:**
```
[Same CHARACTER SPECIFICATIONS as idle]

POSE DETAILS:
- Scheming pose
- Squinted eyes (sly look)
- Sly grin showing buck teeth
- Paws together (plotting gesture)
- Slight crouch (sneaky)
- Playful troublemaker expression

CRITICAL RULES:
[Same as idle]
```

---

## Generation Workflow

```bash
# For each character image:

1. Copy prompt from above
2. Open Gemini AI Studio: https://aistudio.google.com/
3. Select "Image Generation" mode
4. Paste prompt
5. Generate image
6. Review using QA checklist
7. Download high-resolution PNG
8. If fails QA: regenerate with emphasis on failed criteria
9. Export @2x and @3x versions
10. Move to Assets.xcassets/Characters/
```

## Batch Generation Script (Optional)

```python
# generate_characters.py
import google.generativeai as genai
import os

genai.configure(api_key=os.environ['GEMINI_API_KEY'])

characters = {
    'bennie': ['idle', 'waving', 'pointing', 'thinking', 'encouraging', 'celebrating'],
    'lemminge': ['idle', 'curious', 'excited', 'celebrating', 'hiding', 'mischievous']
}

prompts = {
    # Load from this file
}

for character in characters:
    for pose in characters[character]:
        prompt = prompts[f'{character}_{pose}']
        
        # Generate
        response = genai.generate_images(
            prompt=prompt,
            num_images=4,  # Generate 4 variations
            aspect_ratio='16:9',
            safety_filter_level='BLOCK_ONLY_HIGH'
        )
        
        # Save best result
        # ... quality check logic ...
```

## Quality Assurance

Before marking any character image as "complete":

```
BENNIE CHECKLIST:
✓ No clothing/vest/accessories
✓ Fur color is #8C7259 brown
✓ ONLY snout is tan #C4A574
✓ No separate belly patch
✓ Pear-shaped body
✓ Adult bear (not cub, not teddy)
✓ Transparent background
✓ Cel-shaded style
✓ High resolution (@3x ready)
✓ Correct pose/expression

LEMMINGE CHECKLIST:
✓ Body is BLUE #6FA8DC
✓ NOT green, NOT brown
✓ Cream belly with fuzzy edge
✓ Buck teeth visible
✓ Pink nose and paws
✓ Go gopher style (round blob)
✓ Transparent background
✓ Cel-shaded style
✓ High resolution (@3x ready)
✓ Correct pose/expression
```

## Total Asset Count

- **Bennie:** 6 images × 3 sizes (@1x, @2x, @3x) = 18 files
- **Lemminge:** 6 images × 3 sizes = 18 files
- **Total:** 36 character image files

## Delivery Format

```
Assets.xcassets/
└── Characters/
    ├── Bennie/
    │   ├── bennie_idle.imageset/
    │   │   ├── bennie_idle@2x.png
    │   │   ├── bennie_idle@3x.png
    │   │   └── Contents.json
    │   ├── bennie_waving.imageset/
    │   └── ... (6 total)
    └── Lemminge/
        ├── lemminge_idle.imageset/
        └── ... (6 total)
```
