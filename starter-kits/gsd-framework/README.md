# GSD Framework - Get Shit Done

**A lightweight, AI-native project management system for solo developers and small teams working with AI coding assistants.**

## What is GSD?

GSD (Get Shit Done) is a minimalist project management framework designed specifically for developers working with AI assistants like Claude Code. It replaces heavyweight tools (Jira, Linear, ClickUp) with a set of simple Markdown files that live in your repository.

## Why GSD?

### ❌ Traditional Problem
- **Jira/Linear**: Too heavy, requires context switching, AI can't access
- **TODO comments**: Scattered across codebase, hard to prioritize
- **Mental notes**: Forgotten, lost, never shared
- **Text files**: Unstructured, no methodology

### ✅ GSD Solution
- **Single source of truth**: `.gsd/` folder in your repo
- **AI-native**: Claude Code can read/update GSD files directly
- **Zero overhead**: Markdown files, no external tools
- **Git-tracked**: Full history, branches, PRs
- **Structured but simple**: Clear methodology, minimal bureaucracy

## Core Principles

1. **Everything in the repo** - No external tools required
2. **AI can participate** - Claude Code reads/writes GSD files
3. **Atomic tasks** - Every task is clear, specific, testable
4. **State over status** - Track what exists, not what's "in progress"
5. **Ruthless simplicity** - 6 files, that's it

## The 6 Files

```
.gsd/
├── PROJECT.md     # Project vision (1 page)
├── ROADMAP.md     # High-level phases
├── PLAN.md        # Current phase atomic tasks
├── STATE.md       # Build status (what exists)
├── SUMMARY.md     # What got done today
└── ISSUES.md      # Blockers and questions
```

## Quick Start

### 1. Install
```bash
# Clone into your project
cd your-project/
mkdir .gsd
cd .gsd

# Copy templates (or use setup script)
cp path/to/gsd-framework/templates/* .
```

### 2. Initialize
Edit `PROJECT.md`:
```markdown
# Project: Your App Name

## Vision (1 paragraph)
What you're building and why.

## Success Criteria (3-5 bullets)
- Working feature X
- Users can do Y
- Performance metric Z

## Not Building (scope boundaries)
- Feature A (maybe v2)
- Platform B (maybe later)
```

### 3. Create Roadmap
Edit `ROADMAP.md`:
```markdown
## Phase 1: Foundation (4-6 hours)
Core setup, basic screens

## Phase 2: Features (8-12 hours)
Main functionality

## Phase 3: Polish (4-6 hours)
UX refinement, testing
```

### 4. Start First Phase
Edit `PLAN.md`:
```markdown
# Current Phase: 1 - Foundation

## Next Task (do this first)
**1.0** Initialize git repository
- [ ] Run git init
- [ ] Create .gitignore
- [ ] Initial commit

## Remaining Tasks
**1.1** Create Xcode project
**1.2** Set up design system
...
```

### 5. Daily Workflow
```bash
# Morning: What's next?
cat .gsd/PLAN.md

# During work: Update state
# (Claude Code does this)

# Evening: What got done?
cat .gsd/SUMMARY.md
```

## File Details

### PROJECT.md
**Purpose**: One-page project vision  
**Update frequency**: Rarely (only when scope changes)  
**Who updates**: You (manually)

**Contents**:
- Vision (1 paragraph)
- Success criteria (3-5 bullets)
- Not building (scope boundaries)
- Tech stack
- Timeline estimate

### ROADMAP.md
**Purpose**: High-level phases  
**Update frequency**: Rarely (stable milestone structure)  
**Who updates**: You (manually)

**Structure**:
```markdown
## Phase 1: Name (time estimate)
Description

**Deliverables:**
- Item 1
- Item 2

**Exit criteria:**
- [ ] Criterion 1
- [ ] Criterion 2
```

### PLAN.md
**Purpose**: Current phase atomic tasks  
**Update frequency**: Daily (as tasks complete)  
**Who updates**: You + Claude Code

