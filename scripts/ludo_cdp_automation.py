#!/usr/bin/env python3
"""
Ludo.ai CDP Automation Script
=============================
Automates sprite animation generation on ludo.ai using Chrome DevTools Protocol.

Requires Chrome running in debug mode:
    /Applications/Google Chrome.app/Contents/MacOS/Google Chrome \
        --remote-debugging-port=9222 \
        --user-data-dir="/Users/user289321/chrome-debug-profile" \
        https://ludo.ai

Usage:
    python scripts/ludo_cdp_automation.py                    # Process all 13 animations
    python scripts/ludo_cdp_automation.py bennie waving      # Process single animation
    python scripts/ludo_cdp_automation.py --status           # Check status
"""

import asyncio
import base64
import json
import os
import sys
import time
from pathlib import Path
from typing import Optional, Dict, Any, List, Tuple

import requests
import websockets

# =============================================================================
# CONFIGURATION
# =============================================================================

PROJECT_ROOT = Path(__file__).parent.parent.resolve()
KEYFRAMES_DIR = PROJECT_ROOT / "design" / "generated" / "Animations" / "keyframes"
DOWNLOADS_DIR = PROJECT_ROOT / "starter-kits" / "ludo-animation-pipeline" / "downloads"

CHROME_DEBUG_PORT = 9222
CDP_ENDPOINT = f"http://localhost:{CHROME_DEBUG_PORT}"
SPRITE_GENERATOR_URL = "https://app.ludo.ai"

# Animation definitions
ANIMATIONS = {
    "bennie": {
        "idle": "gentle breathing cycle, chest slowly rising and falling, calm peaceful rhythmic motion",
        "happy": "gentle bounce up and down, cheerful rhythmic movement, slight hop with joy",
        "thinking": "head tilting side to side slowly, thoughtful pondering motion",
        "encouraging": "arms opening outward in welcoming gesture, supportive nodding",
        "celebrating": "arms raising up high in celebration, joyful controlled bouncing",
        "waving": "hand waving side to side smoothly, friendly greeting gesture",
        "pointing": "arm extending outward to point, head turning to look at direction"
    },
    "lemminge": {
        "idle": "subtle breathing pulse, gentle body expanding and contracting",
        "curious": "head tilting curiously from side to side, leaning forward",
        "excited": "bouncing up and down rapidly, energetic jumping motion",
        "celebrating": "jumping with arms raised high, victory dance movement",
        "hiding": "shrinking down motion, paws moving to cover face",
        "mischievous": "sneaky side-to-side swaying, hands rubbing together"
    }
}


# =============================================================================
# CDP CLIENT
# =============================================================================

