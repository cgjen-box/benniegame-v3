# Stage 3: Asset Optimization

## Purpose
Optimize all game assets (images, animations, audio) to reduce app size and improve load times.

## Duration
2 days

## Playbook References
- **Part 5.2**: Asset Specifications
- **Part 5.3**: Audio Specifications
- **Part 9.2**: Gemini Image Generation
- **Part 9.3**: Lottie Animation Pipeline
- **Part 9.4**: ElevenLabs Voice Generation
- **Part 9.7**: Asset Export Specifications

## Asset Audit

### Current Asset Inventory

#### Images (from `design/references/`)
```
Characters:
├── bennie/ (6 poses × 2 resolutions = 12 files)
│   ├── bennie_idle@2x.png, @3x.png
│   ├── bennie_waving@2x.png, @3x.png
│   ├── bennie_pointing@2x.png, @3x.png
│   ├── bennie_thinking@2x.png, @3x.png
│   ├── bennie_encouraging@2x.png, @3x.png
│   └── bennie_celebrating@2x.png, @3x.png
│
└── lemminge/ (6 expressions × 2 resolutions = 12 files)
    ├── lemminge_idle@2x.png, @3x.png
    ├── lemminge_curious@2x.png, @3x.png
    ├── lemminge_excited@2x.png, @3x.png
    ├── lemminge_celebrating@2x.png, @3x.png
    ├── lemminge_hiding@2x.png, @3x.png
    └── lemminge_mischievous@2x.png, @3x.png

Screens: (8 backgrounds × 2 resolutions = 16 files)
├── Reference_Loading_Screen.png
├── Reference_Player_Selection_Screen.png
├── Reference_Menu_Screen.png
├── Reference_Matching_Game_Screen.png
├── Reference_Layrinth_Game_Screen.png
├── Reference_Numbers_Game_Screen.png
├── Reference_Treasure_Screen.png
└── Reference_Celebration_Overlay.png

Components: (UI elements)
├── wood_button@2x.png, @3x.png
├── wood_sign@2x.png, @3x.png
├── progress_bar@2x.png, @3x.png
├── chest_closed@2x.png, @3x.png
└── chest_open@2x.png, @3x.png
```

#### Animations
```
Lottie/
├── bennie_idle.json
├── bennie_waving.json
├── bennie_celebrating.json
├── lemminge_idle.json
├── lemminge_celebrating.json
├── confetti.json
├── coin_fly.json
└── progress_fill.json
```

#### Audio
```
Audio/
├── Narrator/ (50+ files @ ~30KB each = ~1.5MB)
├── Bennie/ (40+ files @ ~30KB each = ~1.2MB)
├── Music/ (1 loop @ ~500KB)
└── Effects/ (10 files @ ~10KB each = ~100KB)
Total: ~3.3MB
```

## Image Optimization

### Strategy 1: Format Optimization

#### PNG Compression
```bash
# Use ImageOptim or pngquant for lossless compression
# Target: 30-50% size reduction

# Automated script:
#!/bin/bash
for file in *.png; do
    pngquant --quality=85-95 --output "$file" --force "$file"
done

# Expected results:
# Before: ~25MB total images
# After: ~15MB total images (40% reduction)
```

#### Selective WebP Conversion
```swift
// For non-transparent backgrounds, consider WebP
// Better compression than PNG, native iOS 14+ support

// Convert in Xcode Asset Catalog:
// 1. Select asset
// 2. Attributes Inspector
// 3. Compression: Lossy/Lossless

// Result:
// Background images: PNG → WebP = ~50% reduction
```

**Reference**: Apply to all images in `design/references/screens/`

### Strategy 2: Resolution Optimization

#### @3x Asset Necessity
```
ANALYSIS:
- iPad displays use @2x
- @3x only needed for iPhone
- Since we're iPad-only, we can remove @3x

SAVINGS:
- Remove all @3x assets
- Reduce image bundle by ~40%

IMPLEMENTATION:
1. Delete all @3x assets from xcassets
2. Update Asset Catalog to only include @2x
3. Test on iPad Pro (highest DPI)
```

#### Downsampling Large Backgrounds
```swift
// For full-screen backgrounds, no need for > screen resolution
// iPad resolution: 1194×834 pt @ 2x = 2388×1668 px

// Current: 3582×2502 (@3x)
// Optimal: 2388×1668 (@2x)
// Savings: ~55% per background image
```

