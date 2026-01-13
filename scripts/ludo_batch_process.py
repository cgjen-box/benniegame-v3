#!/usr/bin/env python3
"""
Batch process animations through Ludo.ai
Run with: python scripts/ludo_batch_process.py [character] [emotion]
"""
import asyncio
import json
import base64
import websockets
import urllib.request
from pathlib import Path
import sys
import time

PROJECT_ROOT = Path(__file__).parent.parent
KEYFRAMES_DIR = PROJECT_ROOT / "design" / "generated" / "Animations" / "keyframes"
DOWNLOADS_DIR = PROJECT_ROOT / "starter-kits" / "ludo-animation-pipeline" / "downloads"

# Motion prompts for each animation
MOTION_PROMPTS = {
    "bennie_idle": "gentle breathing cycle, chest slowly rising and falling, calm peaceful rhythmic motion",
    "bennie_happy": "gentle bounce up and down, cheerful rhythmic movement, slight hop with joy",
    "bennie_thinking": "head tilting side to side slowly, thoughtful pondering motion",
    "bennie_encouraging": "arms opening outward in welcoming gesture, supportive nodding",
    "bennie_celebrating": "arms raising up high in celebration, joyful controlled bouncing",
    "bennie_waving": "hand waving side to side smoothly, friendly greeting gesture",
    "bennie_pointing": "arm extending outward to point, directing attention",
    "lemminge_idle": "subtle breathing pulse, gentle body expanding and contracting",
    "lemminge_curious": "head tilting curiously, leaning forward with interest",
    "lemminge_excited": "bouncing up and down rapidly, energetic movement",
    "lemminge_celebrating": "jumping with arms raised high, pure joy expression",
    "lemminge_hiding": "shrinking down, paws covering face shyly",
    "lemminge_mischievous": "sneaky side-to-side swaying, mischievous hand rubbing",
}

async def get_ws_url():
    with urllib.request.urlopen('http://localhost:9222/json') as response:
        tabs = json.loads(response.read())
        return tabs[0]['webSocketDebuggerUrl']

