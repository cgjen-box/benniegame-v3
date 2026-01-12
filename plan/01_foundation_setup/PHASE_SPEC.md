# Phase 1: Foundation & Setup

**Duration**: 4-6 hours  
**Status**: Not Started  
**Dependencies**: None (first phase)

**Playbook References:**
- **File Structure**: `/mnt/project/FULL_ARCHIVE.md` → Part 8: File Structure
- **Technical Requirements**: `/mnt/project/FULL_ARCHIVE.md` → Part 5: Technical Requirements
- **Color System**: `/mnt/project/FULL_ARCHIVE.md` → Part 1.3: Color System
- **Typography**: `/mnt/project/FULL_ARCHIVE.md` → Part 1.4: Typography

## Overview

Establish project structure, configure Xcode, and set up fundamental architecture for the Bennie iPad app following the exact specifications from the playbook.

**CRITICAL**: Playbook is the gold standard. All implementation must match playbook specifications exactly.

## Deliverables

- ✅ Xcode project configured for iPadOS 17+ (Playbook Part 5.1)
- ✅ File structure per playbook Part 8 (exact hierarchy)
- ✅ Git repository initialized with proper .gitignore
- ✅ Asset catalogs organized per playbook Part 5.2
- ✅ Dependencies installed (Lottie, YouTube player per Part 5.3)
- ✅ Project documentation in place

## Exit Criteria

- [ ] App launches without crashes
- [ ] Landscape-only orientation locked (playbook requirement)
- [ ] iPad target (10th gen, Air, Pro) configured per Part 5.1
- [ ] All dependencies resolve correctly
- [ ] Asset catalog structure EXACTLY matches playbook Part 8
- [ ] Colors.swift matches playbook Part 1.3 (all hex values)
- [ ] Typography.swift matches playbook Part 1.4
- [ ] Git history has clean initial commit

---

## Tasks

### 1.0 Initialize Git Repository
**Estimated**: 15 minutes  
**Playbook Reference**: General best practices

**Steps:**
- [ ] Create new directory for project
- [ ] Run `git init`
- [ ] Create .gitignore for Swift/Xcode
- [ ] Add common ignore patterns (DerivedData, xcuserdata)
- [ ] Initial commit with README

**Files Created:**
- `.git/`
- `.gitignore`
- `README.md`

**Validation:**
```bash
git status  # Should show clean working directory
git log     # Should show initial commit
```

---

### 1.1 Create Xcode Project
**Estimated**: 20 minutes  
**Playbook Reference**: `/mnt/project/FULL_ARCHIVE.md` → Part 5.1: Platform & Device

**Steps:**
- [ ] Create new Xcode project
- [ ] Template: iOS App
- [ ] Interface: SwiftUI
- [ ] Target: iPadOS 17.0+ (playbook requirement)
- [ ] Language: Swift
- [ ] Project name: "BennieGame"

**Configuration (MUST MATCH PLAYBOOK):**
- [ ] Set deployment target to iPadOS 17.0
- [ ] Lock orientation to **Landscape ONLY** (playbook Part 5.1)
- [ ] Configure supported devices: iPad only
- [ ] Screen resolution: 1194×834 points (playbook Part 5.1)
- [ ] Add Info.plist key: `UIRequiresFullScreen = true`
- [ ] Add Info.plist key: `UISupportedInterfaceOrientations` = Landscape Left & Right only
- [ ] Bundle ID: `com.bennie.game`

**Files Created:**
- `BennieGame.xcodeproj`
- `BennieGameApp.swift`
- `ContentView.swift` (temporary)
- `Info.plist`

**Validation:**
- [ ] Build project (Cmd+B) - no errors
- [ ] Run on iPad simulator
- [ ] Verify landscape-only orientation (rotate device, should stay landscape)
- [ ] Check resolution: 1194×834 points

---

### 1.2 Create File Structure
**Estimated**: 30 minutes  
**Playbook Reference**: `/mnt/project/FULL_ARCHIVE.md` → Part 8: File Structure (EXACT HIERARCHY)

**CRITICAL**: Structure MUST exactly match playbook Part 8. No deviations.

**Steps:**
- [ ] Create folder hierarchy per playbook Part 8
- [ ] Set up groups in Xcode
- [ ] Add placeholder files where needed