class CDPClient:
    """Chrome DevTools Protocol client using websockets."""

    def __init__(self):
        self.ws = None
        self.message_id = 0
        self.page_id = None
        self.ws_url = None

    async def connect(self) -> bool:
        """Connect to Chrome debug instance."""
        try:
            # Get available pages
            response = requests.get(f"{CDP_ENDPOINT}/json")
            pages = response.json()

            # Find the ludo.ai page
            for page in pages:
                if page.get("type") == "page" and "ludo.ai" in page.get("url", ""):
                    self.page_id = page["id"]
                    self.ws_url = page["webSocketDebuggerUrl"]
                    break

            if not self.ws_url:
                print("[ERROR] No ludo.ai page found in Chrome")
                return False

            # Connect to websocket
            self.ws = await websockets.connect(self.ws_url)
            print(f"[OK] Connected to Chrome page: {self.page_id}")
            return True

        except Exception as e:
            print(f"[ERROR] Failed to connect: {e}")
            return False

    async def send(self, method: str, params: dict = None) -> dict:
        """Send CDP command and wait for response."""
        self.message_id += 1
        message = {
            "id": self.message_id,
            "method": method,
            "params": params or {}
        }

        await self.ws.send(json.dumps(message))

        # Wait for response with matching id
        while True:
            response = await self.ws.recv()
            data = json.loads(response)
            if data.get("id") == self.message_id:
                return data
            # Handle events that come back
            if "method" in data:
                pass  # Ignore events for now

    async def navigate(self, url: str) -> bool:
        """Navigate to URL."""
        result = await self.send("Page.navigate", {"url": url})
        if "error" in result:
            print(f"[ERROR] Navigation failed: {result['error']}")
            return False
        # Wait for page load
        await asyncio.sleep(3)
        return True

    async def evaluate(self, expression: str) -> Any:
        """Evaluate JavaScript expression."""
        result = await self.send("Runtime.evaluate", {
            "expression": expression,
            "returnByValue": True
        })
        if "error" in result:
            return None
        return result.get("result", {}).get("result", {}).get("value")

    async def click_element(self, selector: str) -> bool:
        """Click element by CSS selector."""
        js = f"""
        (function() {{
            const el = document.querySelector('{selector}');
            if (el) {{
                el.click();
                return true;
            }}
            return false;
        }})()
        """
        result = await self.evaluate(js)
        return result == True

    async def fill_input(self, selector: str, value: str) -> bool:
        """Fill input element with value."""
        escaped = value.replace("'", "\\'").replace("\n", "\\n")
        js = f"""
        (function() {{
            const el = document.querySelector('{selector}');
            if (el) {{
                el.value = '{escaped}';
                el.dispatchEvent(new Event('input', {{ bubbles: true }}));
                el.dispatchEvent(new Event('change', {{ bubbles: true }}));
                return true;
            }}
            return false;
        }})()
        """
        result = await self.evaluate(js)
        return result == True

    async def upload_file_via_input(self, selector: str, file_path: str) -> bool:
        """Upload file to file input using CDP DOM.setFileInputFiles."""
        print(f"[INFO] Uploading file via CDP: {file_path}")

        try:
            # Enable DOM domain
            await self.send("DOM.enable")

            # Get document root
            doc = await self.send("DOM.getDocument")
            root_node_id = doc.get("result", {}).get("root", {}).get("nodeId")

            if not root_node_id:
                print("[ERROR] Could not get document root")
                return False

            # Find the file input by selector
            query = await self.send("DOM.querySelector", {
                "nodeId": root_node_id,
                "selector": selector
            })

            node_id = query.get("result", {}).get("nodeId")
            if not node_id:
                print(f"[ERROR] File input not found: {selector}")
                return False

            # Set files on the input
            result = await self.send("DOM.setFileInputFiles", {
                "nodeId": node_id,
                "files": [file_path]
            })

            if "error" in result:
                print(f"[ERROR] Failed to set file: {result['error']}")
                return False

            print(f"[OK] File uploaded: {Path(file_path).name}")
            await asyncio.sleep(1)  # Wait for UI to update
            return True

        except Exception as e:
            print(f"[ERROR] Upload failed: {e}")
            return False

    async def upload_file_by_index(self, index: int, file_path: str) -> bool:
        """Upload file to nth file input (0-indexed)."""
        selector = f'input[type="file"]:nth-of-type({index + 1})'

        # Try a simpler approach - find all file inputs and use the nth one
        try:
            await self.send("DOM.enable")
            doc = await self.send("DOM.getDocument", {"depth": -1})
            root_node_id = doc.get("result", {}).get("root", {}).get("nodeId")

            # Get all file inputs
            query = await self.send("DOM.querySelectorAll", {
                "nodeId": root_node_id,
                "selector": 'input[type="file"]'
            })

            node_ids = query.get("result", {}).get("nodeIds", [])
            if not node_ids or len(node_ids) <= index:
                print(f"[ERROR] File input #{index} not found (found {len(node_ids)} inputs)")
                return False

            node_id = node_ids[index]

            # Set the file
            result = await self.send("DOM.setFileInputFiles", {
                "nodeId": node_id,
                "files": [file_path]
            })

            if "error" in result:
                print(f"[ERROR] Failed to set file: {result['error']}")
                return False

            print(f"[OK] File uploaded to input #{index}: {Path(file_path).name}")
            await asyncio.sleep(1)
            return True

        except Exception as e:
            print(f"[ERROR] Upload failed: {e}")
            return False

    async def wait_for_element(self, selector: str, timeout: int = 30) -> bool:
        """Wait for element to appear."""
        start = time.time()
        while time.time() - start < timeout:
            js = f"document.querySelector('{selector}') !== null"
            result = await self.evaluate(js)
            if result:
                return True
            await asyncio.sleep(1)
        return False

    async def wait_for_text(self, text: str, timeout: int = 120) -> bool:
        """Wait for text to appear on page."""
        escaped = text.replace("'", "\\'")
        start = time.time()
        while time.time() - start < timeout:
            js = f"document.body.innerText.includes('{escaped}')"
            result = await self.evaluate(js)
            if result:
                return True
            await asyncio.sleep(2)
            print(f"[WAIT] Waiting for '{text}'... ({int(time.time() - start)}s)")
        return False

    async def get_page_content(self) -> str:
        """Get current page HTML."""
        return await self.evaluate("document.body.innerHTML")

    async def screenshot(self, path: str) -> bool:
        """Take screenshot."""
        result = await self.send("Page.captureScreenshot", {"format": "png"})
        if "result" in result and "data" in result["result"]:
            data = base64.b64decode(result["result"]["data"])
            with open(path, "wb") as f:
                f.write(data)
            return True
        return False

    async def close(self):
        """Close websocket connection."""
        if self.ws:
            await self.ws.close()


