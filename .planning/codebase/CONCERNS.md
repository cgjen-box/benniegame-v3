# Codebase Concerns

**Analysis Date:** 2026-01-12

## Project Status

**Stage:** Fresh build - Planning & documentation phase
**Code Status:** No Swift code exists yet (planning phase only)
**Architecture:** Fully documented but not implemented

## Tech Debt

**Pre-implementation - No tech debt accumulated yet**

The project is in planning phase. Future tech debt risks identified:

**Potential Future Debt:**
- Large state machine may need refactoring as complexity grows
- Audio system (3-channel) may need optimization for performance
- SwiftData model migrations not yet planned

## Known Bugs

**No bugs - No code exists yet**

## Security Considerations

**Exposed Secrets in `.env` File:**
- Risk: API keys committed to repository (GOOGLE_API_KEY, ELEVENLABS_API_KEY, JIRA secrets, MacinCloud credentials)
- Location: `/.env` (lines 8, 12-14, 20-21, 31-36, 72-73, 85-89)
- Current mitigation: `.gitignore` has `*.env` pattern but file may already be tracked
- Recommendations:
  1. Rotate ALL exposed credentials immediately
  2. Verify `.env` is not in git history
  3. Create `.env.example` with placeholders
  4. Use managed secrets for production

**Missing `.env.example`:**
- Risk: No safe template for environment configuration
- Location: Project root
- Current mitigation: `starter-kits/*/config/.env.example` exist for sub-packages
- Recommendations: Create root-level `.env.example`

**Children's Privacy:**
- Risk: Must ensure no data leaves device
- Current mitigation: Design specifies local-only storage, no analytics
- Recommendations: Verify no third-party SDKs track usage

## Performance Bottlenecks

**Not measurable - No code exists yet**

**Anticipated Performance Concerns:**

**3-Channel Audio System:**
- Problem: Concurrent audio playback (music, voice, effects)
- Expected location: `Core/Services/AudioManager.swift`
- Cause: AVFoundation concurrent session management
- Improvement path: Test on actual iPad hardware, optimize buffer sizes

**Lottie Animations:**
- Problem: Character animations may impact frame rate
- Expected location: `Design/Characters/BennieView.swift`, `LemmingeView.swift`
- Cause: Complex vector animations with many keyframes
- Improvement path: Use PNG-embedded Lottie, limit concurrent animations

## Fragile Areas

**Critical Design Constraints (Not Yet Enforced in Code):**
- Why fragile: Character colors, touch targets, forbidden animations are documented but no compile-time enforcement
- Location: `SWIFTUI_CODING_GUIDELINES.md`, `PLAYBOOK_CONDENSED.md`
- Common failures: AI-generated assets may violate constraints (wrong color Bennie, clothing, green Lemminge)
- Safe modification: Follow design QA checklist for every change
- Test coverage: `DESIGN_QA_CHECKLIST.md` provides manual verification

**YouTube Integration (Research Incomplete):**
- Location: `.gsd/ISSUES.md` lines 81-91 (RESEARCH-003)
- Why fragile: Unanswered questions about WKWebView embedding, UI hiding, related videos prevention
- Common failures: YouTube UI appearing, suggested videos showing
- Safe modification: Complete research before Phase 4 implementation

## Scaling Limits

**Not applicable - Local iPad app**

Target usage:
- 2 players (Alexander, Oliver)
- Local storage only
- No cloud sync
- No multi-device support

## Dependencies at Risk

**MCP Tools Not Validated:**
- Risk: `bennie-image-generator` MCP not provided in starter-kits
- Location: Referenced in `CLAUDE.md` but not in `starter-kits/`
- Impact: Phase 10 (Asset Production) blocked
- Migration plan: Use `gemini-image-pro-3` as fallback, create custom image generator

**Python Dependencies Not Version-Pinned:**
- Risk: Breaking changes from minimum version specs (e.g., `google-genai>=0.4.0`)
- Location: `starter-kits/*/requirements.txt`
- Impact: Asset generation may fail with future package updates
- Migration plan: Pin exact versions after testing

**Lottie-iOS Compatibility:**
- Risk: Lottie 4.x compatibility with iOS 17
- Location: Package dependency
- Impact: Animation failures
- Migration plan: Test on target devices, fallback to static images

## Missing Critical Features

**Implementation Not Started:**
- Problem: All screens, activities, services exist only as specifications
- Location: `plan/01_foundation_setup/` through `plan/16_testflight_prep/`
- Current workaround: Detailed planning documentation
- Implementation complexity: ~68 hours estimated

**Deferred Activities:**
- Problem: Zeichnen (Drawing) and Logik (Logic) activities locked
- Location: `.gsd/ISSUES.md` (DEFER-001, DEFER-002)
- Current workaround: Locked UI with "Noch gesperrt" message
- Implementation complexity: Post-MVP

## Test Coverage Gaps

**No Test Infrastructure:**
- What's not tested: Everything (no code exists)
- Risk: Bugs introduced during implementation
- Priority: High
- Difficulty to test: XCTest setup straightforward, integration tests complex

**Design QA Not Automated:**
- What's not tested: Visual compliance with reference images
- Risk: Character color violations, touch target undersizing
- Priority: High
- Difficulty to test: Consider snapshot testing framework

**YouTube Integration:**
- What's not tested: Video embedding, control hiding, time management
- Risk: YouTube UI showing through, auto-play of related videos
- Priority: High
- Difficulty to test: Requires actual YouTube API integration

## Documentation Gaps

**No Error Handling Strategy:**
- What's missing: Documented patterns for audio failures, network errors, persistence errors
- Risk: Inconsistent error handling across codebase
- Priority: Medium
- Recommendation: Create `Core/Services/ErrorHandler.swift` pattern guide

**No Code Review Checklist:**
- What's missing: PR template with design constraint verification
- Risk: Design violations slip through
- Priority: Medium
- Recommendation: Create `.github/PULL_REQUEST_TEMPLATE.md`

**Performance Baselines Not Established:**
- What's missing: Target frame rate, memory budget, load times
- Risk: Performance issues discovered late
- Priority: Low
- Recommendation: Document in Phase 12 (Performance) - suggest 60fps, <200MB, <2s load

## Immediate Action Items

| Priority | Issue | Action |
|----------|-------|--------|
| 🔴 CRITICAL | `.env` secrets exposed | Rotate all credentials, remove from git history |
| 🔴 CRITICAL | No `.env.example` | Create template file |
| 🟠 HIGH | YouTube API research incomplete | Complete before Phase 4 |
| 🟠 HIGH | MCP tools not validated | Test tool chain on MacinCloud |
| 🟡 MEDIUM | Error handling strategy missing | Draft patterns before Phase 1 |
| 🟢 LOW | Documentation organization | Consider index document |

---

*Concerns audit: 2026-01-12*
*Update as issues are fixed or new ones discovered*
