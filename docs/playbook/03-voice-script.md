# Part 3: Narrator & Voice Script

> **Chapter 3** of the Bennie Brand Playbook
>
> Covers: Voice system, narrator guidelines, complete dialogue script

---

## 3.1 Voice System Overview

The game has **two distinct voices**:

| Voice        | Role                                 | Characteristics                   |
| ------------ | ------------------------------------ | --------------------------------- |
| **Narrator** | Sets the scene, gives instructions   | Warm, clear, neutral German       |
| **Bennie**   | Buddy, helper, celebrates with child | Warm, bear-like, excited but calm |

### Voice Priority System

```swift
struct AudioManager {
    // Three independent channels
    var musicChannel: AVAudioPlayer      // Background forest ambience
    var voiceChannel: AVAudioPlayer      // Narrator + Bennie
    var effectsChannel: AVAudioPlayer    // UI sounds, celebrations

    // Default volumes
    var musicVolume: Float = 0.30
    var voiceVolume: Float = 1.00        // Always priority
    var effectsVolume: Float = 0.70

    // Voice ducking: when voice plays, music drops to 15%
    func playVoice(_ file: String, speaker: Speaker) {
        musicChannel.volume = 0.15
        voiceChannel.play(file)

        // On completion, restore music
        voiceChannel.onComplete = {
            self.musicChannel.volume = 0.30
        }
    }
}

enum Speaker {
    case narrator
    case bennie
}
```

---

## 3.2 Narrator Guidelines

| Property            | Value                              |
| ------------------- | ---------------------------------- |
| **Voice Provider**  | ElevenLabs                         |
| **Language**        | German (de-DE)                     |
| **Voice Character** | Warm, clear, adult, neutral gender |
| **Speaking Rate**   | 85% of normal speed                |
| **Max Words**       | 7 words per sentence               |
| **Tone**            | Warm, encouraging, never rushed    |

**Voice Selection**: Pick ONE voice in ElevenLabs and use consistently for all narrator lines. Never change mid-project.

---

## 3.3 Bennie Voice Guidelines

| Property            | Value                                      |
| ------------------- | ------------------------------------------ |
| **Voice Provider**  | ElevenLabs                                 |
| **Language**        | German (de-DE)                             |
| **Voice Character** | Warm, bear-like, friendly, slightly deeper |
| **Speaking Rate**   | 85% of normal speed                        |
| **Max Words**       | 7 words per sentence                       |
| **Tone**            | Excited but calm, buddy-like               |

**Bennie Speech Bubble Implementation**:
- Bennie walks into view
- Cartoon speech bubble appears
- Words appear as audio plays (typewriter style)
- NO mouth animation (cartoon style)

```swift
struct BennieSpeechView: View {
    let message: String
    @State private var displayedText = ""

    var body: some View {
        HStack(alignment: .bottom) {
            // Bennie character
            BennieView(expression: .speaking)

            // Speech bubble
            SpeechBubbleView {
                Text(displayedText)
                    .font(.sfRounded(size: 20, weight: .semibold))
            }
        }
        .onAppear {
            typewriterEffect(fullText: message)
        }
    }

    func typewriterEffect(fullText: String) {
        // Reveal text character by character synced to audio
    }
}
```

---

## 3.4 Complete Script Reference

### Loading Screen

| Speaker  | Trigger       | German                                | English (Reference)           |
| -------- | ------------- | ------------------------------------- | ----------------------------- |
| Narrator | Progress 100% | "Wir sind gleich bereit zum Spielen." | "We're almost ready to play." |

---

### Player Selection Screen

| Speaker  | Trigger          | German                                  | Notes   |
| -------- | ---------------- | --------------------------------------- | ------- |
| Narrator | Screen appears   | "Wie heisst du? Alexander oder Oliver?" | 5 words |
| Narrator | Alexander tapped | "Hallo Alexander! Los geht's!"          | 4 words |
| Narrator | Oliver tapped    | "Hallo Oliver! Los geht's!"             | 4 words |

---

### Home Screen

| Speaker  | Trigger                        | German                                         | Notes   |
| -------- | ------------------------------ | ---------------------------------------------- | ------- |
| Narrator | First visit                    | "Was möchtest du spielen?"                     | 4 words |
| Bennie   | First visit (Part A)           | "Hi [Name], ich bin Bennie!"                   | 5 words |
| Bennie   | First visit (Part B, 2s pause) | "Wir lösen Aktivitäten um YouTube zu schauen." | 7 words |
| Bennie   | Return from activity           | "Lösen wir noch mehr Aktivitäten."             | 5 words |
| Bennie   | After 2s pause                 | "Dann können wir mehr YouTube schauen!"        | 6 words |
| Bennie   | Tap locked activity            | "Das ist noch gesperrt."                       | 4 words |