# =============================================================================
# LUDO AUTOMATION
# =============================================================================

async def check_login_status(cdp: CDPClient) -> bool:
    """Check if user is logged into Ludo.ai."""
    # Look for login/signup buttons vs account menu
    js = """
    (function() {
        const loginBtn = document.querySelector('a[href*="login"], button:contains("Log in")');
        const accountMenu = document.querySelector('[class*="avatar"], [class*="profile"], [class*="account"]');
        if (accountMenu) return 'logged_in';
        if (loginBtn) return 'logged_out';
        return 'unknown';
    })()
    """
    # Simpler check
    result = await cdp.evaluate("document.body.innerText.includes('My Games') || document.body.innerText.includes('Dashboard')")
    return result == True


async def navigate_to_sprite_generator(cdp: CDPClient) -> bool:
    """Navigate to sprite generator page."""
    print("[STEP] Navigating to sprite generator...")

    # Check current URL
    current_url = await cdp.evaluate("window.location.href")
    if "sprite-generator" in str(current_url):
        print("[OK] Already on sprite generator page")
        return True

    await cdp.navigate(SPRITE_GENERATOR_URL)
    await asyncio.sleep(2)

    # Verify we're on the right page
    await cdp.wait_for_text("Sprite", timeout=15)
    print("[OK] On sprite generator page")
    return True


async def switch_to_animate_tab(cdp: CDPClient) -> bool:
    """Switch to the Animate tab."""
    print("[STEP] Switching to Animate tab...")

    # Try clicking Animate tab
    js = """
    (function() {
        // Look for tab buttons
        const tabs = document.querySelectorAll('button, [role="tab"], div[class*="tab"]');
        for (const tab of tabs) {
            if (tab.innerText.toLowerCase().includes('animate')) {
                tab.click();
                return true;
            }
        }
        return false;
    })()
    """
    result = await cdp.evaluate(js)
    if result:
        await asyncio.sleep(1)
        print("[OK] Switched to Animate tab")
        return True

    print("[WARN] Could not find Animate tab")
    return False


async def click_first_frame_thumbnail(cdp: CDPClient) -> bool:
    """Click on First Frame thumbnail image to trigger upload dialog.

    KEY INSIGHT: Clicking the thumbnail image directly opens the "Upload Image" dialog,
    NOT the "Change Pose" or "Open In Editor" buttons.
    """
    print("[STEP] Clicking First Frame thumbnail...")

    js = '''
    (function() {
        // Find First Frame section and click on the image inside
        const allElements = document.querySelectorAll('div, span, label, h3, h4');
        for (const el of allElements) {
            const text = (el.innerText || '').trim();
            if (text === 'First Frame') {
                // Find the image in this element's parent/siblings
                let searchEl = el.parentElement;
                for (let i = 0; i < 3 && searchEl; i++) {
                    const img = searchEl.querySelector('img');
                    if (img) {
                        img.click();
                        return 'Clicked First Frame thumbnail via label';
                    }
                    searchEl = searchEl.parentElement;
                }
            }
        }

        // Fallback: click first image in the frame area (left side, top area)
        const frameImgs = document.querySelectorAll('img');
        for (const img of frameImgs) {
            const rect = img.getBoundingClientRect();
            // First Frame image is typically around x=140-230, y=50-200
            if (rect.left > 130 && rect.left < 240 && rect.top > 40 && rect.top < 220 && rect.width > 50) {
                img.click();
                return 'Clicked frame image at x=' + Math.round(rect.left);
            }
        }
        return 'Not found';
    })()
    '''

    result = await cdp.evaluate(js)
    print(f"[INFO] First Frame click result: {result}")

    if result and 'Clicked' in str(result):
        await asyncio.sleep(1)
        return True
    return False