### Strategy 3: Sprite Atlas Optimization

#### Create Sprite Atlases
```
// Group related sprites into atlases for better GPU performance
// Xcode: New File → Sprite Atlas

Atlases to create:
1. BennieAtlas - All Bennie poses
2. LemmingeAtlas - All Lemminge expressions  
3. UIComponentsAtlas - Buttons, signs, UI elements

Benefits:
- Faster rendering (single texture)
- Better memory usage
- Automatic optimization by Xcode
```

## Lottie Animation Optimization

### Strategy 1: JSON Minification

#### Remove Unnecessary Data
```bash
# Use lottie-optimizer
npm install -g lottie-optimizer

# Process all animations:
for file in *.json; do
    lottie-optimizer "$file" "optimized_$file"
done

# Remove:
- Unused layers
- Hidden layers
- Excessive keyframes
- Redundant easing curves

# Target: < 100KB per file (from Part 9.7)
```

### Strategy 2: Simplify Animation Complexity

#### Confetti Animation
```
BEFORE:
- 200 particles
- 60fps
- Complex physics
- File size: 150KB

AFTER:
- 100 particles
- 30fps (sufficient for effect)
- Simplified physics
- File size: 75KB (50% reduction)

QUALITY: No visible difference on iPad display
```

#### Character Animations
```
OPTIMIZATION TARGETS:
1. bennie_idle.json
   - Reduce breathing keyframes: 30 → 15
   - Simplify paths
   - Target: < 50KB

2. lemminge_celebrating.json
   - Reduce bounce complexity
   - Fewer motion blur keyframes
   - Target: < 40KB

3. coin_fly.json
   - Simplify arc path
   - Reduce sparkle particles
   - Target: < 30KB
```

**Reference**: Part 9.3 for Lottie pipeline

### Strategy 3: Animation Preloading

#### Smart Preloading Strategy
```swift
class AnimationPreloader {
    // Preload animations for next likely screen
    func preloadForScreen(_ screen: Screen) async {
        switch screen {
        case .home:
            await preload(["bennie_pointing", "lemminge_hiding"])
        case .puzzle:
            await preload(["bennie_thinking", "lemminge_curious"])
        case .celebration:
            await preload(["bennie_celebrating", "lemminge_celebrating", "confetti"])
        // etc...
        }
    }
    
    private func preload(_ animations: [String]) async {
        // Load in background while user is engaged
    }
}
```

## Audio Optimization

### Strategy 1: Format Optimization

#### AAC Encoding Settings
```bash
# Current settings (from Part 5.3):
- Sample Rate: 44.1kHz
- Bitrate: 128kbps (voice), 192kbps (music)
- Format: AAC

# Optimization opportunity:
- Reduce voice to 96kbps (still high quality for speech)
- Reduce music to 160kbps (sufficient for background)

# Process all files:
for file in *.aac; do
    ffmpeg -i "$file" -c:a aac -b:a 96k "optimized_$file"
done

# Expected savings:
# Voice files: 128kbps → 96kbps = 25% reduction
# Music: 192kbps → 160kbps = 17% reduction
# Total: ~0.8MB saved
```

**Reference**: Part 5.3 for audio specifications, Part 9.4 for voice generation

### Strategy 2: Audio File Consolidation

#### Combine Short Sound Effects
```swift
// Instead of multiple tiny files, use audio sprites
// Benefits:
- Fewer files to manage
- Faster loading
- Better caching

// Implementation:
class AudioSprite {
    let sprite: AVAudioPlayer
    let regions: [String: (start: TimeInterval, duration: TimeInterval)]
    
    func play(region: String) {
        guard let (start, duration) = regions[region] else { return }
        sprite.currentTime = start
        sprite.play()
        
        DispatchQueue.main.asyncAfter(deadline: .now() + duration) {
            self.sprite.stop()
        }
    }
}
```

### Strategy 3: Remove Unused Audio

#### Audit Audio Usage
```
Check all audio files against:
1. Part 3.4 - Complete Script Reference
2. Actual voice triggers in code

Remove any orphaned files:
- Unused narrator lines
- Unused Bennie responses
- Unused sound effects

Expected: Find 5-10 unused files = ~200KB savings
```

## Asset Loading Optimization

