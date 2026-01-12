# ROADMAP.md — Bennie und die Lemminge Development Roadmap

> **Project**: Bennie und die Lemminge  
> **Platform**: iPad (iOS 17+, Landscape only)  
> **Target**: Autism-friendly educational game for ages 4-5  
> **Status**: 🚨 FRESH BUILD - No code exists yet

---

## ⚠️ Starting from Zero

```
╔════════════════════════════════════════════════════════════════════════════╗
║  This roadmap tracks a FRESH BUILD. Nothing has been implemented yet.     ║
║  Phase 1 begins with git init and creating the Xcode project.             ║
╚════════════════════════════════════════════════════════════════════════════╝
```

---

## Key Reference Documents

| Document | Purpose | When to Use |
|----------|---------|-------------|
| `PLAYBOOK_CONDENSED.md` | Quick design rules | Before ANY visual work |
| `docs/playbook/FULL_ARCHIVE.md` | Complete specification | Deep implementation details |
| `SWIFTUI_CODING_GUIDELINES.md` | Code patterns & components | When writing SwiftUI code |
| `DESIGN_QA_CHECKLIST.md` | Visual QA verification | Before marking screen complete |
| `design/references/screens/` | Visual mockups (8 files) | UI implementation reference |

---

## Starter-Kit Integration

These starter-kits are available in `starter-kits/` and should be used:

| Starter-Kit | Phase | Purpose |
|-------------|-------|---------|
| `security-infrastructure/` | 1 | Git hooks, secret scanning, .gitignore |
| `gemini-image-pro-3/` | 3-4 | Generate character expressions if needed |
| `lottie-animation-system/` | 3-4 | Create Lottie animations from sprites |
| `ludo-animation-pipeline/` | 3-4 | Advanced character animation pipeline |
| `veo-video-generation/` | 4 | Generate intro/cutscene videos |
| `maestro-orchestration/` | 7 | iOS simulator testing automation |

---

## Development Phases

### Phase 1: Project Foundation ⬜ CURRENT
**Estimated**: 4-6 hours | **Status**: Ready to Start

| Task | Description | Status | Reference |
|------|-------------|--------|-----------|
| 1.0 | Initialize git repository | ⬜ | `starter-kits/security-infrastructure/` |
| 1.1 | Create Xcode project (iPad, landscape, iOS 17+) | ⬜ | SWIFTUI_CODING_GUIDELINES.md |
| 1.2 | Set up folder structure | ⬜ | `docs/playbook/08-file-structure.md` |
| 1.3 | Create BennieColors.swift | ⬜ | SWIFTUI_CODING_GUIDELINES.md |
| 1.4 | Create BennieTypography.swift | ⬜ | SWIFTUI_CODING_GUIDELINES.md |
| 1.5 | Create basic UI components (WoodButton, WoodSign) | ⬜ | SWIFTUI_CODING_GUIDELINES.md |
| 1.6 | Create LoadingView | ⬜ | `design/references/screens/Reference_Loading Screen.png` |
| 1.7 | Test on iPad Simulator | ⬜ | |

**Deliverable**: App launches, shows loading screen, design system works

---

### Phase 2: Core Screens ⬜ Pending
**Estimated**: 6-8 hours | **Dependencies**: Phase 1

| Task | Description | Status | Reference |
|------|-------------|--------|-----------|
| 2.1 | PlayerSelectionView (Alexander/Oliver) | ⬜ | `Reference_Player_Selection_Screen.png` |
| 2.2 | HomeView (Waldabenteuer menu) | ⬜ | `Reference_Menu_Screen.png` |
| 2.3 | Navigation/state management | ⬜ | `docs/playbook/02-screen-flow.md` |
| 2.4 | Activity sign components (locked/unlocked) | ⬜ | |
| 2.5 | Treasure chest component | ⬜ | `design/references/components/` |
| 2.6 | Progress bar component | ⬜ | |

**Deliverable**: Full navigation flow from loading → player select → home

---

### Phase 3: Activities ⬜ Pending
**Estimated**: 8-10 hours | **Dependencies**: Phase 2

| Task | Description | Status | Reference |
|------|-------------|--------|-----------|
| 3.1 | PuzzleMatchingView (Rätsel - pattern matching) | ⬜ | `Reference_Matching Game Screen.png` |
| 3.2 | LabyrinthView (Rätsel - maze tracing) | ⬜ | `Reference_Layrinth_Game_Screen.png` |
| 3.3 | WuerfelView (Zahlen - dice counting) | ⬜ | |
| 3.4 | WaehleZahlView (Zahlen - number selection) | ⬜ | `Reference_Numbers_Game_Screen.png` |
| 3.5 | Activity selection screens | ⬜ | |
| 3.6 | Difficulty progression system | ⬜ | `docs/playbook/00-game-overview.md` |

**Starter-Kits**: May use `gemini-image-pro-3/` for additional character poses

**Deliverable**: All 4 activities playable with level progression

---

### Phase 4: Reward System ⬜ Pending
**Estimated**: 4-6 hours | **Dependencies**: Phase 3

