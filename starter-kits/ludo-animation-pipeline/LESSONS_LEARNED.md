# Ludo.ai Animation Pipeline - Lessons Learned

> **Project**: Bennie und die Lemminge
> **Phase**: 08-03 (Lottie Animations)
> **Date**: 2026-01-13
> **Result**: 13 animations successfully generated

---

## Executive Summary

We successfully automated Ludo.ai's sprite animation generator using Chrome DevTools Protocol (CDP), processing all 13 character animations for Bennie and Lemminge. This document captures key learnings for future animation work.

---

## What Worked Well

### 1. CDP over MCP

Using raw CDP commands via websockets proved more reliable than MCP browser tools:
- Direct control over DOM manipulation
- Reliable file upload via `DOM.setFileInputFiles`
- Precise element targeting with JavaScript evaluation

### 2. Batch Processing Script

The `ludo_batch_process.py` script successfully automated:
- Interface reset between animations
- Frame uploads (start + end)
- Motion prompt filling
- Generation monitoring
- Export flow

### 3. Motion Prompts Strategy

Descriptive, specific motion prompts produced better results:
- **Good**: "gentle breathing cycle, chest slowly rising and falling, calm peaceful rhythmic motion"
- **Bad**: "breathing animation"

### 4. Consistent Character Reference

Using Gemini-generated keyframes ensured character consistency across all animation frames.

---

## Problems Encountered & Solutions

### Problem 1: Upload Dialog Not Opening

**Symptom**: Clicking buttons didn't trigger file upload dialog.

**Root Cause**: Wrong element targeted - "Change Pose" and "Open In Editor" buttons open different dialogs.

**Solution**: Click the frame THUMBNAIL IMAGE directly, or:
1. Click trash icon to clear existing frame
2. Then click "Choose Image" button that appears

**Code Pattern**:
```javascript
// Find and click thumbnail in First Frame section
const labels = document.querySelectorAll('*');
for (const l of labels) {
    if ((l.innerText || '').trim() === 'First Frame') {
        const parent = l.parentElement;
        const img = parent.querySelector('img');
        if (img) img.click();
    }
}
```

### Problem 2: Wrong Animate Button Clicked

**Symptom**: Automation navigated away instead of starting generation.

**Root Cause**: Two elements contain "Animate" text:
- Sidebar navigation tab (~100px wide)
- Action button (>200px wide)

**Solution**: Filter by element dimensions:
```javascript
if (b.innerText.trim() === 'Animate' && rect.width > 200 && rect.x > 200) {
    b.click();
}
```

### Problem 3: Export Sprite Selection Failed

**Symptom**: Coordinate-based clicks missed the sprite format option.

**Root Cause**: Dialog position varies; fixed coordinates unreliable.

**Solution**: Find image elements in dialog and click parent:
```javascript
const dialog = document.querySelector('[role="dialog"]');
const imgs = dialog.querySelectorAll('img');
for (const img of imgs) {
    const rect = img.getBoundingClientRect();
    if (rect.width > 60 && rect.width < 200) {
        img.parentElement.click();  // Click parent container
    }
}
```

### Problem 4: Downloads Not Found After Export

**Symptom**: ZIP file not in ~/Downloads after export completed.

**Root Cause**: Export dialog takes time; automation moved on too quickly.

**Solution**: Add 5+ second wait after "Export Animation Pack" click:
```python
await asyncio.sleep(5)  # Wait for download to complete
```

### Problem 5: Help Dialog Interruptions

**Symptom**: Help/tutorial modals appeared unexpectedly during batch processing.

**Root Cause**: Ludo.ai shows help tips on certain actions.

**Solution**: Close any dialogs at start of each animation:
```javascript
document.querySelectorAll('[role="dialog"] button').forEach(b => {
    if (b.innerText.includes('Close') || b.innerText.includes('Got it')) {
        b.click();
    }
});
```

---

## Performance Metrics

| Metric | Value |
|--------|-------|
| Total animations | 13 |
| Generation time (each) | ~2 minutes |
| Batch processing time | ~45 minutes |
| Credits used | ~65 (5 per animation) |
| Success rate | 100% |

---

## Recommendations for Future Work

### 1. Always Use CDP for Browser Automation

CDP provides more reliable control than MCP tools:
```bash
# Launch Chrome in debug mode
./scripts/launch-chrome-debug.sh https://app.ludo.ai
```

### 2. Keep Debug Profile Persistent

Use `--user-data-dir` to maintain login session:
```bash
--user-data-dir="$HOME/chrome-debug-profile"
```

### 3. Screenshot on Failure

Always capture screenshots when automation fails:
```python
if not success:
    await cdp.screenshot(f"debug_{animation_name}.png")
```

### 4. Add Retry Logic

Network or UI timing issues may cause single failures:
```python
for attempt in range(3):
    success = await process_animation(char, emotion)
    if success:
        break
    await asyncio.sleep(5)
```

### 5. Validate Motion Prompts

Test prompts on a single animation before batch processing:
```bash
python scripts/ludo_batch_process.py bennie idle
# Review result before processing all
```

---

## File Outputs

### Generated Lottie Files

```
BennieGame/Resources/Lottie/
├── bennie_idle.json        (2.7 MB)
├── bennie_happy.json       (2.6 MB)
├── bennie_thinking.json    (2.7 MB)
├── bennie_encouraging.json (2.6 MB)
├── bennie_celebrating.json (2.7 MB)
├── bennie_waving.json      (2.4 MB)
├── bennie_pointing.json    (2.6 MB)
├── lemminge_idle.json      (2.6 MB)
├── lemminge_curious.json   (2.6 MB)
├── lemminge_excited.json   (2.6 MB)
├── lemminge_celebrating.json (2.6 MB)
├── lemminge_hiding.json    (2.7 MB)
└── lemminge_mischievous.json (2.6 MB)
```

### Lottie Format Details

- **Frames**: 36 per animation (6x6 grid)
- **FPS**: 30
- **Duration**: ~1.2 seconds
- **Format**: PNG frames embedded as base64

---

## Plan Mode Context

When planning future animation work, include this context:

```markdown
## Animation Generation Context

**Pipeline**: Gemini keyframes → Ludo.ai interpolation → Lottie JSON

**Prerequisites**:
1. Chrome running in debug mode (port 9222)
2. Logged into Ludo.ai with sufficient credits
3. Keyframe images generated (start.png + end.png)

**Key Learnings**:
- Click frame THUMBNAIL to upload (not buttons)
- Clear frames with trash icon before uploading
- Filter Animate button by width > 200px
- Click img.parentElement for export sprite selection
- Wait 5+ seconds after export for download

**Scripts**:
- `scripts/launch-chrome-debug.sh` - Start Chrome
- `scripts/ludo_batch_process.py` - Batch automation
- `starter-kits/ludo-animation-pipeline/process.py` - ZIP → Lottie

**Documentation**:
- `starter-kits/ludo-animation-pipeline/LUDO_CDP_WORKFLOW.md`
- `starter-kits/ludo-animation-pipeline/LESSONS_LEARNED.md`
```

---

## Related Files

| File | Purpose |
|------|---------|
| `scripts/launch-chrome-debug.sh` | Launch Chrome with debug port |
| `scripts/ludo_cdp_automation.py` | Core CDP client class |
| `scripts/ludo_batch_process.py` | Batch processing script |
| `starter-kits/ludo-animation-pipeline/process.py` | ZIP to Lottie converter |
| `.planning/phases/08-asset-production/08-03-SUMMARY.md` | Phase execution summary |
