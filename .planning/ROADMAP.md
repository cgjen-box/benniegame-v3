# Roadmap: Bennie Bear Learning Game

## Milestones

- ✅ **v1.0 MVP** — Phases 1-8 (shipped 2026-01-13) — [Full archive](milestones/v1.0-ROADMAP.md)
- 🚧 **v1.1 Polish & Production** — Phases 9-14 (in progress)

## Source of Truth

**Design validation:** All visual work MUST comply with `PLAYBOOK_CONDENSED.md`
- Check character colors, touch targets, forbidden elements before marking any screen complete
- Run `DESIGN_QA_CHECKLIST.md` verification at end of each visual phase

---

## Completed Milestones

<details>
<summary>v1.0 MVP (Phases 1-8) — SHIPPED 2026-01-13</summary>

### Phase 1: Foundation
**Goal**: Xcode project running on iPad simulator with design system in place
**Plans**: 3 plans (complete)
- [x] 01-01: Project setup
- [x] 01-02: Design system
- [x] 01-03: Core components

### Phase 2: Core Screens
**Goal**: Full navigation flow from loading → player select → home
**Plans**: 3 plans (complete)
- [x] 02-01: State management
- [x] 02-02: Loading & player selection
- [x] 02-03: Home screen

### Phase 3: Activities
**Goal**: All 4 activities playable with level progression
**Plans**: 4 plans (complete)
- [x] 03-01: Puzzle Matching
- [x] 03-02: Labyrinth
- [x] 03-03: Würfel/Dice
- [x] 03-04: Wähle die Zahl

### Phase 4: Reward System
**Goal**: Complete coin → celebration → YouTube loop
**Plans**: 3 plans (complete)
- [x] 04-01: Coin economy
- [x] 04-02: Celebration overlay
- [x] 04-03: Treasure & video

### Phase 5: Audio Integration
**Goal**: Full audio experience with voices
**Plans**: 3 plans (complete)
- [x] 05-01: AudioManager
- [x] 05-02: Voice services
- [x] 05-03: Integration

### Phase 6: Parent Features
**Goal**: Parents can manage videos and time limits
**Plans**: 2 plans (complete)
- [x] 06-01: Parent gate & dashboard
- [x] 06-02: Video & time management

### Phase 7: Polish & Testing
**Goal**: Polished app ready for TestFlight
**Plans**: 2 plans (complete)
- [x] 07-01: Design QA
- [x] 07-02: Full playthrough

### Phase 8: Asset Production
**Goal**: Generate and import all visual/audio assets
**Plans**: 3 plans (complete)
- [x] 08-01: UI Components
- [x] 08-02: Background Images
- [x] 08-03: Lottie Animations

**Total: 8 phases, 23 plans, 100% complete**

</details>

---

## 🚧 v1.1 Polish & Production (In Progress)

**Milestone Goal:** Production-quality polish with full spec compliance — visual alignment to references, voice audio generation, adaptive difficulty, accessibility, performance optimization, and recursive testing until 100% Playbook compliance.

**Key References:**
- `PLAYBOOK_CONDENSED.md` — Design rules source of truth
- `design/references/screens/Reference_*.png` — 8 reference screen mockups
- `plan/12_adaptive_difficulty/` — Adaptive difficulty spec
- `plan/13_accessibility/` — Accessibility spec
- `plan/14_performance/` — Performance spec
- `plan/15_recursive_testing/` — Recursive testing spec
- `starter-kits/maestro-orchestration/` — MCP servers for automated testing

### Phase 9: Visual QA & Reference Alignment

**Goal**: Screen-by-screen comparison to Reference_*.png, fix all deviations to match exactly
**Depends on**: v1.0 MVP complete
**Research**: Unlikely (internal QA patterns)
**Plans**: TBD

Plans:
- [ ] 09-01: TBD (run /gsd:plan-phase 9 to break down)

### Phase 10: Voice Audio Generation

**Goal**: Generate all German voice lines via ElevenLabs, integrate into AudioManager
**Depends on**: Phase 9
**Research**: Likely (ElevenLabs API integration)
**Research topics**: ElevenLabs API, German voice selection, audio file format/compression
**Plans**: TBD

Plans:
- [ ] 10-01: TBD

### Phase 11: Adaptive Difficulty

**Goal**: Implement LearningProfile, difficulty rules, per-activity configs for Alexander/Oliver
**Depends on**: Phase 10
**Research**: Unlikely (spec exists in plan/12_adaptive_difficulty/)
**Plans**: TBD

Plans:
- [ ] 11-01: TBD

### Phase 12: Accessibility

**Goal**: Touch target enforcement (96pt), VoiceOver German labels, color blindness, haptics, reduce motion
**Depends on**: Phase 11
**Research**: Unlikely (standard iOS accessibility APIs)
**Plans**: TBD

Plans:
- [ ] 12-01: TBD

### Phase 13: Performance

**Goal**: Profiling, memory optimization (<200MB), asset optimization, 60fps validation, <100ms touch response
**Depends on**: Phase 12
**Research**: Unlikely (Xcode Instruments, internal profiling)
**Plans**: TBD

Plans:
- [ ] 13-01: TBD

### Phase 14: Recursive Testing

**Goal**: Full playthrough automation via maestro-orchestration MCP, Playbook compliance validation until 100%
**Depends on**: Phase 13
**Research**: Likely (maestro-orchestration MCP integration)
**Research topics**: iOS Simulator MCP, run_tests(), take_screenshot(), XCUITest automation
**Plans**: TBD

Plans:
- [ ] 14-01: TBD

---

## Progress Summary

| Milestone | Phases | Plans | Status | Date |
|-----------|--------|-------|--------|------|
| v1.0 MVP | 1-8 | 23/23 | SHIPPED | 2026-01-13 |
| v1.1 Polish & Production | 9-14 | 0/? | In progress | — |