**Directory Structure (FROM PLAYBOOK PART 8):**
```
BennieGame/
├── App/
│   ├── BennieGameApp.swift
│   └── AppCoordinator.swift
├── Features/
│   ├── Loading/
│   │   └── LoadingView.swift
│   ├── PlayerSelection/
│   │   └── PlayerSelectionView.swift
│   ├── Home/
│   │   └── HomeView.swift
│   ├── Activities/
│   │   ├── Raetsel/
│   │   │   ├── RaetselSelectionView.swift
│   │   │   ├── PuzzleMatchingView.swift
│   │   │   └── LabyrinthView.swift
│   │   └── Zahlen/
│   │       ├── ZahlenSelectionView.swift
│   │       ├── WuerfelView.swift
│   │       └── WaehleZahlView.swift
│   ├── Celebration/
│   │   └── CelebrationOverlay.swift
│   ├── Treasure/
│   │   └── TreasureView.swift
│   ├── Video/
│   │   ├── VideoSelectionView.swift
│   │   └── VideoPlayerView.swift
│   └── Parent/
│       ├── ParentGateView.swift
│       ├── ParentDashboardView.swift
│       └── VideoManagementView.swift
├── Design/
│   ├── Components/
│   │   ├── WoodButton.swift
│   │   ├── WoodSign.swift
│   │   ├── ProgressBar.swift
│   │   ├── NavigationHeader.swift
│   │   ├── StoneTablet.swift
│   │   └── AnalogClock.swift
│   ├── Theme/
│   │   ├── Colors.swift
│   │   └── Typography.swift
│   └── Characters/
│       ├── BennieView.swift
│       ├── LemmingeView.swift
│       └── SpeechBubbleView.swift
├── Services/
│   ├── AudioManager.swift
│   ├── NarratorService.swift
│   ├── GameStateManager.swift
│   ├── PlayerDataStore.swift
│   ├── YouTubeService.swift
│   └── NetworkMonitor.swift
└── Resources/
    ├── Assets.xcassets/
    ├── Lottie/
    └── Audio/
```

**Validation:**
- [ ] All folders visible in Xcode navigator
- [ ] Structure EXACTLY matches playbook Part 8
- [ ] No build errors from empty folders
- [ ] Placeholder files compile

---

### 1.3 Configure Asset Catalogs
**Estimated**: 20 minutes  
**Playbook Reference**: `/mnt/project/FULL_ARCHIVE.md` → Part 5.2: Asset Specifications

**Steps:**
- [ ] Set up Assets.xcassets structure per playbook Part 8
- [ ] Create image sets for characters (playbook Part 5.2)
- [ ] Configure for @2x and @3x (playbook requirement)
- [ ] Set up color assets (playbook Part 1.3)

**Asset Structure (FROM PLAYBOOK PART 8):**
```
Assets.xcassets/
├── Characters/
│   ├── Bennie/
│   │   ├── bennie_idle.imageset/
│   │   ├── bennie_waving.imageset/
│   │   ├── bennie_pointing.imageset/
│   │   ├── bennie_thinking.imageset/
│   │   ├── bennie_encouraging.imageset/
│   │   └── bennie_celebrating.imageset/
│   └── Lemminge/
│       ├── lemminge_idle.imageset/
│       ├── lemminge_curious.imageset/
│       ├── lemminge_excited.imageset/
│       ├── lemminge_celebrating.imageset/
│       ├── lemminge_hiding.imageset/
│       └── lemminge_mischievous.imageset/
├── Backgrounds/
│   └── forest_background.imageset/
├── UI/
│   ├── wood_button.imageset/
│   └── wood_sign.imageset/
└── Colors/
    ├── Woodland.colorset/          (#738F66)
    ├── Bark.colorset/               (#8C7259)
    ├── Sky.colorset/                (#B3D1E6)
    ├── Cream.colorset/              (#FAF5EB)
    ├── BennieBrown.colorset/        (#8C7259)
    ├── BennieTan.colorset/          (#C4A574)
    ├── LemmingeBlue.colorset/       (#6FA8DC - CRITICAL!)
    ├── Success.colorset/            (#99BF8C)
    ├── CoinGold.colorset/           (#D9C27A)
    ├── WoodLight.colorset/          (#C4A574)
    ├── WoodMedium.colorset/         (#A67C52)
    └── WoodDark.colorset/           (#6B4423)
```

**Validation:**
- [ ] Asset catalog builds without warnings
- [ ] Color assets appear in Interface Builder
- [ ] All hex values EXACTLY match playbook Part 1.3
- [ ] Structure EXACTLY matches playbook Part 8

---

