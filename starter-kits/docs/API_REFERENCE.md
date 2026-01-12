# API Reference - Bennie v3 Starter Kits

## Gemini Image Generation

### Models

| Model ID | Type | Max References |
|----------|------|----------------|
| `gemini-3-pro-image-preview` | Primary | 6 object |
| `gemini-2.5-flash-image` | Fallback | 3 |
| `imagen-4.0-generate-001` | Fallback | 0 |

### API Call

```python
from google import genai
from google.genai import types

client = genai.Client(api_key=API_KEY)

response = client.models.generate_content(
    model="gemini-3-pro-image-preview",
    contents=[
        Image.open("reference.png"),  # Reference first
        "Generate character"           # Prompt last
    ],
    config=types.GenerateContentConfig(
        response_modalities=["IMAGE", "TEXT"],
        image_config=types.ImageConfig(
            image_size="1K",  # or "2K", "4K"
            aspect_ratio="16:9"
        )
    )
)
```

### Parameters

| Parameter | Options | Default |
|-----------|---------|---------|
| `image_size` | 1K, 2K, 4K | None |
| `aspect_ratio` | 16:9, 4:3, 1:1, 9:16 | 16:9 |
| `response_modalities` | IMAGE, TEXT | Both |

---

## Veo Video Generation

### Models

| Model ID | Type |
|----------|------|
| `veo-3.1-generate-preview` | Primary |
| `veo-3.1-fast-generate-preview` | Fast |
| `veo-3.0-generate-001` | Legacy |

### API Call

```python
from google import genai
from google.genai import types

client = genai.Client(api_key=API_KEY)

operation = client.models.generate_videos(
    model="veo-3.1-generate-preview",
    prompt="Bear walking through forest",
    config=types.GenerateVideosConfig(
        aspect_ratio="16:9",
        reference_images=[
            types.VideoGenerationReferenceImage(
                image=types.Image(
                    image_bytes=image_bytes,
                    mime_type="image/png"
                ),
                reference_type="asset"
            )
        ]
    )
)

# Poll for completion
while not operation.done:
    time.sleep(10)
    operation = client.operations.get(operation)

# Get result
video = operation.response.generated_videos[0]
```

### Parameters

| Parameter | Options | Default |
|-----------|---------|---------|
| `duration` | 4, 6, 8 | 8 |
| `resolution` | 720p, 1080p | 720p |
| `aspect_ratio` | 16:9, 9:16 | 16:9 |
| `reference_images` | Up to 3 | None |

### Constraints

- 1080p only supports 8s duration
- Generation takes 1-5 minutes
- Max timeout: 20 minutes

---

## Chrome DevTools MCP

### Page Navigation

```python
# Navigate to URL
mcp__chrome-devtools__navigate_page(
    type="url",
    url="https://example.com"
)

# Reload
mcp__chrome-devtools__navigate_page(type="reload")

# Back/Forward
mcp__chrome-devtools__navigate_page(type="back")
```

### Element Interaction

```python
# Take snapshot to get UIDs
mcp__chrome-devtools__take_snapshot()

# Click element
mcp__chrome-devtools__click(uid="...")

# Fill text input
mcp__chrome-devtools__fill(uid="...", value="text")

# Upload file
mcp__chrome-devtools__upload_file(
    uid="...",
    filePath="C:/path/to/file.png"
)
```

### JavaScript Execution

```python
# Execute JavaScript
mcp__chrome-devtools__evaluate_script(
    function="() => { return document.title; }"
)
```

### Waiting

```python
# Wait for text
mcp__chrome-devtools__wait_for(
    text="Download",
    timeout=180000
)
```

---

## Lottie JSON Format

### Root Object

```json
{
  "v": "5.7.4",        // Version
  "fr": 30,            // Frame rate
  "ip": 0,             // In-point
  "op": 60,            // Out-point
  "w": 100,            // Width
  "h": 100,            // Height
  "nm": "name",        // Name
  "ddd": 0,            // 3D flag
  "assets": [...],     // Assets array
  "layers": [...],     // Layers array
  "markers": [...]     // Markers array
}
```

### Asset (Embedded Image)

```json
{
  "id": "frame_000",
  "w": 96,
  "h": 288,
  "e": 1,              // 1 = embedded
  "u": "",
  "p": "data:image/png;base64,..."
}
```

### Layer Types

| ty | Type |
|----|------|
| 0 | Precomp |
| 1 | Solid |
| 2 | Image |
| 3 | Null |
| 4 | Shape |
| 5 | Text |

### Image Layer

```json
{
  "ty": 2,
  "refId": "frame_000",
  "ip": 0,
  "op": 2,
  "ks": {
    "o": {"a": 0, "k": 100},    // Opacity
    "r": {"a": 0, "k": 0},      // Rotation
    "p": {"a": 0, "k": [50, 50]},  // Position
    "a": {"a": 0, "k": [50, 50]},  // Anchor
    "s": {"a": 0, "k": [100, 100]} // Scale
  }
}
```

### Keyframe Animation

```json
{
  "a": 1,  // Animated
  "k": [
    {"t": 0, "s": [100, 100]},
    {"t": 30, "s": [110, 110]},
    {"t": 60, "s": [100, 100]}
  ]
}
```

---

## SecretGuard API

### Get Secret

```python
from secret_guard import SecretGuard

# Required secret
api_key = SecretGuard.get("API_KEY")

# Optional with default
api_key = SecretGuard.get("API_KEY", default="", required=False)
```

### Validate Required

```python
SecretGuard.validate_required([
    "GOOGLE_API_KEY",
    "ELEVENLABS_API_KEY"
])
```

### Run Audit

```python
success = SecretGuard.audit()  # Returns bool
```

### Scan File

```python
findings = SecretGuard.scan_file_for_secrets(Path("file.py"))
# Returns list of {"file", "line", "pattern", "severity", "content"}
```

---

## Environment Variables

### Required

| Variable | Purpose |
|----------|---------|
| `GOOGLE_API_KEY` | Gemini, Veo |
| `GEMINI_API_KEY` | Alternative to above |

### Optional

| Variable | Purpose |
|----------|---------|
| `ANTHROPIC_API_KEY` | Claude auto-selection |
| `REPLICATE_API_TOKEN` | Fallback generation |
| `ELEVENLABS_API_KEY` | Voice generation |

### Model Overrides

| Variable | Default |
|----------|---------|
| `GEMINI_MODEL` | gemini-3-pro-image-preview |
| `VEO_MODEL` | veo-3.1-generate-preview |
| `CLAUDE_MODEL` | claude-sonnet-4-20250514 |

---

## Error Codes

### Gemini/Veo

| Code | Meaning | Solution |
|------|---------|----------|
| 429 | Rate limited | Retry with backoff |
| 500-504 | Server error | Retry |
| timeout | Generation slow | Increase timeout |

### SecretGuard

| Exception | Meaning |
|-----------|---------|
| `SecretNotFoundError` | Required secret missing |
| `SecretValidationError` | Invalid/placeholder value |
| `HardcodedSecretError` | Secret in code |
