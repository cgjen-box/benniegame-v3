# Voice Line Production with ElevenLabs

## Purpose

Complete production checklist for all narrator and Bennie voice lines in German using ElevenLabs TTS.

## Tool: ElevenLabs

**URL:** https://elevenlabs.io  
**Language:** German (de-DE)  
**Output Format:** AAC (44.1kHz, 128kbps for voice, 192kbps for music)

## Voice Selection

### Narrator Voice

| Property | Value |
|----------|-------|
| Characteristics | Clear, warm, neutral, adult |
| Gender | Neutral/ambiguous |
| Tone | Patient, encouraging, never rushed |
| Speaking Rate | 85% of default speed (-15%) |
| Stability | 0.75 |
| Similarity | 0.75 |

**Selection Criteria:**
- Warm but not overly emotional
- Clear enunciation for children
- Neutral enough for both boys to relate to
- Professional but friendly

---

### Bennie Voice

| Property | Value |
|----------|-------|
| Characteristics | Slightly deeper, bear-like, friendly |
| Gender | Male-leaning but soft |
| Tone | Encouraging buddy, excited but calm |
| Speaking Rate | 85% of default speed |
| Stability | 0.65 (allows more expressiveness) |
| Similarity | 0.80 |

**Selection Criteria:**
- Warm, bear-like quality
- Friendly and approachable
- Slightly deeper than narrator
- Expressive without being over-the-top

---

## Complete Voice Line Checklist

### LOADING SCREEN (1 file)

- [ ] **narrator_loading_complete.aac**  
  **German:** "Wir sind gleich bereit zum Spielen."  
  **English:** "We're almost ready to play."  
  **Trigger:** Progress reaches 100%  
  **Duration:** ~2s  
  **Tone:** Warm, welcoming

---

### PLAYER SELECTION (3 files)

- [ ] **narrator_player_question.aac**  
  **German:** "Wie heisst du? Alexander oder Oliver?"  
  **English:** "What's your name? Alexander or Oliver?"  
  **Trigger:** Screen appears  
  **Duration:** ~3s  
  **Tone:** Friendly question

- [ ] **narrator_hello_alexander.aac**  
  **German:** "Hallo Alexander! Los geht's!"  
  **English:** "Hello Alexander! Let's go!"  
  **Trigger:** Alexander button tapped  
  **Duration:** ~2s  
  **Tone:** Excited, welcoming

- [ ] **narrator_hello_oliver.aac**  
  **German:** "Hallo Oliver! Los geht's!"  
  **English:** "Hello Oliver! Let's go!"  
  **Trigger:** Oliver button tapped  
  **Duration:** ~2s  
  **Tone:** Excited, welcoming

---

### HOME SCREEN (6 files)

- [ ] **narrator_home_question.aac**  
  **German:** "Was möchtest du spielen?"  
  **English:** "What would you like to play?"  
  **Trigger:** First visit to home  
  **Duration:** ~2s

- [ ] **bennie_greeting_part1.aac**  
  **German:** "Hi [Name], ich bin Bennie!"  
  **English:** "Hi [Name], I'm Bennie!"  
  **Trigger:** First visit (immediately after narrator)  
  **Duration:** ~2s  
  **Tone:** Friendly introduction

- [ ] **bennie_greeting_part2.aac**  
  **German:** "Wir lösen Aktivitäten um YouTube zu schauen."  
  **English:** "We solve activities to watch YouTube."  
  **Trigger:** 2s pause after part 1  
  **Duration:** ~3s  
  **Tone:** Explaining, excited

- [ ] **bennie_return_part1.aac**  
  **German:** "Lösen wir noch mehr Aktivitäten."  
  **English:** "Let's solve more activities."  
  **Trigger:** Return from activity  
  **Duration:** ~2s

- [ ] **bennie_return_part2.aac**  
  **German:** "Dann können wir mehr YouTube schauen!"  
  **English:** "Then we can watch more YouTube!"  
  **Trigger:** 2s after part 1  
  **Duration:** ~2s  
  **Tone:** Motivating

- [ ] **bennie_locked.aac**  
  **German:** "Das ist noch gesperrt."  
  **English:** "That's still locked."  
  **Trigger:** Tap locked activity  
  **Duration:** ~1.5s  
  **Tone:** Gentle, matter-of-fact

---

### PUZZLE MATCHING (4 files)

- [ ] **narrator_puzzle_start.aac**  
  **German:** "Mach das Muster nach!"  
  **English:** "Copy the pattern!"  
  **Trigger:** Activity starts  
  **Duration:** ~2s

