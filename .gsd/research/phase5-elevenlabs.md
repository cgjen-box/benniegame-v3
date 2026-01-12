# Research: ElevenLabs Voice Generation (Phase 5)

> **Status**: 🔬 Pre-Research  
> **Needed Before**: Phase 5 execution  
> **Estimated Research Time**: 1-2 hours

---

## Overview

The game requires ~50 German voice lines split between:
- **Narrator**: Warm, clear, neutral adult voice
- **Bennie**: Deeper, friendly, bear-like character voice

All voice lines are documented in `docs/playbook/03-voice-script.md`.

---

## Research Questions

### Voice Selection
- [ ] Which ElevenLabs German voices sound warm and child-friendly?
- [ ] Can we clone/customize a voice to sound more "bear-like"?
- [ ] What stability/similarity settings work best for children's content?

### Technical Integration
- [ ] API rate limits for batch generation (~50 lines)
- [ ] Pricing estimate for project
- [ ] Output format options (need AAC 44.1kHz/128kbps)
- [ ] ffmpeg conversion command for MP3 → AAC

### Implementation
- [ ] Generate all lines in one batch or incrementally?
- [ ] Cache strategy for audio files (bundle in app)
- [ ] File naming convention matching code expectations

---

## Voice Line Categories

| Category | Count | Speaker | Example |
|----------|-------|---------|---------|
| Loading | 1 | Narrator | "Wir sind gleich bereit zum Spielen." |
| Player Selection | 3 | Narrator | "Wie heisst du? Alexander oder Oliver?" |
| Home | 6 | Mixed | "Hi [Name], ich bin Bennie!" |
| Puzzle Matching | 6 | Mixed | "Mach das Muster nach!" |
| Labyrinth | 5 | Mixed | "Hilf Bennie den Weg finden!" |
| Zahlen | 15+ | Mixed | "Zeig mir die [N]!" (for 1-10) |
| Success Pool | 7 | Mixed | "Super!", "Toll gemacht!" |
| Celebration | 4 | Bennie | "Wir haben schon fünf Goldmünzen!" |
| Treasure | 4 | Mixed | "Du kannst jetzt YouTube schauen." |
| Video | 2 | Bennie | "Noch eine Minute.", "Die Zeit ist um." |

**Estimated Total**: ~50 unique lines

---

## ElevenLabs Settings to Test

### Narrator Voice
```
Voice: [TBD - test German voices]
Stability: 0.75 (consistent)
Similarity Boost: 0.75
Style: 0
Speaker Boost: true
Speed: 0.85 (slightly slower for children)
```

### Bennie Voice
```
Voice: [TBD - deeper German voice]
Stability: 0.65 (slight variation for character)
Similarity Boost: 0.80
Style: 0.1 (slight warmth)
Speaker Boost: true
Speed: 0.85
```

---

## Audio Conversion

After generating MP3 from ElevenLabs:

```bash
# Convert to AAC format for iOS
ffmpeg -i input.mp3 -c:a aac -b:a 128k -ar 44100 output.aac

# Batch convert all files
for f in *.mp3; do
  ffmpeg -i "$f" -c:a aac -b:a 128k -ar 44100 "${f%.mp3}.aac"
done
```

---

## File Naming Convention

```
{speaker}_{screen}_{trigger}.aac

Examples:
- narrator_loading_complete.aac
- narrator_player_question.aac
- bennie_home_greeting_part1.aac
- bennie_celebration_5coins.aac
```

---

## Cost Estimate

| Plan | Characters/month | Price | Enough? |
|------|------------------|-------|---------|
| Free | 10,000 | $0 | Maybe (short lines) |
| Starter | 30,000 | $5/mo | Yes |
| Creator | 100,000 | $22/mo | Definitely |

**Estimate**: ~50 lines × ~50 chars avg = 2,500 characters  
**Conclusion**: Free tier might work, Starter tier definitely enough

---

## Action Items Before Phase 5

1. [ ] Create ElevenLabs account
2. [ ] Test 3-5 German voices for Narrator
3. [ ] Test 3-5 German voices for Bennie
4. [ ] Generate 2-3 test lines with chosen voices
5. [ ] Verify audio quality in iOS Simulator
6. [ ] Document chosen voice IDs and settings

---

## Resources

- ElevenLabs API Docs: https://docs.elevenlabs.io/
- Voice Library: https://elevenlabs.io/voice-library
- Pricing: https://elevenlabs.io/pricing

---

*Last Updated: 2025-01-11*
