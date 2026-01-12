# Voice Integration Guide

## 📚 Playbook References

**CRITICAL: Read these playbook sections first:**
- **Part 3**: Narrator & Voice Script - COMPLETE script with all triggers, timings, and German text
- **Part 3.2**: Narrator Guidelines - Voice character, rate, max words
- **Part 3.3**: Bennie Voice Guidelines - Voice character, speech bubble behavior
- **Part 3.4**: Complete Script Reference - Every screen's voice lines organized by trigger

**Voice Production:**
- **Part 9.4**: ElevenLabs Voice Generation - Step-by-step generation workflow
- **Part 9.4 Voice Line Checklist**: Complete inventory of all 60+ voice files needed

**Audio System:**
- **Part 5.3**: Audio Specifications - Format, sample rate, bitrate requirements
- **Part 6.3**: Character Animation States - Sync voice with character expressions

**Character References:**
- `design/references/character/bennie/expressions/` - Bennie expressions to sync with voice
- `design/references/character/bennie/states/` - Bennie animation states
- Note: Voice lines should trigger appropriate Bennie expressions (e.g., "encouraging" expression during hints)

**Reference Screens:**
No specific screen references needed for Phase 6 (audio is cross-cutting concern)

---

## 🗣️ Overview

This guide shows how to integrate voice lines into each screen, following the complete script from the playbook.

## Voice Line Organization

All voice scripts are documented in **FULL_ARCHIVE.md Part 3: Narrator & Voice Script**

## Complete File Inventory Required

From the playbook Part 9.4 checklist, we need these files:

### Loading Screen
- `narrator_loading_complete.aac`

### Player Selection
- `narrator_player_question.aac`
- `narrator_hello_alexander.aac`
- `narrator_hello_oliver.aac`

### Home Screen
- `narrator_home_question.aac`
- `bennie_greeting_part1.aac`
- `bennie_greeting_part2.aac`
- `bennie_return_part1.aac`
- `bennie_return_part2.aac`
- `bennie_locked.aac`

### Puzzle Matching
- `narrator_puzzle_start.aac`
- `bennie_puzzle_start.aac`
- `bennie_puzzle_hint_10s.aac`
- `bennie_puzzle_hint_20s.aac`

### Labyrinth
- `narrator_labyrinth_start.aac`
- `bennie_labyrinth_start.aac`
- `bennie_labyrinth_wrong.aac`
- `bennie_labyrinth_hint.aac`

### Zahlen (Dice)
- `narrator_dice_start.aac`
- `narrator_show_number_1.aac` through `narrator_show_number_6.aac` (6 files)
- `bennie_wrong_number.aac`
- `bennie_dice_hint_10s.aac`
- `bennie_dice_hint_20s.aac`
- `bennie_dice_hint_30s.aac`

### Zahlen (Choose)
- `narrator_choose_number_1.aac` through `narrator_choose_number_10.aac` (10 files)
- `bennie_wrong_choose.aac`
- `bennie_choose_hint_10s.aac`
- `bennie_choose_hint_20s.aac`

### Success Pool (Shared)
- `success_super.aac`
- `success_toll.aac`
- `success_wunderbar.aac`
- `success_genau.aac`
- `success_super_gemacht.aac`

### Celebration
- `bennie_celebration_5.aac`
- `bennie_celebration_10.aac`
- `bennie_celebration_15.aac`
- `bennie_celebration_20.aac`

### Treasure
- `bennie_treasure_under10.aac`
- `bennie_treasure_over10.aac`
- `bennie_treasure_over20.aac`
- `narrator_film_ab.aac`

### Video Player
- `bennie_video_1min.aac`
- `bennie_video_timeup.aac`

## Screen-by-Screen Integration

### 1. Loading Screen

