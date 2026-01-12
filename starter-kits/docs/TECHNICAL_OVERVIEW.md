# Technical Overview - Bennie v3 Starter Kits

## Architecture Summary

This knowledge transfer package provides 5 standalone starter kits for AI-powered content generation:

```
┌─────────────────────────────────────────────────────────────────┐
│                    CONTENT GENERATION STACK                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   IMAGES              VIDEOS              ANIMATIONS             │
│   ───────             ──────              ──────────             │
│   Gemini 3.0          Veo 3.1             Ludo.ai               │
│   Pro Image           Generate            Sprite Gen             │
│        │                  │                    │                 │
│        └──────────────────┴────────────────────┘                │
│                          │                                       │
│                    Reference Images                              │
│                    (Character Consistency)                       │
│                          │                                       │
│                    ┌─────┴─────┐                                │
│                    │  Lottie   │                                │
│                    │   JSON    │                                │
│                    └───────────┘                                │
│                          │                                       │
│                    SecretGuard                                  │
│                    (7-Layer Protection)                         │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Key Technologies

### 1. Gemini 3.0 Pro Image Preview

**Purpose**: High-quality AI image generation with character consistency

**Key Innovation**: Reference image technique
- Pass "perfect" reference images to lock character identity
- Maximum 6 reference images per generation
- Works across pose variations, expressions, scenes

**API Structure**:
```python
contents = [
    Image.open("reference.png"),  # Reference FIRST
    "Generate same character dancing"  # Prompt LAST
]
```

### 2. Veo 3.1 Video Generation

**Purpose**: AI video clip generation

**Capabilities**:
- Duration: 4, 6, or 8 seconds
- Resolution: 720p or 1080p
- Reference image support (up to 3)
- Async operation with long polling

### 3. Ludo.ai Animation Pipeline

**Purpose**: Sprite animation from keyframes

**Pipeline**:
```
Gemini Keyframes → Ludo.ai Interpolation → Lottie JSON
   (2 frames)          (42 frames)         (Embedded PNG)
```

**Key Components**:
- Keyframe generation with character references
- Chrome DevTools MCP browser automation
- Alpha-based grid detection for spritesheets
- PNG-embedded Lottie output

### 4. Lottie Animation System

**Purpose**: Create and validate Lottie animations

**Format**: Lottie 5.7.4 JSON with embedded base64 PNG frames

**Types**:
- Micro-interactions (coin spin, button press)
- Character loops (breathing, idle)

### 5. SecretGuard Security

**Purpose**: 7-layer defense against secret leaks

**Layers**:
1. Code-level validation (Python module)
2. Pre-commit git hook
3. Pre-push git hook
4. CI/CD scanning (GitHub Actions)
5. IDE integration
6. Documentation templates
7. Audit scripts

---

## Pattern Learning System

### Scoring System

| Score | Meaning |
|-------|---------|
| +3 | Strong Positive - Always include |
| +1 | Positive - Include when relevant |
| 0 | Neutral - Test and evaluate |
| -1 | Negative - Avoid |
| -3 | Strong Negative - Never include |

### Pattern Evolution

```python
PROMOTION_THRESHOLD = 5   # Votes to promote
DEMOTION_THRESHOLD = 3    # Votes to demote
MIN_APPEARANCES = 3       # Before evolution possible
```

---

## File Formats

### Lottie JSON (PNG-Embedded)

```json
{
  "v": "5.7.4",
  "fr": 30,
  "assets": [{
    "id": "frame_000",
    "e": 1,
    "p": "data:image/png;base64,..."
  }],
  "layers": [{
    "ty": 2,
    "refId": "frame_000"
  }]
}
```

### Keyframe Metadata

```json
{
  "character": "bennie",
  "emotion": "waving",
  "start_frame": "path/to/start.png",
  "end_frame": "path/to/end.png",
  "motion_hint": "waving gesture"
}
```

---

## Integration Points

### Chrome DevTools MCP

Browser automation for Ludo.ai:
- Navigate pages
- Take snapshots (get UIDs)
- Click, fill, upload
- Wait for elements

### Environment Variables

All kits use consistent environment variable naming:

```bash
GOOGLE_API_KEY       # Gemini, Veo
GEMINI_API_KEY       # Alternative
ELEVENLABS_API_KEY   # Voice (future)
ANTHROPIC_API_KEY    # Claude (optional)
```

---

## Security Model

### Never Commit Secrets

```
CRITICAL: Use SecretGuard.get() for ALL API access
```

### Validation

```python
from secret_guard import SecretGuard

# Raises clear error if missing
api_key = SecretGuard.get("GOOGLE_API_KEY")
```

### Detection Patterns

40+ patterns including:
- ElevenLabs, Google, OpenAI, Anthropic keys
- GitHub, GitLab tokens
- Database connection strings
- Private keys, JWT tokens

---

## Best Practices

1. **Always use reference images** for character consistency
2. **Use SecretGuard** for all API key access
3. **Run security audit** before commits
4. **Keep LEARNINGS.md updated** with pattern discoveries
5. **Test with --raw flag** to understand base model output
6. **Use motion hints** for better Ludo.ai results
7. **Validate Lottie output** before deployment

---

## Related Documentation

| Document | Purpose |
|----------|---------|
| Individual SKILL.md | Kit-specific details |
| API_REFERENCE.md | All API endpoints |
| TROUBLESHOOTING.md | Common issues |