### 1.4 Install Lottie Dependency
**Estimated**: 15 minutes  
**Playbook Reference**: `/mnt/project/FULL_ARCHIVE.md` → Part 5.3: Dependencies

**Steps:**
- [ ] Add Lottie-iOS via SPM
- [ ] Package URL: `https://github.com/airbnb/lottie-ios`
- [ ] Version: Latest compatible with iOS 17
- [ ] Add to target
- [ ] Verify import works

**Validation:**
```swift
import Lottie
// Should compile without errors
```

---

### 1.5 Plan YouTube Player Implementation
**Estimated**: 30 minutes  
**Playbook Reference**: `/mnt/project/FULL_ARCHIVE.md` → Part 4.9 & 4.10: Video Player specs

**CRITICAL REQUIREMENT**: Controlled YouTube playback (playbook Part 4.10)
- NO YouTube app access
- NO browsing/search
- Only pre-approved videos
- Custom controls only

**Steps:**
- [ ] Research: YouTubeiOSPlayerHelper vs custom WKWebView
- [ ] Decision: Use custom WKWebView approach (more control per playbook)
- [ ] Create YouTubeService stub with playbook parameters
- [ ] Document embed parameters from playbook Part 4.10

**Playbook Parameters (MUST USE THESE):**
```swift
let playerVars = [
    "controls": 0,           // Hide YouTube controls
    "rel": 0,                // No related videos
    "showinfo": 0,           // No video info
    "modestbranding": 1,     // Minimal YouTube branding
    "iv_load_policy": 3,     // No annotations
    "fs": 0,                 // No fullscreen button
    "disablekb": 1,          // Disable keyboard controls
    "playsinline": 1         // Play inline
]
```

**Files Created:**
- `Services/YouTubeService.swift`
- `Video/YouTubePlayerView.swift`

**Validation:**
- [ ] Stubs compile
- [ ] Can instantiate YouTubePlayerView
- [ ] Parameters match playbook exactly

---

### 1.6 Create Colors.swift
**Estimated**: 20 minutes  
**Playbook Reference**: `/mnt/project/FULL_ARCHIVE.md` → Part 1.3: Color System (GOLD STANDARD)

**CRITICAL**: All hex values MUST EXACTLY match playbook Part 1.3. No approximations.

**Steps:**
- [ ] Create Design/Theme/Colors.swift
- [ ] Define ALL colors from playbook Part 1.3
- [ ] Use exact hex values
- [ ] Include usage comments from playbook

**Implementation (ALL VALUES FROM PLAYBOOK PART 1.3):**
```swift
import SwiftUI

// PLAYBOOK REFERENCE: Part 1.3 - Color System
// CRITICAL: These hex values are NON-NEGOTIABLE
// Source: /mnt/project/FULL_ARCHIVE.md → Part 1.3

extension Color {
    // MARK: - Primary Palette (Playbook Part 1.3)
    static let woodland = Color(hex: "738F66")    // Primary buttons, safe areas
    static let bark = Color(hex: "8C7259")        // Bennie fur, wood elements
    static let sky = Color(hex: "B3D1E6")         // Sky areas, calm accents
    static let cream = Color(hex: "FAF5EB")       // Backgrounds, safe space
    
    // MARK: - Character Colors (Playbook Part 1.3)
    // ⚠️ CRITICAL: Bennie MUST be brown, NO clothing
    static let bennieBrown = Color(hex: "8C7259")  // Main fur - EXACT hex required
    static let bennieTan = Color(hex: "C4A574")    // Snout ONLY - no belly patch
    static let bennieNose = Color(hex: "3D2B1F")   // Dark espresso triangle
    
    // ⚠️ CRITICAL: Lemminge MUST be BLUE #6FA8DC - NEVER green, NEVER brown
    static let lemmingeBlue = Color(hex: "6FA8DC")   // Body - NON-NEGOTIABLE
    static let lemmingePink = Color(hex: "E8A0A0")   // Nose and paws
    static let lemmingeBelly = Color(hex: "FAF5EB")  // Cream belly
    
    // MARK: - UI Colors (Playbook Part 1.3)
    static let success = Color(hex: "99BF8C")      // Positive feedback, progress
    static let coinGold = Color(hex: "D9C27A")     // Rewards, treasure, coins
    
    // MARK: - Wood UI Colors (Playbook Part 1.3)
    static let woodLight = Color(hex: "C4A574")    // Highlights, top edges
    static let woodMedium = Color(hex: "A67C52")   // Main plank color
    static let woodDark = Color(hex: "6B4423")     // Shadows, grain lines
    static let rope = Color(hex: "B8956B")         // Sign mounting ropes
    static let chain = Color(hex: "6B6B6B")        // Lock chains
    
    // MARK: - Forest Environment (Playbook Part 1.3)
    static let farTrees = Color(hex: "4A6B5C")     // Distant misty background
    static let midTrees = Color(hex: "738F66")     // Main canopy
    static let nearFoliage = Color(hex: "7A9973")  // Foreground bushes
    static let moss = Color(hex: "5D6B4D")         // Ground covering
    static let pathStone = Color(hex: "A8A090")    // Labyrinth paths
    
    // MARK: - Hex Initializer
    init(hex: String) {
        let hex = hex.trimmingCharacters(in: CharacterSet.alphanumerics.inverted)
        var int: UInt64 = 0
        Scanner(string: hex).scanHexInt64(&int)
        let a, r, g, b: UInt64
        switch hex.count {
        case 3: // RGB (12-bit)
            (a, r, g, b) = (255, (int >> 8) * 17, (int >> 4 & 0xF) * 17, (int & 0xF) * 17)
        case 6: // RGB (24-bit)
            (a, r, g, b) = (255, int >> 16, int >> 8 & 0xFF, int & 0xFF)
        case 8: // ARGB (32-bit)
            (a, r, g, b) = (int >> 24, int >> 16 & 0xFF, int >> 8 & 0xFF, int & 0xFF)
        default:
            (a, r, g, b) = (255, 0, 0, 0)
        }
        self.init(
            .sRGB,
            red: Double(r) / 255,
            green: Double(g) / 255,
            blue: Double(b) / 255,
            opacity: Double(a) / 255
        )
    }
}

// MARK: - Forbidden Colors (Playbook Part 1.3)
// ⚠️ NEVER USE THESE:
// - Pure Red #FF0000 (triggers anxiety)
// - Pure White #FFFFFF (too harsh for large areas)
// - Pure Black #000000 (too harsh for large areas)
// - Any neon colors (overstimulating)
// - Saturation > 80% (overstimulating)
```

