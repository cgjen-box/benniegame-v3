# Ludo.ai CDP Automation Workflow

> **Created**: 2026-01-13
> **Purpose**: Complete guide for automating Ludo.ai sprite animation via Chrome DevTools Protocol
> **Status**: Production-tested (13 animations processed)

---

## Overview

This document captures the complete workflow for automating Ludo.ai's sprite animation generator using Chrome DevTools Protocol (CDP). This approach bypasses MCP limitations and provides full control over the browser automation.

---

## Prerequisites

### 1. Chrome in Debug Mode

```bash
# Launch Chrome with remote debugging enabled
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
    --remote-debugging-port=9222 \
    --user-data-dir="$HOME/chrome-debug-profile" \
    https://app.ludo.ai

# Or use the helper script:
./scripts/launch-chrome-debug.sh https://app.ludo.ai
```

### 2. Login to Ludo.ai

- Navigate to app.ludo.ai manually in the debug Chrome instance
- Log in with your Ludo.ai account
- Verify you see the Dashboard/My Games page

### 3. Navigate to Sprite Generator

- Click "Sprite Generator" in the sidebar
- You should see "First Frame" and "Final Frame" upload areas

---

## Critical UI Workflow Discovery

### The Upload Dialog Pattern

**Key Insight**: Clicking the frame THUMBNAIL IMAGE triggers the "Upload Image" dialog.

```
NOT:  "Change Pose" button → Opens different dialog
NOT:  "Open In Editor" → Opens sprite editor
YES:  Click the thumbnail image itself → Opens "Upload Image" dialog
```

### Frame Upload Sequence

1. **Clear existing frame first** (if any)
   - Find the trash/delete icon near the frame
   - Click to clear the current image

2. **Click thumbnail to open dialog**
   - Click on the empty frame area or placeholder
   - "Choose Image" button appears after clearing

3. **Upload via file input**
   - The dialog contains a hidden `<input type="file">`
   - Use CDP `DOM.setFileInputFiles` to set the file

### The Two Animate Buttons

**Critical**: There are TWO elements containing "Animate":

| Element | Location | Width | Purpose |
|---------|----------|-------|---------|
| Sidebar tab | Left side | ~100px | Navigation tab |
| Action button | Main area | >200px | Starts generation |

**Solution**: Filter for the action button by width:
```javascript
const btns = document.querySelectorAll('button');
for (const b of btns) {
    const rect = b.getBoundingClientRect();
    if (b.innerText.trim() === 'Animate' && rect.width > 200 && rect.x > 200) {
        b.click();  // This is the correct action button
    }
}
```

---

## Complete Automation Steps

### Step 1: Reset Interface

```javascript
// Scroll to top
window.scrollTo(0, 0);

// Click Reset button
const btns = document.querySelectorAll('button');
for (const b of btns) {
    if (b.innerText.trim() === 'Reset') {
        b.click();
        break;
    }
}
```

### Step 2: Upload First Frame (START)

```javascript
// Option A: Click "Choose Image" button (if frame is empty)
(function() {
    const els = document.querySelectorAll('*');
    for (const el of els) {
        if ((el.innerText || '').trim() === 'Choose Image') {
            const rect = el.getBoundingClientRect();
            // First "Choose Image" is for First Frame (top area, y < 300)
            if (rect.width > 50 && rect.width < 200 && rect.y > 0 && rect.y < 300) {
                el.click();
                return;
            }
        }
    }
})()

// Option B: Click trash icon first, then Choose Image
// (If frame already has an image)
```

Then upload via CDP:
```python
# Python CDP upload
await send_cmd('DOM.enable')
doc = await send_cmd('DOM.getDocument', {'depth': -1, 'pierce': True})
query = await send_cmd('DOM.querySelector', {
    'nodeId': doc['root']['nodeId'],
    'selector': 'input[type="file"]'
})
await send_cmd('DOM.setFileInputFiles', {
    'nodeId': query['nodeId'],
    'files': ['/path/to/start.png']
})
```

### Step 3: Clear Final Frame

```javascript
// Find Final Frame section and click trash/clear icon
(function() {
    const labels = document.querySelectorAll('*');
    for (const l of labels) {
        if ((l.innerText || '').trim().includes('Final Frame')) {
            let p = l.parentElement;
            for (let i = 0; i < 5 && p; i++) {
                const btns = p.querySelectorAll('button');
                for (const btn of btns) {
                    const rect = btn.getBoundingClientRect();
                    // Trash button is small with no text
                    if (rect.width > 10 && rect.width < 50 && !btn.innerText.trim()) {
                        btn.click();
                        return 'Cleared';
                    }
                }
                p = p.parentElement;
            }
        }
    }
    return 'Not cleared';
})()
```

### Step 4: Upload Final Frame (END)

```javascript
// Find the second "Choose Image" button (for Final Frame)
(function() {
    const els = document.querySelectorAll('*');
    const found = [];
    for (const el of els) {
        if ((el.innerText || '').trim() === 'Choose Image') {
            const rect = el.getBoundingClientRect();
            if (rect.width > 50 && rect.width < 200) {
                found.push({x: rect.left + rect.width/2, y: rect.top + rect.height/2});
            }
        }
    }
    // Last one is Final Frame's Choose Image
    return found.length > 0 ? found[found.length - 1] : null;
})()
```

### Step 5: Set Motion Prompt

