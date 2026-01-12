# Troubleshooting Guide - Bennie v3 Starter Kits

## Gemini Image Generation

### API Key Not Found

**Error**: `SecretNotFoundError: GOOGLE_API_KEY`

**Solution**:
1. Create `.env` file in project root
2. Add: `GOOGLE_API_KEY=your_key_here`
3. Or: `export GOOGLE_API_KEY=your_key` (Unix)

### Rate Limit Errors

**Error**: `429 Too Many Requests`

**Solution**:
- Built-in retry handles this automatically
- If persistent, reduce `--count` parameter
- Add delay between generations

### Character Drift / Inconsistency

**Problem**: Generated character doesn't match reference

**Solution**:
1. Use `--reference` flag with approved image
2. Reference images go FIRST in API call
3. Use `--raw` to bypass prompt enhancement
4. Check LEARNINGS.md for drift-causing patterns

### Multiple Characters Appearing

**Problem**: Getting 2+ characters instead of 1

**Solution**:
Add to prompt or negatives:
```
--no multiple characters, two characters, group
```
Add to prompt:
```
ONE character only centered in frame
```

### Limbs Look Like Stamps

**Problem**: Arms/legs appear flat, like surface marks

**Solution**:
Add to negatives:
```
--no stamps, flat paws, 2D limbs, surface marks
```
Add to prompt:
```
ARMS extending outward as separate 3D shapes
```

### Too Glossy / Shiny

**Problem**: Character has plastic/wet appearance

**Solution**:
Add to negatives:
```
--no glossy, shiny, plastic, wet, reflective, chrome, metallic
```

### Text Appearing in Image

**Problem**: Random text/letters in output

**Solution**:
1. Remove triggering words like "FLUFFY" from prompt
2. Add to negatives:
```
--no text, words, letters, writing, watermark, logo
```

---

## Veo Video Generation

### Timeout After 20 Minutes

**Problem**: `TimeoutError: Video generation timed out`

**Solution**:
1. Try shorter duration (4s instead of 8s)
2. Use 720p instead of 1080p
3. Simplify the prompt
4. Try `veo-3.1-fast-generate-preview` model

### 1080p with Short Duration

**Error**: `1080p only supports 8s duration`

**Solution**:
- Use 720p for 4s or 6s videos
- Or use 8s duration with 1080p

### Reference Images Not Working

**Problem**: Video doesn't match reference

**Solution**:
1. Maximum 3 reference images
2. Use high-quality PNG images
3. Use `reference_type="asset"`
4. Show character from clear angles

---

## Ludo.ai Animation Pipeline

### Tab Not Switching

**Problem**: MCP click doesn't switch to Animate tab

**Solution**:
Use JavaScript instead:
```python
mcp__chrome-devtools__evaluate_script(function="() => {
  const tabs = document.querySelectorAll('[role=\"tab\"]');
  for (const tab of tabs) {
    if (tab.textContent.includes('Animate')) {
      tab.click();
      return 'Clicked';
    }
  }
}")
```

### Upload Not Working

**Problem**: File upload dialog issues

**Solution**:
1. Take fresh snapshot (UIDs change on reload)
2. Click "Choose Image" button first
3. Then use `upload_file` with correct UID

### Generation Stuck

**Problem**: Ludo.ai shows "Generating..." indefinitely

**Solution**:
1. Take screenshot to check progress
2. Wait additional 60 seconds
3. If error message visible, reload and retry
4. Check Ludo.ai credits balance

### Wrong Grid Detected

**Problem**: Spritesheet split incorrectly

**Solution**:
Manual override:
```bash
python process.py --grid 7x6
```

### Element UID Not Found

**Problem**: Click fails because UID doesn't exist

**Solution**:
1. UIDs change on page reload
2. Always take fresh snapshot before interacting
3. Don't reuse UIDs from old snapshots

---

## Lottie Animation System

### Invalid JSON

**Error**: `JSONDecodeError`

**Solution**:
1. Validate with `python validate_lottie.py file.json`
2. Check for trailing commas
3. Verify base64 encoding is complete

### Animation Not Playing

**Problem**: Lottie shows static image

**Solution**:
1. Check `ip` and `op` values (in/out points)
2. Verify layer timing (`ip`/`op` per layer)
3. Ensure `fr` (frame rate) is set

### Large File Size

**Problem**: Lottie file is too big (> 1MB)

**Solution**:
1. Reduce frame count
2. Compress PNG frames before embedding
3. Use lower resolution frames

### SwiftUI Integration Issues

**Problem**: LottieView not rendering

**Solution**:
1. Verify file is in Resources/Lottie/
2. Check file is included in target
3. Use exact filename without extension

---

## Security Infrastructure

### Pre-Commit Hook Not Running

**Problem**: Hook doesn't trigger on commit

**Solution**:
1. Verify file exists: `.git/hooks/pre-commit`
2. Make executable: `chmod +x .git/hooks/pre-commit`
3. Check hook has no `.sample` extension

### False Positive on Pattern

**Problem**: Legitimate code flagged as secret

**Solution**:
1. Add to allowlist in `.gitleaks.toml`
2. Update `SKIP_PATTERNS` in check_secrets.py
3. Use comments to mark false positives

### .env Not Loading

**Problem**: `SecretGuard.get()` returns None

**Solution**:
1. Verify `.env` file exists in project root
2. Install python-dotenv: `pip install python-dotenv`
3. Check for typos in variable names

---

## General Issues

### Import Errors

**Problem**: `ModuleNotFoundError`

**Solution**:
```bash
pip install -r requirements.txt
```

### Permission Denied

**Problem**: Can't execute scripts

**Solution**:
```bash
chmod +x script.py        # Unix
python script.py          # Windows
```

### Path Issues on Windows

**Problem**: Paths with backslashes fail

**Solution**:
Use forward slashes or raw strings:
```python
path = "C:/Users/name/file.png"
# or
path = r"C:\Users\name\file.png"
```

### Encoding Errors

**Problem**: `UnicodeDecodeError` reading files

**Solution**:
```python
content = file.read_text(encoding="utf-8", errors="ignore")
```

---

## Getting Help

1. Check individual SKILL.md for kit-specific issues
2. Search error messages in documentation
3. Review API_REFERENCE.md for correct usage
4. Check environment variables are set correctly