**Validation:**
- [ ] All hex values EXACTLY match playbook Part 1.3
- [ ] Preview colors visually
- [ ] Verify bennieBrown is #8C7259 (not too dark, not too light)
- [ ] Verify lemmingeBlue is #6FA8DC (BLUE, not green)
- [ ] Comments include playbook references

**Test:**
```swift
struct ColorTest: View {
    var body: some View {
        VStack {
            Rectangle().fill(Color.bennieBrown)
                .frame(height: 50)
            Rectangle().fill(Color.lemmingeBlue)
                .frame(height: 50)
            Rectangle().fill(Color.woodland)
                .frame(height: 50)
        }
    }
}
```

---

### 1.7 Create Typography.swift
**Estimated**: 15 minutes  
**Playbook Reference**: `/mnt/project/FULL_ARCHIVE.md` → Part 1.4: Typography

**Steps:**
- [ ] Create Design/Theme/Typography.swift
- [ ] Define font system using SF Rounded (playbook Part 1.4)
- [ ] Match all size/weight presets from playbook

**Implementation (FROM PLAYBOOK PART 1.4):**
```swift
import SwiftUI

// PLAYBOOK REFERENCE: Part 1.4 - Typography
// Source: /mnt/project/FULL_ARCHIVE.md → Part 1.4

extension Font {
    // MARK: - SF Rounded Helper
    static func sfRounded(size: CGFloat, weight: Font.Weight = .regular) -> Font {
        return .system(size: size, weight: weight, design: .rounded)
    }
    
    // MARK: - Preset Styles (Playbook Part 1.4)
    
    // Titles: 32-48pt, Bold (Screen headers)
    static let bennieTitle = sfRounded(size: 48, weight: .bold)
    static let bennieHeading = sfRounded(size: 32, weight: .bold)
    
    // Body: 17-24pt, Regular (Descriptions)
    static let bennieBody = sfRounded(size: 20, weight: .regular)
    static let bennieBodyLarge = sfRounded(size: 24, weight: .regular)
    
    // Buttons: 20-28pt, Semibold (All buttons)
    static let bennieButton = sfRounded(size: 24, weight: .semibold)
    static let bennieButtonSmall = sfRounded(size: 20, weight: .semibold)
    
    // Labels: 14-17pt, Medium (Small UI text)
    static let bennieCaption = sfRounded(size: 17, weight: .medium)
    static let bennieLabel = sfRounded(size: 14, weight: .medium)
    
    // Numbers: 40-72pt, Bold (Game numbers)
    static let bennieNumberLarge = sfRounded(size: 72, weight: .bold)
    static let bennieNumber = sfRounded(size: 60, weight: .bold)
    static let bennieNumberMedium = sfRounded(size: 40, weight: .bold)
}

// MARK: - Language Rules (Playbook Part 1.4)
// ✅ German only - all UI text in German
// ✅ Literal language - no metaphors or idioms
// ✅ Max 7 words per sentence (Narrator & Bennie)
// ✅ Positive framing always
// ✅ Simple, concrete vocabulary
// ⚠️ NEVER say "Falsch" (wrong)
// ⚠️ NEVER say "Fehler" (error)
```

