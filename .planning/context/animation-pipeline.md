# Animation Pipeline Context

> **Use**: Reference this when planning animation-related tasks
> **Last Updated**: 2026-01-13

---

## Pipeline Overview

```
Gemini 3.0 Pro → Ludo.ai → Lottie JSON
(Keyframes)      (Interpolation)   (Output)
2 frames    →    36 frames    →    Embedded PNG
```

---

## Prerequisites

### Chrome Debug Mode

```bash
./scripts/launch-chrome-debug.sh https://app.ludo.ai
```

- Port: 9222
- Profile: `$HOME/chrome-debug-profile`
- Login to Ludo.ai manually (session persists)

### Required Credits

- 5 credits per animation
- ~65 credits for full character set (13 animations)

---

## Scripts

| Script | Purpose | Usage |
|--------|---------|-------|
| `generate_keyframes.py` | Create START/END frames | `python generate_keyframes.py bennie waving` |
| `ludo_batch_process.py` | CDP automation | `python scripts/ludo_batch_process.py` |
| `process.py` | ZIP → Lottie | `python process.py` |

---

## Key CDP Workflow Learnings

### Upload Pattern

1. **Clear existing frame**: Click trash icon
2. **Open dialog**: Click "Choose Image" button
3. **Upload**: Use `DOM.setFileInputFiles` CDP command

### Critical UI Elements

| Element | Selector Strategy |
|---------|------------------|
| First Frame upload | Find "Choose Image" with y < 300 |
| Final Frame upload | Find last "Choose Image" button |
| Animate button | Filter by `width > 200 && x > 200` |
| Export sprite | Click `img.parentElement` in dialog |

### Common Issues

| Issue | Solution |
|-------|----------|
| Dialog doesn't open | Click trash icon first, then "Choose Image" |
| Wrong button clicked | Filter by width > 200px |
| Export fails | Click parent of image element |
| Download missing | Wait 5+ seconds after export |

---

## Motion Prompts

### Bennie (7 animations)

| Emotion | Prompt |
|---------|--------|
| idle | gentle breathing cycle, chest slowly rising and falling, calm peaceful rhythmic motion |
| happy | gentle bounce up and down, cheerful rhythmic movement, slight hop with joy |
| thinking | head tilting side to side slowly, thoughtful pondering motion |
| encouraging | arms opening outward in welcoming gesture, supportive nodding |
| celebrating | arms raising up high in celebration, joyful controlled bouncing |
| waving | hand waving side to side smoothly, friendly greeting gesture |
| pointing | arm extending outward to point, directing attention |

### Lemminge (6 animations)

| Emotion | Prompt |
|---------|--------|
| idle | subtle breathing pulse, gentle body expanding and contracting |
| curious | head tilting curiously, leaning forward with interest |
| excited | bouncing up and down rapidly, energetic movement |
| celebrating | jumping with arms raised high, pure joy expression |
| hiding | shrinking down, paws covering face shyly |
| mischievous | sneaky side-to-side swaying, mischievous hand rubbing |

---

## Output Specs

| Property | Value |
|----------|-------|
| Grid | 6x6 |
| Frames | 36 |
| FPS | 30 |
| Duration | ~1.2s |
| Format | Lottie JSON with embedded PNG |
| Size | ~2.6 MB per animation |

---

## File Locations

```
design/generated/Animations/keyframes/
├── {char}_{emotion}/
│   ├── start.png
│   └── end.png

starter-kits/ludo-animation-pipeline/downloads/
├── {char}_{emotion}.zip

BennieGame/Resources/Lottie/
├── {char}_{emotion}.json
```

---

## Documentation

- **Full CDP Workflow**: `starter-kits/ludo-animation-pipeline/LUDO_CDP_WORKFLOW.md`
- **Lessons Learned**: `starter-kits/ludo-animation-pipeline/LESSONS_LEARNED.md`
- **Pipeline Docs**: `starter-kits/ludo-animation-pipeline/SKILL.md`
- **Animation Skill**: `.claude/skills/animation/SKILL.md`

---

## Example Plan Mode Usage

When asked to add new animations:

```markdown
## Task: Add new animation for [character]

### Prerequisites Check
- [ ] Chrome debug mode running (port 9222)
- [ ] Logged into Ludo.ai
- [ ] Sufficient credits available

### Steps
1. Generate keyframes: `python generate_keyframes.py {char} {emotion}`
2. Run automation: `python scripts/ludo_batch_process.py {char} {emotion}`
3. Process to Lottie: `python starter-kits/ludo-animation-pipeline/process.py`
4. Verify output in `BennieGame/Resources/Lottie/`
```
