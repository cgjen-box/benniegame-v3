# Part 10: Implementation Checklist

> **Chapter 10** of the Bennie Brand Playbook
>
> Covers: Development phases, asset checklist, QA verification

---

## 10.1 Development Phase Checklist

### Phase 1: Setup

```
[ ] Create Xcode project with SwiftUI
[ ] Configure for iPad landscape only
[ ] Set up file structure per Part 8
[ ] Configure asset catalogs
[ ] Install dependencies:
    [ ] Lottie-iOS
    [ ] YouTubeiOSPlayerHelper (or custom implementation)
```

### Phase 2: Design System

```
[ ] Implement Colors.swift with all hex values
[ ] Implement Typography.swift with SF Rounded
[ ] Create WoodButton component
[ ] Create WoodSign component
[ ] Create ProgressBar component
[ ] Create NavigationHeader component
[ ] Create StoneTablet component
[ ] Create AnalogClock component
[ ] Create SpeechBubble component
[ ] Create BennieView with all expressions
[ ] Create LemmingeView with all expressions
```

### Phase 3: Core Screens

```
[ ] LoadingView
    [ ] Progress bar animation
    [ ] Bennie idle animation
    [ ] Lemminge peek animations
    [ ] Voice trigger at 100%

[ ] PlayerSelectionView
    [ ] Player cards with coin counts
    [ ] Bennie waving
    [ ] Voice interaction

[ ] HomeView
    [ ] Activity signs (4)
    [ ] Lock/unlock states
    [ ] Chest component
    [ ] Settings/help buttons
    [ ] Bennie pointing
    [ ] Lemminge hiding
```

### Phase 4: Activities

```
[ ] PuzzleMatchingView
    [ ] Dual grid display (ZIEL / DU)
    [ ] Color picker
    [ ] Pattern validation
    [ ] Difficulty progression
    [ ] Voice hints

[ ] LabyrinthView
    [ ] Path rendering
    [ ] Touch tracking
    [ ] Path validation
    [ ] Start/Goal markers

[ ] WuerfelView
    [ ] Dice animation
    [ ] Number buttons
    [ ] Voice prompts

[ ] WaehleZahlView
    [ ] Number tracing
    [ ] Trace validation
    [ ] Voice prompts
```

### Phase 5: Reward System

```
[ ] CelebrationOverlay
    [ ] Transparent overlay design
    [ ] Confetti animation
    [ ] Character celebrations
    [ ] Milestone messages

[ ] TreasureView
    [ ] Chest visualization
    [ ] YouTube buttons
    [ ] Coin counter
    [ ] Button states

[ ] VideoSelectionView
    [ ] Thumbnail grid
    [ ] Pre-approved videos only
    [ ] Time display

[ ] VideoPlayerView
    [ ] Controlled YouTube embed
    [ ] Analog clock countdown
    [ ] Time warnings
    [ ] Auto-exit on time up
```

### Phase 6: Parent Features

```
[ ] ParentGateView
    [ ] Math question generation
    [ ] Answer validation

[ ] ParentDashboardView
    [ ] Per-player settings
    [ ] Time tracking display
    [ ] Activity lock toggles

[ ] VideoManagementView
    [ ] Add video by URL
    [ ] Remove videos
    [ ] Thumbnail preview
```

### Phase 7: Audio Integration

```
[ ] AudioManager
    [ ] Three-channel system
    [ ] Voice ducking
    [ ] Volume controls

[ ] NarratorService
    [ ] Voice line playback
    [ ] Queue management

[ ] Import all voice files (see Part 9.4 checklist)
[ ] Import all sound effects
[ ] Import background music
```

### Phase 8: Testing

```
[ ] Touch target verification (>=96pt)
[ ] Color verification against hex values
[ ] Animation smoothness (60fps)
[ ] Voice timing verification
[ ] Offline mode testing
[ ] Progress persistence testing
[ ] Accessibility testing (VoiceOver)
[ ] Full playthrough test: 100 coins with YouTube watching
```

---

## 10.2 Asset Production Checklist

### Character Images

```
BENNIE:
[ ] bennie_idle.png (@2x, @3x)
[ ] bennie_waving.png (@2x, @3x)
[ ] bennie_pointing.png (@2x, @3x)
[ ] bennie_thinking.png (@2x, @3x)
[ ] bennie_encouraging.png (@2x, @3x)
[ ] bennie_celebrating.png (@2x, @3x)

LEMMINGE:
[ ] lemminge_idle.png (@2x, @3x)
[ ] lemminge_curious.png (@2x, @3x)
[ ] lemminge_excited.png (@2x, @3x)
[ ] lemminge_celebrating.png (@2x, @3x)
[ ] lemminge_hiding.png (@2x, @3x)
[ ] lemminge_mischievous.png (@2x, @3x)
```

### Lottie Animations

```
[ ] bennie_idle.json
[ ] bennie_waving.json
[ ] bennie_celebrating.json
[ ] lemminge_idle.json
[ ] lemminge_celebrating.json
[ ] confetti.json
[ ] coin_fly.json
[ ] progress_fill.json
```

---

## 10.3 QA Verification Matrix

| Screen           | Touch | Colors | Animation | Voice | Accessibility |
| ---------------- | ----- | ------ | --------- | ----- | ------------- |
| Loading          | [ ]   | [ ]    | [ ]       | [ ]   | [ ]           |
| Player Select    | [ ]   | [ ]    | [ ]       | [ ]   | [ ]           |
| Home             | [ ]   | [ ]    | [ ]       | [ ]   | [ ]           |
| Puzzle           | [ ]   | [ ]    | [ ]       | [ ]   | [ ]           |
| Labyrinth        | [ ]   | [ ]    | [ ]       | [ ]   | [ ]           |
| Würfel           | [ ]   | [ ]    | [ ]       | [ ]   | [ ]           |
| Wähle Zahl       | [ ]   | [ ]    | [ ]       | [ ]   | [ ]           |
| Celebration      | [ ]   | [ ]    | [ ]       | [ ]   | [ ]           |
| Treasure         | [ ]   | [ ]    | [ ]       | [ ]   | [ ]           |
| Video Select     | [ ]   | [ ]    | [ ]       | [ ]   | [ ]           |
| Video Player     | [ ]   | [ ]    | [ ]       | [ ]   | [ ]           |
| Parent Gate      | [ ]   | [ ]    | [ ]       | [ ]   | [ ]           |
| Parent Dashboard | [ ]   | [ ]    | [ ]       | [ ]   | [ ]           |