**Validation:**
- [ ] Font sizes match playbook Part 1.4 exactly
- [ ] SF Rounded design confirmed
- [ ] All presets render correctly

**Test:**
```swift
VStack {
    Text("Waldabenteuer").font(.bennieTitle)
    Text("Was möchtest du spielen?").font(.bennieBody)
    Text("Weiter").font(.bennieButton)
}
```

---

### 1.8 Create AppCoordinator
**Estimated**: 30 minutes  
**Playbook Reference**: `/mnt/project/FULL_ARCHIVE.md` → Part 2.2: State Machine Definition

**Steps:**
- [ ] Create App/AppCoordinator.swift
- [ ] Define GameState enum per playbook Part 2.2
- [ ] Implement state machine
- [ ] Create navigation logic

**Implementation (FROM PLAYBOOK PART 2.2):**
```swift
import SwiftUI
import Combine

// PLAYBOOK REFERENCE: Part 2.2 - State Machine Definition
// Source: /mnt/project/FULL_ARCHIVE.md → Part 2.2

enum GameState {
    case loading
    case playerSelection
    case home
    case activitySelection(ActivityType)
    case playing(ActivityType, SubActivity)
    case levelComplete
    case celebrationOverlay      // Only at 5-coin milestones
    case treasureScreen
    case videoSelection
    case videoPlaying
    case parentGate              // Math question gate
    case parentDashboard         // Settings screen
}

enum ActivityType {
    case raetsel    // Rätsel
    case zahlen     // Zahlen 1,2,3
    // Future phases:
    // case zeichnen
    // case logik
}

enum SubActivity {
    // Rätsel
    case puzzleMatching
    case labyrinth
    
    // Zahlen
    case wuerfel     // Dice game
    case waehleZahl  // Choose the number
}

class AppCoordinator: ObservableObject {
    @Published var currentState: GameState = .loading
    
    func navigate(to state: GameState) {
        currentState = state
    }
}
```

**Validation:**
- [ ] States match playbook Part 2.2 exactly
- [ ] ActivityType matches playbook
- [ ] SubActivity matches playbook
- [ ] Create coordinator in App
- [ ] Verify state changes work

---

### 1.9 Update BennieGameApp.swift
**Estimated**: 15 minutes  
**Playbook Reference**: General architecture

**Steps:**
- [ ] Add AppCoordinator as StateObject
- [ ] Set up main app structure
- [ ] Configure window group

**Implementation:**
```swift
import SwiftUI

@main
struct BennieGameApp: App {
    @StateObject private var coordinator = AppCoordinator()
    
    var body: some Scene {
        WindowGroup {
            ContentView()
                .environmentObject(coordinator)
        }
    }
}
```

**Validation:**
- [ ] App launches
- [ ] Coordinator accessible in views via @EnvironmentObject

---

### 1.10 Create Project Documentation
**Estimated**: 30 minutes  
**Playbook Reference**: All parts

**Steps:**
- [ ] Copy playbook condensed to project root for reference
- [ ] Create DEVELOPMENT.md with setup instructions
- [ ] Update README.md with project overview
- [ ] Document playbook compliance

**Files:**
- `README.md`
- `PLAYBOOK_REFERENCE.md` (copy of condensed playbook)
- `DEVELOPMENT.md`