```swift
struct LoadingView: View {
    @State private var progress: CGFloat = 0.0
    @State private var hasPlayedComplete = false
    
    var body: some View {
        // ... UI ...
        .onChange(of: progress) { oldValue, newValue in
            if newValue >= 1.0 && !hasPlayedComplete {
                hasPlayedComplete = true
                AudioManager.shared.playNarrator("narrator_loading_complete.aac") {
                    // Navigate to player selection after voice completes
                    DispatchQueue.main.asyncAfter(deadline: .now() + 1) {
                        navigateToPlayerSelection()
                    }
                }
            }
        }
    }
}
```

### 2. Player Selection

```swift
struct PlayerSelectionView: View {
    @State private var hasPlayedQuestion = false
    
    var body: some View {
        // ... UI ...
        .onAppear {
            if !hasPlayedQuestion {
                hasPlayedQuestion = true
                AudioManager.shared.playNarrator("narrator_player_question.aac")
            }
        }
    }
    
    func selectPlayer(_ name: String) {
        let voiceFile = name == "alexander" ? 
            "narrator_hello_alexander.aac" : 
            "narrator_hello_oliver.aac"
        
        AudioManager.shared.playNarrator(voiceFile) {
            navigateToHome()
        }
    }
}
```

### 3. Home Screen

```swift
struct HomeView: View {
    @StateObject private var voiceSequence = VoiceSequencer()
    let isFirstVisit: Bool
    let isReturning: Bool
    
    var body: some View {
        // ... UI ...
        .onAppear {
            if isFirstVisit {
                playFirstVisitSequence()
            } else if isReturning {
                playReturnSequence()
            }
        }
    }
    
    func playFirstVisitSequence() {
        // 1. Narrator asks question
        AudioManager.shared.playNarrator("narrator_home_question.aac") {
            // 2. Bennie introduces himself
            AudioManager.shared.playBennie("bennie_greeting_part1.aac") {
                // 3. Wait 2 seconds
                DispatchQueue.main.asyncAfter(deadline: .now() + 2) {
                    // 4. Bennie explains activities
                    AudioManager.shared.playBennie("bennie_greeting_part2.aac")
                }
            }
        }
    }
    
    func playReturnSequence() {
        // 1. Bennie encourages more activities
        AudioManager.shared.playBennie("bennie_return_part1.aac") {
            // 2. Wait 2 seconds
            DispatchQueue.main.asyncAfter(deadline: .now() + 2) {
                // 3. Bennie mentions YouTube reward
                AudioManager.shared.playBennie("bennie_return_part2.aac")
            }
        }
    }
    
    func handleLockedActivity() {
        AudioManager.shared.playBennie("bennie_locked.aac")
    }
}
```

### 4. Activity Screens (Puzzle Matching Example)

```swift
struct PuzzleMatchingView: View {
    @State private var hasPlayedIntro = false
    @State private var idleTimer: Timer?
    @State private var idleSeconds = 0
    
    var body: some View {
        // ... UI ...
        .onAppear {
            playIntroSequence()
            startIdleTimer()
        }
        .onDisappear {
            stopIdleTimer()
        }
    }
    
    func playIntroSequence() {
        guard !hasPlayedIntro else { return }
        hasPlayedIntro = true
        
        // 1. Narrator gives instruction
        AudioManager.shared.playNarrator("narrator_puzzle_start.aac") {
            // 2. Bennie encourages
            AudioManager.shared.playBennie("bennie_puzzle_start.aac")
        }
    }
    
    func startIdleTimer() {
        idleTimer = Timer.scheduledTimer(withTimeInterval: 1.0, repeats: true) { _ in
            idleSeconds += 1
            
            if idleSeconds == 10 {
                AudioManager.shared.playBennie("bennie_puzzle_hint_10s.aac")
            } else if idleSeconds == 20 {
                AudioManager.shared.playBennie("bennie_puzzle_hint_20s.aac")
            }
        }
    }
    
    func stopIdleTimer() {
        idleTimer?.invalidate()
        idleTimer = nil
    }
    
    func onCellTapped() {
        // Reset idle timer on interaction
        idleSeconds = 0
    }
    
    func onSuccess() {
        stopIdleTimer()
        playSuccessPhrase()
    }
    
    func playSuccessPhrase() {
        let successPhrases = [
            "success_super.aac",
            "success_toll.aac",
            "success_wunderbar.aac",
            "success_genau.aac",
            "success_super_gemacht.aac"
        ]
        
        let random = successPhrases.randomElement()!
        AudioManager.shared.playBennie(random) {
            awardCoin()
        }
    }
}
```

