# 08-03 Investigation: Gemini Image Generation Issue

## Problem
The keyframe generation script failed with error:
```
"Image generation is not available in your country."
```

## Root Cause
The script was using the wrong model: `gemini-2.0-flash-exp`

This model does NOT support image generation in many regions.

## Solution
Use a model that DOES support image generation:

**Working Models (tested):**
1. `gemini-2.5-flash-image` ✓
2. `gemini-3-pro-image-preview` ✓
3. `imagen-4.0-generate-001` ✓
4. `imagen-4.0-fast-generate-001` ✓

**Not Working:**
- `gemini-2.0-flash-exp` - "Image generation not available in your country"
- `imagen-3.0-generate-001` - 404 Not Found

## Changes Made
Updated `scripts/generate_all_keyframes.py`:
1. Changed model from `gemini-2.0-flash-exp` to `gemini-2.5-flash-image`
2. Added direct .env file reading (bypasses broken dotenv on Python 3.14)
3. Added retry logic with exponential backoff for rate limits
4. Added 3-second delays between API calls to respect rate limits

## Additional Issue: .env File Format
The `.env` file contains malformed content (Python code on lines 66-82) which causes dotenv parsing warnings. This doesn't break functionality but should be cleaned up eventually.

## Next Step
Run the updated script:
```bash
source .venv/bin/activate && python scripts/generate_all_keyframes.py
```
