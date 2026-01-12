# Animation Production with Ludo.ai

## Purpose

Transform static character images into animated Lottie files for smooth in-game motion.

## Tool: Ludo.ai

**URL:** https://ludo.ai  
**Mode:** Character Animation  
**Output Format:** Lottie JSON

## Animation Parameters Reference

| Property | Value | Notes |
|----------|-------|-------|
| FPS | 30fps (idle), 60fps (effects) | Standard for smooth animation |
| Easing | Ease In Out | Organic, natural feel |
| Loop | Yes (idle), No (actions) | Based on animation type |
| Duration | 0.5-2.0s | See specific animations below |
| File Size | <100KB per file | Performance target |

---

## Bennie Animations

### 1. bennie_idle.json

**Base Image:** bennie_idle.png  
**Animation Type:** Breathing loop  
**Duration:** 2.0s  
**Loop:** Yes

**Animation Details:**
```
Keyframes:
- 0.0s: Scale 1.0 (normal)
- 1.0s: Scale 1.03 (inhale - subtle expansion)
- 2.0s: Scale 1.0 (exhale - return to normal)

Transform Origin: Center bottom (feet stay planted)
Easing: Ease In Out (smooth breathing)
```

**Ludo.ai Settings:**
- Select "Breathing" preset
- Amplitude: 3% (subtle)
- Speed: 2 seconds per cycle
- Loop: Infinite
- Anchor point: Bottom center

**Success Criteria:**
- Smooth, calming motion
- No jarring movements
- Feet remain stationary
- Gentle expansion/contraction of torso

---

### 2. bennie_waving.json

**Base Image:** bennie_waving.png  
**Animation Type:** Arm wave gesture  
**Duration:** 1.5s  
**Loop:** No (play once)

**Animation Details:**
```
Keyframes:
- 0.0s: Arm at starting position (raised)
- 0.3s: Rotate wrist right 15°
- 0.6s: Rotate wrist left 15°
- 0.9s: Rotate wrist right 15°
- 1.2s: Rotate wrist left 15°
- 1.5s: Return to starting position

Paw rotates back and forth (waving motion)
Body remains stationary
```

**Ludo.ai Settings:**
- Select "Wave" preset
- Focus region: Right arm + paw
- Oscillation count: 3 waves
- Amplitude: 15° rotation
- Easing: Ease Out (friendly, welcoming)

---

### 3. bennie_pointing.json

**Base Image:** bennie_pointing.png  
**Animation Type:** Point emphasis  
**Duration:** 0.5s  
**Loop:** No

**Animation Details:**
```
Keyframes:
- 0.0s: Arm extended (starting pose)
- 0.25s: Arm extends slightly further (emphasis)
- 0.5s: Return to starting pose

Subtle forward motion of pointing arm
Slight body lean in pointing direction
```

**Ludo.ai Settings:**
- Select "Emphasis" preset
- Focus region: Left arm
- Motion: Forward extension
- Distance: 5% of arm length
- Easing: Ease Out

---

### 4. bennie_thinking.json

**Base Image:** bennie_thinking.png  
**Animation Type:** Thoughtful loop  
**Duration:** 2.0s  
**Loop:** Yes

**Animation Details:**
```
Keyframes:
- 0.0s: Head neutral
- 0.5s: Head tilts slightly more up
- 1.0s: Head returns to neutral
- 1.5s: Head tilts slightly down
- 2.0s: Return to neutral

Gentle head bobbing (thinking motion)
Paw on chin remains stationary
```

**Ludo.ai Settings:**
- Select "Head Bob" preset
- Rotation range: ±5° vertical
- Speed: 2 seconds per cycle
- Loop: Infinite
- Body remains still

---

### 5. bennie_encouraging.json

**Base Image:** bennie_encouraging.png  
**Animation Type:** Welcoming gesture  
**Duration:** 1.0s  
**Loop:** No

**Animation Details:**
```
Keyframes:
- 0.0s: Arms slightly forward (starting)
- 0.5s: Arms extend further forward (inviting)
- 1.0s: Return to starting position

Both arms move in sync
Slight forward body lean
Welcoming, open gesture
```

**Ludo.ai Settings:**
- Select "Gesture" preset
- Focus: Both arms
- Motion: Forward extension
- Synchronization: Both arms together
- Easing: Ease In Out

---

### 6. bennie_celebrating.json

**Base Image:** bennie_celebrating.png  
**Animation Type:** Victory jump  
**Duration:** 1.0s  
**Loop:** No

**Animation Details:**
```
Keyframes:
- 0.0s: Crouch position (anticipation)
- 0.3s: Jump peak (highest point, arms up)
- 0.6s: Mid-descent
- 1.0s: Landing (slight squash on impact)

Vertical motion: Jump up and down
Arms remain raised throughout
Slight squash & stretch on landing
```

