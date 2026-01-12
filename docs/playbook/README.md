# Bennie Brand Playbook

> **Version 3.1** | Detailed specifications for Bennie und die Lemminge
>
> **Quick Reference**: Use `PLAYBOOK_CONDENSED.md` for daily work.
> **Deep Dives**: Load individual chapters below when you need full details.

---

## Table of Contents

| Chapter | File | Description |
|---------|------|-------------|
| 0 | [Game Overview](00-game-overview.md) | Philosophy, core loop, activities, reward system |
| 1 | [Brand Identity](01-brand-identity.md) | Characters, colors, typography |
| 2 | [Screen Flow](02-screen-flow.md) | State machine, transitions, coin system |
| 3 | [Voice Script](03-voice-script.md) | All narrator & Bennie dialogue |
| 4 | [Screen Specifications](04-screens/) | Detailed screen layouts (split into sub-files) |
| 5 | [Technical Requirements](05-technical-requirements.md) | Platform, assets, audio, data |
| 6 | [Animation & Sound](06-animation-sound.md) | Animation principles, character states |
| 7 | [Quick Reference](07-quick-reference.md) | One-page cheat sheet |
| 8 | [File Structure](08-file-structure.md) | Project layout |
| 9 | [Asset Pipeline](09-asset-pipeline.md) | Production workflow |
| 10 | [Implementation](10-implementation.md) | Development checklist |
| 11 | [Coding Guidelines](11-coding-guidelines.md) | SwiftUI patterns |

---

## Screen Specifications (Chapter 4)

Part 4 is split into sub-files for manageability:

| Section | File | Contents |
|---------|------|----------|
| 4.0 | [Shared Components](04-screens/README.md) | NavigationHeader, WoodButton, ProgressBar |
| 4.1-4.2 | [Loading & Player](04-screens/loading-player.md) | Loading screen, Player selection |
| 4.3-4.6 | [Home & Activities](04-screens/home-activities.md) | Home, Puzzle, Labyrinth, Numbers |
| 4.7-4.8 | [Celebration & Treasure](04-screens/celebration-treasure.md) | Celebration overlay, Treasure screen |
| 4.9-4.11 | [Video & Parent](04-screens/video-parent.md) | Video selection, Video player, Parent dashboard |

---

## Critical Design Rules

```
+--------------------------------------------------------------------+
|  BENNIE: Brown (#8C7259) - NO VEST - NO CLOTHING - EVER            |
|  LEMMINGE: Blue (#6FA8DC) - NEVER GREEN - NEVER BROWN              |
|  TOUCH TARGETS: Minimum 96pt                                        |
|  FORBIDDEN: Red, neon colors, flashing, shaking, "wrong" messages  |
|  LANGUAGE: German only, literal (no metaphors/idioms)              |
+--------------------------------------------------------------------+
```

---

## Archive

The original monolithic file is preserved at [FULL_ARCHIVE.md](FULL_ARCHIVE.md) (~38k tokens).
