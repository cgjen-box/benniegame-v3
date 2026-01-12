# GSD Framework - Complete Methodology

## Table of Contents

1. [Philosophy](#philosophy)
2. [Core Concepts](#core-concepts)
3. [File Specifications](#file-specifications)
4. [Task Atomicity Rules](#task-atomicity-rules)
5. [State Tracking System](#state-tracking-system)
6. [Daily Workflow](#daily-workflow)
7. [AI Collaboration Patterns](#ai-collaboration-patterns)
8. [Phase Management](#phase-management)
9. [Issue Resolution Framework](#issue-resolution-framework)
10. [Quality Gates](#quality-gates)

---

## Philosophy

### The GSD Manifesto

**We believe:**
1. Project management should be **in the code**, not in external tools
2. AI assistants should **participate** in planning, not just execute
3. Tasks should be **atomic** and **testable**, not vague goals
4. State should be **tracked**, not assumed
5. Overhead should be **minimal**, not bureaucratic

**We reject:**
- Tools that require context switching (Jira, Asana, etc.)
- Plans that AI can't read or update
- TODO comments scattered across the codebase
- "In progress" status that tells you nothing
- Meeting-driven development

### Design Goals

**Primary:**
- ✅ Single source of truth in the repository
- ✅ AI-native (Claude Code can read/write)
- ✅ Zero external dependencies
- ✅ Git-tracked with full history
- ✅ Structured but not bureaucratic

**Secondary:**
- ⚠️ Scales to small teams (3-5 people)
- ⚠️ Supports multiple workstreams
- ⚠️ Generates metrics if needed

**Non-goals:**
- ❌ Replace Jira for large teams
- ❌ Client-facing dashboards
- ❌ Time tracking or billing
- ❌ Cross-repository coordination

---

## Core Concepts

### 1. Atomic Tasks

**Definition**: A task that can be completed in <30 minutes with clear acceptance criteria.

**Good Examples:**
```markdown
**1.3** Create WoodButton component
- [ ] Create WoodButton.swift with @ViewBuilder
- [ ] Add 96pt minimum touch target
- [ ] Support icon + text layouts
- [ ] Add pressed state animation
- [ ] Test: Verify touch target size
```

**Bad Examples:**
```markdown
❌ **1.3** Implement UI
❌ **1.3** Make the app look good
❌ **1.3** Fix bugs
```

**Why Atomic?**
- AI can complete in one session
- Clear when "done"
- Easy to estimate
- Reduces scope creep

### 2. State Over Status

**Traditional PM:**
```
Task: Implement HomeView
Status: In Progress (75%)
```
*Problem*: What does 75% mean? What actually exists?

**GSD Approach:**
```markdown
## Screens
- [~] HomeView ⚠️ PARTIAL
  - [x] Activity signs (4/4)
  - [x] Chest component
  - [ ] Settings button
  - [ ] Help button
```
*Better*: You know exactly what exists and what's missing.

### 3. Next Task Discipline

**Rule**: PLAN.md always has exactly ONE "Next Task" at the top.

**Why?**
- Eliminates decision paralysis
- AI knows what to work on
- No "everything is priority 1"
- Forces explicit prioritization

**Example:**
```markdown
# Current Phase: 1 - Foundation

## Next Task (do this first)
**1.3** Create WoodButton component
- [ ] Create file
- [ ] Implement layout
- [ ] Add animation

## Remaining Tasks
**1.4** Create ProgressBar component
**1.5** Create NavigationHeader component

## Completed This Phase
✅ **1.0** Initialize git repository (2026-01-11 14:30)
✅ **1.1** Create Xcode project (2026-01-11 15:00)
✅ **1.2** Set up Colors.swift (2026-01-11 15:30)
```

### 4. Build State Reality

**Rule**: STATE.md reflects the actual build, not plans or intentions.

**Good STATE.md:**
```markdown
## Screens
- [x] LoadingView ✅ COMPLETE
  - Progress bar works
  - Voice trigger at 100%
  - Tested on iPad
  
- [~] HomeView ⚠️ PARTIAL
  - Activity signs present
  - Missing: Settings button
  - Blocker: See ISSUES.md #12
  
- [ ] GameView ❌ NOT STARTED
```

**Bad STATE.md:**
```markdown
❌ LoadingView (almost done)
❌ HomeView (working on it)
❌ GameView (planned for tomorrow)
```

---

## File Specifications

### PROJECT.md

**Purpose**: One-page project vision and scope

**Template:**
```markdown
# Project: [Name]

## Vision
[1-2 paragraphs: What you're building and why it matters]

## Success Criteria
- [ ] Criterion 1 (measurable)
- [ ] Criterion 2 (testable)
- [ ] Criterion 3 (clear)

## Not Building (Scope Boundaries)
- Feature X (maybe v2)
- Platform Y (out of scope)
- Integration Z (too complex)

## Tech Stack
- Language: Swift
- Framework: SwiftUI
- Platform: iPadOS 17+
- Tools: Xcode 15+

## Timeline Estimate
- Development: 40-50 hours
- Testing: 10-15 hours
- Polish: 5-10 hours
- **Total**: 55-75 hours over 3-4 weeks

## Team
- Solo developer + Claude Code assistant

## Risks
1. **Risk**: API rate limits
   **Mitigation**: Batch requests, cache results
   
2. **Risk**: Scope creep
   **Mitigation**: Strict "Not Building" list
```

**Update Frequency**: Rarely (only when scope changes)

**Who Updates**: You (manually)

---

### ROADMAP.md

**Purpose**: High-level phase breakdown

**Structure:**
```markdown
# Project Roadmap

## Overview
7 phases | Estimated 45-60 hours total

## Phase 1: Foundation (4-6 hours)
Set up project structure and design system

**Deliverables:**
- Xcode project configured
- Design system (colors, typography)
- LoadingView implemented
- PlayerSelectionView implemented

**Exit Criteria:**
- [ ] App launches without crashes
- [ ] Design system in place
- [ ] First 2 screens working
- [ ] Colors match brand guide exactly

---

## Phase 2: Core Screens (6-8 hours)
Implement main navigation and structure

**Deliverables:**
- HomeView with activity selection
- Activity selection screens
- Navigation system

**Exit Criteria:**
- [ ] User can navigate all screens
- [ ] Touch targets >= 96pt
- [ ] No placeholder content

[... more phases ...]

---

## Milestones

- **Alpha** (Phase 1-3): Core functionality | Week 1
- **Beta** (Phase 4-6): Full features | Week 2-3
- **RC** (Phase 7-8): Polish & testing | Week 4
```

**Rules:**
- Each phase has time estimate
- Clear deliverables (nouns, not verbs)
- Testable exit criteria
- Phases build on each other (dependencies clear)

**Update Frequency**: Rarely (milestone structure is stable)

**Who Updates**: You (manually)

---

### PLAN.md

**Purpose**: Current phase atomic task list

**Structure:**
```markdown
# Current Phase: [N] - [Name]

[Brief phase description from ROADMAP]

---

## Next Task (do this first)
**[N.X]** [Task name]
- [ ] Atomic step 1
- [ ] Atomic step 2
- [ ] Atomic step 3
- [ ] Test: [specific test]

**Context**: [Why this task, any background]
**Files**: [Which files will be modified]
**Dependencies**: [What must exist first]

---

## Remaining Tasks

**[N.Y]** [Task name]
**[N.Z]** [Task name]
**[N.A]** [Task name]

---

## Completed This Phase

✅ **[N.B]** [Task name] (2026-01-11 14:30)
✅ **[N.C]** [Task name] (2026-01-11 15:00)

---

## Phase Progress

- Tasks completed: 2/8
- Estimated remaining: 4-6 hours
- On track for phase exit criteria: ✅ YES
```

**Numbering:**
- Format: `Phase.Task` (e.g., `1.3`, `2.5`)
- Sequential within phase
- Skipped numbers OK (don't renumber)

**Task Anatomy:**
- Name: Clear, specific action
- Checkboxes: Atomic steps
- Test: How to verify completion
- Context: Why this matters
- Files: Scope preview

**Update Rules:**
- ✅ When task complete: Move to "Completed", add timestamp
- ✅ Update "Next Task": Pull from "Remaining Tasks"
- ✅ New tasks: Can add to "Remaining Tasks" as discovered
- ❌ Don't delete: Keep completed tasks for history

**Update Frequency**: Multiple times per day

**Who Updates**: You + Claude Code (collaborative)

---

### STATE.md

**Purpose**: Accurate build inventory

**Structure:**
```markdown
# Build State

*Last updated: 2026-01-11 16:45*

---

## Screens

### ✅ COMPLETE
- [x] LoadingView
  - Progress bar animation
  - Voice trigger at 100%
  - Bennie idle animation
  - All lemminge expressions
  - Tested on iPad 10th gen

### ⚠️ PARTIAL
- [~] HomeView
  - ✅ Activity signs (4/4) with correct colors
  - ✅ Chest component with coin counter
  - ✅ Bennie pointing animation
  - ❌ Settings button missing
  - ❌ Help button missing
  - ⚠️ Touch targets not all verified

### ❌ NOT STARTED
- [ ] GameView
- [ ] TreasureView
- [ ] VideoPlayerView

---

## Components

### ✅ COMPLETE
- [x] WoodButton (96pt minimum, tested)
- [x] ProgressBar (coin slots working)
- [x] WoodSign (rope mounting, tested)

### ⚠️ PARTIAL
- [~] NavigationHeader
  - ✅ Home button
  - ❌ Volume button not wired

### ❌ NOT STARTED
- [ ] AnalogClock
- [ ] SpeechBubble
- [ ] StoneTablet

---

## Services

### ✅ COMPLETE
- [x] AudioManager (3-channel, ducking works)
- [x] PlayerDataStore (saving/loading tested)

### ⚠️ PARTIAL
- [~] GameStateManager
  - ✅ State transitions work
  - ❌ Celebration logic buggy

### ❌ NOT STARTED
- [ ] YouTubeService
- [ ] NetworkMonitor

---

## Assets

### ✅ COMPLETE
- [x] Character images (12/12)
  - Bennie: 6 poses @ 2x, 3x
  - Lemminge: 6 expressions @ 2x, 3x
  
- [x] Voice files (25/80)
  - Narrator: Loading, Player Select
  - Bennie: Greetings, Celebrations
  
### ⚠️ PARTIAL
- [~] Lottie animations (2/8)
  - ✅ bennie_idle.json
  - ✅ confetti.json
  - ❌ 6 more needed

### ❌ NOT STARTED
- [ ] Sound effects (0/12)
- [ ] Background music

---

## Known Issues
*(Link to ISSUES.md for details)*

- [HIGH] Touch target too small on Settings (#5)
- [MED] Celebration overlay doesn't dismiss (#8)

---

## Test Coverage

- Screens: 2/10 tested (20%)
- Components: 3/8 tested (37%)
- Services: 2/5 tested (40%)

**Next to test**: HomeView, NavigationHeader
```

**Status Definitions:**
- ✅ `[x]` COMPLETE: Implemented + tested + works
- ⚠️ `[~]` PARTIAL: Partially done (specify what's missing)
- ❌ `[ ]` NOT STARTED: No code written yet

**Update Rules:**
- Update immediately after implementing something
- Be brutally honest (reality, not hopes)
- Specify what's missing in PARTIAL items
- Link to ISSUES.md for blockers

**Update Frequency**: Continuous (after every meaningful change)

**Who Updates**: Claude Code (automated), you verify

---

### SUMMARY.md

**Purpose**: Daily progress journal

**Structure:**
```markdown
# Daily Progress Log

## 2026-01-11 - Phase 1: Foundation

### Completed Today
- ✅ **1.0** Initialize git repository
- ✅ **1.1** Create Xcode project
- ✅ **1.2** Implement Colors.swift
- ✅ **1.3** Create WoodButton component

### Started (Not Finished)
- ⚠️ **1.4** Create ProgressBar component
  - Progress: 75% done
  - Remaining: Coin slot animation
  - Blocked: Waiting for Lottie file

### Blockers Resolved Today
1. **Xcode build error** (Issue #3)
   - Problem: Missing Info.plist key
   - Solution: Added UIRequiresFullScreen = true
   - Time lost: 30 minutes

2. **Color hex values wrong** (Issue #7)
   - Problem: #8C7259 rendered too dark
   - Solution: Color space was sRGB not Display P3
   - Time lost: 15 minutes

### Discoveries / Learnings
- Insight: SF Symbols don't scale well below 16pt
- Gotcha: Lottie animations need explicit content mode
- TIL: iPad simulator runs slower than device

### Metrics
- Hours worked: 4.5
- Tasks completed: 4
- Blockers hit: 2
- Phase progress: 4/8 tasks (50%)

### Next Session Plan
- [ ] Complete task 1.4 (ProgressBar)
- [ ] Start task 1.5 (NavigationHeader)
- [ ] If time: Begin task 1.6

### Energy / Focus
- Morning: ⚡⚡⚡ High (got 4 tasks done)
- Afternoon: ⚡⚡ Medium (hit blocker, researched)

---

## 2026-01-10 - Phase 1: Foundation

[Previous day...]
```

**Daily Entry Template:**
```markdown
## [DATE] - Phase [N]: [Name]

### Completed Today
- ✅ Task X
- ✅ Task Y

### Started (Not Finished)
- ⚠️ Task Z (progress, remaining, blocker)

### Blockers Resolved Today
1. **Title**
   - Problem:
   - Solution:
   - Time lost:

### Discoveries / Learnings
- Insight:
- Gotcha:
- TIL:

### Metrics
- Hours worked:
- Tasks completed:
- Phase progress:

### Next Session Plan
- [ ] Top priority
- [ ] Second priority

### Energy / Focus
- Morning: ⚡⚡⚡
- Afternoon: ⚡⚡
```

**Update Rules:**
- Add entry at end of each work session
- Be honest about progress (don't exaggerate)
- Capture learnings (for future reference)
- Note energy patterns (optimize schedule)

**Update Frequency**: Daily (end of session)

**Who Updates**: You (manually), Claude can help draft

---

### ISSUES.md

**Purpose**: Active blocker and question tracking

**Structure:**
```markdown
# Active Issues

---

## [HIGH] Celebration overlay doesn't dismiss

**ID**: #8  
**Status**: BLOCKED  
**Priority**: HIGH  
**Task**: 5.2 - Implement celebration overlay  
**Phase**: 5 - Reward System

**Problem:**
After tapping "Weiter" button, overlay remains on screen. No console errors. Button tap is registered (see logs) but view doesn't dismiss.

**Context:**
- Overlay appears correctly at 5-coin milestones
- Animation plays fine
- Button is pressable (haptic works)
- Dismiss function is called but view persists

**What We Tried:**
1. ✅ Verified button action is called (added print statement)
2. ✅ Checked if overlay has wrong zIndex (tested changing values)
3. ✅ Tried .sheet instead of .overlay (same result)
4. ❌ Checked for retain cycle (none found, but not 100% sure)

**Hypothesis:**
Possibly a SwiftUI state binding issue. The @State variable that controls visibility might not be propagating correctly.

**Next Steps:**
1. Review state management pattern
2. Try using @Binding instead of @State
3. Test with simpler overlay first
4. If still stuck: Ask on Swift forums

**Research:**
- Similar issue: https://stackoverflow.com/q/12345
- Apple docs: sheet() vs overlay()

**Time Impact:**
- Blocked since: 2026-01-11 14:00
- Time lost: 2 hours
- Phase delay: 0.5 days

**Created**: 2026-01-11 14:30

---

## [MED] Touch target verification needed

**ID**: #12  
**Status**: NEEDS RESEARCH  
**Priority**: MEDIUM  
**Task**: Multiple  
**Phase**: 1 - Foundation

**Problem:**
Need systematic way to verify all touch targets are >= 96pt. Manual checking is error-prone.

**Context:**
- Brand playbook requires 96pt minimum
- Critical for autism-friendly design
- Many buttons already created
- No automated verification yet

**What We Tried:**
1. ✅ Manual measurement with Xcode inspector (tedious)
2. ❌ Looking for Xcode accessibility scanner (doesn't check size)

**Hypothesis:**
Could write SwiftUI view modifier that draws debug overlay showing touch target size.

**Next Steps:**
1. Research SwiftUI layout protocols
2. Create TouchTargetDebug view modifier
3. Apply to all buttons
4. Run through all screens

**Priority Rationale:**
Not blocking current work, but needed before TestFlight. Can be done in Phase 8 (Polish).

**Created**: 2026-01-10 16:00

---

## [LOW] Lottie file optimization

**ID**: #15  
**Status**: INVESTIGATING  
**Priority**: LOW  
**Task**: 9.3 - Export Lottie animations  
**Phase**: 9 - Asset Production

**Problem:**
confetti.json is 250KB, should be <100KB per guideline.

**Context:**
- File works but is large
- Affects app download size
- Not blocking functionality

**What We Tried:**
1. ✅ Checked Lottie compression settings (maxed out)
2. ❌ Looking for post-processing tool

**Next Steps:**
1. Research lottie-web compression
2. Try reducing particle count
3. Consider sprite sheet alternative

**Priority Rationale:**
Nice-to-have optimization, not critical path.

**Created**: 2026-01-09 11:00

---

# Resolved Issues

## [HIGH] Xcode project won't build (RESOLVED)

**ID**: #3  
**Status**: ✅ RESOLVED  
**Task**: 1.1 - Create Xcode project  
**Resolved**: 2026-01-11 10:30

**Problem:**
Build failed with "Info.plist missing required keys" error.

**Solution:**
Added UIRequiresFullScreen = true to Info.plist. This is required for iPad landscape-only apps.

**Prevention:**
Added to project template checklist.

**Time Impact:**
- Time lost: 30 minutes
- Resolved by: Manual research + Stack Overflow

---

## [MED] Colors rendering wrong (RESOLVED)

**ID**: #7  
**Status**: ✅ RESOLVED  
**Task**: 1.2 - Implement Colors.swift  
**Resolved**: 2026-01-11 11:45

**Problem:**
Hex color #8C7259 (Bennie brown) appeared too dark on device.

**Solution:**
Color was in sRGB space, needed Display P3. Changed Color initialization:
```swift
// Before
Color(hex: "8C7259")

// After  
Color(hex: "8C7259", colorSpace: .displayP3)
```

**Prevention:**
Updated Colors.swift template with colorSpace parameter.

**Time Impact:**
- Time lost: 15 minutes
- Resolved by: Claude Code research

---
```

**Issue Priorities:**
- **HIGH**: Blocks current work, needs immediate resolution
- **MEDIUM**: Important but has workaround or not blocking
- **LOW**: Nice-to-have, can defer to polish phase

**Status Values:**
- **BLOCKED**: Cannot proceed, need external help
- **INVESTIGATING**: Actively researching solution
- **NEEDS RESEARCH**: Understand problem, need to research options
- **RESOLVED**: Fixed (move to "Resolved Issues")

**Update Rules:**
- Create issue when stuck >30 minutes
- Update as you try solutions
- Resolve when fixed (don't delete)
- Link from STATE.md when relevant

**Update Frequency**: As needed (when stuck or resolved)

**Who Updates**: You + Claude Code (collaborative)

---

## Task Atomicity Rules

### Definition
An **atomic task** is completable in one focused session (<30 min) with clear success criteria.

### Atomic Task Checklist
```
✅ Has a clear action verb?
✅ Specifies what files to create/modify?
✅ Includes acceptance criteria?
✅ Can be completed in <30 minutes?
✅ Has no hidden dependencies?
✅ Is testable/verifiable?
```

### Examples

**❌ TOO VAGUE:**
```markdown
**2.3** Implement game logic
```
*Problem*: What game? What logic? When is it done?

**❌ TOO BROAD:**
```markdown
**2.3** Create entire reward system
- [ ] Celebration overlay
- [ ] Treasure screen
- [ ] Video player
- [ ] Coin tracking
```
*Problem*: This is 4+ hours of work, should be 4 separate tasks.

**❌ NO CRITERIA:**
```markdown
**2.3** Make HomeView look better
```
*Problem*: Subjective, no way to verify completion.

**✅ ATOMIC:**
```markdown
**2.3** Create WoodButton component
- [ ] Create WoodButton.swift
- [ ] Implement init(text:icon:action:)
- [ ] Add wood texture background gradient
- [ ] Enforce 96pt minimum touch target
- [ ] Test: Tap on iPad, verify size with inspector
```
*Good*: Specific file, clear steps, testable, <30 min.

**✅ ATOMIC:**
```markdown
**3.7** Implement coin fly animation
- [ ] Create CoinFlyView SwiftUI view
- [ ] Use .offset animation along arc path
- [ ] Duration: 0.8s with ease-in-out
- [ ] Test: Trigger from PuzzleView, coin reaches progress bar
```
*Good*: One animation, clear parameters, testable.

### Breaking Down Large Tasks

**Original (too big):**
```markdown
**5.0** Implement celebration system
```

**Broken down (atomic):**
```markdown
**5.1** Create CelebrationOverlay component
- [ ] Create CelebrationOverlay.swift
- [ ] Add transparent cream background (90% opacity)
- [ ] Position Bennie celebrating sprite
- [ ] Add "Weiter" button
- [ ] Test: Overlay appears over GameView

**5.2** Add confetti animation
- [ ] Import confetti.json Lottie file
- [ ] Create LottieView wrapper
- [ ] Trigger on overlay appear
- [ ] Duration: 3 seconds, no loop
- [ ] Test: Confetti plays then stops

**5.3** Wire celebration to coin milestones
- [ ] Add celebrationShouldShow computed property
- [ ] Check: coins % 5 == 0
- [ ] Present CelebrationOverlay when true
- [ ] Pass current coin count to overlay
- [ ] Test: Complete activity at 5 coins, overlay appears

**5.4** Add voice line to celebration
- [ ] Import bennie_celebration_5.aac
- [ ] Trigger on overlay appear
- [ ] Music ducks to 15% during voice
- [ ] Test: Voice plays, music ducks, music returns
```

### Task Numbering

**Format**: `Phase.Task`

**Examples:**
- `1.0`, `1.1`, `1.2` - Phase 1 tasks
- `2.0`, `2.1`, `2.2` - Phase 2 tasks

**Rules:**
- Sequential within phase
- Don't renumber when tasks complete
- Gaps are OK if you remove/skip tasks
- Subtasks use letters: `2.3a`, `2.3b` (avoid if possible)

---

## State Tracking System

### Status Definitions

**✅ COMPLETE** (`[x]`)
- Implemented fully
- Tested manually
- Works as expected
- No known bugs
- Meets acceptance criteria

**⚠️ PARTIAL** (`[~]`)
- Some functionality working
- Missing features (specify which)
- Has known bugs (link to ISSUES.md)
- Not ready for production

**❌ NOT STARTED** (`[ ]`)
- No code written yet
- Planned but not begun
- May have design docs

### State Update Workflow

```
1. Start task from PLAN.md
   └─→ No STATE.md change yet

2. Write code, implement feature
   └─→ Still no STATE.md change

3. Feature works, test passes
   └─→ NOW update STATE.md to [x] COMPLETE

4. Discover bug or missing piece
   └─→ Downgrade STATE.md to [~] PARTIAL
   └─→ Create ISSUES.md entry

5. Fix bug, feature complete
   └─→ Upgrade STATE.md to [x] COMPLETE
```

### State Update Example

**After completing WoodButton:**

```markdown
## Components

### ✅ COMPLETE
- [x] WoodButton
  - Supports text + icon layouts
  - 96pt minimum touch target enforced
  - Pressed state animation (scale 0.95)
  - Wood texture gradient applied
  - Tested on iPad 10th gen
  - File: Components/WoodButton.swift
```

**After discovering button bug:**

```markdown
## Components

### ⚠️ PARTIAL
- [~] WoodButton
  - ✅ Supports text + icon layouts
  - ✅ 96pt minimum touch target enforced
  - ❌ Pressed state animation broken (see Issue #18)
  - ✅ Wood texture gradient applied
  - ⚠️ Touch target not verified on iPad Pro size
  - File: Components/WoodButton.swift
```

### Testing Status

Include test coverage in STATE.md:

```markdown
## Test Coverage

### Screens
- LoadingView: ✅ Tested (manual + XCTest)
- HomeView: ⚠️ Partial (manual only)
- GameView: ❌ Not tested

### Components
- WoodButton: ✅ Tested (unit + manual)
- ProgressBar: ⚠️ Partial (manual only)
- AnalogClock: ❌ Not tested

### Coverage Summary
- Screens: 1/3 fully tested (33%)
- Components: 1/3 fully tested (33%)
- Services: 0/3 fully tested (0%)

**Next to test**: HomeView, ProgressBar
```

---

## Daily Workflow

### Morning (Session Start)

**1. Review where you left off**
```bash
cat .gsd/SUMMARY.md | tail -30
```

**2. Check what's next**
```bash
cat .gsd/PLAN.md | head -40
```

**3. Review any blockers**
```bash
cat .gsd/ISSUES.md | head -50
```

**4. Start work on Next Task**
```bash
# Tell Claude
"Claude, let's work on task 1.3 from PLAN.md"
```

### During Work (Task Execution)

**Completing atomic steps:**
```
1. Complete a checkbox in task
   ↓
2. Test it works
   ↓
3. Tell Claude to update STATE.md
   ↓
4. Commit
```

**Example dialog:**
```
You: "Claude, I just finished the WoodButton implementation"

Claude: "Great! I'll update STATE.md to mark WoodButton as complete."
[Claude updates STATE.md]

You: "Verify the changes look correct"
git diff .gsd/STATE.md

You: "Good. Commit it."
git add Components/WoodButton.swift .gsd/STATE.md
git commit -m "Task 1.3: WoodButton component"
```

### Hitting a Blocker

**When stuck >30 minutes:**

1. **Create issue in ISSUES.md**
   ```
   "Claude, add a HIGH priority issue to ISSUES.md:
   - Problem: Overlay won't dismiss
   - Task: 5.2
   - What we tried: [...list...]
   ```

2. **Switch to different task**
   ```
   "Claude, move task 5.2 to a 'Blocked' section in PLAN.md.
   What's the next unblocked task we can work on?"
   ```

3. **Research solution**
   - Google, Stack Overflow, docs
   - Update ISSUES.md with findings
   - If solved: resolve issue, resume task

### Evening (Session End)

**1. Update SUMMARY.md**
```
"Claude, create today's entry in SUMMARY.md:
- Completed tasks 1.3, 1.4
- Started 1.5 (75% done)
- Hit blocker on Issue #8
- 4 hours worked today"
```

**2. Review progress**
```bash
cat .gsd/SUMMARY.md | tail -30
cat .gsd/PLAN.md | grep "✅"
```

**3. Plan tomorrow**
```
"Claude, what should we tackle tomorrow?"
[Claude reviews PLAN.md, suggests priorities]
```

**4. Commit daily wrap**
```bash
git add .gsd/
git commit -m "Daily wrap 2026-01-11: Phase 1 progress"
```

### Weekly (Phase Review)

**Friday end-of-week:**

1. **Review phase progress**
   ```bash
   cat .gsd/PLAN.md
   ```

2. **Check if phase exit criteria met**
   ```bash
   cat .gsd/ROADMAP.md
   ```

3. **Decide: Continue phase or move to next?**
   - If ready: Start Phase N+1
   - If not: Identify what's blocking

4. **Update ROADMAP.md**
   ```markdown
   ## Phase 1: Foundation ✅ COMPLETE (2026-01-15)
   
   ## Phase 2: Core Screens 🔄 IN PROGRESS
   ```

---

## AI Collaboration Patterns

### Claude Code as Active Participant

**Good patterns:**

```
✅ "Claude, check PLAN.md and tell me what's next"
✅ "Claude, update STATE.md after completing WoodButton"
✅ "Claude, summarize today's progress in SUMMARY.md"
✅ "Claude, create an issue for this blocker"
✅ "Claude, review ROADMAP and estimate time remaining"
```

**Anti-patterns:**

```
❌ "Update the plan" (which file?)
❌ "Mark that as done" (mark what where?)
❌ "Add a blocker" (where? what details?)
```

### Delegation Examples

**Task completion:**
```
You: "I just finished implementing the ProgressBar"

Claude: "Great! Let me update STATE.md and PLAN.md."
[Updates files]

Claude: "I've marked task 1.4 complete and moved 1.5 to Next Task.
The ProgressBar is now showing as ✅ COMPLETE in STATE.md.
Ready to start task 1.5?"
```

**Blocker hit:**
```
You: "I've been stuck on this overlay issue for an hour"

Claude: "Let me create an issue in ISSUES.md for tracking."
[Creates issue #8]

Claude: "Created Issue #8 (HIGH priority). I can see tasks 1.6 and 1.7
aren't blocked. Should we pivot to one of those while we research this?"
```

**Progress check:**
```
You: "Claude, where are we in Phase 1?"

Claude: "Looking at PLAN.md:
- Completed: 4 tasks
- Next: Task 1.5
- Remaining: 3 tasks
- Estimate: 2-3 hours to phase completion

STATE.md shows:
- Screens: 2/4 complete
- Components: 3/6 complete
- You're on track for phase exit criteria."
```

### Review Patterns

**Always verify AI updates:**
```bash
# After Claude updates GSD files
git diff .gsd/

# Check changes make sense
# If good: git add .gsd/ && git commit -m "..."
# If wrong: git checkout .gsd/ (revert)
```

**Teach Claude your preferences:**
```
You: "Claude, when marking tasks complete, always add timestamp"
Claude: "Got it. I'll add timestamps like: ✅ Task 1.3 (2026-01-11 14:30)"

You: "Claude, in STATE.md, always link to source files"
Claude: "Understood. I'll add file paths like: File: Components/WoodButton.swift"
```

---

## Phase Management

### Starting a Phase

**1. Review ROADMAP.md for phase details**
```markdown
## Phase 2: Core Screens (6-8 hours)
Implement main navigation screens

**Deliverables:**
- HomeView with activity selection
- Activity selection screens
- Navigation system

**Exit criteria:**
- [ ] All screens navigable
- [ ] Touch targets >= 96pt
- [ ] No placeholder content
```

**2. Create PLAN.md for phase**

Break deliverables into atomic tasks:
```markdown
# Current Phase: 2 - Core Screens

## Next Task
**2.0** Create HomeView structure
- [ ] Create HomeView.swift
- [ ] Add title "Waldabenteuer"
- [ ] Create 4 activity sign buttons
- [ ] Position using coordinates from playbook
- [ ] Test: All buttons appear correctly

## Remaining Tasks
**2.1** Implement activity sign states
**2.2** Add chest component
**2.3** Wire navigation to activity selection
**2.4** Create activity selection template
**2.5** Implement Rätsel selection screen
**2.6** Implement Zahlen selection screen
**2.7** Add navigation back buttons
**2.8** Test full navigation flow
```

**3. Update STATE.md with new trackable items**
```markdown
## Screens (Phase 2 additions)

### ❌ NOT STARTED
- [ ] HomeView
- [ ] RätselSelectionView
- [ ] ZahlenSelectionView
```

**4. Commit phase start**
```bash
git add .gsd/
git commit -m "Phase 2 start: Core screens"
```

### During a Phase

**Steady progress pattern:**
```
1. Work on Next Task
2. Complete task
3. Update PLAN.md (mark complete, move next)
4. Update STATE.md (reflect reality)
5. Commit
6. Repeat
```

**If blocked:**
```
1. Create ISSUES.md entry
2. Mark task as blocked in PLAN.md
3. Switch to unblocked task
4. Research/resolve blocker
5. Return to blocked task
```

**If scope changes:**
```
1. Add new tasks to PLAN.md "Remaining Tasks"
2. Update ROADMAP.md if deliverables change
3. Re-estimate time remaining
4. Communicate change (if team project)
```

### Completing a Phase

**1. Verify exit criteria from ROADMAP.md**
```markdown
**Exit Criteria:**
- [x] All screens navigable ✅
- [x] Touch targets >= 96pt ✅
- [x] No placeholder content ✅
```

**2. Check STATE.md reality matches**
```markdown
## Screens
- [x] HomeView ✅ COMPLETE
- [x] RätselSelectionView ✅ COMPLETE
- [x] ZahlenSelectionView ✅ COMPLETE

## Components
- [x] ActivitySign ✅ COMPLETE
- [x] NavigationHeader ✅ COMPLETE
```

**3. Update ROADMAP.md**
```markdown
## Phase 1: Foundation ✅ COMPLETE (2026-01-15)

## Phase 2: Core Screens ✅ COMPLETE (2026-01-18)

## Phase 3: Activities - Rätsel 🔄 STARTING
```

**4. Archive PLAN.md**
```bash
# Save completed phase plan
cp .gsd/PLAN.md .gsd/archive/PLAN-phase2.md

# Create new PLAN.md for Phase 3
# (copy Phase 3 tasks from ROADMAP)
```

**5. Commit phase completion**
```bash
git add .gsd/
git commit -m "Phase 2 complete: All core screens working"
```

### Phase Velocity Tracking

Track actual vs estimated time:

```markdown
## Phase Completion History

| Phase | Estimated | Actual | Variance | Notes |
|-------|-----------|--------|----------|-------|
| 1     | 4-6h      | 5.5h   | ✅ Good   | On track |
| 2     | 6-8h      | 9h     | ⚠️ Over  | Blocker added 2h |
| 3     | 8-10h     | ?      | ...      | In progress |
```

Use this to improve future estimates.

---

## Issue Resolution Framework

### Issue Lifecycle

```
1. DISCOVER
   └─→ Working on task, hit unexpected problem
   
2. DIAGNOSE
   └─→ Understand what's wrong (30 min research)
   
3. DOCUMENT
   └─→ Create ISSUES.md entry with details
   
4. DECIDE
   ├─→ Can fix now? → Fix → Mark resolved
   ├─→ Can fix later? → Mark as known issue, continue
   └─→ Blocking? → Escalate → Switch tasks
   
5. RESOLVE
   └─→ Implement fix → Test → Mark resolved → Document solution
```

### Issue Template

```markdown
## [PRIORITY] Issue Title

**ID**: #[number]
**Status**: [BLOCKED / INVESTIGATING / NEEDS RESEARCH]
**Priority**: [HIGH / MEDIUM / LOW]
**Task**: [task number] - [task name]
**Phase**: [phase number] - [phase name]

**Problem:**
[Clear description of what's wrong, what you expected, what actually happened]

**Context:**
[Background info: what you were trying to do, why this matters, impact]

**What We Tried:**
1. ✅ [Thing that didn't work but we learned from]
2. ✅ [Another attempt and result]
3. ❌ [Thing we tried that failed completely]

**Hypothesis:**
[Your current theory about what's causing this]

**Next Steps:**
1. [First thing to try]
2. [Second thing to try]
3. [If still stuck: escalation path]

**Research:**
- [Link to relevant docs]
- [Link to similar issues]
- [Link to Stack Overflow]

**Time Impact:**
- Blocked since: [timestamp]
- Time lost: [hours]
- Phase delay: [days]

**Created**: [timestamp]
```

### Priority Guidelines

**HIGH Priority:**
- Blocks current task completely
- Affects core functionality
- Crashes or data loss
- Needs resolution <24 hours

**MEDIUM Priority:**
- Workaround exists but is painful
- Affects secondary features
- Should fix within current phase
- Blocks future work

**LOW Priority:**
- Nice-to-have fix
- Cosmetic issue
- Can defer to polish phase
- Document for future

### Resolution Template

```markdown
## [PRIORITY] Issue Title (RESOLVED)

**ID**: #[number]
**Status**: ✅ RESOLVED
**Task**: [task number]
**Resolved**: [timestamp]

**Problem:**
[Original problem description]

**Solution:**
[What fixed it, why it worked]

**Code Changes:**
```swift
// Before
[problematic code]

// After
[fixed code]
```

**Prevention:**
[How to avoid this in future]

**Time Impact:**
- Total time lost: [hours]
- Resolved by: [you / Claude / Stack Overflow / etc]
```

---

## Quality Gates

### Phase Exit Criteria

**Every phase must pass:**

```markdown
## Phase Exit Checklist

### Functional
- [ ] All deliverables implemented
- [ ] All tasks marked complete in PLAN.md
- [ ] STATE.md shows all components ✅ COMPLETE
- [ ] No HIGH priority issues blocking

### Technical
- [ ] Code compiles without warnings
- [ ] All new code tested manually
- [ ] No crashes or obvious bugs
- [ ] Performance acceptable (no lag)

### Design
- [ ] Matches playbook specifications
- [ ] Touch targets >= 96pt verified
- [ ] Colors match hex values exactly
- [ ] Animations smooth and pleasant

### Documentation
- [ ] STATE.md accurately reflects build
- [ ] SUMMARY.md has final phase entry
- [ ] All issues resolved or documented
- [ ] ROADMAP.md updated with ✅

### Git
- [ ] All changes committed
- [ ] Clean working directory
- [ ] Meaningful commit messages
- [ ] Branch merged (if using branches)
```

### Pre-TestFlight Checklist

**Before submitting to TestFlight:**

```markdown
## TestFlight Readiness

### Core Functionality
- [ ] All Phase 1-7 deliverables complete
- [ ] Full playthrough test passes
- [ ] No critical bugs (crashes, data loss)
- [ ] All screens accessible

### Assets
- [ ] All images @ 2x, 3x
- [ ] All voice files imported
- [ ] All animations working
- [ ] All sound effects present

### Performance
- [ ] Memory < 200MB peak
- [ ] FPS > 55 constant
- [ ] No lag or stuttering
- [ ] Battery usage reasonable

### Design Compliance
- [ ] Bennie NEVER wears clothing
- [ ] Lemminge are BLUE #6FA8DC
- [ ] Touch targets >= 96pt everywhere
- [ ] No forbidden colors (red, neon)

### Accessibility
- [ ] VoiceOver labels on all UI
- [ ] Support for Reduce Motion
- [ ] Color blindness compatible
- [ ] Haptic feedback working

### Technical
- [ ] Code signed correctly
- [ ] Privacy manifest complete
- [ ] No hardcoded secrets
- [ ] Offline mode works

### Testing
- [ ] Tested on iPad 10th gen
- [ ] Tested on iPad Pro
- [ ] Tested on iPad Air
- [ ] Parent dashboard tested
```

---

## Appendix: Templates

### Quick Copy-Paste Templates

**New PLAN.md Phase:**
```markdown
# Current Phase: [N] - [Phase Name]

[Brief description from ROADMAP]

---

## Next Task (do this first)
**[N.0]** [First task name]
- [ ] Step 1
- [ ] Step 2
- [ ] Test: [verification]

---

## Remaining Tasks

**[N.1]** [Task name]
**[N.2]** [Task name]

---

## Completed This Phase

(none yet)

---

## Phase Progress

- Tasks completed: 0/[total]
- Estimated remaining: [hours]
- On track: ✅ YES
```

**New Issue:**
```markdown
## [PRIORITY] Issue Title

**ID**: #[next number]
**Status**: INVESTIGATING
**Priority**: [HIGH/MED/LOW]
**Task**: [task#]
**Phase**: [phase#]

**Problem:**
[Description]

**What We Tried:**
1. [Attempt 1]

**Next Steps:**
1. [Next thing to try]

**Created**: [timestamp]
```

**Daily Summary:**
```markdown
## [DATE] - Phase [N]: [Name]

### Completed Today
- ✅ Task X
- ✅ Task Y

### Metrics
- Hours worked: [hours]
- Tasks completed: [count]

### Next Session Plan
- [ ] [Top priority]
```

---

**End of SKILL.md**

For practical examples, see `examples/` folder.
For quick templates, see `templates/` folder.
For project-specific usage, see your `.gsd/` folder.