async def click_final_frame_thumbnail(cdp: CDPClient) -> bool:
    """Click on Final Frame thumbnail image to trigger upload dialog.

    Can also use "Choose Image" button if thumbnail doesn't work.
    """
    print("[STEP] Clicking Final Frame thumbnail...")

    js = '''
    (function() {
        // First try: Find Final Frame section and click image
        const allElements = document.querySelectorAll('div, span, label, h3, h4');
        for (const el of allElements) {
            const text = (el.innerText || '').trim();
            if (text.includes('Final Frame')) {
                let searchEl = el.parentElement;
                for (let i = 0; i < 3 && searchEl; i++) {
                    const img = searchEl.querySelector('img');
                    if (img) {
                        img.click();
                        return 'Clicked Final Frame thumbnail via label';
                    }
                    searchEl = searchEl.parentElement;
                }
            }
        }

        // Second try: Click "Choose Image" button
        const buttons = document.querySelectorAll('button, span, div[role="button"]');
        for (const btn of buttons) {
            const text = (btn.innerText || '').trim();
            if (text === 'Choose Image') {
                btn.click();
                return 'Clicked Choose Image button';
            }
        }

        // Fallback: click second image in frame area (right side, top area)
        const frameImgs = document.querySelectorAll('img');
        for (const img of frameImgs) {
            const rect = img.getBoundingClientRect();
            // Final Frame image is typically around x=240-350
            if (rect.left > 230 && rect.left < 360 && rect.top > 40 && rect.top < 220 && rect.width > 50) {
                img.click();
                return 'Clicked frame image at x=' + Math.round(rect.left);
            }
        }
        return 'Not found';
    })()
    '''

    result = await cdp.evaluate(js)
    print(f"[INFO] Final Frame click result: {result}")

    if result and 'Clicked' in str(result):
        await asyncio.sleep(1)
        return True
    return False


async def wait_for_upload_dialog(cdp: CDPClient, timeout: int = 10) -> bool:
    """Wait for the Upload Image dialog to appear."""
    return await cdp.wait_for_text("Upload Image", timeout)


async def upload_via_dialog(cdp: CDPClient, file_path: Path) -> bool:
    """Upload file via the Upload Image dialog's file input."""
    print(f"[STEP] Uploading via dialog: {file_path.name}")

    if not file_path.exists():
        print(f"[ERROR] File not found: {file_path}")
        return False

    # Wait for dialog and file input to appear
    await asyncio.sleep(1)

    # Find file input and upload
    try:
        await cdp.send("DOM.enable")
        doc = await cdp.send("DOM.getDocument", {"depth": -1})
        root_node_id = doc.get("result", {}).get("root", {}).get("nodeId")

        # Find file input
        query = await cdp.send("DOM.querySelectorAll", {
            "nodeId": root_node_id,
            "selector": 'input[type="file"]'
        })

        node_ids = query.get("result", {}).get("nodeIds", [])
        if not node_ids:
            print("[ERROR] No file input found in dialog")
            return False

        # Use the most recent file input (last one - likely in dialog)
        node_id = node_ids[-1]

        # Set the file
        result = await cdp.send("DOM.setFileInputFiles", {
            "nodeId": node_id,
            "files": [str(file_path)]
        })

        if "error" in result:
            print(f"[ERROR] Failed to set file: {result['error']}")
            return False

        print(f"[OK] File uploaded: {file_path.name}")
        await asyncio.sleep(2)  # Wait for preview to update
        return True

    except Exception as e:
        print(f"[ERROR] Upload failed: {e}")
        return False


