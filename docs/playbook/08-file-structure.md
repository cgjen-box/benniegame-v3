# Part 8: File Structure

> **Chapter 8** of the Bennie Brand Playbook
>
> Covers: Project organization and folder layout

---

## Project Structure

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
├── Resources/
│   ├── Assets.xcassets/
│   │   ├── Characters/
│   │   │   ├── Bennie/
│   │   │   │   ├── bennie_idle.imageset/
│   │   │   │   ├── bennie_waving.imageset/
│   │   │   │   ├── bennie_pointing.imageset/
│   │   │   │   ├── bennie_thinking.imageset/
│   │   │   │   ├── bennie_encouraging.imageset/
│   │   │   │   └── bennie_celebrating.imageset/
│   │   │   └── Lemminge/
│   │   │       ├── lemminge_idle.imageset/
│   │   │       ├── lemminge_curious.imageset/
│   │   │       ├── lemminge_excited.imageset/
│   │   │       ├── lemminge_celebrating.imageset/
│   │   │       ├── lemminge_hiding.imageset/
│   │   │       └── lemminge_mischievous.imageset/
│   │   ├── Backgrounds/
│   │   └── UI/
│   ├── Lottie/
│   │   ├── bennie_idle.json
│   │   ├── bennie_waving.json
│   │   ├── bennie_celebrating.json
│   │   ├── lemminge_idle.json
│   │   ├── lemminge_celebrating.json
│   │   ├── confetti.json
│   │   ├── coin_fly.json
│   │   └── progress_fill.json
│   └── Audio/
│       ├── Narrator/
│       │   ├── loading_complete.aac
│       │   ├── player_select.aac
│       │   └── ...
│       ├── Bennie/
│       │   ├── greeting.aac
│       │   ├── celebration_5.aac
│       │   └── ...
│       ├── Music/
│       │   └── forest_ambient.aac
│       └── Effects/
│           ├── tap_wood.aac
│           ├── success_chime.aac
│           ├── coin_collect.aac
│           └── ...
└── ParentDashboard/
    ├── ParentGateView.swift
    └── SettingsView.swift
```

---

## File Naming Conventions

### Swift Files
- Views: `{ScreenName}View.swift`
- Components: `{ComponentName}.swift`
- Services: `{ServiceName}Service.swift` or `{ServiceName}Manager.swift`

### Assets
- Characters: `{character}_{expression}.png`
- Lottie: `{character}_{animation}.json`
- Audio: `{speaker}_{screen}_{trigger}.aac`

### Examples
```
bennie_celebrating.png
lemminge_curious.json
narrator_loading_complete.aac
bennie_celebration_5coins.aac
```
