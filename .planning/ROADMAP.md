# Roadmap: Bennie Bear Learning Game

## Overview

Build an autism-friendly iPad educational game for Alexander (5) and Oliver (4). From Xcode project setup through polished TestFlight build, delivering 4 activities with coin rewards exchangeable for YouTube time.

## Source of Truth

**Design validation:** All visual work MUST comply with `PLAYBOOK_CONDENSED.md`
- Check character colors, touch targets, forbidden elements before marking any screen complete
- Run `DESIGN_QA_CHECKLIST.md` verification at end of each visual phase

## Domain Expertise

None (no matching expertise folder available)

## Phases

**Phase Numbering:**
- Integer phases (1, 2, 3): Planned milestone work
- Decimal phases (2.1, 2.2): Urgent insertions (marked with INSERTED)

- [x] **Phase 1: Foundation** - Xcode project, design system, basic components
- [ ] **Phase 2: Core Screens** - Loading, player selection, home, navigation
- [ ] **Phase 3: Activities** - 4 playable games (puzzle, labyrinth, dice, numbers)
- [ ] **Phase 4: Reward System** - Coins, celebrations, treasure, YouTube redemption
- [ ] **Phase 5: Audio Integration** - 3-channel audio, ElevenLabs voices, effects
- [ ] **Phase 6: Parent Features** - Gate, dashboard, video management, time limits
- [ ] **Phase 7: Polish & Testing** - QA validation, accessibility, full playthrough

## Phase Details

### Phase 1: Foundation
**Goal**: Xcode project running on iPad simulator with design system in place
**Depends on**: Nothing (first phase)
**Research**: Unlikely (established SwiftUI patterns)
**Plans**: 3 plans

Plans:
- [x] 01-01: Project setup (Xcode, git, folder structure, Lottie dependency)
- [x] 01-02: Design system (BennieColors, BennieTypography, color compliance)
- [x] 01-03: Core components (WoodButton, WoodSign, ProgressBar)

**Playbook validation**: Colors match palette, touch targets ≥96pt

### Phase 2: Core Screens
**Goal**: Full navigation flow from loading → player select → home
**Depends on**: Phase 1
**Research**: Unlikely (standard SwiftUI navigation)
**Plans**: 3 plans

Plans:
- [ ] 02-01: State management (GameState, PlayerData, navigation coordinator)
- [ ] 02-02: Loading & player selection screens
- [ ] 02-03: Home screen with activity signs and treasure chest

**Playbook validation**: Bennie brown (#8C7259, NO clothing), Lemminge blue (#6FA8DC)

### Phase 3: Activities
**Goal**: All 4 activities playable with level progression
**Depends on**: Phase 2
**Research**: Unlikely (internal game logic)
**Plans**: 4 plans

Plans:
- [ ] 03-01: Puzzle Matching (dual grid, color picker, pattern validation)
- [ ] 03-02: Labyrinth (path tracing, touch validation, START→ZIEL)
- [ ] 03-03: Würfel/Dice (dice animation, number buttons 1-6)
- [ ] 03-04: Wähle die Zahl (numbers 1-10, tracing validation)

**Playbook validation**: German UI only, positive feedback only (never "Falsch")

### Phase 4: Reward System
**Goal**: Complete coin → celebration → YouTube loop working
**Depends on**: Phase 3
**Research**: Likely (YouTube embedding)
**Research topics**: WKWebView YouTube embed, hiding controls, preventing related videos, time tracking
**Plans**: 3 plans

Plans:
- [ ] 04-01: Coin economy (+1 per level, celebration at 5-coin intervals)
- [ ] 04-02: Celebration overlay (confetti, character animations, voice)
- [ ] 04-03: Treasure & video (redemption, selection, controlled playback)

**Playbook validation**: Celebration triggers at 5, 10, 15, 20 coins; 10 coins = 5 min, 20 coins = 12 min

### Phase 5: Audio Integration
**Goal**: Full audio experience with narrator and Bennie voices
**Depends on**: Phase 4
**Research**: Likely (ElevenLabs API)
**Research topics**: ElevenLabs German voice selection, API integration, voice quality settings
**Plans**: 3 plans

Plans:
- [ ] 05-01: AudioManager (3-channel: music, voice, effects; voice ducking)
- [ ] 05-02: Voice generation (ElevenLabs narrator + Bennie voices, ~50 lines)
- [ ] 05-03: Integration (trigger points, speech bubbles, sound effects)

**Playbook validation**: Voice ducking works, mute control affects all channels

### Phase 6: Parent Features
**Goal**: Parents can manage videos, time limits, and activity locks
**Depends on**: Phase 5
**Research**: Unlikely (internal CRUD with SwiftData)
**Plans**: 2 plans

Plans:
- [ ] 06-01: Parent gate (math question) and dashboard (per-player stats)
- [ ] 06-02: Video management and time limit controls

**Playbook validation**: Math gate range 5-15, graceful time limit enforcement

### Phase 7: Polish & Testing
**Goal**: Polished app ready for TestFlight
**Depends on**: Phase 6
**Research**: Unlikely (standard QA patterns)
**Plans**: 2 plans

Plans:
- [ ] 07-01: Design QA (touch targets, colors, accessibility, animations)
- [ ] 07-02: Full playthrough (0→100 coins journey, edge cases, persistence)

**Playbook validation**: Run full DESIGN_QA_CHECKLIST.md, 100% critical + 90% high priority = PASS

## Progress

**Execution Order:**
Phases execute in numeric order: 1 → 2 → 3 → 4 → 5 → 6 → 7

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. Foundation | 3/3 | Complete | 2026-01-12 |
| 2. Core Screens | 0/3 | Next | - |
| 3. Activities | 0/4 | Not started | - |
| 4. Reward System | 0/3 | Not started | - |
| 5. Audio Integration | 0/3 | Not started | - |
| 6. Parent Features | 0/2 | Not started | - |
| 7. Polish & Testing | 0/2 | Not started | - |
| **Total** | **3/20** | | |