---

### Rätsel: Puzzle Matching

| Speaker  | Trigger             | German                                | Notes     |
| -------- | ------------------- | ------------------------------------- | --------- |
| Narrator | Activity start      | "Mach das Muster nach!"               | 4 words   |
| Bennie   | Activity start      | "Das packen wir!"                     | 3 words   |
| —        | Correct cell tapped | *Sound effect only*                   | No voice  |
| Both     | Pattern complete    | Random from success pool              | See below |
| Bennie   | 10s no action       | "Wir können das, YouTube kommt bald." | 6 words   |
| Bennie   | 20s no action       | "Welche Farbe fehlt noch?"            | 4 words   |

---

### Rätsel: Labyrinth

| Speaker  | Trigger        | German                        | Notes     |
| -------- | -------------- | ----------------------------- | --------- |
| Narrator | Activity start | "Hilf Bennie den Weg finden!" | 5 words   |
| Bennie   | Activity start | "Wie fange ich die Lemminge?" | 5 words   |
| —        | Path started   | *Sound effect only*           | No voice  |
| Bennie   | Wrong path     | "Da komme ich nicht durch."   | 5 words   |
| Both     | Path complete  | Random from success pool      | See below |
| Bennie   | 15s no action  | "Wo ist der Anfang?"          | 4 words   |

---

### Zahlen: Würfel (Dice)

| Speaker  | Trigger        | German                              | Notes     |
| -------- | -------------- | ----------------------------------- | --------- |
| Narrator | Activity start | "Wirf den Würfel!"                  | 3 words   |
| Narrator | Dice shows N   | "Zeig mir die [N]!"                 | 4 words   |
| Both     | Correct number | Random from success pool            | See below |
| Bennie   | Wrong number   | "Das ist die [X]. Probier nochmal!" | 6 words   |
| Bennie   | 10s no action  | "Zähle die Punkte."                 | 3 words   |
| Bennie   | 20s no action  | "Du hast die [N] gewürfelt."        | 5 words   |
| Bennie   | 30s no action  | "Wo ist die [N]?"                   | 4 words   |

---

### Zahlen: Wähle die Zahl

| Speaker  | Trigger        | German                              | Notes     |
| -------- | -------------- | ----------------------------------- | --------- |
| Narrator | Activity start | "Zeig mir die [N]!"                 | 4 words   |
| Both     | Correct number | Random from success pool            | See below |
| Bennie   | Wrong number   | "Das ist die [X]. Probier nochmal!" | 6 words   |
| Bennie   | 10s no action  | "Der Erzähler hat [N] gesagt."      | 5 words   |
| Bennie   | 20s no action  | "Wo ist die [N]?"                   | 4 words   |

---

### Success Phrase Pool

```swift
let successPhrases = [
    "Super!",                        // 1 word
    "Toll gemacht!",                 // 2 words
    "Wunderbar!",                    // 1 word
    "Ja, genau!",                    // 2 words
    "Das hast du super gemacht!",    // 5 words
    "Perfekt!",                      // 1 word
    "Bravo!"                         // 1 word
]

// Randomly select one per success
func getRandomSuccessPhrase() -> String {
    successPhrases.randomElement()!
}
```

---

### Celebration Overlay

| Speaker | Trigger  | German                                              | Notes   |
| ------- | -------- | --------------------------------------------------- | ------- |
| Bennie  | 5 coins  | "Wir haben schon fünf Goldmünzen!"                  | 5 words |
| Bennie  | 10 coins | "Zehn Goldmünzen! Du kannst jetzt YouTube schauen." | 7 words |
| Bennie  | 15 coins | "Fünfzehn! Weiter so!"                              | 3 words |
| Bennie  | 20 coins | "Zwanzig Münzen! Du bekommst Bonuszeit!"            | 5 words |

---

### Treasure Screen

| Speaker  | Condition          | German                                        | Notes   |
| -------- | ------------------ | --------------------------------------------- | ------- |
| Bennie   | coins < 10         | "Wir haben [X] Münzen. Noch [Y] bis YouTube!" | 7 words |
| Bennie   | coins 10-19        | "Wir können fünf Minuten schauen!"            | 5 words |
| Bennie   | coins >= 20        | "Wir können zwölf Minuten schauen!"           | 5 words |
| Narrator | Tap YouTube button | "Film ab!"                                    | 2 words |

---

### Video Player

| Speaker | Trigger            | German                               | Notes   |
| ------- | ------------------ | ------------------------------------ | ------- |
| Bennie  | 1 minute remaining | "Noch eine Minute."                  | 3 words |
| Bennie  | Time up            | "Die Zeit ist um. Lass uns spielen!" | 6 words |