**DEVELOPMENT.md Contents:**
```markdown
# Development Guide

## Playbook Compliance
**CRITICAL**: The playbook is the gold standard. All implementation MUST match playbook specifications.

Playbook location: `/mnt/project/FULL_ARCHIVE.md`
Condensed version: `PLAYBOOK_REFERENCE.md` (in project root)

## Setup
1. Clone repository
2. Open BennieGame.xcodeproj
3. Wait for SPM dependencies to resolve (Lottie)
4. Build and run (Cmd+R)

## Requirements
- Xcode 15+
- macOS 14+
- iPad simulator (iPadOS 17+)

## Architecture
- SwiftUI + UIKit hybrid
- AppCoordinator for navigation (Playbook Part 2.2)
- Services for cross-cutting concerns

## Key Files & Playbook References
- `Colors.swift`: Brand color palette (Playbook Part 1.3)
- `Typography.swift`: Font system (Playbook Part 1.4)
- `AppCoordinator.swift`: Navigation state machine (Playbook Part 2.2)
- File structure: MUST match Playbook Part 8 exactly

## Critical Design Rules (From Playbook)
- Bennie: Brown #8C7259, NO clothing/vest EVER
- Lemminge: BLUE #6FA8DC, NEVER green, NEVER brown
- Touch targets: Minimum 96pt (Playbook requirement)
- Orientation: Landscape ONLY
- Screen resolution: 1194×834 points

## Testing
- Target devices: iPad 10th gen, iPad Air, iPad Pro
- Orientation: Landscape only (verify by rotating device)
- Minimum touch targets: 96pt (measure in Xcode)
- Color validation: Compare against playbook hex values

## Playbook Sections
- Part 1: Brand Identity (characters, colors, typography)
- Part 2: Screen Flow & State Machine
- Part 3: Narrator & Voice Script
- Part 4: Screen Specifications
- Part 5: Technical Requirements
- Part 8: File Structure
```

**Validation:**
- [ ] Documentation is accurate
- [ ] Links to playbook are correct
- [ ] Instructions can be followed
- [ ] Critical rules are highlighted

---

## Phase Completion Checklist

### Playbook Compliance ⚠️
- [ ] File structure EXACTLY matches playbook Part 8
- [ ] Colors.swift hex values EXACTLY match playbook Part 1.3
- [ ] Typography.swift matches playbook Part 1.4
- [ ] AppCoordinator states match playbook Part 2.2
- [ ] Asset catalog structure matches playbook Part 8
- [ ] iPad config matches playbook Part 5.1 (landscape, 1194×834)

### Functional
- [ ] Xcode project builds without errors
- [ ] App launches on iPad simulator
- [ ] Landscape orientation locked (verify by rotating device)
- [ ] File structure matches playbook Part 8

### Technical
- [ ] Git repository initialized
- [ ] Lottie dependency installed and working
- [ ] No warnings in build output
- [ ] Asset catalogs configured per playbook
- [ ] YouTube service stubbed with playbook parameters

### Documentation
- [ ] README.md complete with playbook references
- [ ] DEVELOPMENT.md written with playbook compliance notes
- [ ] Playbook reference accessible
- [ ] Code comments reference playbook sections

### Quality
- [ ] Clean git history
- [ ] Meaningful commit messages
- [ ] No temporary files committed
- [ ] .gitignore working correctly
- [ ] All hex values verified against playbook

---

## Common Issues

### Issue: "Colors don't match playbook exactly"
**Solution**: 
1. Open `/mnt/project/FULL_ARCHIVE.md` → Part 1.3
2. Copy hex values EXACTLY (e.g., #8C7259 for Bennie brown)
3. Use Color(hex: "8C7259") with no variations
4. Validate visually and with color picker

### Issue: "File structure doesn't match playbook"
**Solution**:
1. Open playbook Part 8
2. Compare directory tree line by line
3. Rename/move folders to match exactly
4. Do NOT deviate from playbook structure

### Issue: "UIRequiresFullScreen not found"
**Solution**: Add to Info.plist manually
```xml
<key>UIRequiresFullScreen</key>
<true/>
<key>UISupportedInterfaceOrientations</key>
<array>
    <string>UIInterfaceOrientationLandscapeLeft</string>
    <string>UIInterfaceOrientationLandscapeRight</string>
</array>
```

### Issue: "Landscape orientation not locked"
**Solution**: 
1. Select project in navigator
2. Select target
3. General tab → Device Orientation
4. Uncheck Portrait, check Landscape Left & Right ONLY
5. Add Info.plist keys above

### Issue: "SPM dependencies won't resolve"
**Solution**:
1. File → Packages → Reset Package Caches
2. Clean build folder (Cmd+Shift+K)
3. Rebuild

---

## Next Phase

After Phase 1 completion, proceed to:
**Phase 2: Design System Implementation**
- Create reusable components per playbook
- Build WoodButton, ProgressBar, etc.
- Establish animation presets
- Reference screens: `/mnt/project/Reference_*.png`