- [ ] **bennie_puzzle_start.aac**  
  **German:** "Das packen wir!"  
  **English:** "We've got this!"  
  **Trigger:** After narrator  
  **Duration:** ~1.5s  
  **Tone:** Encouraging

- [ ] **bennie_puzzle_hint_10s.aac**  
  **German:** "Wir können das, YouTube kommt bald."  
  **English:** "We can do this, YouTube is coming soon."  
  **Trigger:** 10s no action  
  **Duration:** ~3s  
  **Tone:** Patient encouragement

- [ ] **bennie_puzzle_hint_20s.aac**  
  **German:** "Welche Farbe fehlt noch?"  
  **English:** "Which color is still missing?"  
  **Trigger:** 20s no action  
  **Duration:** ~2s  
  **Tone:** Gentle hint

---

### LABYRINTH (4 files)

- [ ] **narrator_labyrinth_start.aac**  
  **German:** "Hilf Bennie den Weg finden!"  
  **English:** "Help Bennie find the way!"  
  **Trigger:** Activity starts  
  **Duration:** ~2s

- [ ] **bennie_labyrinth_start.aac**  
  **German:** "Wie fange ich die Lemminge?"  
  **English:** "How do I catch the Lemminge?"  
  **Trigger:** After narrator  
  **Duration:** ~2s  
  **Tone:** Curious, playful

- [ ] **bennie_labyrinth_wrong.aac**  
  **German:** "Da komme ich nicht durch."  
  **English:** "I can't get through there."  
  **Trigger:** Path goes off track  
  **Duration:** ~2s  
  **Tone:** Matter-of-fact, not frustrated

- [ ] **bennie_labyrinth_hint.aac**  
  **German:** "Wo ist der Anfang?"  
  **English:** "Where is the start?"  
  **Trigger:** 15s no action  
  **Duration:** ~1.5s  
  **Tone:** Gentle reminder

---

### ZAHLEN - WÜRFEL (Dice) (14 files)

- [ ] **narrator_dice_start.aac**  
  **German:** "Wirf den Würfel!"  
  **English:** "Roll the dice!"  
  **Trigger:** Activity starts  
  **Duration:** ~1.5s

- [ ] **narrator_show_number_1.aac**  
  **German:** "Zeig mir die eins!"  
  **Duration:** ~1.5s

- [ ] **narrator_show_number_2.aac**  
  **German:** "Zeig mir die zwei!"

- [ ] **narrator_show_number_3.aac**  
  **German:** "Zeig mir die drei!"

- [ ] **narrator_show_number_4.aac**  
  **German:** "Zeig mir die vier!"

- [ ] **narrator_show_number_5.aac**  
  **German:** "Zeig mir die fünf!"

- [ ] **narrator_show_number_6.aac**  
  **German:** "Zeig mir die sechs!"  
  **Note:** All 6 number files, same structure

- [ ] **bennie_wrong_number.aac**  
  **German:** "Das ist die [X]. Probier nochmal!"  
  **English:** "That's the [X]. Try again!"  
  **Note:** Record with placeholder, splice in numbers dynamically  
  **Trigger:** Wrong number tapped  
  **Duration:** ~2.5s

- [ ] **bennie_dice_hint_10s.aac**  
  **German:** "Zähle die Punkte."  
  **English:** "Count the dots."  
  **Trigger:** 10s no action  
  **Duration:** ~1.5s

- [ ] **bennie_dice_hint_20s.aac**  
  **German:** "Du hast die [N] gewürfelt."  
  **English:** "You rolled the [N]."  
  **Trigger:** 20s no action  
  **Duration:** ~2s

- [ ] **bennie_dice_hint_30s.aac**  
  **German:** "Wo ist die [N]?"  
  **English:** "Where is the [N]?"  
  **Trigger:** 30s no action  
  **Duration:** ~1.5s

---

### ZAHLEN - WÄHLE DIE ZAHL (Choose Number) (13 files)

- [ ] **narrator_choose_number_1.aac**  
  **German:** "Zeig mir die eins!"  
  **Duration:** ~1.5s

- [ ] **narrator_choose_number_2.aac**  
  **German:** "Zeig mir die zwei!"

- [ ] **narrator_choose_number_3.aac**  
  **German:** "Zeig mir die drei!"

- [ ] **narrator_choose_number_4.aac**  
  **German:** "Zeig mir die vier!"

- [ ] **narrator_choose_number_5.aac**  
  **German:** "Zeig mir die fünf!"

- [ ] **narrator_choose_number_6.aac**  
  **German:** "Zeig mir die sechs!"

- [ ] **narrator_choose_number_7.aac**  
  **German:** "Zeig mir die sieben!"

