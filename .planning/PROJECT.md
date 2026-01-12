# PROJECT.md — Bennie Bear Learning Game

> **Core project definition. Always loaded for context.**

## Vision

**Bennie Bear** is an autism-friendly educational iPad game for children ages 4-5, specifically designed for Alexander (5, autism spectrum) and Oliver (4).

A magical forest adventure where children learn numbers, puzzles, logic, and drawing through play — earning YouTube time as rewards.

## Problem

- Neurodivergent children need learning approaches that match their needs
- Traditional educational apps are overstimulating, punitive, or confusing
- Screen time is a powerful motivator but needs structure

## Solution

A calming, journey-based learning experience in a magical forest world with:
- **Bennie the Bear** as a gentle guide (brown #8C7259, no clothing)
- **Blue Lemminge** as playful companions (#6FA8DC, never green/brown)
- **Super Forest Design** - wooden UI, warm lighting, parallax backgrounds
- **Positive-only feedback** - never "wrong", only gentle redirection
- **Coin rewards** → YouTube time exchange (10 coins = 5 min, 20 coins = 12 min)

## Target Users

| User | Description |
|------|-------------|
| **Primary** | Alexander (5, autism spectrum) and Oliver (4) |
| **Secondary** | Parents managing screen time and learning |
| **Platform** | iPad (10th gen+, landscape only, iPadOS 17+) |

## Core Principles

| Principle | Implementation |
|-----------|----------------|
| **Autism-friendly** | 96pt touch targets, no red/neon, no flashing |
| **Journey-based** | Progress through discovery, not drilling |
| **Positive only** | No "wrong", only encouragement |
| **Visual consistency** | Same characters, same world, always |
| **Predictable** | Clear patterns, gentle transitions |

## Tech Stack

| Layer | Technology |
|-------|------------|
| **Platform** | Native iPad (SwiftUI + SwiftData) |
| **Animation** | Lottie (PNG-embedded JSON) |
| **Voice** | ElevenLabs German |
| **Audio** | AVFoundation (3-channel: music, voice, effects) |
| **Build** | Xcode, MacinCloud remote |
| **Asset Generation** | Google Gemini (images), ElevenLabs (voice) |

## Non-Goals

- NOT for App Store (private family app via TestFlight)
- NOT multiplayer
- NOT cloud-synced (local device storage only)
- NOT supporting iPhone

## Success Metrics

| Metric | Target |
|--------|--------|
| Kids want to play without prompting | Observed behavior |
| No meltdowns from app frustration | Zero incidents |
| Learning happens (numbers, shapes) | Progress tracked |
| Screen time stays structured | Parent controls work |
| Full playthrough 0→100 coins | Works without crashes |

## Key Activities

| Activity | Category | Description |
|----------|----------|-------------|
| Puzzle Matching | Rätsel | Match color patterns on dual grids |
| Labyrinth | Rätsel | Trace path from START to ZIEL |
| Würfel | Zahlen | Identify dice values 1-6 |
| Wähle die Zahl | Zahlen | Select numbers 1-10 with tracing |
| Zeichnen | (Locked) | Drawing activities (future) |
| Logik | (Locked) | Logic puzzles (future) |

## Design Constraints (Critical)

```
🐻 Bennie: Brown #8C7259 — NO VEST/CLOTHING EVER
🔵 Lemminge: Blue #6FA8DC — NEVER green, NEVER brown
👆 Touch: Minimum 96pt × 96pt targets
🚫 Forbidden: Red, neon colors, flashing, shaking
🇩🇪 Language: German only, literal (no metaphors)
✅ Feedback: Positive only — never "Falsch" or "Fehler"
```

---

**Status**: 🟡 Active Development (Phase 1 Ready)
**Last Updated**: 2026-01-12