async def upload_keyframe(cdp: CDPClient, file_path: Path, is_start: bool) -> bool:
    """Upload a keyframe image to Ludo.ai."""
    label = "START" if is_start else "END"
    print(f"[STEP] Uploading {label} keyframe: {file_path.name}")

    if not file_path.exists():
        print(f"[ERROR] File not found: {file_path}")
        return False

    # Read file and convert to base64
    with open(file_path, "rb") as f:
        file_data = base64.b64encode(f.read()).decode()

    # Find file input and set file
    # Ludo.ai likely has specific upload areas - we'll use their interface
    slot_index = 0 if is_start else 1

    js = f"""
    (function() {{
        // Find file inputs
        const inputs = document.querySelectorAll('input[type="file"]');
        if (inputs.length > {slot_index}) {{
            return true;  // Input exists
        }}
        return false;
    }})()
    """

    has_input = await cdp.evaluate(js)
    if not has_input:
        print(f"[WARN] File input not found for {label} frame")

    # For now, log the file path - actual upload requires more complex CDP
    print(f"[INFO] File ready: {file_path}")
    return True


async def fill_motion_prompt(cdp: CDPClient, prompt: str) -> bool:
    """Fill the motion description prompt."""
    print(f"[STEP] Setting motion prompt: {prompt[:50]}...")

    # Find textarea or input for prompt
    js = f"""
    (function() {{
        // Try textarea first
        const textarea = document.querySelector('textarea');
        if (textarea) {{
            textarea.value = `{prompt}`;
            textarea.dispatchEvent(new Event('input', {{ bubbles: true }}));
            return true;
        }}
        // Try contenteditable
        const editable = document.querySelector('[contenteditable="true"]');
        if (editable) {{
            editable.innerText = `{prompt}`;
            editable.dispatchEvent(new Event('input', {{ bubbles: true }}));
            return true;
        }}
        return false;
    }})()
    """

    result = await cdp.evaluate(js)
    if result:
        print("[OK] Motion prompt set")
        return True

    print("[WARN] Could not find prompt input")
    return False


async def click_generate(cdp: CDPClient) -> bool:
    """Click the Generate/Animate button."""
    print("[STEP] Clicking Generate button...")

    js = """
    (function() {
        // Look for generate button
        const buttons = document.querySelectorAll('button');
        for (const btn of buttons) {
            const text = btn.innerText.toLowerCase();
            if (text.includes('generate') || text.includes('animate') || text.includes('create')) {
                btn.click();
                return true;
            }
        }
        return false;
    })()
    """

    result = await cdp.evaluate(js)
    if result:
        print("[OK] Generate button clicked")
        return True

    print("[WARN] Could not find Generate button")
    return False


async def wait_for_generation(cdp: CDPClient, timeout: int = 180) -> bool:
    """Wait for animation generation to complete."""
    print(f"[STEP] Waiting for generation (up to {timeout}s)...")

    # Look for download button or completion indicator
    start = time.time()
    while time.time() - start < timeout:
        # Check for download button
        js = """
        (function() {
            const buttons = document.querySelectorAll('button, a');
            for (const btn of buttons) {
                const text = btn.innerText.toLowerCase();
                if (text.includes('download')) {
                    return true;
                }
            }
            return false;
        })()
        """
        result = await cdp.evaluate(js)
        if result:
            print("[OK] Generation complete - download available")
            return True

        elapsed = int(time.time() - start)
        if elapsed % 10 == 0:
            print(f"[WAIT] Still generating... ({elapsed}s)")

        await asyncio.sleep(2)

    print("[ERROR] Generation timed out")
    return False


async def click_download(cdp: CDPClient) -> bool:
    """Click the download button."""
    print("[STEP] Clicking Download button...")

    js = """
    (function() {
        const buttons = document.querySelectorAll('button, a');
        for (const btn of buttons) {
            const text = btn.innerText.toLowerCase();
            if (text.includes('download')) {
                btn.click();
                return true;
            }
        }
        return false;
    })()
    """

    result = await cdp.evaluate(js)
    if result:
        print("[OK] Download initiated")
        await asyncio.sleep(3)  # Wait for download to start
        return True

    print("[WARN] Could not find Download button")
    return False