### 5. Celebration Overlay

```swift
struct CelebrationOverlay: View {
    let coins: Int
    @Binding var isShowing: Bool
    @State private var hasPlayedVoice = false
    
    var body: some View {
        // ... UI ...
        .onAppear {
            if !hasPlayedVoice {
                hasPlayedVoice = true
                playMilestoneVoice()
            }
        }
    }
    
    func playMilestoneVoice() {
        let voiceFile: String
        switch coins {
        case 5:
            voiceFile = "bennie_celebration_5.aac"
        case 10:
            voiceFile = "bennie_celebration_10.aac"
        case 15:
            voiceFile = "bennie_celebration_15.aac"
        case 20:
            voiceFile = "bennie_celebration_20.aac"
        default:
            voiceFile = "bennie_celebration_5.aac" // Fallback
        }
        
        AudioManager.shared.playBennie(voiceFile)
    }
}
```

### 6. Treasure Screen

```swift
struct TreasureScreen: View {
    @EnvironmentObject var coinManager: CoinManager
    @State private var hasPlayedGreeting = false
    
    var body: some View {
        // ... UI ...
        .onAppear {
            if !hasPlayedGreeting {
                hasPlayedGreeting = true
                playGreeting()
            }
        }
    }
    
    func playGreeting() {
        let voiceFile: String
        if coinManager.currentCoins < 10 {
            voiceFile = "bennie_treasure_under10.aac"
        } else if coinManager.currentCoins >= 20 {
            voiceFile = "bennie_treasure_over20.aac"
        } else {
            voiceFile = "bennie_treasure_over10.aac"
        }
        
        AudioManager.shared.playBennie(voiceFile)
    }
    
    func handleRedemption(tier: YouTubeTier) {
        AudioManager.shared.playNarrator("narrator_film_ab.aac") {
            navigateToVideoSelection(duration: tier.duration)
        }
    }
}
```

### 7. Video Player

```swift
struct VideoPlayerView: View {
    @State private var remainingTime: TimeInterval
    @State private var hasShownWarning = false
    
    var body: some View {
        // ... UI ...
        .onChange(of: remainingTime) { oldValue, newValue in
            // 1-minute warning
            if newValue <= 60 && oldValue > 60 && !hasShownWarning {
                hasShownWarning = true
                AudioManager.shared.playBennie("bennie_video_1min.aac")
                triggerHaptic(.warning)
            }
            
            // Time up
            if newValue <= 0 {
                handleTimeUp()
            }
        }
    }
    
    func handleTimeUp() {
        AudioManager.shared.playBennie("bennie_video_timeup.aac") {
            // Navigate home after voice completes
            DispatchQueue.main.asyncAfter(deadline: .now() + 1) {
                navigateToHome()
            }
        }
    }
}
```

## VoiceSequencer Helper

For complex multi-step voice sequences:

