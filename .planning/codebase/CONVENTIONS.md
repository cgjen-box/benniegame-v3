# Coding Conventions

**Analysis Date:** 2026-01-12

## Naming Patterns

**Files:**
- PascalCase for Swift files (e.g., `BennieColors.swift`, `WoodButton.swift`)
- snake_case for assets (e.g., `bennie_idle.png`, `narrator_loading_complete.aac`)
- kebab-case for markdown (e.g., `full-archive.md`)
- `*View.swift` suffix for SwiftUI views
- `*Service.swift` or `*Manager.swift` for services

**Functions:**
- camelCase for all functions (e.g., `playVoice()`, `updateCoins()`)
- No special prefix for async functions
- `handle*` for event handlers (e.g., `handleTap()`, `handleCompletion()`)

**Variables:**
- camelCase for variables (e.g., `currentPlayer`, `isAudioEnabled`)
- No underscore prefix for private members
- Constants in enums with static properties (e.g., `BennieColors.bennieBrown`)

**Types:**
- PascalCase for all types (e.g., `GameState`, `PlayerData`, `WoodButton`)
- No I/E prefix for interfaces/enums
- Enum values in camelCase (e.g., `.loading`, `.playerSelection`)

## Code Style

**Formatting:**
- 4 spaces per indentation level (Xcode default)
- No explicit line length limit (~140 chars)
- Section dividers: `// ═══════════════════════════════════════════════════`

**Linting:**
- No explicit linter configured
- Xcode build-time checks
- Manual review against SWIFTUI_CODING_GUIDELINES.md

**Comments:**
- Section headers with box-drawing characters
- Inline comments for critical rules
- German UI text, English code comments

## Import Organization

**Order:**
1. SwiftUI / UIKit (system frameworks)
2. Third-party frameworks (Lottie)
3. Project modules (@Environment dependencies)

**Grouping:**
- Blank line between groups
- No specific sorting within groups

**Path Aliases:**
- Not applicable (standard Swift imports)

## Error Handling

**Patterns:**
- Graceful degradation for audio/network failures
- Never show negative messages to children
- Log warnings, continue operation where possible
- Try/catch for file operations and API calls

**Error Types:**
- Audio loading: Show visual feedback instead
- Network (YouTube): Display "Keine Verbindung" message
- Persistence: Retry with exponential backoff

**Logging:**
- Development: `print()` statements, Xcode console
- Production: No logging (privacy for children)

## Logging

**Framework:**
- Standard `print()` for development
- No production logging framework

**Patterns:**
- Log state transitions during development
- Log external API calls (asset generation)
- No user data in logs

## Comments

**When to Comment:**
- Explain critical design constraints (autism-friendly rules)
- Document business rules (coin economy, celebration triggers)
- Mark validation checkpoints

**Section Headers:**
```swift
// ═══════════════════════════════════════════════════════════════════
// AUDIO MANAGER - Three independent channels with voice priority
// ═══════════════════════════════════════════════════════════════════
```

**Critical Rules:**
```swift
// ⚠️ CRITICAL: Bennie MUST be brown, NO clothing
// ⚠️ NEVER say "Falsch" (wrong) or "Fehler" (error)
```

**TODO Comments:**
- Format: `// TODO: description`
- Link to issue if exists: `// TODO: Fix race condition (DEFER-003)`

## Function Design

**Size:**
- Keep under 50 lines
- Extract helpers for complex logic

**Parameters:**
- Max 3-4 parameters
- Use options struct for more
- Destructure in parameter list for complex types

**Return Values:**
- Explicit return statements
- Return early for guard clauses
- Use optionals for fallible operations

## Module Design

**Exports:**
- Internal access by default
- Public only for cross-module access
- No barrel files (SwiftUI doesn't use index files)

**State Management:**
```swift
@Observable
final class GameState {
    var currentScreen: GameScreen = .loading
    var currentPlayer: String?
    // ...
}
```

**Component Pattern:**
```swift
struct WoodButton: View {
    let title: String
    let action: () -> Void

    var body: some View {
        Button(action: action) {
            Text(title)
        }
        .frame(minWidth: 96, minHeight: 96)  // ≥96pt touch target
    }
}
```

## Design Constraint Enforcement

**Touch Targets (CRITICAL):**
```swift
// All interactive elements MUST be ≥96pt
.frame(minWidth: 96, minHeight: 96)
.contentShape(Rectangle())  // Expand hit area
```

**Color Validation:**
```swift
// Character colors are non-negotiable
static let bennieBrown = Color(hex: "8C7259")  // Bennie - NO clothing
static let lemmingeBlue = Color(hex: "6FA8DC")  // NEVER green/brown
```

**Forbidden Colors:**
```swift
// ⚠️ NEVER USE:
// - Pure red #FF0000
// - Neon colors
// - >80% saturation
```

**Animation Rules:**
```swift
// ⚠️ FORBIDDEN:
// - No flashing (>3 flashes/sec)
// - No shaking/jarring motion
// - No strobing effects
```

---

*Convention analysis: 2026-01-12*
*Update when patterns change*