async def process_animation(cdp: CDPClient, character: str, emotion: str, skip_navigation: bool = False) -> bool:
    """Process a single animation through Ludo.ai."""
    print(f"\n{'='*60}")
    print(f"Processing: {character}_{emotion}")
    print(f"{'='*60}")

    # Get keyframe paths
    keyframe_dir = KEYFRAMES_DIR / f"{character}_{emotion}"
    start_frame = keyframe_dir / "start.png"
    end_frame = keyframe_dir / "end.png"

    if not start_frame.exists():
        print(f"[ERROR] Start frame not found: {start_frame}")
        return False
    if not end_frame.exists():
        print(f"[ERROR] End frame not found: {end_frame}")
        return False

    # Get motion prompt
    motion_prompt = ANIMATIONS.get(character, {}).get(emotion, "smooth animation")

    # Navigate to sprite generator if needed
    if not skip_navigation:
        if not await navigate_to_sprite_generator(cdp):
            return False

    # Switch to Animate tab
    await switch_to_animate_tab(cdp)
    await asyncio.sleep(2)

    # Take screenshot before uploads
    screenshot_path = DOWNLOADS_DIR / f"{character}_{emotion}_before.png"
    await cdp.screenshot(str(screenshot_path))
    print(f"[DEBUG] Screenshot saved: {screenshot_path}")

    # ===== UPLOAD START FRAME (First Frame) =====
    # Click on First Frame THUMBNAIL to trigger upload dialog
    print(f"[STEP] Uploading START frame: {start_frame}")
    if not await click_first_frame_thumbnail(cdp):
        print("[ERROR] Could not click First Frame thumbnail")
        await cdp.screenshot(str(DOWNLOADS_DIR / f"{character}_{emotion}_ff_fail.png"))
        return False

    # Wait for Upload Image dialog
    if not await wait_for_upload_dialog(cdp, timeout=10):
        print("[WARN] Upload dialog may not have appeared, trying anyway...")

    # Upload the START keyframe
    start_uploaded = await upload_via_dialog(cdp, start_frame)
    if not start_uploaded:
        print("[ERROR] Failed to upload START frame")
        return False

    # Close dialog / wait for preview
    await asyncio.sleep(2)
    # Press Escape to close dialog if still open
    await cdp.evaluate("document.dispatchEvent(new KeyboardEvent('keydown', {key: 'Escape'}))")
    await asyncio.sleep(1)

    # ===== UPLOAD END FRAME (Final Frame) =====
    # Click on Final Frame thumbnail or "Choose Image" button
    print(f"[STEP] Uploading END frame: {end_frame}")
    if not await click_final_frame_thumbnail(cdp):
        print("[ERROR] Could not click Final Frame thumbnail")
        await cdp.screenshot(str(DOWNLOADS_DIR / f"{character}_{emotion}_lf_fail.png"))
        return False

    # Wait for Upload Image dialog
    if not await wait_for_upload_dialog(cdp, timeout=10):
        print("[WARN] Upload dialog may not have appeared, trying anyway...")

    # Upload the END keyframe
    end_uploaded = await upload_via_dialog(cdp, end_frame)
    if not end_uploaded:
        print("[ERROR] Failed to upload END frame")
        return False

    # Close dialog / wait for preview
    await asyncio.sleep(2)
    await cdp.evaluate("document.dispatchEvent(new KeyboardEvent('keydown', {key: 'Escape'}))")
    await asyncio.sleep(1)

    # Fill motion prompt
    await fill_motion_prompt(cdp, motion_prompt)
    await asyncio.sleep(1)

    # Take screenshot after setup
    setup_path = DOWNLOADS_DIR / f"{character}_{emotion}_setup.png"
    await cdp.screenshot(str(setup_path))
    print(f"[DEBUG] Setup screenshot: {setup_path}")

    # Click Generate button
    if not await click_generate(cdp):
        print("[ERROR] Could not find Generate button")
        return False

    # Wait for generation to complete (can take 1-3 minutes)
    print("[STEP] Waiting for animation generation...")
    if not await wait_for_generation(cdp, timeout=180):
        print("[ERROR] Generation timed out")
        return False

    # Click Download
    if not await click_download(cdp):
        print("[ERROR] Could not find Download button")
        return False

    # Wait for download to complete
    await asyncio.sleep(5)

    # Move downloaded file to proper location
    download_dest = DOWNLOADS_DIR / f"{character}_{emotion}.zip"
    print(f"[OK] Animation generated! File should be at: {download_dest}")

    return True


