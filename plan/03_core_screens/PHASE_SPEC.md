# Phase 3: Core Screens Implementation

**Duration**: 5-7 hours  
**Status**: Not Started  
**Dependencies**: Phase 2 (Design System)

## Overview

Implement Loading, Player Selection, and Home screens with navigation flow, voice integration, and character animations.

## Documentation References

### Playbook Sections
- **Loading & Player Selection**: `docs/playbook/04-screens/loading-player.md`
- **Home Screen**: `docs/playbook/04-screens/home-activities.md` (Section 4.3)
- **Voice Script**: `docs/playbook/03-voice-script.md`
- **Animation Guide**: `docs/playbook/06-animation-sound.md`
- **Screen Flow**: `docs/playbook/02-screen-flow.md`

### Design References
- **Screen Designs**:
  - Loading: `design/references/screens/Reference_Loading Screen.png`
  - Player Selection: `design/references/screens/Reference_Player_Selection_Screen.png`
  - Home/Menu: `design/references/screens/Reference_Menu_Screen.png`

- **Character References**:
  - Bennie: `design/references/character/bennie/reference/`
  - Lemminge: `design/references/character/lemminge/reference/`

- **Component References**:
  - Navigation Bar: `design/references/components/navigation-bar-top_20260110_122359.png`
  - Treasure Chest Closed: `design/references/components/treasure-chest-closed_20260110_122421.png`
  - Treasure Chest Open: `design/references/components/treasure-chest-open_20260110_122445.png`
  - Activity Buttons: `design/references/components/activity-button-*`
  - Settings Button: `design/references/components/settings-button-wooden_20260110_123306.png`
  - Sound Button: `design/references/components/sound-button-wooden_20260110_123401.png`

## Deliverables

- ✅ LoadingView with progress animation
- ✅ PlayerSelectionView with player cards
- ✅ HomeView with activity signs
- ✅ Navigation flow working
- ✅ Voice triggers integrated
- ✅ Character animations playing

## Tasks

### 3.0 Create LoadingView (60 min)

**Reference Documentation**:
- Playbook Section 4.1: `docs/playbook/04-screens/loading-player.md`
- Screen Design: `design/references/screens/Reference_Loading Screen.png`

**Implementation**:
- Progress bar 0-100% over 5 seconds (fake loading)
- Bennie idle animation (center-left)
  - Reference: `design/references/character/bennie/reference/bennie-reference.png`
  - Animation: `bennie_idle.json` (Lottie)
  - At 100%: Switch to `bennie_waving.json`
- 5-6 Lemminge peeking from tree holes (various positions)
  - Reference: `design/references/character/lemminge/reference/lemminge-reference.png`
  - Expressions: `lemminge_hiding.png`, `lemminge_curious.png`
- Narrator voice at 100%: "Wir sind gleich bereit zum Spielen"
  - Audio file: `narrator_loading_complete.aac`
  - Trigger: When progress reaches 100%
  - After voice completes: 2s pause → Transition to PlayerSelection
- 4-layer parallax forest background
  - Golden hour lighting from upper-left
  - Gentle floating leaf particles

**Components Used**: 
- ProgressBar (from Phase 2)
- BennieView (from Phase 2)
- LemmingeView (from Phase 2)
- AudioManager
- NarratorService

**Playbook Specifications**:
- Progress bar: 600×40pt, berry-decorated wooden log
- Bennie size: 200×300pt
- Lemminge size: 60×80pt each
- Load duration: Exactly 5 seconds (0.05s per percentage)
- Background: 4 layers (far/mid/near trees + light rays)