### Strategy 1: Asset Bundle Organization

#### Group by Screen
```
Assets.xcassets/
├── Loading/
│   ├── LoadingBackground
│   ├── BennieIdle
│   └── LemmingeHiding
├── Home/
│   ├── HomeBackground
│   ├── ActivitySigns
│   └── Chest
├── Puzzle/
│   ├── PuzzleBackground
│   ├── GridElements
│   └── ColorPicker
└── Shared/
    ├── BennieCommon
    ├── LemmingeCommon
    └── UIComponents
```

### Strategy 2: On-Demand Resources (ODR)

#### Consider ODR for Large Assets
```swift
// For assets > 20MB, use on-demand resources
// Benefits:
- Smaller initial download
- Assets downloaded as needed
- iOS manages caching

// Tag assets in Xcode:
// 1. Select asset group
// 2. Set "On Demand Resource Tags"
// 3. Tag: "puzzle_assets", "video_assets", etc.
```

## Testing Protocol

### Asset Performance Tests

#### Test 1: Load Time Benchmark
```
BEFORE OPTIMIZATION:
- Cold app launch: _____ ms
- Screen transition: _____ ms
- Animation load: _____ ms

AFTER OPTIMIZATION:
- Cold app launch: _____ ms (target: < 2000ms)
- Screen transition: _____ ms (target: < 300ms)  
- Animation load: _____ ms (target: < 100ms)
```

#### Test 2: Quality Verification
```
For each optimized asset:
☐ Visual quality acceptable on iPad
☐ No compression artifacts visible
☐ Animations play smoothly
☐ Audio quality remains clear

Review on actual device, not simulator!
```

#### Test 3: App Size Check
```
BEFORE OPTIMIZATION:
App size: _____ MB

AFTER OPTIMIZATION:
App size: _____ MB

TARGET: < 150MB (from Part 5.6)
SAVINGS: _____ MB (____%)
```

## Automation Script

### Asset Optimization Pipeline
**File**: `scripts/optimize_assets.sh`

```bash
#!/bin/bash

echo "🎨 Bennie Asset Optimization Pipeline"
echo "======================================"

# 1. Optimize PNGs
echo "📸 Optimizing PNG images..."
find design/references -name "*.png" -exec pngquant --quality=85-95 --output {} --force {} \;

# 2. Optimize Lottie animations
echo "🎬 Optimizing Lottie animations..."
for file in Resources/Lottie/*.json; do
    lottie-optimizer "$file" "$file.tmp"
    mv "$file.tmp" "$file"
done

# 3. Optimize audio files
echo "🔊 Optimizing audio files..."
for file in Resources/Audio/**/*.aac; do
    ffmpeg -i "$file" -c:a aac -b:a 96k "$file.tmp" -y
    mv "$file.tmp" "$file"
done

# 4. Clean up unused assets
echo "🧹 Cleaning unused assets..."
# (Add logic to check asset usage)

# 5. Generate report
echo "📊 Generating optimization report..."
# (Add size comparison logic)

echo "✅ Asset optimization complete!"
```

## Deliverables

### 1. Optimized Asset Catalog
**Location**: `Resources/Assets.xcassets/`
- All images optimized
- Proper organization
- Sprite atlases created

### 2. Optimized Animations
**Location**: `Resources/Lottie/`
- All JSON files < 100KB
- Quality verified
- Load tested

### 3. Optimized Audio
**Location**: `Resources/Audio/`
- All files optimized
- Quality verified
- Unused files removed

### 4. Optimization Report
**File**: `14_performance/asset_optimization_report.md`
- Size reductions achieved
- Quality verification results
- Load time improvements

### 5. Automation Scripts
**Location**: `scripts/`
- `optimize_assets.sh` - Main optimization script
- `verify_asset_quality.sh` - Quality check script
- `measure_asset_performance.sh` - Performance benchmark

## Success Criteria

### Stage Complete When:
- ✅ All images optimized (30-50% reduction)
- ✅ All animations < 100KB
- ✅ All audio optimized (20-30% reduction)
- ✅ App size < 150MB
- ✅ No quality degradation visible
- ✅ Load times improved
- ✅ Automation scripts functional

## Next Stage Preview
**Stage 4: Animation Performance**
- Will ensure 60fps during all animations
- Optimize animation rendering
- Fix any frame drops