async def process_animation(character, emotion):
    """Process a single animation through Ludo.ai"""
    anim_name = f"{character}_{emotion}"
    keyframes_path = KEYFRAMES_DIR / anim_name
    start_file = str(keyframes_path / "start.png")
    end_file = str(keyframes_path / "end.png")
    motion_prompt = MOTION_PROMPTS.get(anim_name, "smooth animation motion")
    
    if not Path(start_file).exists():
        print(f"[ERROR] Start file not found: {start_file}")
        return False
    
    print(f"\n{'='*60}")
    print(f"Processing: {anim_name}")
    print(f"{'='*60}")
    
    ws_url = await get_ws_url()
    
    async with websockets.connect(ws_url) as ws:
        msg_id = 1
        
        async def send_cmd(method, params=None):
            nonlocal msg_id
            cmd = {'id': msg_id, 'method': method}
            if params:
                cmd['params'] = params
            await ws.send(json.dumps(cmd))
            msg_id += 1
            return json.loads(await ws.recv()).get('result', {})
        
        async def evaluate(js):
            result = await send_cmd('Runtime.evaluate', {'expression': js, 'returnByValue': True})
            return result.get('result', {}).get('value')
        
        async def click_at(x, y):
            await send_cmd('Input.dispatchMouseEvent', {'type': 'mousePressed', 'x': x, 'y': y, 'button': 'left', 'clickCount': 1})
            await send_cmd('Input.dispatchMouseEvent', {'type': 'mouseReleased', 'x': x, 'y': y, 'button': 'left', 'clickCount': 1})
        
        # Step 1: Scroll to top and click Reset
        print("[1/8] Resetting interface...")
        await evaluate('window.scrollTo(0, 0)')
        await asyncio.sleep(0.5)
        
        reset_result = await evaluate('''
            (function() {
                const btns = document.querySelectorAll('button');
                for (const b of btns) {
                    if (b.innerText.trim() === 'Reset') { b.click(); return 'Reset clicked'; }
                }
                return 'Reset not found';
            })()
        ''')
        print(f"   {reset_result}")
        await asyncio.sleep(1)
        
        # Scroll container to top
        await evaluate('''
            (function() {
                const containers = document.querySelectorAll('[class*="scroll"], main');
                for (const c of containers) { if (c.scrollTop > 0) c.scrollTop = 0; }
            })()
        ''')
        await asyncio.sleep(1)
        
        # Step 2: Upload First Frame
        print("[2/8] Uploading start frame...")
        pos = await evaluate('''
            (function() {
                const els = document.querySelectorAll('*');
                for (const el of els) {
                    if ((el.innerText || '').trim() === 'Choose Image') {
                        const rect = el.getBoundingClientRect();
                        if (rect.width > 50 && rect.width < 200 && rect.y > 0 && rect.y < 300) {
                            return JSON.stringify({x: Math.round(rect.left + rect.width/2), y: Math.round(rect.top + rect.height/2)});
                        }
                    }
                }
                return null;
            })()
        ''')
        
        if pos:
            coords = json.loads(pos)
            await click_at(coords['x'], coords['y'])
            await asyncio.sleep(2)
            
            # Upload file
            await send_cmd('DOM.enable')
            doc = await send_cmd('DOM.getDocument', {'depth': -1, 'pierce': True})
            query = await send_cmd('DOM.querySelector', {'nodeId': doc['root']['nodeId'], 'selector': 'input[type="file"]'})
            if query.get('nodeId'):
                await send_cmd('DOM.setFileInputFiles', {'nodeId': query['nodeId'], 'files': [start_file]})
                print(f"   Uploaded: {start_file}")
            await asyncio.sleep(3)
        
        # Step 3: Clear Final Frame (click trash)
        print("[3/8] Clearing final frame...")
        await evaluate('''
            (function() {
                const labels = document.querySelectorAll('*');
                for (const l of labels) {
                    if ((l.innerText || '').trim().includes('Final Frame')) {
                        let p = l.parentElement;
                        for (let i = 0; i < 5 && p; i++) {
                            const btns = p.querySelectorAll('button');
                            for (const btn of btns) {
                                const rect = btn.getBoundingClientRect();
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
        ''')
        await asyncio.sleep(1)
        
        # Step 4: Upload Final Frame
        print("[4/8] Uploading end frame...")
        pos2 = await evaluate('''
            (function() {
                const els = document.querySelectorAll('*');
                const found = [];
                for (const el of els) {
                    if ((el.innerText || '').trim() === 'Choose Image') {
                        const rect = el.getBoundingClientRect();
                        if (rect.width > 50 && rect.width < 200) {
                            found.push({x: Math.round(rect.left + rect.width/2), y: Math.round(rect.top + rect.height/2)});
                        }
                    }
                }
                return found.length > 0 ? JSON.stringify(found[found.length - 1]) : null;
            })()
        ''')
        
        if pos2:
            coords2 = json.loads(pos2)
            await click_at(coords2['x'], coords2['y'])
            await asyncio.sleep(2)
            
            doc = await send_cmd('DOM.getDocument', {'depth': -1, 'pierce': True})
            query = await send_cmd('DOM.querySelector', {'nodeId': doc['root']['nodeId'], 'selector': 'input[type="file"]'})
            if query.get('nodeId'):
                await send_cmd('DOM.setFileInputFiles', {'nodeId': query['nodeId'], 'files': [end_file]})
                print(f"   Uploaded: {end_file}")
            await asyncio.sleep(3)
        
        # Step 5: Fill motion prompt
        print("[5/8] Setting motion prompt...")
        await evaluate(f'''
            (function() {{
                const inputs = document.querySelectorAll('input, textarea');
                for (const inp of inputs) {{
                    const ph = inp.placeholder || '';
                    if (ph.toLowerCase().includes('animation') || ph.toLowerCase().includes('describe')) {{
                        inp.value = '{motion_prompt}';
                        inp.dispatchEvent(new Event('input', {{bubbles: true}}));
                        return 'Set';
                    }}
                }}
            }})()
        ''')
        await asyncio.sleep(0.5)
        
        # Step 6: Click Animate
        print("[6/8] Starting generation...")
        await evaluate('''
            (function() {
                const btns = document.querySelectorAll('button');
                for (const b of btns) {
                    const rect = b.getBoundingClientRect();
                    if (b.innerText.trim() === 'Animate' && rect.width > 200 && rect.x > 200) {
                        b.click();
                        return 'Animate clicked';
                    }
                }
            })()
        ''')
        
        # Wait for generation (poll for 3 minutes max)
        print("   Waiting for generation (up to 3 min)...")
        for i in range(90):
            await asyncio.sleep(2)
            status = await evaluate('''
                document.body.innerText.toLowerCase().includes('generating') ? 'generating' : 'done'
            ''')
            if status == 'done':
                print(f"   Generation complete ({(i+1)*2}s)")
                break
            if i % 15 == 0:
                print(f"   Still generating... ({(i+1)*2}s)")
        
        # Step 7: Export
        print("[7/8] Exporting animation...")
        await evaluate('''
            (function() {
                const btns = document.querySelectorAll('button');
                for (const b of btns) {
                    if (b.innerText.includes('Export Pack')) { b.click(); return; }
                }
            })()
        ''')
        await asyncio.sleep(2)
        
        # Select sprite and continue
        await evaluate('''
            (function() {
                const dialog = document.querySelector('[role="dialog"]') || document.body;
                const imgs = dialog.querySelectorAll('img');
                for (const img of imgs) {
                    const rect = img.getBoundingClientRect();
                    if (rect.width > 60 && rect.width < 200 && rect.height > 60) {
                        img.parentElement.click();
                        return;
                    }
                }
            })()
        ''')
        await asyncio.sleep(1)
        
        # Click Continue to Export
        pos3 = await evaluate('''
            (function() {
                const els = document.querySelectorAll('*');
                for (const el of els) {
                    if ((el.innerText || '').trim() === 'Continue to Export') {
                        const rect = el.getBoundingClientRect();
                        return JSON.stringify({x: Math.round(rect.left + rect.width/2), y: Math.round(rect.top + rect.height/2)});
                    }
                }
                return null;
            })()
        ''')
        if pos3:
            coords3 = json.loads(pos3)
            await click_at(coords3['x'], coords3['y'])
        await asyncio.sleep(3)
        
        # Click Export Animation Pack
        pos4 = await evaluate('''
            (function() {
                const btns = document.querySelectorAll('button');
                for (const b of btns) {
                    if (b.innerText.includes('Export Animation Pack')) {
                        const rect = b.getBoundingClientRect();
                        return JSON.stringify({x: Math.round(rect.left + rect.width/2), y: Math.round(rect.top + rect.height/2)});
                    }
                }
                return null;
            })()
        ''')
        if pos4:
            coords4 = json.loads(pos4)
            await click_at(coords4['x'], coords4['y'])
        await asyncio.sleep(5)
        
        # Step 8: Move download
        print("[8/8] Moving download...")
        import subprocess
        result = subprocess.run(
            ['mv', str(Path.home() / 'Downloads' / 'animation-pack-spritesheets.zip'), 
             str(DOWNLOADS_DIR / f'{anim_name}.zip')],
            capture_output=True
        )
        if result.returncode == 0:
            print(f"   Saved: {DOWNLOADS_DIR / f'{anim_name}.zip'}")
            return True
        else:
            print(f"   Warning: Download not found")
            return False

async def main():
    if len(sys.argv) >= 3:
        character, emotion = sys.argv[1], sys.argv[2]
        await process_animation(character, emotion)
    else:
        # Process all remaining animations
        animations = [
            ("bennie", "happy"),
            ("bennie", "thinking"),
            ("bennie", "encouraging"),
            ("bennie", "celebrating"),
            ("bennie", "pointing"),
            ("lemminge", "idle"),
            ("lemminge", "curious"),
            ("lemminge", "excited"),
            ("lemminge", "celebrating"),
            ("lemminge", "hiding"),
            ("lemminge", "mischievous"),
        ]
        
        completed = []
        for char, emo in animations:
            try:
                success = await process_animation(char, emo)
                if success:
                    completed.append(f"{char}_{emo}")
            except Exception as e:
                print(f"[ERROR] {char}_{emo}: {e}")
        
        print(f"\n{'='*60}")
        print(f"Completed: {len(completed)}/{len(animations)}")
        print(f"{'='*60}")

if __name__ == "__main__":
    asyncio.run(main())
