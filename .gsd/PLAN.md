# PLAN.md — Current Phase Execution Plan

> **Current Phase**: 1 - Project Foundation  
> **Status**: ⬜ Ready to Execute  
> **Estimated Time**: 4-6 hours

---

## Pre-Phase Assumptions Verified

Before starting Phase 1, verify these assumptions:

| Assumption | Status | Notes |
|------------|--------|-------|
| macOS with Xcode 15+ available | ⬜ Verify | Required for iOS development |
| Apple Developer account (free tier OK) | ⬜ Verify | For simulator testing |
| iPad Simulator available | ⬜ Verify | Target: iPad 10th gen |
| Git installed | ⬜ Verify | For version control |
| Design assets ready | ✅ Verified | `design/references/` populated |

---

## Phase 1 Tasks

### Task 1.0: Initialize Git Repository ⬜
**Priority**: FIRST - Before any code  
**Time**: 5 minutes

**Steps**:
```bash
cd "C:\Users\christoph\Bennie und die Lemminge v3"
git init
```

**Create .gitignore**:
```
# Xcode
*.xcodeproj/project.xcworkspace/
*.xcodeproj/xcuserdata/
*.xcworkspace/xcuserdata/
DerivedData/
*.hmap
*.ipa
*.dSYM.zip
*.dSYM

# Swift Package Manager
.build/
Packages/

# CocoaPods
Pods/

# macOS
.DS_Store
*.swp
*~

# IDE
.idea/
*.sublime-*

# Secrets (CRITICAL)
*.env
*secrets*
*api_key*

# Build outputs
build/
*.app

# Archives
*.zip
!GSD start.zip
```

**Initial commit**:
```bash
git add .
git commit -m "Initial commit: GSD framework and design assets"
```

**Done when**: `.git/` directory exists, initial commit made

---

### Task 1.1: Create Xcode Project ⬜
**Priority**: High  
**Time**: 15 minutes  
**Depends on**: Task 1.0

**Steps**:
1. Open Xcode → New Project
2. Select: iOS → App
3. Settings:
   - Product Name: `BennieGame`
   - Team: Personal Team
   - Organization Identifier: `com.bennie`
   - Interface: SwiftUI
   - Language: Swift
   - Storage: SwiftData
   - ✅ Include Tests
4. Save to: `C:\Users\christoph\Bennie und die Lemminge v3\BennieGame`
5. Configure project:
   - Deployment Target: iOS 17.0
   - Device: iPad
   - Orientation: Landscape Left, Landscape Right only
   - Status Bar: Hidden

**Done when**: Project builds successfully on iPad Simulator

---

### Task 1.2: Create Folder Structure ⬜
**Priority**: High  
**Time**: 10 minutes  
**Depends on**: Task 1.1

**Create folders in BennieGame/**:
```
BennieGame/
├── App/
│   ├── BennieGameApp.swift (exists)
│   └── AppCoordinator.swift
├── Features/
│   ├── Loading/
│   ├── PlayerSelection/
│   ├── Home/
│   ├── Activities/
│   │   ├── Raetsel/
│   │   └── Zahlen/
│   ├── Celebration/
│   ├── Treasure/
│   ├── Video/
│   └── Parent/
├── Design/
│   ├── Theme/
│   ├── Components/
│   └── Characters/
├── Services/
└── Resources/
    ├── Assets.xcassets/
    ├── Audio/
    └── Lottie/
```

**Done when**: All folders created in Xcode project navigator

---

### Task 1.3: Create BennieColors.swift ⬜
**Priority**: High  
**Time**: 20 minutes  
**Depends on**: Task 1.2  
**Reference**: `SWIFTUI_CODING_GUIDELINES.md` Section 2

**File**: `BennieGame/Design/Theme/BennieColors.swift`

**Must include**:
- All color hex values from PLAYBOOK_CONDENSED.md
- BennieBrown: #8C7259
- LemmingeBlue: #6FA8DC
- Woodland: #738F66
- Success: #99BF8C
- CoinGold: #D9C27A
- Wood colors (light/medium/dark)
- Forbidden colors documented in comments

**Done when**: All colors accessible as `BennieColors.woodland` etc.

---

### Task 1.4: Create BennieTypography.swift ⬜
**Priority**: High  
**Time**: 15 minutes  
**Depends on**: Task 1.2  
**Reference**: `SWIFTUI_CODING_GUIDELINES.md` Section 3

**File**: `BennieGame/Design/Theme/BennieTypography.swift`

**Must include**:
- SF Rounded font family
- Title style (32-48pt Bold)
- Body style (17-24pt Regular)
- Button style (20-28pt Semibold)
- Number style (40-72pt Bold)

**Done when**: Typography accessible via `BennieFont.title` etc.

---

### Task 1.5: Create Basic UI Components ⬜
**Priority**: High  
**Time**: 45 minutes  
**Depends on**: Tasks 1.3, 1.4  
**Reference**: `SWIFTUI_CODING_GUIDELINES.md` Sections 4-5

**Files to create**:

1. `BennieGame/Design/Components/WoodButton.swift`
   - Wood gradient background
   - ≥96pt touch target
   - Press animation (scale 0.95)

2. `BennieGame/Design/Components/WoodSign.swift`
   - Hanging sign with rope
   - Wood texture gradient
   - Swing animation on appear

3. `BennieGame/Design/Components/ProgressBar.swift`
   - Berry decorations
   - Coin slots (10 max)
   - Fill animation

**Done when**: Components render correctly in preview

---

### Task 1.6: Create LoadingView ⬜
**Priority**: High  
**Time**: 45 minutes  
**Depends on**: Task 1.5  
**Reference**: `design/references/screens/Reference_Loading Screen.png`

**File**: `BennieGame/Features/Loading/LoadingView.swift`

**Requirements**:
- Forest background (use placeholder gradient initially)
- "Waldabenteuer lädt" hanging sign
- Progress bar with berry decorations (0-100%)
- "Lade Spielewelt..." text below
- Bennie character (placeholder initially)
- Lemminge peeking (placeholders initially)
- Fake loading animation (5 seconds total)
- Transition to player selection at 100%

**Done when**: Loading screen matches reference, progress animates 0→100%

---

### Task 1.7: Test on iPad Simulator ⬜
**Priority**: High  
**Time**: 15 minutes  
**Depends on**: Task 1.6

**Verification checklist**:
- [ ] App launches without crashes
- [ ] Landscape orientation only
- [ ] Loading screen displays correctly
- [ ] Progress bar animates smoothly
- [ ] Colors match specifications
- [ ] Touch targets ≥96pt (use Accessibility Inspector)
- [ ] 60fps performance (no stutters)

**Done when**: All checks pass on iPad (10th gen) Simulator

---

## Phase 1 Completion Criteria

| Criteria | Status |
|----------|--------|
| Git repository initialized | ⬜ |
| Xcode project builds | ⬜ |
| Design system (colors, typography) | ⬜ |
| Basic components (button, sign, progress) | ⬜ |
| LoadingView implemented | ⬜ |
| iPad Simulator test passes | ⬜ |

**Phase 1 Complete when**: All criteria checked ✅

---

## After Phase 1

1. Run `/gsd:map-codebase` to document architecture
2. Update STATE.md with completion status
3. Update ROADMAP.md Phase 1 → ✅
4. Git commit: `"Phase 1 complete: Project foundation"`
5. Begin Phase 2 planning

---

*Last Updated: 2025-01-11*
