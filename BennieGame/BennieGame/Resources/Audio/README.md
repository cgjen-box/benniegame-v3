# Audio Assets Directory

This directory contains all audio assets for the BennieGame app.

## Directory Structure

```
Audio/
├── Music/              # Background music (looping ambient tracks)
├── Voice/              # Voice lines
│   ├── Narrator/       # Narrator voice lines (instructions, feedback)
│   └── Bennie/         # Bennie character voice lines
├── Effects/            # Sound effects (button taps, success sounds)
├── Narrator/           # [Legacy] Narrator files
└── Bennie/             # [Legacy] Bennie character files
```

## Audio Specifications

### Voice Lines
- **Format**: AAC (.aac) preferred, MP3 (.mp3) supported
- **Bitrate**: 128kbps
- **Sample Rate**: 44.1kHz
- **Channels**: Mono

### Background Music
- **Format**: AAC (.aac) preferred
- **Bitrate**: 192kbps
- **Sample Rate**: 44.1kHz
- **Channels**: Stereo
- **Looping**: Files should be designed for seamless looping

### Sound Effects
- **Format**: AAC (.aac), WAV (.wav), or CAF (.caf)
- **Bitrate**: 128kbps (for compressed formats)
- **Sample Rate**: 44.1kHz
- **Duration**: Keep short (< 2 seconds typically)

## Naming Convention

### Voice Lines (Narrator)
```
narrator_{screen}_{action}.aac

Examples:
- narrator_loading_complete.aac
- narrator_player_question.aac
- narrator_puzzle_start.aac
- narrator_show_number_1.aac
```

### Voice Lines (Bennie)
```
bennie_{screen}_{action}.aac

Examples:
- bennie_greeting_part1.aac
- bennie_celebration_5.aac
- bennie_hint_puzzle_10s.aac
```

### Sound Effects
```
{action}_{type}.aac

Examples:
- tap_wood.aac
- success_chime.aac
- coin_collect.aac
- celebration_fanfare.aac
```

### Background Music
```
{theme}_ambient.aac

Examples:
- forest_ambient.aac
```

## AudioManager Integration

The `AudioManager` service handles all audio playback with three independent channels:

1. **Music Channel**: Background music (30% default volume, ducks to 15% during voice)
2. **Voice Channel**: Narrator and Bennie (100% volume, queued playback)
3. **Effects Channel**: Sound effects (70% volume, immediate playback)

### Usage Example

```swift
// In your view
@Environment(AudioManager.self) private var audioManager

// Play background music
audioManager.playMusic("forest_ambient")

// Play voice line (with optional completion handler)
audioManager.playVoice("narrator_puzzle_start") {
    // Voice finished playing
}

// Play sound effect
audioManager.playEffect("tap_wood")
```

## Voice Line Categories

### Loading Screen
- `narrator_loading_complete` - "Wir sind gleich bereit zum Spielen."

### Player Selection
- `narrator_player_question` - "Wie heisst du? Alexander oder Oliver?"
- `narrator_hello_alexander` - "Hallo Alexander! Los geht's!"
- `narrator_hello_oliver` - "Hallo Oliver! Los geht's!"

### Home Screen
- `narrator_home_question` - "Was moechtest du spielen?"
- `bennie_greeting_part1` - "Hi [Name], ich bin Bennie!"
- `bennie_greeting_part2` - "Wir loesen Aktivitaeten um YouTube zu schauen."

### Activities
- `narrator_puzzle_start` - "Mach das Muster nach!"
- `narrator_labyrinth_start` - "Hilf Bennie den Weg finden!"
- `narrator_dice_start` - "Wirf den Wuerfel!"

### Success Phrases (Random Pool)
- `success_super` - "Super!"
- `success_toll` - "Toll gemacht!"
- `success_wunderbar` - "Wunderbar!"
- `success_genau` - "Ja, genau!"
- `success_perfekt` - "Perfekt!"
- `success_bravo` - "Bravo!"

### Celebration
- `bennie_celebration_5` - "Wir haben schon fuenf Goldmuenzen!"
- `bennie_celebration_10` - "Zehn Goldmuenzen! Du kannst jetzt YouTube schauen."
- `bennie_celebration_15` - "Fuenfzehn! Weiter so!"
- `bennie_celebration_20` - "Zwanzig Muenzen! Du bekommst Bonuszeit!"

## Notes

- All text is in German (de-DE)
- Audio files should be added to the Xcode project target
- The AudioManager gracefully handles missing files with console warnings
- Voice lines are queued automatically if another voice is playing