**Structure**:
```markdown
# Current Phase: N - Name

## Next Task (do this first)
**N.X** Task name
- [ ] Atomic step 1
- [ ] Atomic step 2

## Remaining Tasks
**N.Y** Task name
**N.Z** Task name

## Completed This Phase
✅ **N.A** Task name (timestamp)
```

**Rules**:
- ✅ One "Next Task" at a time
- ✅ Tasks must be atomic (< 30 min)
- ✅ Clear acceptance criteria
- ❌ No vague tasks ("improve UX")

### STATE.md
**Purpose**: What exists in the build  
**Update frequency**: Continuous (after every meaningful change)  
**Who updates**: Claude Code (automated)

**Structure**:
```markdown
# Build State

## Screens
- [x] LoadingView ✅ COMPLETE
- [~] HomeView ⚠️ PARTIAL (missing settings button)
- [ ] GameView ❌ NOT STARTED

## Components
- [x] WoodButton ✅ COMPLETE
- [x] ProgressBar ✅ COMPLETE

## Services
- [x] AudioManager ✅ COMPLETE
- [ ] YouTubeService ❌ NOT STARTED
```

**Status Icons**:
- ✅ `[x]` - Complete and tested
- ⚠️ `[~]` - Partial (specify what's missing)
- ❌ `[ ]` - Not started

### SUMMARY.md
**Purpose**: Daily progress log  
**Update frequency**: Daily (end of session)  
**Who updates**: You + Claude Code

**Structure**:
```markdown
# 2026-01-11 - Phase 1 Progress

## Completed Today
- ✅ Task 1.0 - Project setup
- ✅ Task 1.1 - Design system

## Started (not finished)
- ⚠️ Task 1.2 - LoadingView (75% done)

## Blockers Resolved
- Fixed: API key configuration
- Worked around: Lottie animation crash

## Next Session Plan
- Complete Task 1.2
- Start Task 1.3
```

### ISSUES.md
**Purpose**: Active blockers and questions  
**Update frequency**: As needed (when stuck)  
**Who updates**: You + Claude Code

**Structure**:
```markdown
# Active Issues

## [HIGH] Issue title
**Status**: BLOCKED / INVESTIGATING / NEEDS RESEARCH  
**Task**: 2.3 - Feature implementation  
**Problem**: Specific description  
**Tried**: What we attempted  
**Next**: What to try next  
**Created**: 2026-01-11

## [MED] Issue title
...

## Resolved
### Issue title (RESOLVED)
**Solution**: How we fixed it
**Resolved**: 2026-01-10
```

## AI Integration

### What Claude Code Can Do

**READ**:
```
Claude can you check what's next in PLAN.md?
Claude can you list all blockers in ISSUES.md?
Claude can you summarize today's progress?
```

**WRITE**:
```
Claude please update STATE.md after implementing WoodButton
Claude mark task 1.2 as complete in PLAN.md
Claude add this blocker to ISSUES.md
```

**REASON**:
```
Claude based on STATE.md, what components do we still need?
Claude looking at ROADMAP.md, how much work is left?
Claude can you estimate time remaining for Phase 2?
```

### Best Practices

1. **Be explicit**: "Update PLAN.md" not "update the plan"
2. **Verify**: Always check Claude's updates (`git diff .gsd/`)
3. **Guide**: Give Claude context ("We just finished LoadingView, update STATE.md")
4. **Atomic commits**: Each GSD update = separate commit

## Workflow Examples

### Starting a New Phase
```bash
# 1. Review completed phase
cat .gsd/SUMMARY.md

# 2. Move to next phase in ROADMAP
# Edit ROADMAP.md: Add ✅ to completed phase

# 3. Create new PLAN.md for next phase
# Copy tasks from ROADMAP → PLAN.md
# Break into atomic tasks
# Mark first task as "Next Task"

# 4. Commit
git add .gsd/
git commit -m "Phase 2 start"
```

### Completing a Task
```bash
# Claude finishes implementing WoodButton

# Claude updates:
# - STATE.md: Add WoodButton as [x] COMPLETE
# - PLAN.md: Move task to "Completed This Phase"
# - PLAN.md: Move next task to "Next Task" position

# You verify:
git diff .gsd/

# Commit:
git add .gsd/ src/
git commit -m "Task 1.3: WoodButton component"
```

### Hitting a Blocker
```bash
# You discover API rate limit issue

# 1. Add to ISSUES.md
**[HIGH] Gemini API rate limit**
**Status**: BLOCKED
**Task**: 9.1 - Generate character images
**Problem**: Getting 429 errors after 10 images
**Tried**: Added delay between requests (didn't help)
**Next**: Research API quotas, consider batching

# 2. Move to different task in PLAN.md
# Work on something else while researching

# 3. When resolved, move to "Resolved" section in ISSUES.md
```

### Daily Wrap-Up
```bash
# End of day: Update SUMMARY.md
# Either manually or:
"Claude please summarize today's progress in SUMMARY.md"

# Review what got done:
cat .gsd/SUMMARY.md

# Commit:
git add .gsd/
git commit -m "Daily wrap: Phase 1 progress"
```

## Advanced Features

### Branch-Specific Plans
```bash
# Create experimental branch
git checkout -b experiment-new-ui

# GSD files come with you
# Work on experimental tasks in .gsd/PLAN.md

# Merge or abandon
git checkout main
git merge experiment-new-ui  # GSD changes merge too
```

### Multiple Workstreams
```bash
# If working on 2 phases simultaneously:
.gsd/
├── PLAN-phase1.md    # Frontend work
├── PLAN-phase2.md    # Backend work
└── PLAN.md           # Master (references others)
```

### Team Collaboration
```bash
# Each dev has their own branch
# GSD files in PR show exactly what they're working on

# PR description auto-generated from GSD:
git diff main...feature-x .gsd/
```

## Comparison to Other Systems

| Feature | GSD | Jira | GitHub Issues | TODO Comments |
|---------|-----|------|---------------|---------------|
| In repo | ✅ | ❌ | ❌ | ✅ |
| AI accessible | ✅ | ❌ | ⚠️ | ⚠️ |
| Structured | ✅ | ✅ | ⚠️ | ❌ |
| Zero overhead | ✅ | ❌ | ⚠️ | ✅ |
| Git tracked | ✅ | ❌ | ❌ | ✅ |
| Atomic tasks | ✅ | ⚠️ | ⚠️ | ❌ |
| State tracking | ✅ | ⚠️ | ❌ | ❌ |

## When NOT to Use GSD

- **Large teams (>5)**: Use proper PM tools
- **Client-facing**: They want dashboards, not Markdown
- **Compliance requirements**: May need audit trails
- **Cross-repo projects**: GSD is single-repo focused

## Examples

See `examples/` folder for real-world implementations:
- **bennie-v3**: 7-phase iPad game (33-45 hours)
- **api-wrapper**: 3-phase library (8-12 hours)
- **static-site**: 2-phase website (4-6 hours)

## Setup Script

Use the included setup script for new projects:

```bash
# Unix/Mac
./setup-gsd.sh

# Windows
.\setup-gsd.ps1

# Manual
mkdir .gsd
cp templates/* .gsd/
```

## License

Open source. Use freely. No attribution required.

## Support

- **Full methodology**: See `SKILL.md`
- **Templates**: See `templates/` folder
- **Examples**: See `examples/` folder
- **Issues**: Open an issue (if this were a public repo!)

---

**TL;DR**: GSD is 6 Markdown files that replace Jira/Linear for AI-native development. Everything lives in `.gsd/` folder. Claude Code can read/write it. Zero overhead. Git-tracked. Simple.
