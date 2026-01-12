# Architecture

**Analysis Date:** 2026-01-12

## Pattern Overview

**Overall:** Layered SwiftUI Application with Coordinator Pattern

**Key Characteristics:**
- Feature-based modular screens
- Observable state machine (@Observable)
- Service-oriented business logic
- Local-only persistence (no cloud)
- Autism-friendly design constraints embedded in architecture

## Layers

**App Layer:**
- Purpose: Application entry point and root coordination
- Contains: `BennieGameApp.swift`, `AppCoordinator.swift`
- Location: `App/`
- Depends on: All other layers
- Used by: iOS runtime

**Core Layer:**
- Purpose: Shared state management and services
- Contains: GameState, PlayerData, AudioManager, NarratorService
- Location: `Core/State/`, `Core/Services/`
- Depends on: SwiftData, AVFoundation
- Used by: Feature screens, App coordinator

**Design Layer:**
- Purpose: Reusable UI components and theming
- Contains: BennieColors, BennieTypography, WoodButton, WoodSign, character views
- Location: `Design/Theme/`, `Design/Components/`, `Design/Characters/`
- Depends on: SwiftUI, Lottie
- Used by: All Feature screens

**Feature Layer:**
- Purpose: Individual screen implementations
- Contains: LoadingView, HomeView, ActivityViews, CelebrationOverlay, etc.
- Location: `Features/Loading/`, `Features/Home/`, `Features/Activities/`, etc.
- Depends on: Design layer, Core layer
- Used by: AppCoordinator

**Resources Layer:**
- Purpose: Static assets (images, animations, audio)
- Contains: Character images, Lottie JSON, audio files
- Location: `Resources/Assets.xcassets/`, `Resources/Lottie/`, `Resources/Audio/`
- Depends on: Nothing
- Used by: Design and Feature layers

## Data Flow

**App Launch Lifecycle:**

1. `BennieGameApp` initializes GameState
2. `AppCoordinator` observes `gameState.currentScreen`
3. LoadingView displays progress animation (0→100%)
4. At completion, state transitions to `.playerSelection`
5. User selects player (Alexander/Oliver)
6. State transitions to `.home`
7. User navigates through activities, earning coins

**Activity Completion Flow:**

1. User completes activity level
2. ActivityView calls `gameState.awardCoin()`
3. GameState updates player's coin count
4. Check: `coins % 5 == 0` → trigger celebration
5. CelebrationOverlay displays (confetti, voice, character animations)
6. User taps "Weiter" → continue or navigate to Treasure

**State Management:**
- Single source of truth: `GameState` (@Observable)
- Persistence: SwiftData for PlayerData
- Transient state: UI flags (showCelebration, isAudioEnabled)
- Computed properties: `activePlayer`, `canAccessTreasure`

## Key Abstractions

**GameState:**
- Purpose: Central state container for entire app
- Examples: `currentScreen`, `currentPlayer`, `players`, `showCelebration`
- Pattern: @Observable (SwiftUI 6+)
- Location: `Core/State/GameState.swift`

**Services:**
- Purpose: Encapsulate business logic and external interactions
- Examples: `AudioManager`, `NarratorService`, `PlayerDataStore`
- Pattern: Singleton-like (injected via @Environment)
- Location: `Core/Services/`

**Components:**
- Purpose: Reusable UI building blocks with design constraints
- Examples: `WoodButton` (≥96pt), `WoodSign`, `ProgressBar`, `StoneTablet`
- Pattern: SwiftUI View composition
- Location: `Design/Components/`

**Characters:**
- Purpose: Animated character rendering with expression states
- Examples: `BennieView` (6 expressions), `LemmingeView` (6 expressions)
- Pattern: State-driven Lottie animations
- Location: `Design/Characters/`

## Entry Points

**App Entry:**
- Location: `App/BennieGameApp.swift`
- Triggers: iOS app launch
- Responsibilities: Initialize GameState, inject environment, render AppCoordinator

**Screen Coordinator:**
- Location: `App/AppCoordinator.swift`
- Triggers: GameState.currentScreen changes
- Responsibilities: Route to appropriate View, manage transitions

**Feature Entry Points:**
- Location: `Features/{FeatureName}/{ScreenName}View.swift`
- Triggers: Coordinator routing
- Responsibilities: Render screen, handle user interaction, update GameState

## Error Handling

**Strategy:** Graceful degradation with positive feedback

**Patterns:**
- Audio failures: Continue without sound, show visual feedback
- Network failures (YouTube): Show "Keine Verbindung" message
- Data persistence failures: Retry, log warning
- Never show negative messages to children (autism-friendly)

## Cross-Cutting Concerns

**Logging:**
- Development: Xcode console
- Production: Not configured (privacy for children)

**Validation:**
- Design constraints: Color validation, touch target enforcement
- Input validation: Parent gate math questions
- State validation: `canTransition(from:to:)` method

**Audio System:**
- 3 independent channels: Music, Voice, Effects
- Voice ducking: Music volume 30% → 15% during voice playback
- Queue system for sequential voice lines
- Mute control affects all channels

**Accessibility:**
- Touch targets: Minimum 96pt × 96pt (enforced)
- Reduce motion: Alternative animations planned
- VoiceOver: German labels (planned)
- No flashing/shaking animations (autism-friendly)

---

*Architecture analysis: 2026-01-12*
*Update when major patterns change*