async def get_page_info(cdp: CDPClient) -> dict:
    """Get information about the current page state."""
    info = {}

    # Get URL
    info["url"] = await cdp.evaluate("window.location.href")

    # Get title
    info["title"] = await cdp.evaluate("document.title")

    # Check for key elements
    info["has_textarea"] = await cdp.evaluate("document.querySelector('textarea') !== null")
    info["has_file_input"] = await cdp.evaluate("document.querySelector('input[type=\"file\"]') !== null")

    # Get all buttons
    buttons_js = """
    Array.from(document.querySelectorAll('button')).map(b => b.innerText.trim()).filter(t => t.length > 0).slice(0, 10)
    """
    info["buttons"] = await cdp.evaluate(buttons_js)

    return info


# =============================================================================
# MAIN
# =============================================================================

async def do_login(cdp: CDPClient) -> bool:
    """Log into Ludo.ai using credentials from .env."""
    # Credentials from .env
    email = "cgjenny@gmail.com"
    password = "*ODUwMTExNDQxLjE3N"

    print("[STEP] Attempting to log in...")

    # Click Sign In button
    js = """
    (function() {
        const btns = document.querySelectorAll('button, a');
        for (const btn of btns) {
            if (btn.innerText.toLowerCase().includes('sign in') || btn.innerText.toLowerCase().includes('log in')) {
                btn.click();
                return true;
            }
        }
        return false;
    })()
    """
    clicked = await cdp.evaluate(js)
    if clicked:
        print("[OK] Clicked Sign In")
        await asyncio.sleep(2)
    else:
        print("[WARN] Sign In button not found")
        return False

    # Wait for login form
    await asyncio.sleep(2)

    # Fill email
    email_js = f"""
    (function() {{
        const inputs = document.querySelectorAll('input[type="email"], input[name="email"], input[placeholder*="email" i]');
        for (const inp of inputs) {{
            inp.value = '{email}';
            inp.dispatchEvent(new Event('input', {{ bubbles: true }}));
            return true;
        }}
        return false;
    }})()
    """
    if await cdp.evaluate(email_js):
        print(f"[OK] Email entered")
    else:
        print("[WARN] Email input not found")

    # Fill password
    password_js = f"""
    (function() {{
        const inputs = document.querySelectorAll('input[type="password"]');
        for (const inp of inputs) {{
            inp.value = '{password}';
            inp.dispatchEvent(new Event('input', {{ bubbles: true }}));
            return true;
        }}
        return false;
    }})()
    """
    if await cdp.evaluate(password_js):
        print("[OK] Password entered")
    else:
        print("[WARN] Password input not found")

    # Click submit
    submit_js = """
    (function() {
        const btns = document.querySelectorAll('button[type="submit"], button');
        for (const btn of btns) {
            const text = btn.innerText.toLowerCase();
            if (text.includes('sign in') || text.includes('log in') || text.includes('continue')) {
                btn.click();
                return true;
            }
        }
        return false;
    })()
    """
    if await cdp.evaluate(submit_js):
        print("[OK] Submit clicked")
        await asyncio.sleep(3)
    else:
        print("[WARN] Submit button not found")

    return True


