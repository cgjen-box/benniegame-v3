# CLAUDE.md — Bennie Bear Learning Game

> **Framework**: GSD (Get Shit Done)
> **For**: Claude Code autonomous execution

---

## Quick Reference

| Key | Value |
|-----|-------|
| **Project** | Bennie und die Lemminge |
| **Platform** | iPad, iPadOS 17+, Landscape only |
| **Language** | German UI, Swift code |
| **Stack** | SwiftUI + SwiftData + Lottie |
| **Target Users** | Alexander (5, autism) & Oliver (4) |

---

## Critical Design Rules

```
╔══════════════════════════════════════════════════════════════════╗
║  🐻 BENNIE: Brown (#8C7259) • NO VEST • NO CLOTHING • EVER       ║
║  🔵 LEMMINGE: Blue (#6FA8DC) • NEVER GREEN • NEVER BROWN         ║
║  👆 TOUCH TARGETS: Minimum 96pt × 96pt                           ║
║  🚫 FORBIDDEN: Red, neon colors, flashing, shaking, "Falsch"     ║
║  🇩🇪 LANGUAGE: German only, literal (no metaphors/idioms)        ║
║  ✅ FEEDBACK: Positive only — never "wrong" or "error"           ║
╚══════════════════════════════════════════════════════════════════╝
```

---

## GSD Framework

This project uses the GSD framework for planning and execution.

### Key Files

| File | Purpose |
|------|---------|
| `.planning/PROJECT.md` | Project vision and core definition |
| `.planning/ROADMAP.md` | Phase breakdown (7 phases, 20 plans) |
| `.planning/STATE.md` | Current position and context |
| `PLAYBOOK_CONDENSED.md` | **Source of truth** for design rules |
| `SWIFTUI_CODING_GUIDELINES.md` | Code patterns and components |
| `DESIGN_QA_CHECKLIST.md` | Visual validation checklist |

### Key Commands

| Command | Purpose |
|---------|---------|
| `/gsd:progress` | Check current status |
| `/gsd:plan-phase N` | Plan tasks for phase N |
| `/gsd:execute-plan` | Execute current plan |
| `/gsd:research-phase N` | Research unknowns before planning |

---

## Design Validation

**Before marking ANY screen complete:**

1. Run `DESIGN_QA_CHECKLIST.md` verification
2. Check Bennie: Brown #8C7259, NO clothing
3. Check Lemminge: Blue #6FA8DC, never green/brown
4. Verify all touch targets ≥ 96pt
5. Confirm German text only, positive phrasing

---

## Reference Documents

### Design Specs
- `PLAYBOOK_CONDENSED.md` — Quick rules (read first)
- `docs/playbook/FULL_ARCHIVE.md` — Complete specification

### Screen References
- `design/references/screens/Reference_*.png` — Visual mockups (8 screens)

### Starter Kits
- `starter-kits/gemini-image-pro-3/` — Image generation
- `starter-kits/ludo-animation-pipeline/` — Lottie animations

---

## Coin Economy

| Coins | Unlocks |
|-------|---------|
| 1 | Earned per activity level completed |
| 5 | Celebration milestone (confetti, voice) |
| 10 | 5 minutes YouTube |
| 20 | 12 minutes YouTube (2 min bonus) |

---

## Activities

| Activity | Category | Status |
|----------|----------|--------|
| Puzzle Matching | Rätsel | Unlocked |
| Labyrinth | Rätsel | Unlocked |
| Würfel (Dice) | Zahlen | Unlocked |
| Wähle die Zahl | Zahlen | Unlocked |
| Zeichnen | — | Locked (MVP+) |
| Logik | — | Locked (MVP+) |

---

## Current Status

See `.planning/STATE.md` for current position.

Run `/gsd:progress` to check status and next steps.

---

## Legacy Documentation

The original detailed execution plan is preserved in `CLAUDE_ORIGINAL.md` (4420 lines).
This streamlined version works with the GSD framework for better context management.