- [ ] **narrator_choose_number_8.aac**  
  **German:** "Zeig mir die acht!"

- [ ] **narrator_choose_number_9.aac**  
  **German:** "Zeig mir die neun!"

- [ ] **narrator_choose_number_10.aac**  
  **German:** "Zeig mir die zehn!"  
  **Note:** All 10 number files

- [ ] **bennie_wrong_choose.aac**  
  **German:** "Das ist die [X]. Probier nochmal!"  
  **Trigger:** Wrong number traced  
  **Duration:** ~2.5s

- [ ] **bennie_choose_hint_10s.aac**  
  **German:** "Der Erzähler hat [N] gesagt."  
  **English:** "The narrator said [N]."  
  **Trigger:** 10s no action  
  **Duration:** ~2s

- [ ] **bennie_choose_hint_20s.aac**  
  **German:** "Wo ist die [N]?"  
  **Trigger:** 20s no action  
  **Duration:** ~1.5s

---

### SUCCESS POOL (7 files - SHARED ACROSS ALL ACTIVITIES)

- [ ] **success_super.aac**  
  **German:** "Super!"  
  **Duration:** ~0.5s  
  **Tone:** Excited, congratulatory

- [ ] **success_toll.aac**  
  **German:** "Toll gemacht!"  
  **English:** "Well done!"  
  **Duration:** ~1s

- [ ] **success_wunderbar.aac**  
  **German:** "Wunderbar!"  
  **English:** "Wonderful!"  
  **Duration:** ~1s

- [ ] **success_genau.aac**  
  **German:** "Ja, genau!"  
  **English:** "Yes, exactly!"  
  **Duration:** ~1s

- [ ] **success_super_gemacht.aac**  
  **German:** "Das hast du super gemacht!"  
  **English:** "You did that super well!"  
  **Duration:** ~2s

- [ ] **success_perfekt.aac**  
  **German:** "Perfekt!"  
  **Duration:** ~0.5s

- [ ] **success_bravo.aac**  
  **German:** "Bravo!"  
  **Duration:** ~0.5s

**Implementation:**
```swift
let successPhrases = [
    "success_super.aac",
    "success_toll.aac",
    "success_wunderbar.aac",
    "success_genau.aac",
    "success_super_gemacht.aac",
    "success_perfekt.aac",
    "success_bravo.aac"
]

func playRandomSuccess() {
    let random = successPhrases.randomElement()!
    AudioManager.shared.playVoice(random, speaker: .bennie)
}
```

---

### CELEBRATION (4 files)

- [ ] **bennie_celebration_5.aac**  
  **German:** "Wir haben schon fünf Goldmünzen!"  
  **English:** "We already have five gold coins!"  
  **Trigger:** 5 coins milestone  
  **Duration:** ~2.5s  
  **Tone:** Excited discovery

- [ ] **bennie_celebration_10.aac**  
  **German:** "Zehn Goldmünzen! Du kannst jetzt YouTube schauen."  
  **English:** "Ten gold coins! You can watch YouTube now."  
  **Trigger:** 10 coins milestone  
  **Duration:** ~3s  
  **Tone:** Celebration + information

- [ ] **bennie_celebration_15.aac**  
  **German:** "Fünfzehn! Weiter so!"  
  **English:** "Fifteen! Keep it up!"  
  **Trigger:** 15 coins milestone  
  **Duration:** ~1.5s  
  **Tone:** Encouraging momentum

- [ ] **bennie_celebration_20.aac**  
  **German:** "Zwanzig Münzen! Du bekommst Bonuszeit!"  
  **English:** "Twenty coins! You get bonus time!"  
  **Trigger:** 20 coins milestone  
  **Duration:** ~2.5s  
  **Tone:** Extra excited

**Note:** For milestones 25, 30, 35... rotate through celebration_15.aac (generic encouragement)

---

### TREASURE SCREEN (4 files)

- [ ] **bennie_treasure_under10.aac**  
  **German:** "Wir haben [X] Münzen. Noch [Y] bis YouTube!"  
  **English:** "We have [X] coins. [Y] more until YouTube!"  
  **Trigger:** Open chest with <10 coins  
  **Duration:** ~3s  
  **Note:** Dynamic values, record template

- [ ] **bennie_treasure_over10.aac**  
  **German:** "Wir können fünf Minuten schauen!"  
  **English:** "We can watch for five minutes!"  
  **Trigger:** 10-19 coins  
  **Duration:** ~2s  
  **Tone:** Excited announcement

- [ ] **bennie_treasure_over20.aac**  
  **German:** "Wir können zwölf Minuten schauen!"  
  **English:** "We can watch for twelve minutes!"  
  **Trigger:** 20+ coins  
  **Duration:** ~2s  
  **Tone:** Very excited