**Ludo.ai Settings:**
- Select "Jump" preset
- Jump height: 15% of character height
- Hang time: 0.3s at peak
- Landing: Slight squash (1.05x width, 0.95x height)
- Easing: Spring (for natural bounce)

---

## Lemminge Animations

### 1. lemminge_idle.json

**Base Image:** lemminge_idle.png  
**Animation Type:** Gentle sway + blink  
**Duration:** 2.0s  
**Loop:** Yes

**Animation Details:**
```
Sway Motion:
- 0.0s: Centered
- 1.0s: Lean right 3°
- 2.0s: Return to center

Blink:
- Random blinks every 3-4 seconds
- Blink duration: 0.1s
```

**Ludo.ai Settings:**
- Select "Idle" preset
- Sway amplitude: 3° rotation
- Sway speed: 2s per cycle
- Add random blink: Yes
- Blink frequency: Every 3-4s

---

### 2. lemminge_curious.json

**Base Image:** lemminge_curious.png  
**Animation Type:** Head tilt loop  
**Duration:** 1.5s  
**Loop:** Yes

**Animation Details:**
```
Keyframes:
- 0.0s: Head tilted left (starting pose)
- 0.75s: Head tilts further left (curious)
- 1.5s: Return to starting tilt

Ears perk up
Eyes widen slightly
Inquisitive motion
```

**Ludo.ai Settings:**
- Select "Curiosity" preset
- Focus: Head + ears
- Tilt range: ±8° from starting position
- Ear perk: Slight upward motion
- Easing: Ease In Out

---

### 3. lemminge_excited.json

**Base Image:** lemminge_excited.png  
**Animation Type:** Bounce loop  
**Duration:** 0.8s  
**Loop:** Yes

**Animation Details:**
```
Keyframes:
- 0.0s: Normal position
- 0.4s: Bounce up (slight jump)
- 0.8s: Return to normal

Fast, energetic bouncing
Body compresses slightly on landing
Continuous motion (high energy)
```

**Ludo.ai Settings:**
- Select "Bounce" preset
- Bounce height: 8% of body height
- Speed: Fast (0.8s per bounce)
- Compression: 5% squash on landing
- Loop: Infinite
- Easing: Ease In Out

---

### 4. lemminge_celebrating.json

**Base Image:** lemminge_celebrating.png  
**Animation Type:** Victory jump  
**Duration:** 1.0s  
**Loop:** No

**Animation Details:**
```
Keyframes:
- 0.0s: Crouch (anticipation)
- 0.4s: Jump peak (arms raised, eyes closed)
- 0.7s: Mid-descent
- 1.0s: Landing (slight squash)

Similar to Bennie's jump but faster
More energetic, playful
Eyes closed in joy throughout
```

**Ludo.ai Settings:**
- Select "Jump" preset
- Jump height: 20% of body height (higher than Bennie)
- Speed: Fast (1.0s total)
- Squash on landing: Yes
- Easing: Spring

---

### 5. lemminge_hiding.json

**Base Image:** lemminge_hiding.png  
**Animation Type:** Peek in/out loop  
**Duration:** 2.0s  
**Loop:** Yes

**Animation Details:**
```
Keyframes:
- 0.0s: Peeking out (visible)
- 0.5s: Hide (slide left, mostly hidden)
- 1.5s: Stay hidden
- 2.0s: Peek out again

Horizontal sliding motion
Eyes peek from edge
Playful hide-and-seek motion
```

**Ludo.ai Settings:**
- Select "Slide" preset
- Motion: Horizontal (left/right)
- Distance: 30% of body width
- Timing: 0.5s hide, 1.0s wait, 0.5s reveal
- Loop: Infinite

---

### 6. lemminge_mischievous.json

**Base Image:** lemminge_mischievous.png  
**Animation Type:** Scheming loop  
**Duration:** 1.5s  
**Loop:** Yes

**Animation Details:**
```
Keyframes:
- 0.0s: Normal scheming pose
- 0.75s: Lean forward slightly (plotting)
- 1.5s: Return to starting pose

Paws rub together slightly
Body rocks forward/back
Sly, playful motion
```

**Ludo.ai Settings:**
- Select "Rock" preset
- Motion: Forward/backward lean
- Amplitude: 5° rotation
- Add paw gesture: Subtle rubbing motion
- Easing: Ease In Out

---

## Effect Animations (Non-Character)

### confetti.json

**Animation Type:** Particle explosion  
**Duration:** 3.0s  
**Loop:** No  
**FPS:** 60fps