```swift
class VoiceSequencer: ObservableObject {
    private var queue: [VoiceStep] = []
    private var isPlaying = false
    
    struct VoiceStep {
        let speaker: Speaker
        let filename: String
        let delayBefore: TimeInterval
        let completion: (() -> Void)?
    }
    
    func add(_ step: VoiceStep) {
        queue.append(step)
    }
    
    func play() {
        guard !isPlaying, !queue.isEmpty else { return }
        isPlaying = true
        playNext()
    }
    
    private func playNext() {
        guard !queue.isEmpty else {
            isPlaying = false
            return
        }
        
        let step = queue.removeFirst()
        
        DispatchQueue.main.asyncAfter(deadline: .now() + step.delayBefore) {
            switch step.speaker {
            case .narrator:
                AudioManager.shared.playNarrator(step.filename) {
                    step.completion?()
                    self.playNext()
                }
            case .bennie:
                AudioManager.shared.playBennie(step.filename) {
                    step.completion?()
                    self.playNext()
                }
            }
        }
    }
    
    func clear() {
        queue.removeAll()
        isPlaying = false
    }
}

// Usage
let sequencer = VoiceSequencer()
sequencer.add(.init(speaker: .narrator, filename: "narrator_home_question.aac", delayBefore: 0, completion: nil))
sequencer.add(.init(speaker: .bennie, filename: "bennie_greeting_part1.aac", delayBefore: 0, completion: nil))
sequencer.add(.init(speaker: .bennie, filename: "bennie_greeting_part2.aac", delayBefore: 2.0, completion: nil))
sequencer.play()
```

## Testing Voice Integration

### Manual Test Script

```
TEST 1: Loading Screen
□ Wait for progress to reach 100%
□ Hear: "Wir sind gleich bereit zum Spielen."
□ After voice completes, navigate to player selection

TEST 2: Player Selection
□ On screen appear, hear: "Wie heisst du? Alexander oder Oliver?"
□ Tap Alexander → hear: "Hallo Alexander! Los geht's!"
□ Tap Oliver → hear: "Hallo Oliver! Los geht's!"

TEST 3: Home Screen (First Visit)
□ Hear: "Was möchtest du spielen?"
□ Then: "Hi [Name], ich bin Bennie!"
□ After 2s pause: "Wir lösen Aktivitäten um YouTube zu schauen."

TEST 4: Home Screen (Return)
□ Hear: "Lösen wir noch mehr Aktivitäten."
□ After 2s pause: "Dann können wir mehr YouTube schauen!"

TEST 5: Locked Activity
□ Tap locked activity
□ Hear: "Das ist noch gesperrt."

TEST 6: Puzzle Matching
□ On start, hear: "Mach das Muster nach!"
□ Then: "Das packen wir!"
□ Wait 10s with no action → hear: "Wir können das, YouTube kommt bald."
□ Wait 20s with no action → hear: "Welche Farbe fehlt noch?"
□ Complete puzzle → hear random success phrase

TEST 7: Celebration (5 coins)
□ Hear: "Wir haben schon fünf Goldmünzen!"

TEST 8: Celebration (10 coins)
□ Hear: "Zehn Goldmünzen! Du kannst jetzt YouTube schauen."

TEST 9: Treasure (10+ coins)
□ Hear: "Wir können fünf Minuten schauen!"

TEST 10: Treasure (20+ coins)
□ Hear: "Wir können zwölf Minuten schauen!"

TEST 11: Video Redemption
□ Tap YouTube button
□ Hear: "Film ab!"

TEST 12: Video Warning
□ At 1 minute remaining, hear: "Noch eine Minute."

TEST 13: Video Time Up
□ At 0 seconds, hear: "Die Zeit ist um. Lass uns spielen!"
```

## Voice File Generation Checklist

All voice files must be generated using ElevenLabs with these settings:

```
Voice Provider: ElevenLabs
Language: German (de-DE)
Speaking Rate: 85% of normal speed
Max Words: 7 words per sentence

Narrator Voice:
- Stability: 0.75
- Similarity: 0.75
- Character: Warm, clear, neutral adult

Bennie Voice:
- Stability: 0.65
- Similarity: 0.80
- Character: Deeper, friendly, bear-like

Export Settings:
- Format: AAC
- Sample Rate: 44.1kHz
- Bitrate: 128kbps
```

See **Part 9.4** of the playbook for the complete generation workflow.