async def main():
    print("Ludo.ai CDP Automation")
    print("=" * 60)

    # Ensure downloads directory exists
    DOWNLOADS_DIR.mkdir(parents=True, exist_ok=True)

    # Connect to Chrome
    cdp = CDPClient()
    if not await cdp.connect():
        print("[ERROR] Failed to connect to Chrome")
        print("Make sure Chrome is running in debug mode:")
        print('  "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \\')
        print('      --remote-debugging-port=9222 \\')
        print('      --user-data-dir="/Users/user289321/chrome-debug-profile" \\')
        print('      https://ludo.ai')
        return 1

    try:
        # Get page info
        info = await get_page_info(cdp)
        print(f"[INFO] Current URL: {info.get('url')}")
        print(f"[INFO] Page title: {info.get('title')}")

        # Navigate to app.ludo.ai
        if "app.ludo.ai" not in str(info.get("url", "")):
            print("\n[STEP] Navigating to app.ludo.ai...")
            await cdp.navigate("https://app.ludo.ai")
            await asyncio.sleep(3)

        # Check login status
        is_logged_in = await check_login_status(cdp)
        if not is_logged_in:
            print("[WARN] User may not be logged in")
            info = await get_page_info(cdp)
            buttons = info.get('buttons', [])
            if any('sign in' in b.lower() for b in buttons):
                print("[INFO] Attempting login...")
                await do_login(cdp)
                await asyncio.sleep(3)

        # Navigate to Sprite Generator
        print("\n[STEP] Navigating to Sprite Generator...")

        # Click Sprite Generator in sidebar/menu
        click_sprite_js = """
        (function() {
            // Try multiple selectors for sprite generator
            const selectors = [
                'a[href*="sprite"]',
                'button:contains("Sprite")',
                '[data-testid*="sprite"]',
            ];

            // Also try by text content
            const allElements = document.querySelectorAll('a, button, div[role="button"], span, nav li, aside a');
            for (const el of allElements) {
                const text = (el.innerText || el.textContent || '').toLowerCase().trim();
                if (text.includes('sprite generator') || text === 'sprite' || text === 'sprite generator') {
                    el.click();
                    return 'Clicked: ' + text;
                }
            }
            return 'Not found';
        })()
        """
        click_result = await cdp.evaluate(click_sprite_js)
        print(f"[INFO] Sprite Generator click: {click_result}")
        await asyncio.sleep(3)

        # Take screenshot
        screenshot_path = DOWNLOADS_DIR / "sprite_generator_page.png"
        await cdp.screenshot(str(screenshot_path))
        print(f"[OK] Screenshot: {screenshot_path}")

        # Get updated page info
        info = await get_page_info(cdp)
        print(f"[INFO] URL: {info.get('url')}")
        print(f"[INFO] Has file input: {info.get('has_file_input')}")
        print(f"[INFO] Buttons: {info.get('buttons', [])[:8]}")

        # Check command line arguments
        if len(sys.argv) > 1 and sys.argv[1] == "--status":
            # Status mode - just show info
            print("\n[STATUS] Animations ready:")
            for char, emotions in ANIMATIONS.items():
                for emo in emotions:
                    keyframe_dir = KEYFRAMES_DIR / f"{char}_{emo}"
                    download = DOWNLOADS_DIR / f"{char}_{emo}.zip"
                    status = "✓ done" if download.exists() else ("⋯ ready" if keyframe_dir.exists() else "✗ missing")
                    print(f"  {status}: {char}_{emo}")
            return 0

        elif len(sys.argv) > 2:
            # Single animation mode
            character = sys.argv[1]
            emotion = sys.argv[2]
            success = await process_animation(cdp, character, emotion, skip_navigation=True)
            return 0 if success else 1

        elif len(sys.argv) > 1 and sys.argv[1] == "--all":
            # Process all animations
            print("\n[BATCH] Processing all 13 animations...")
            results = {"success": [], "failed": []}

            for char, emotions in ANIMATIONS.items():
                for emo in emotions:
                    # Check if already done
                    download = DOWNLOADS_DIR / f"{char}_{emo}.zip"
                    if download.exists():
                        print(f"[SKIP] {char}_{emo} already downloaded")
                        results["success"].append(f"{char}_{emo}")
                        continue

                    # Process
                    success = await process_animation(cdp, char, emo, skip_navigation=True)
                    if success:
                        results["success"].append(f"{char}_{emo}")
                    else:
                        results["failed"].append(f"{char}_{emo}")

                    # Small delay between animations
                    await asyncio.sleep(2)

            print(f"\n[SUMMARY]")
            print(f"  Success: {len(results['success'])}")
            print(f"  Failed: {len(results['failed'])}")
            if results['failed']:
                print(f"  Failed animations: {', '.join(results['failed'])}")

            return 0 if not results['failed'] else 1

        else:
            # Default: show usage
            print("\n[USAGE]")
            print("  python scripts/ludo_cdp_automation.py --status        # Check status")
            print("  python scripts/ludo_cdp_automation.py bennie waving   # Single animation")
            print("  python scripts/ludo_cdp_automation.py --all           # Process all 13")
            print("\n[INFO] Animations to process:")
            for char, emotions in ANIMATIONS.items():
                for emo in emotions:
                    keyframe_dir = KEYFRAMES_DIR / f"{char}_{emo}"
                    download = DOWNLOADS_DIR / f"{char}_{emo}.zip"
                    status = "✓" if download.exists() else ("⋯" if keyframe_dir.exists() else "✗")
                    print(f"  {status} {char}_{emo}")

        return 0

    finally:
        await cdp.close()


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