**Details:**
```
Multicolor particles (woodland colors):
- Green (#738F66)
- Gold (#D9C27A)
- Sky blue (#B3D1E6)
- Cream (#FAF5EB)

Explosion from center
Particles fall with gravity
Fade out at end
```

**Generation:** Use After Effects or Lottie template

---

### coin_fly.json

**Animation Type:** Coin arc motion  
**Duration:** 0.8s  
**Loop:** No  
**FPS:** 60fps

**Details:**
```
Path: Arc from activity center to progress bar
Rotation: 3 full rotations during flight
Scale: Grows 1.0 → 1.2 → 1.0
Sparkle trail: Optional gold particles

End position: Progress bar location
```

---

### progress_fill.json

**Animation Type:** Fill progress bar  
**Duration:** 0.5s  
**Loop:** No  
**FPS:** 30fps

**Details:**
```
Green fill (#99BF8C) grows left to right
Sparkle effect at fill edge
Smooth easing
Ends with subtle glow pulse
```

---

## Production Workflow

### Step-by-Step Process

```
1. Upload Base Image
   - Drag PNG to Ludo.ai
   - Confirm transparent background detected

2. Select Animation Type
   - Choose preset from library
   - Or create custom keyframes

3. Configure Parameters
   - Set duration, loop, FPS
   - Define animation region (which parts move)
   - Set easing curves

4. Preview Animation
   - Play in Ludo.ai preview
   - Check for smoothness
   - Verify no artifacts

5. Export Lottie
   - Download as .json
   - Verify file size <100KB

6. Test in App
   - Import to Xcode
   - Test with LottieView
   - Verify performance (60fps)

7. Finalize
   - Rename: {character}_{state}.json
   - Move to Resources/Lottie/
   - Update asset catalog
```

---

## Quality Assurance

### Animation Checklist

```
✓ Smooth motion (no jitter)
✓ Correct duration
✓ Proper loop setting
✓ File size <100KB
✓ 30fps (idle) or 60fps (effects)
✓ Transparent background preserved
✓ No unwanted artifacts
✓ Easing feels natural
✓ Matches design intent
✓ Tested in app at 60fps
```

### Performance Testing

```swift
// Test animation performance
struct AnimationPerformanceTest {
    func testLottiePerformance(animation: String) {
        let view = LottieAnimationView(name: animation)
        view.frame = CGRect(x: 0, y: 0, width: 300, height: 450)
        view.loopMode = .loop
        view.play()
        
        // Monitor FPS
        let displayLink = CADisplayLink(target: self, selector: #selector(checkFPS))
        displayLink.add(to: .main, forMode: .common)
        
        // Should maintain 60fps for 10 seconds
        DispatchQueue.main.asyncAfter(deadline: .now() + 10) {
            assert(self.averageFPS > 58, "Animation drops below 60fps")
        }
    }
}
```

---

## Delivery Format

```
Resources/
└── Lottie/
    ├── bennie_idle.json
    ├── bennie_waving.json
    ├── bennie_pointing.json
    ├── bennie_thinking.json
    ├── bennie_encouraging.json
    ├── bennie_celebrating.json
    ├── lemminge_idle.json
    ├── lemminge_curious.json
    ├── lemminge_excited.json
    ├── lemminge_celebrating.json
    ├── lemminge_hiding.json
    ├── lemminge_mischievous.json
    ├── confetti.json
    ├── coin_fly.json
    └── progress_fill.json
```

**Total:** 15 Lottie animation files

---

## Integration Code

```swift
import Lottie

struct BennieView: View {
    @State private var expression: BennieExpression = .idle
    
    var body: some View {
        LottieView(animation: .named("bennie_\(expression.rawValue)"))
            .playing(loopMode: expression.loopMode)
            .frame(width: 300, height: 450)
    }
}

enum BennieExpression: String {
    case idle, waving, pointing, thinking, encouraging, celebrating
    
    var loopMode: LottieLoopMode {
        switch self {
        case .idle, .thinking:
            return .loop
        case .waving, .pointing, .encouraging, .celebrating:
            return .playOnce
        }
    }
}
```

---

## Troubleshooting

### Common Issues

**Issue:** Animation jitters  
**Solution:** Reduce keyframe count, simplify motion

**Issue:** File size >100KB  
**Solution:** Reduce FPS, simplify paths, remove unnecessary layers

**Issue:** Transparent background lost  
**Solution:** Re-export base image as PNG with alpha channel

**Issue:** Loop not smooth  
**Solution:** Ensure first and last keyframes match exactly

**Issue:** Performance drops  
**Solution:** Reduce number of animated layers, lower FPS to 30
