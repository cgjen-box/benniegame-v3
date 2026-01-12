# ISSUES.md — Bennie und die Lemminge Issue Tracker

> **Purpose**: Track bugs, blockers, and deferred enhancements  
> **Status**: Fresh build - planning phase

---

## Active Issues

*None - project starting fresh*

---

## Planned Work (Phase Backlog)

| ID | Title | Phase | Priority | Status |
|----|-------|-------|----------|--------|
| PLAN-001 | Set up Xcode project with SwiftUI | 1 | High | ⬜ Ready |
| PLAN-002 | Implement BennieColors design system | 1 | High | ⬜ Ready |
| PLAN-003 | Create LoadingView screen | 1 | High | ⬜ Ready |
| PLAN-004 | Implement PlayerSelectionView | 2 | High | ⬜ Blocked |
| PLAN-005 | Implement HomeView (Waldabenteuer) | 2 | High | ⬜ Blocked |

---

## Deferred Enhancements

Features identified for future phases or post-MVP:

| ID | Title | Description | Phase | Priority |
|----|-------|-------------|-------|----------|
| DEFER-001 | Drawing Activity (Zeichnen) | Add drawing/tracing activity - currently marked as locked | Post-MVP | Medium |
| DEFER-002 | Logic Activity (Logik) | Add logic puzzle activity - currently marked as locked | Post-MVP | Medium |
| DEFER-003 | Auto-Difficulty Adjustment | AI-powered difficulty scaling based on child's performance patterns | Post-MVP | Low |
| DEFER-004 | Additional Lemminge Expressions | More character poses: sleeping, eating, playing, scared | Post-MVP | Low |
| DEFER-005 | Offline Mode Enhancements | Cache YouTube videos for offline playback | Post-MVP | Medium |
| DEFER-006 | Full VoiceOver Support | Complete accessibility with screen reader support | 7 | Medium |
| DEFER-007 | iPad Mini Support | Test and optimize for smaller iPad screens | Post-MVP | Low |
| DEFER-008 | iCloud Sync | Sync progress between family devices | Post-MVP | Low |
| DEFER-009 | More Voice Line Variations | Additional success phrases, hints, encouragement | Post-MVP | Low |
| DEFER-010 | Haptic Feedback | Add haptic responses for interactions | 7 | Low |
| DEFER-011 | Parent Analytics Dashboard | Detailed learning progress charts | Post-MVP | Low |
| DEFER-012 | Multiple Language Support | Add English, French options | Post-MVP | Low |

---

## Research Notes

### RESEARCH-001: ElevenLabs Voice Generation (Phase 5)

**Status**: 🔬 Needs Research Before Phase 5

**Questions to Answer**:
- [ ] Which German voices sound warm and child-friendly?
- [ ] API rate limits and pricing for ~50 voice lines
- [ ] Best settings for narrator vs Bennie character voice
- [ ] Audio format export (need AAC 44.1kHz/128kbps)
- [ ] Caching strategy for generated audio files

**Reference**: `docs/playbook/03-voice-script.md` contains full script

---

### RESEARCH-002: Autism-Friendly Game Mechanics (Phase 3)

**Status**: 🔬 Reference Available

**Key Considerations**:
- [x] Touch targets ≥96pt (documented in PLAYBOOK_CONDENSED.md)
- [x] No time pressure (no countdowns during gameplay)
- [x] Positive-only feedback (never "wrong" or "falsch")
- [x] Predictable patterns and transitions
- [x] Calm color palette (no red, no neon, saturation <80%)
- [x] No flashing or shaking animations
- [ ] Test with actual target users (Alexander, Oliver)

**Reference**: `docs/playbook/05-technical.md` has accessibility specs

---

### RESEARCH-003: YouTube API Integration (Phase 4)

**Status**: 🔬 Needs Research Before Phase 4

**Questions to Answer**:
- [ ] Use YouTubeiOSPlayerHelper vs custom WebView?
- [ ] How to hide YouTube UI completely?
- [ ] Prevent access to suggested videos
- [ ] Handle offline gracefully
- [ ] Privacy compliance for children's app

---

## Blocked Items

*None currently - Phase 1 ready to start*

---

## Resolved Issues

*None yet - fresh build*

---

## Issue Template

```markdown
### ISSUE-XXX: [Title]

**Type**: Bug / Blocker / Enhancement
**Phase**: [Phase number]
**Priority**: Critical / High / Medium / Low
**Status**: 🔴 Open / 🟡 In Progress / 🟢 Resolved

**Description**:
[Detailed description]

**Steps to Reproduce** (for bugs):
1. 
2. 
3. 

**Expected Behavior**:

**Actual Behavior**:

**Resolution**:
[How it was fixed]
```

---

*Last Updated: 2025-01-11*