| Task | Description | Status | Reference |
|------|-------------|--------|-----------|
| 4.1 | Coin earning logic (+1 per level) | ⬜ | `docs/playbook/00-game-overview.md` |
| 4.2 | CelebrationOverlay (every 5 coins) | ⬜ | `Reference_Celebration_Overlay.png` |
| 4.3 | TreasureView (YouTube redemption) | ⬜ | `Reference_Treasure_Screen.png` |
| 4.4 | VideoSelectionView (pre-approved videos) | ⬜ | |
| 4.5 | VideoPlayerView (controlled playback) | ⬜ | |
| 4.6 | Analog clock countdown | ⬜ | |

**Starter-Kits**: 
- `lottie-animation-system/` for celebration animations
- `veo-video-generation/` for optional intro video

**Deliverable**: Complete coin → celebration → YouTube reward loop

---

### Phase 5: Audio Integration ⬜ Pending
**Estimated**: 4-5 hours | **Dependencies**: Phase 4

| Task | Description | Status | Reference |
|------|-------------|--------|-----------|
| 5.1 | AudioManager (3-channel system) | ⬜ | `docs/playbook/06-animation-sound.md` |
| 5.2 | Generate narrator voice lines (ElevenLabs) | ⬜ | `docs/playbook/03-voice-script.md` |
| 5.3 | Generate Bennie voice lines (ElevenLabs) | ⬜ | `docs/playbook/03-voice-script.md` |
| 5.4 | Sound effects integration | ⬜ | |
| 5.5 | Voice ducking (music drops during speech) | ⬜ | |
| 5.6 | Speech bubble with typewriter text | ⬜ | |

**Research Needed**: ElevenLabs API integration, German voice selection

**Deliverable**: Full audio experience with narrator and Bennie voices

---

### Phase 6: Parent Features ⬜ Pending
**Estimated**: 3-4 hours | **Dependencies**: Phase 5

| Task | Description | Status | Reference |
|------|-------------|--------|-----------|
| 6.1 | ParentGateView (math question) | ⬜ | `docs/playbook/04-screens/video-parent.md` |
| 6.2 | ParentDashboardView (settings) | ⬜ | |
| 6.3 | Video management (add/remove approved videos) | ⬜ | |
| 6.4 | Daily time limits per child | ⬜ | |
| 6.5 | Activity lock/unlock controls | ⬜ | |
| 6.6 | Progress tracking display | ⬜ | |

**Deliverable**: Parents can manage videos, time limits, and locks

---

### Phase 7: Polish & Testing ⬜ Pending
**Estimated**: 4-6 hours | **Dependencies**: Phase 6

| Task | Description | Status | Reference |
|------|-------------|--------|-----------|
| 7.1 | Touch target verification (≥96pt) | ⬜ | DESIGN_QA_CHECKLIST.md |
| 7.2 | Color compliance check | ⬜ | DESIGN_QA_CHECKLIST.md |
| 7.3 | Animation smoothness (60fps) | ⬜ | |
| 7.4 | Accessibility testing (VoiceOver) | ⬜ | |
| 7.5 | Offline mode testing | ⬜ | |
| 7.6 | Data persistence testing | ⬜ | |
| 7.7 | Full playthrough: 0 → 100 coins | ⬜ | |

**Starter-Kits**: `maestro-orchestration/` for automated UI testing on simulator

**Deliverable**: Polished, tested app ready for family use

---

## Timeline Summary

| Phase | Name | Hours | Status |
|-------|------|-------|--------|
| 1 | Project Foundation | 4-6 | ⬜ CURRENT |
| 2 | Core Screens | 6-8 | ⬜ Pending |
| 3 | Activities | 8-10 | ⬜ Pending |
| 4 | Reward System | 4-6 | ⬜ Pending |
| 5 | Audio Integration | 4-5 | ⬜ Pending |
| 6 | Parent Features | 3-4 | ⬜ Pending |
| 7 | Polish & Testing | 4-6 | ⬜ Pending |
| **Total** | | **33-45** | |

---

## Success Metrics

| Metric | Target | Current |
|--------|--------|---------|
| Screens implemented | 13 | 0 |
| Activities working | 4 | 0 |
| Voice lines integrated | ~50 | 0 |
| Touch targets ≥96pt | 100% | N/A |
| Test: 0→100 coins clean run | Pass | Not tested |

---

## Critical Design Rules

Every screen must comply:

```
🐻 Bennie: Brown #8C7259, NO VEST/CLOTHING
🔵 Lemminge: Blue #6FA8DC, NEVER green/brown
👆 Touch: ≥96pt minimum
🚫 Forbidden: Red, neon, flashing, shaking
🇩🇪 Language: German only, literal
✅ Feedback: Positive only, never "wrong"/"falsch"
```

---

## GSD Commands Reference

| Command | When to Use |
|---------|-------------|
| `/gsd:plan-phase N` | Generate atomic tasks for phase N |
| `/gsd:execute-plan` | Execute current PLAN.md tasks via subagent |
| `/gsd:map-codebase` | After Phase 1, document architecture |
| `/gsd:research-phase N` | Before complex phases (e.g., Phase 5 audio) |
| `/gsd:list-phase-assumptions` | Verify assumptions before planning |

---

*Last Updated: 2025-01-11*
