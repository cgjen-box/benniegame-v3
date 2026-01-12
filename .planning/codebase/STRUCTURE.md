# Codebase Structure

**Analysis Date:** 2026-01-12

## Directory Layout

```
BennieGame-v3/
├── .gsd/                    # GSD framework (project management)
├── .planning/               # Codebase analysis output
├── .claude/                 # Claude Code skills
├── design/                  # Reference design assets
├── docs/                    # Documentation & playbook
├── plan/                    # Phase-by-phase specifications
├── starter-kits/            # Tool templates & examples
├── CLAUDE.md                # Main execution plan (107KB)
├── PLAYBOOK_CONDENSED.md    # Quick design reference
├── SWIFTUI_CODING_GUIDELINES.md  # Code patterns
├── .env                     # Environment configuration
└── [BennieGame/]            # (To be created - Xcode project)
```

## Directory Purposes

**.gsd/**
- Purpose: GSD framework project management
- Contains: PROJECT.md, ROADMAP.md, STATE.md, PLAN.md, ISSUES.md, SUMMARY.md
- Key files: `STATE.md` - current project status, `PLAN.md` - current phase tasks
- Subdirectories: `codebase/` (empty), `research/`

**.planning/codebase/**
- Purpose: Codebase analysis output (this folder)
- Contains: STACK.md, ARCHITECTURE.md, STRUCTURE.md, CONVENTIONS.md, TESTING.md, INTEGRATIONS.md, CONCERNS.md
- Key files: All 7 analysis documents

**design/references/**
- Purpose: Visual reference assets for design compliance
- Contains: Character expressions, screen mockups, component references
- Key files: `Reference_*.png` (8+ screen mockups)
- Subdirectories: `character/bennie/`, `character/lemminge/`, `screens/`, `components/`

**docs/playbook/**
- Purpose: Complete game specification
- Contains: 11 playbook sections + full archive
- Key files: `FULL_ARCHIVE.md` (162KB complete spec), `README.md` (playbook guide)
- Subdirectories: `04-screens/` (detailed screen specs)

**plan/**
- Purpose: Phase-by-phase implementation specifications
- Contains: 16 phase folders with detailed specs
- Key files: `PHASE_SPEC.md` in each folder
- Subdirectories: `01_foundation_setup/` through `16_testflight_prep/`

**starter-kits/**
- Purpose: Tool templates, examples, and asset generation pipelines
- Contains: Python scripts, requirements files, documentation
- Key files: `*/generate_*.py`, `*/requirements.txt`, `*/SKILL.md`
- Subdirectories: `gemini-image-pro-3/`, `ludo-animation-pipeline/`, `maestro-orchestration/`, `veo-video-generation/`

## Key File Locations

**Entry Points:**
- `CLAUDE.md` - Main execution plan, phase-by-phase instructions
- `App/BennieGameApp.swift` (to be created) - iOS app entry point
- `App/AppCoordinator.swift` (to be created) - Navigation coordinator

**Configuration:**
- `.env` - API keys, credentials, environment configuration
- `MCP_SETUP.md` - MCP tool configuration guide
- `Info.plist` (to be created) - iOS app configuration

**Core Logic (Planned):**
- `Core/State/GameState.swift` - Central state machine
- `Core/State/PlayerData.swift` - Player profile model
- `Core/Services/AudioManager.swift` - 3-channel audio system
- `Core/Services/NarratorService.swift` - Voice playback

**Design System (Planned):**
- `Design/Theme/BennieColors.swift` - Color definitions
- `Design/Theme/BennieTypography.swift` - Typography system
- `Design/Components/WoodButton.swift` - Primary button
- `Design/Characters/BennieView.swift` - Bear character

**Testing:**
- `DESIGN_QA_CHECKLIST.md` - Visual QA verification
- `plan/15_recursive_testing/` - Full playthrough test specs

**Documentation:**
- `README.md` - Getting started guide
- `PLAYBOOK_CONDENSED.md` - Quick design reference
- `SWIFTUI_CODING_GUIDELINES.md` - Code patterns (52KB)

## Naming Conventions

**Files:**
- PascalCase.swift for Swift source files (e.g., `BennieColors.swift`)
- kebab-case.md for documentation (e.g., `full-archive.md`)
- snake_case for assets (e.g., `bennie_idle.png`)
- UPPERCASE.md for important project files (e.g., `CLAUDE.md`, `README.md`)

**Directories:**
- PascalCase for Swift modules (e.g., `Design/`, `Features/`)
- kebab-case for documentation (e.g., `docs/playbook/`)
- snake_case with numbers for phases (e.g., `01_foundation_setup/`)

**Special Patterns:**
- `*View.swift` for SwiftUI views
- `*Service.swift` or `*Manager.swift` for services
- `Reference_*.png` for design reference images
- `PHASE_SPEC.md` for phase specifications

## Where to Add New Code

**New Feature:**
- Primary code: `Features/{FeatureName}/{ScreenName}View.swift`
- Tests: Not yet configured
- Config if needed: Environment flags in GameState

**New Component/Module:**
- Implementation: `Design/Components/{ComponentName}.swift`
- Types: In-file or `Design/Types/`
- Tests: Not yet configured

**New Route/Command:**
- Definition: Update `GameScreen` enum in `Core/State/GameState.swift`
- Handler: `Features/{FeatureName}View.swift`
- Coordinator: Add case in `AppCoordinator.swift`

**Utilities:**
- Shared helpers: `Core/Utilities/`
- Type definitions: In-file or dedicated types file
- Extensions: `Core/Utilities/Extensions.swift`

**New Activity:**
- Implementation: `Features/Activities/{ActivityType}/{ActivityName}View.swift`
- Level generation: `Core/Services/LevelGeneratorService.swift`
- State handling: Update `ActivityType` enum

## Special Directories

**.gsd/**
- Purpose: GSD framework project management files
- Source: Created by /gsd:new-project command
- Committed: Yes (project tracking)

**starter-kits/**
- Purpose: Asset generation tools and templates
- Source: Copied/developed for this project
- Committed: Yes (development tooling)

**design/references/**
- Purpose: Visual reference for design compliance
- Source: Generated/exported from design tools
- Committed: Yes (design specifications)

**Resources/ (to be created)**
- Purpose: App assets (images, animations, audio)
- Source: Generated by asset pipelines in starter-kits/
- Committed: Yes (bundled in app)

---

*Structure analysis: 2026-01-12*
*Update when directory structure changes*