**Test**: 
- [ ] Smooth 5-second progression 0→100%
- [ ] Voice plays at 100%
- [ ] Bennie switches from idle to waving at 100%
- [ ] Lemminge animations play
- [ ] Transitions to PlayerSelection after voice + 2s
- [ ] Colors match playbook (Bennie brown #8C7259, Lemminge blue #6FA8DC)

---

### 3.1 Create PlayerSelectionView (50 min)

**Reference Documentation**:
- Playbook Section 4.2: `docs/playbook/04-screens/loading-player.md`
- Screen Design: `design/references/screens/Reference_Player_Selection_Screen.png`
- Voice Script: `docs/playbook/03-voice-script.md` (Player Selection section)

**Implementation**:
- Title sign at top: "Wer spielt heute?" (hanging wood plank with rope)
- Two player cards in horizontal layout:
  - **Alexander** card (left): 
    - Avatar circle (120×120pt)
    - Name: "Alexander"
    - Coin display: "🪙 [count]"
    - Touch target: 200×180pt
    - Center position: (400, 350)
  - **Oliver** card (right):
    - Same structure
    - Center position: (800, 350)
- Bennie waving at center-bottom
  - Reference: `design/references/character/bennie/reference/bennie-reference.png`
  - Animation: `bennie_waving.json`
  - Position: Center bottom (597, 600)
- Lemminge hiding in bottom corners
  - Expression: `lemminge_hiding.png`
  - Positions: Bottom-left (150, 700), Bottom-right (1044, 700)
- Profile icon button: Top-right (1140, 50)
- Forest background with golden light

**Voice Triggers**:
- On appear: Narrator "Wie heisst du? Alexander oder Oliver?"
  - Audio: `narrator_player_question.aac`
- On Alexander tap: Narrator "Hallo Alexander! Los geht's!"
  - Audio: `narrator_hello_alexander.aac`
  - Load player data for Alexander
  - Transition to Home after voice
- On Oliver tap: Narrator "Hallo Oliver! Los geht's!"
  - Audio: `narrator_hello_oliver.aac`
  - Load player data for Oliver
  - Transition to Home after voice

**Components Used**:
- WoodSign (player cards)
- BennieView (waving state)
- LemmingeView (hiding state)
- PlayerCard (custom component)
- AudioManager
- NarratorService

**Playbook Specifications**:
- Wood card background: Gradient #C4A574 → #A67C52
- Touch targets: Minimum 200×180pt per card
- Avatar circles: #FAF5EB background
- Text: SF Rounded, name 24pt bold, coins 18pt medium

**Test**:
- [ ] Voice plays on screen appear
- [ ] Both player cards are tappable
- [ ] Touch targets are ≥ 200×180pt
- [ ] Player data loads correctly
- [ ] Voice plays on tap
- [ ] Transitions to Home after voice completes
- [ ] Bennie waving animation plays smoothly
- [ ] Bennie has NO clothing/vest (design validation)
- [ ] Lemminge are BLUE #6FA8DC (design validation)

---

### 3.2 Create HomeView (90 min)

**Reference Documentation**:
- Playbook Section 4.3: `docs/playbook/04-screens/home-activities.md`
- Screen Design: `design/references/screens/Reference_Menu_Screen.png`
- Voice Script: `docs/playbook/03-voice-script.md` (Home Screen section)

**Implementation**:
- Title sign at top: "Waldabenteuer" (large hanging wood sign)
- 4 activity signs in 2×2 grid layout:
  - **Rätsel** (top-left, 300×150pt, unlocked)
    - Reference: `design/references/components/activity-button-raetsel_20260110_123032.png`
    - Icon: 🔍 magnifying glass
    - State: Glowing golden outline, no chains
    - Tap: Navigate to Rätsel Selection
  - **Zahlen 1,2,3** (top-right, 300×150pt, unlocked)
    - Reference: `design/references/components/activity-button-zahlen_20260110_123105.png`
    - Icon: 123 numbers
    - State: Glowing golden outline, no chains
    - Tap: Navigate to Zahlen Selection
  - **Zeichnen** (bottom-left, 300×150pt, locked)
    - Icon: ✏️ pencil
    - State: Dimmed (60% opacity), X-pattern chains, padlock
    - Tap: Bennie says "Das ist noch gesperrt."
  - **Logik** (bottom-right, 300×150pt, locked)
    - Icon: 🧩 puzzle piece
    - State: Dimmed (60% opacity), X-pattern chains, padlock
    - Tap: Bennie says "Das ist noch gesperrt."
- Treasure chest (bottom-right corner, 1050×700)
  - Reference: `design/references/components/treasure-chest-closed_20260110_122421.png`
  - Reference: `design/references/components/treasure-chest-open_20260110_122445.png`
  - States: Closed (< 10 coins), Open (≥ 10 coins), Open+sparkles (≥ 20 coins)
- Settings button (top-right, 1134×50)
  - Reference: `design/references/components/settings-button-wooden_20260110_123306.png`
  - Tap: Navigate to Parent Gate
- Help button (bottom-right corner)
- Bennie pointing at activities (left side)
  - Animation: `bennie_pointing.json`
  - Position: Left-center
- Lemminge mischievous (bottom-left)
  - Animation: `lemminge_mischievous.png`
  - Position: Bottom-left corner

**Voice Triggers**:

*First Visit:*
- Narrator: "Was möchtest du spielen?"
  - Audio: `narrator_home_question.aac`
- Bennie Part 1 (immediate): "Hi [Name], ich bin Bennie!"
  - Audio: `bennie_greeting_part1.aac`
- Bennie Part 2 (after 2s): "Wir lösen Aktivitäten um YouTube zu schauen."
  - Audio: `bennie_greeting_part2.aac`

*Return from Activity:*
- Bennie Part 1: "Lösen wir noch mehr Aktivitäten."
  - Audio: `bennie_return_part1.aac`
- Bennie Part 2 (after 2s): "Dann können wir mehr YouTube schauen!"
  - Audio: `bennie_return_part2.aac`

*Tap Locked Activity:*
- Bennie: "Das ist noch gesperrt."
  - Audio: `bennie_locked.aac`

**Components Used**:
- NavigationHeader (from Phase 2)
  - Reference: `design/references/components/navigation-bar-top_20260110_122359.png`
- WoodSign (×4 activity signs)
- ActivitySign (custom component for locked/unlocked states)
- TreasureChest component
- BennieView (pointing state)
- LemmingeView (mischievous state)
- AudioManager
- NarratorService

**Playbook Specifications**:
- Activity sign layout coordinates: (300,400), (500,400), (700,400), (900,400)
- Treasure chest position: (1050, 700)
- Settings button: (1134, 50)
- All touch targets: ≥ 96pt
- Unlocked glow: Golden #D9C27A with subtle pulse
- Locked chains: X-pattern, dark #6B6B6B
- Activity sign swing animation: ±3° rotation, 0.5s loop

**Test**:
- [ ] All 4 activity signs render correctly
- [ ] Unlocked signs have golden glow
- [ ] Locked signs have chains and padlock
- [ ] All voice triggers fire at correct times
- [ ] Voice sequences play in correct order
- [ ] Navigation to activities works
- [ ] Treasure chest displays correct state based on coins
- [ ] Settings button navigates to Parent Gate
- [ ] Touch targets are ≥ 96pt
- [ ] Bennie pointing animation plays
- [ ] Bennie has NO clothing (design validation)
- [ ] Lemminge are BLUE #6FA8DC (design validation)
- [ ] Colors match playbook exactly

---

### 3.3 Implement Activity Sign Component (40 min)

**Reference Documentation**:
- Playbook Section 4.3: `docs/playbook/04-screens/home-activities.md` (Locked Sign Visual)
- Component References: `design/references/components/activity-button-*`

**Implementation**:
- Create reusable ActivitySign SwiftUI component
- Two states: Unlocked, Locked
- **Unlocked State**:
  - Golden glow effect around edges (#D9C27A)
  - Gentle pulse animation (1.0 → 1.05 scale, 2s loop)
  - No chains or padlock
  - Full opacity (1.0)
  - Tappable
- **Locked State**:
  - Dimmed appearance (opacity 0.6)
  - X-pattern chains overlay (dark gray #6B6B6B)
  - Padlock icon at center-bottom
  - Non-interactive for navigation
  - Shows Bennie voice on tap: "Das ist noch gesperrt."
- Subtle hanging animation for both states:
  - Rotation: ±3° oscillation
  - Duration: 0.5s per swing
  - Easing: Ease-in-out
  - Continuous loop
- Touch feedback:
  - Scale to 0.95 on press
  - Spring animation (response 0.3)

**Components**:
```swift
struct ActivitySign: View {
    enum State {
        case unlocked
        case locked
    }
    
    let activity: ActivityType
    let state: State
    let onTap: () -> Void
}
```

**Playbook Specifications**:
- Size: 300×150pt minimum
- Wood background: Gradient #C4A574 → #A67C52
- Border: 2pt #6B4423
- Corner radius: 12pt
- Icon size: 60×60pt
- Text: SF Rounded 20pt semibold
- Chain pattern: Diagonal X, 4pt width

**Test**:
- [ ] Unlocked signs have golden glow
- [ ] Locked signs have chains and padlock
- [ ] Hanging animation is subtle and smooth
- [ ] Touch feedback works on both states
- [ ] Locked signs trigger Bennie voice
- [ ] Unlocked signs navigate to activities
- [ ] Visual matches reference images exactly

---

### 3.4 Implement Treasure Chest Component (45 min)

**Reference Documentation**:
- Playbook Section 4.3: `docs/playbook/04-screens/home-activities.md` (Chest Behavior)
- Component References:
  - Closed: `design/references/components/treasure-chest-closed_20260110_122421.png`
  - Open: `design/references/components/treasure-chest-open_20260110_122445.png`

**Implementation**:
- Three visual states based on coin count:
  
  **State 1: Closed (coins < 10)**
  - Dull wood texture, no glow
  - Chest lid closed
  - Padlock visible
  - On tap: Bennie voice "Noch [X] Münzen!"
    - Calculate: remaining = 10 - currentCoins
    - Audio: Dynamic or use `bennie_treasure_under10.aac`
  
  **State 2: Open (coins 10-19)**
  - Golden glow around chest (#D9C27A)
  - Lid open, gold coins visible spilling out
  - 1 chest icon displayed
  - Gentle sparkle particles
  - On tap: Navigate to Treasure Screen
  
  **State 3: Open + Bonus (coins ≥ 20)**
  - Extra-bright golden glow
  - Lid fully open, more coins visible
  - 2 chest icons displayed
  - Enhanced sparkle particles
  - "BONUS!" badge or indicator
  - On tap: Navigate to Treasure Screen

- Animations:
  - Idle: Gentle breathing (scale 1.0 → 1.03, 2s loop)
  - On tap when closed: Shake animation (no access yet)
  - State transition (closed → open): Lid opening animation (0.5s)
  - Sparkles: Continuous floating particles when open

**Components**:
```swift
struct TreasureChest: View {
    @Binding var coins: Int
    let onTap: () -> Void
    
    var state: ChestState {
        if coins < 10 { return .closed }
        else if coins < 20 { return .open }
        else { return .openBonus }
    }
}
```

**Playbook Specifications**:
- Size: 150×150pt
- Position: Bottom-right corner (1050, 700)
- Touch target: ≥ 96pt (use larger invisible frame if needed)
- Glow color: #D9C27A (CoinGold)
- Sparkle color: #FAF5EB (Cream)
- Animation timing: All animations spring-based (response 0.3)

**Test**:
- [ ] Closed state shows at < 10 coins
- [ ] Open state shows at 10-19 coins
- [ ] Open+bonus state shows at ≥ 20 coins
- [ ] Voice plays when tapping closed chest
- [ ] Navigates to Treasure Screen when tapping open chest
- [ ] Lid opening animation is smooth
- [ ] Sparkles render correctly
- [ ] Touch target is ≥ 96pt
- [ ] Visual matches reference images

---

### 3.5 Create AudioManager Service (60 min)

**Reference Documentation**:
- Playbook Section 6: `docs/playbook/06-animation-sound.md`
- Technical Requirements: `docs/playbook/05-technical-requirements.md` (Section 5.3)

**Implementation**:
- Three independent audio channels using AVAudioPlayer:
  
  **Channel 1: Music**
  - Background forest ambience
  - Default volume: 30% (0.3)
  - During voice: Ducks to 15% (0.15)
  - Continuous loop
  - File: `forest_ambient.aac`
  
  **Channel 2: Voice**
  - Narrator and Bennie voice lines
  - Volume: 100% (1.0) - always priority
  - Prevents overlapping: Only one voice at a time
  - Queue system for sequential voice lines
  - Callbacks on completion
  
  **Channel 3: Effects**
  - UI sounds (taps, success, coins)
  - Default volume: 70% (0.7)
  - Never plays during voice (queued)
  - Short-duration sounds (< 1s)

- Voice ducking behavior:
  ```swift
  func playVoice(_ file: String, speaker: Speaker) {
      // Duck music
      musicChannel.volume = 0.15
      
      // Play voice
      voiceChannel.play(file)
      
      // On completion, restore music
      voiceChannel.onComplete = {
          self.musicChannel.volume = 0.30
      }
  }
  ```

- Queue management:
  - Voice queue: FIFO, prevents overlap
  - Effect queue: Discards if voice is playing
  - Music: Always playing, only volume changes

**Playbook Specifications**:
- Audio format: AAC, 44.1kHz
- Voice bitrate: 128kbps
- Music bitrate: 192kbps
- Effects bitrate: 128kbps
- Voice priority: ALWAYS wins over everything
- Music ducking: Smooth 0.3s fade transition

**Test**:
- [ ] Music plays continuously at 30%
- [ ] Music ducks to 15% when voice plays
- [ ] Music restores to 30% after voice
- [ ] Voice lines never overlap
- [ ] Effects don't play during voice
- [ ] Volume levels match specifications
- [ ] No audio glitches or pops
- [ ] All three channels work independently

---

### 3.6 Create NarratorService (50 min)

**Reference Documentation**:
- Playbook Section 3: `docs/playbook/03-voice-script.md`
- Voice triggers for all screens

**Implementation**:
- Wrapper service around AudioManager for voice-specific logic
- Tracks current speaker (narrator or bennie)
- Prevents voice overlaps
- Provides callback system
- Manages voice file loading

**Core Functions**:
```swift
class NarratorService: ObservableObject {
    enum Speaker {
        case narrator
        case bennie
    }
    
    @Published var isPlaying: Bool = false
    @Published var currentSpeaker: Speaker?
    
    private let audioManager: AudioManager
    private var voiceQueue: [VoiceLine] = []
    
    func play(_ audioFile: String, speaker: Speaker, onComplete: (() -> Void)? = nil)
    func queue(_ audioFile: String, speaker: Speaker)
    func stop()
    func clearQueue()
}
```

- Voice line structure:
```swift
struct VoiceLine {
    let audioFile: String
    let speaker: Speaker
    let onComplete: (() -> Void)?
}
```

- Queue processing:
  - FIFO queue
  - Waits for current voice to complete
  - Calls completion callback
  - Automatically plays next in queue

**Playbook Specifications**:
- All voice files in: `Resources/Audio/Narrator/` and `Resources/Audio/Bennie/`
- File naming: `{speaker}_{screen}_{trigger}.aac`
- Speaking rate: 85% of normal (pre-configured in audio files)
- Max 7 words per sentence (per audio file)

**Test**:
- [ ] Voice files load correctly
- [ ] Queue system works (FIFO)
- [ ] No overlapping voices
- [ ] Completion callbacks fire
- [ ] Speaker tracking works
- [ ] Stop function works
- [ ] Clear queue works
- [ ] Integration with AudioManager works

---

### 3.7 Integrate Voice into Screens (40 min)

**Reference Documentation**:
- Playbook Section 3: `docs/playbook/03-voice-script.md`
- Complete voice script for all three screens

**Implementation**:

**LoadingView Voice**:
- Trigger: progress = 100%
- Speaker: Narrator
- Audio: `narrator_loading_complete.aac`
- Text: "Wir sind gleich bereit zum Spielen."
- After voice + 2s: Transition to PlayerSelection

**PlayerSelectionView Voice**:
- Trigger 1 (on appear):
  - Speaker: Narrator
  - Audio: `narrator_player_question.aac`
  - Text: "Wie heisst du? Alexander oder Oliver?"
- Trigger 2 (on Alexander tap):
  - Speaker: Narrator
  - Audio: `narrator_hello_alexander.aac`
  - Text: "Hallo Alexander! Los geht's!"
  - After voice: Transition to Home
- Trigger 3 (on Oliver tap):
  - Speaker: Narrator
  - Audio: `narrator_hello_oliver.aac`
  - Text: "Hallo Oliver! Los geht's!"
  - After voice: Transition to Home

**HomeView Voice**:
- Trigger 1 (first visit):
  - Speaker: Narrator
  - Audio: `narrator_home_question.aac`
  - Text: "Was möchtest du spielen?"
- Trigger 2 (first visit, immediate):
  - Speaker: Bennie
  - Audio: `bennie_greeting_part1.aac`
  - Text: "Hi [Name], ich bin Bennie!"
- Trigger 3 (first visit, after 2s):
  - Speaker: Bennie
  - Audio: `bennie_greeting_part2.aac`
  - Text: "Wir lösen Aktivitäten um YouTube zu schauen."
- Trigger 4 (return from activity):
  - Speaker: Bennie
  - Audio: `bennie_return_part1.aac`
  - Text: "Lösen wir noch mehr Aktivitäten."
- Trigger 5 (return, after 2s):
  - Speaker: Bennie
  - Audio: `bennie_return_part2.aac`
  - Text: "Dann können wir mehr YouTube schauen!"
- Trigger 6 (tap locked activity):
  - Speaker: Bennie
  - Audio: `bennie_locked.aac`
  - Text: "Das ist noch gesperrt."

**Implementation Pattern**:
```swift
struct LoadingView: View {
    @StateObject private var narrator = NarratorService.shared
    @State private var progress: Int = 0
    
    var body: some View {
        // ... UI ...
    }
    
    func animateProgress() async {
        for percent in 0...100 {
            progress = percent
            try? await Task.sleep(nanoseconds: 50_000_000)
            
            if percent == 100 {
                narrator.play("narrator_loading_complete.aac", speaker: .narrator) {
                    Task {
                        try? await Task.sleep(nanoseconds: 2_000_000_000)
                        // Transition to next screen
                    }
                }
            }
        }
    }
}
```

**Test**:
- [ ] All voice triggers fire at correct times
- [ ] Voice files are correct
- [ ] Sequential voices wait for previous to complete
- [ ] 2-second delays work correctly
- [ ] Transitions happen after voice completes
- [ ] No voice overlaps
- [ ] Music ducks during voice
- [ ] Player name substitution works ([Name])

---

### 3.8 Implement Navigation Flow (45 min)

**Reference Documentation**:
- Playbook Section 2: `docs/playbook/02-screen-flow.md`
- State machine and flow diagram

**Implementation**:
- Create AppCoordinator for state management
- Screen enum:
```swift
enum Screen {
    case loading
    case playerSelection
    case home
    case activitySelection(ActivityType)
    // ... more screens in later phases
}
```

- Navigation stack:
  - Use NavigationPath for iOS 17+
  - Maintain navigation history
  - Support back navigation
  - Preserve state across screens

- Transitions:
  - Cross-fade animation (0.3s)
  - No jarring movements
  - Smooth and predictable

- State persistence:
  - Remember current player
  - Track navigation history
  - Preserve progress data

**AppCoordinator Structure**:
```swift
@MainActor
class AppCoordinator: ObservableObject {
    @Published var currentScreen: Screen = .loading
    @Published var currentPlayer: Player?
    @Published var navigationPath = NavigationPath()
    
    func navigate(to screen: Screen)
    func goBack()
    func reset()
}
```

**Test**:
- [ ] Can navigate forward through all screens
- [ ] Back button works on all screens
- [ ] State persists across navigation
- [ ] Current player is tracked
- [ ] Transitions are smooth (0.3s fade)
- [ ] No memory leaks in navigation
- [ ] Navigation history is correct

---

### 3.9 Add Forest Backgrounds (30 min)

**Reference Documentation**:
- Playbook Section 1: `docs/playbook/01-brand-identity.md` (Forest Environment Colors)
- Playbook Section 6: `docs/playbook/06-animation-sound.md` (Animation Principles)

**Implementation**:
- 4-layer parallax background system:
  
  **Layer 1: Far Trees (Deepest)**
  - Color: #4A6B5C (misty sage)
  - Opacity: 40%
  - Parallax factor: 0.1 (slowest movement)
  - Silhouettes only
  
  **Layer 2: Mid Trees**
  - Color: #738F66 (woodland green)
  - Opacity: 60%
  - Parallax factor: 0.3
  - More detail visible
  
  **Layer 3: Near Foliage**
  - Color: #7A9973 (bright foliage)
  - Opacity: 100%
  - Parallax factor: 0.5 (faster movement)
  - Leaves and branches visible
  
  **Layer 4: Light Rays**
  - Color: #F5E6C8 @ 30% opacity
  - Golden sunbeams from upper-left
  - Subtle glow effect
  - Static (no parallax)

- Particle effects:
  - Floating leaves (5-8 particles)
  - Occasional fireflies (3-5 particles, evening only)
  - Slow gentle movement
  - Fade in/out softly

- Golden hour lighting:
  - Warm golden glow overlay
  - Direction: Upper-left to lower-right
  - Subtle vignette around edges

**Parallax Implementation**:
```swift
struct ParallaxBackground: View {
    @State private var offset: CGFloat = 0
    
    var body: some View {
        ZStack {
            ForestLayer(depth: .far, offset: offset * 0.1)
            ForestLayer(depth: .mid, offset: offset * 0.3)
            ForestLayer(depth: .near, offset: offset * 0.5)
            LightRays()
            FloatingParticles()
        }
    }
}
```

**Playbook Specifications**:
- Background should never distract from foreground
- Animations must be subtle (no jarring movements)
- Performance: 60fps constant, < 10% CPU
- No texture compression artifacts
- Colors must match playbook exactly

**Test**:
- [ ] 4 layers render correctly
- [ ] Parallax movement is subtle
- [ ] Particles animate smoothly
- [ ] Colors match playbook specifications
- [ ] Golden hour lighting visible
- [ ] Performance: 60fps maintained
- [ ] No visual glitches or artifacts
- [ ] Background doesn't distract from UI

---

### 3.10 QA Pass on Core Screens (45 min)

**Reference Documentation**:
- Complete Playbook: All sections
- QA Checklist: `docs/playbook/10-implementation.md` (Section 10.3)

**Visual QA**:
- [ ] **Colors Verification**:
  - [ ] Bennie brown: #8C7259 (warm chocolate)
  - [ ] Bennie snout: #C4A574 (tan)
  - [ ] Lemminge body: #6FA8DC (soft blue)
  - [ ] Lemminge belly: #FAF5EB (cream)
  - [ ] Wood signs: #C4A574 → #A67C52 gradient
  - [ ] Woodland green: #738F66
  - [ ] Sky blue: #B3D1E6
  - [ ] Cream background: #FAF5EB
  - [ ] Success green: #99BF8C
  - [ ] Coin gold: #D9C27A

- [ ] **Character Design Validation**:
  - [ ] Bennie has NO clothing/vest/accessories
  - [ ] Bennie has ONLY tan snout (no belly patch)
  - [ ] Bennie is adult bear (not cub, not teddy)
  - [ ] Lemminge are BLUE #6FA8DC
  - [ ] Lemminge are NOT green or brown
  - [ ] Lemminge have white belly with fuzzy edge
  - [ ] Lemminge have buck teeth visible
  - [ ] All expressions match reference images

- [ ] **Touch Target Validation**:
  - [ ] All buttons ≥ 96pt minimum
  - [ ] Player cards: 200×180pt
  - [ ] Activity signs: 300×150pt
  - [ ] Settings button: 60×60pt
  - [ ] Treasure chest: Effective area ≥ 96pt
  - [ ] All targets respond immediately (< 100ms)

- [ ] **Animation QA**:
  - [ ] All animations run at 60fps
  - [ ] No dropped frames
  - [ ] No jarring movements
  - [ ] Character animations loop smoothly
  - [ ] Transitions are smooth (0.3s cross-fade)
  - [ ] No flashing or strobing effects
  - [ ] Parallax is subtle and smooth

- [ ] **Voice QA**:
  - [ ] All voice triggers fire correctly
  - [ ] Voice files are correct German
  - [ ] No voice overlaps
  - [ ] Music ducks during voice (30% → 15%)
  - [ ] Music restores after voice (15% → 30%)
  - [ ] Timing is correct (2s pauses where specified)
  - [ ] Player name substitution works

- [ ] **Navigation QA**:
  - [ ] All screen transitions work
  - [ ] Back buttons function correctly
  - [ ] State persists across navigation
  - [ ] No broken navigation flows
  - [ ] Loading → PlayerSelection → Home works
  - [ ] Can return from Home to PlayerSelection

- [ ] **Performance QA**:
  - [ ] 60fps constant on all screens
  - [ ] No memory leaks
  - [ ] App launch < 2s
  - [ ] Screen transitions < 0.3s
  - [ ] Memory usage < 100MB
  - [ ] No audio glitches

- [ ] **Accessibility QA**:
  - [ ] VoiceOver labels present (German)
  - [ ] Touch targets accessible
  - [ ] Color contrast ≥ 4.5:1
  - [ ] Reduce Motion support

**Issue Tracking**:
- Document all issues found
- Prioritize by severity: Critical, High, Medium, Low
- Fix all Critical and High issues before Phase 4
- Create tickets for Medium/Low issues

**Final Sign-off**:
- [ ] All exit criteria met
- [ ] All critical/high issues resolved
- [ ] Approved for Phase 4

---

## Exit Criteria

### Functional
- [ ] All three screens render correctly
- [ ] Voice integration complete and working
- [ ] Navigation flow fully functional
- [ ] Character animations play correctly
- [ ] Audio system working (3 channels, ducking)

### Visual/Design
- [ ] Touch targets validated (all ≥ 96pt)
- [ ] Colors verified against playbook (exact match)
- [ ] Character designs validated (Bennie NO clothing, Lemminge BLUE)
- [ ] Forest backgrounds render correctly
- [ ] UI components match reference images

### Performance
- [ ] 60fps maintained on all screens
- [ ] No memory leaks
- [ ] No audio glitches
- [ ] Smooth transitions (0.3s)

### Quality
- [ ] QA pass complete
- [ ] All critical issues resolved
- [ ] Code reviewed
- [ ] Ready for Phase 4

---

## Next Phase

**Phase 4: Activities Implementation**
- Puzzle Matching game (Rätsel)
- Labyrinth game (Rätsel)
- Würfel game (Zahlen)
- Wähle die Zahl game (Zahlen)

**Dependencies for Phase 4**:
- All Phase 3 components working
- AudioManager and NarratorService ready
- Navigation system functional
- Character animations available