```javascript
// Find textarea/input for animation description
(function() {
    const inputs = document.querySelectorAll('input, textarea');
    for (const inp of inputs) {
        const ph = inp.placeholder || '';
        if (ph.toLowerCase().includes('animation') || ph.toLowerCase().includes('describe')) {
            inp.value = 'gentle breathing cycle, calm rhythmic motion';
            inp.dispatchEvent(new Event('input', {bubbles: true}));
            return 'Set';
        }
    }
})()
```

### Step 6: Click Animate (Generate)

```javascript
// IMPORTANT: Filter for the ACTION button, not sidebar tab
(function() {
    const btns = document.querySelectorAll('button');
    for (const b of btns) {
        const rect = b.getBoundingClientRect();
        // Action button is wide (>200px) and not in sidebar (x > 200)
        if (b.innerText.trim() === 'Animate' && rect.width > 200 && rect.x > 200) {
            b.click();
            return 'Animate clicked';
        }
    }
})()
```

### Step 7: Wait for Generation

```python
# Poll for completion (up to 3 minutes)
for i in range(90):
    await asyncio.sleep(2)
    status = await evaluate('''
        document.body.innerText.toLowerCase().includes('generating') ? 'generating' : 'done'
    ''')
    if status == 'done':
        print(f"Generation complete ({(i+1)*2}s)")
        break
```

### Step 8: Export Animation

```javascript
// Step 8a: Click "Export Pack"
(function() {
    const btns = document.querySelectorAll('button');
    for (const b of btns) {
        if (b.innerText.includes('Export Pack')) {
            b.click();
            return;
        }
    }
})()

// Step 8b: Select sprite sheet format (click on sprite image)
(function() {
    const dialog = document.querySelector('[role="dialog"]') || document.body;
    const imgs = dialog.querySelectorAll('img');
    for (const img of imgs) {
        const rect = img.getBoundingClientRect();
        // Sprite option is medium-sized image in dialog
        if (rect.width > 60 && rect.width < 200 && rect.height > 60) {
            img.parentElement.click();
            return;
        }
    }
})()

// Step 8c: Click "Continue to Export"
// Step 8d: Click "Export Animation Pack"
```

### Step 9: Move Download

```bash
# Downloads go to ~/Downloads/animation-pack-spritesheets.zip
mv ~/Downloads/animation-pack-spritesheets.zip \
   starter-kits/ludo-animation-pipeline/downloads/bennie_idle.zip
```

---

## Motion Prompts Reference

| Animation | Motion Prompt |
|-----------|---------------|
| bennie_idle | gentle breathing cycle, chest slowly rising and falling, calm peaceful rhythmic motion |
| bennie_happy | gentle bounce up and down, cheerful rhythmic movement, slight hop with joy |
| bennie_thinking | head tilting side to side slowly, thoughtful pondering motion |
| bennie_encouraging | arms opening outward in welcoming gesture, supportive nodding |
| bennie_celebrating | arms raising up high in celebration, joyful controlled bouncing |
| bennie_waving | hand waving side to side smoothly, friendly greeting gesture |
| bennie_pointing | arm extending outward to point, directing attention |
| lemminge_idle | subtle breathing pulse, gentle body expanding and contracting |
| lemminge_curious | head tilting curiously, leaning forward with interest |
| lemminge_excited | bouncing up and down rapidly, energetic movement |
| lemminge_celebrating | jumping with arms raised high, pure joy expression |
| lemminge_hiding | shrinking down, paws covering face shyly |
| lemminge_mischievous | sneaky side-to-side swaying, mischievous hand rubbing |

---

## Troubleshooting

### "Upload Image" Dialog Doesn't Open

**Problem**: Clicking thumbnail doesn't trigger dialog.

**Solution**:
1. Check if frame already has an image
2. Click trash icon to clear first
3. Then click "Choose Image" button

### Wrong Animate Button Clicked

**Problem**: Clicks sidebar "Animate" tab instead of action button.

**Solution**: Filter by button width:
```javascript
rect.width > 200 && rect.x > 200
```

### Sprite Selection Fails in Export Dialog

**Problem**: Coordinate-based clicks miss the sprite option.

**Solution**: Use image element selection:
```javascript
const imgs = dialog.querySelectorAll('img');
for (const img of imgs) {
    if (rect.width > 60 && rect.width < 150) {
        img.parentElement.click();  // Click parent, not img
    }
}
```

### Download Not Found

**Problem**: ZIP file not in ~/Downloads after export.

**Solution**:
1. Add longer wait (5+ seconds after Export click)
2. Check for download progress indicators
3. Verify filename: `animation-pack-spritesheets.zip`

### Help Dialog Opens Unexpectedly

**Problem**: Help/tutorial modal appears mid-automation.

**Solution**: Close dialogs at start of each animation:
```javascript
document.querySelectorAll('[role="dialog"] button').forEach(b => {
    if (b.innerText.includes('Close') || b.innerText.includes('Got it')) {
        b.click();
    }
});
```

---

## Scripts Reference

| Script | Purpose |
|--------|---------|
| `scripts/launch-chrome-debug.sh` | Launch Chrome in debug mode |
| `scripts/ludo_cdp_automation.py` | Core CDP automation class |
| `scripts/ludo_batch_process.py` | Batch processing for all animations |

---

## Performance Notes

- **Generation time**: ~2 minutes per animation
- **Credits per animation**: 5
- **Total for 13 animations**: ~65 credits
- **Batch processing time**: ~45 minutes for all 13

---

## Related Documentation

- `SKILL.md` - Pipeline overview
- `process.py` - ZIP to Lottie conversion
- `.planning/phases/08-asset-production/08-03-SUMMARY.md` - Execution summary