- [ ] **narrator_film_ab.aac**  
  **German:** "Film ab!"  
  **English:** "Lights, camera, action!" (literal: "Film on!")  
  **Trigger:** YouTube button tapped  
  **Duration:** ~1s  
  **Tone:** Playful announcement

---

### VIDEO PLAYER (2 files)

- [ ] **bennie_video_1min.aac**  
  **German:** "Noch eine Minute."  
  **English:** "One more minute."  
  **Trigger:** 1 minute remaining  
  **Duration:** ~1.5s  
  **Tone:** Gentle warning

- [ ] **bennie_video_timeup.aac**  
  **German:** "Die Zeit ist um. Lass uns spielen!"  
  **English:** "Time's up. Let's play!"  
  **Trigger:** Video time ends  
  **Duration:** ~2s  
  **Tone:** Friendly transition

---

## Production Workflow

### For Each Voice Line:

```
1. Copy German text from checklist above
2. Log into ElevenLabs: https://elevenlabs.io
3. Select appropriate voice (Narrator or Bennie)
4. Configure settings:
   - Speaking rate: 85%
   - Stability: As specified above
   - Similarity: As specified above
5. Paste German text
6. Generate audio
7. Preview and verify:
   - Pronunciation correct?
   - Tone appropriate?
   - Duration reasonable?
   - No artifacts?
8. Download as MP3
9. Convert to AAC:
   ffmpeg -i input.mp3 -c:a aac -b:a 128k output.aac
10. Verify sample rate: 44.1kHz
11. Rename according to naming convention
12. Move to Resources/Audio/{Narrator|Bennie}/
```

---

## Naming Convention

```
{speaker}_{screen}_{trigger}.aac

Examples:
- narrator_loading_complete.aac
- bennie_celebration_10.aac
- narrator_show_number_3.aac
```

---

## Audio Specifications

| Property | Value |
|----------|-------|
| Format | AAC |
| Sample Rate | 44.1kHz |
| Bitrate | 128kbps (voice), 192kbps (music) |
| Channels | Stereo |
| Max Duration | 5 seconds per file |
| Normalization | -3dB peak |

---

## Quality Assurance

### Voice Line Checklist

For each audio file:
```
✓ Correct German pronunciation
✓ Appropriate tone for context
✓ Speaking rate is 85% (not too fast)
✓ No background noise or artifacts
✓ Duration is reasonable (not too long)
✓ Volume normalized (-3dB peak)
✓ Converted to AAC format
✓ 44.1kHz sample rate verified
✓ File named correctly
✓ File size reasonable (<500KB)
```

---

## Total Asset Count

| Category | Count |
|----------|-------|
| Loading | 1 |
| Player Selection | 3 |
| Home Screen | 6 |
| Puzzle Matching | 4 |
| Labyrinth | 4 |
| Dice (Würfel) | 14 |
| Choose Number | 13 |
| Success Pool | 7 |
| Celebration | 4 |
| Treasure | 4 |
| Video Player | 2 |
| **TOTAL** | **62 voice files** |

**Additional:**
- Background music: 1-2 loops
- Sound effects: ~10 files (tap, success chime, coin collect, etc.)

---

## Delivery Format

```
Resources/
└── Audio/
    ├── Narrator/
    │   ├── narrator_loading_complete.aac
    │   ├── narrator_player_question.aac
    │   └── ... (20 files)
    ├── Bennie/
    │   ├── bennie_greeting_part1.aac
    │   ├── bennie_celebration_10.aac
    │   └── ... (35 files)
    ├── Success/
    │   ├── success_super.aac
    │   └── ... (7 files)
    ├── Music/
    │   └── forest_ambient.aac
    └── Effects/
        ├── tap_wood.aac
        ├── success_chime.aac
        └── ... (10 files)
```

---

## Testing Integration

```swift
// Test all voice lines are present
class VoiceAssetTests: XCTestCase {
    func testAllVoiceLinesExist() {
        let requiredFiles = [
            "narrator_loading_complete",
            "narrator_player_question",
            "bennie_greeting_part1",
            // ... all 62 files
        ]
        
        for file in requiredFiles {
            let path = Bundle.main.path(forResource: file, ofType: "aac")
            XCTAssertNotNil(path, "\(file).aac is missing!")
        }
    }
    
    func testVoiceLinePlayback() {
        // Verify each file plays without errors
        AudioManager.shared.playVoice("narrator_loading_complete.aac", speaker: .narrator)
        // Wait for playback to complete
    }
}
```
