# 13.1: Touch Target Audit & Enforcement

**Status**: 🔵 Ready to Start
**Duration**: 1 day
**Priority**: CRITICAL - Blocker for all subsequent work

---

## 📋 Overview

Ensure **every single interactive element** in the app meets the **96pt minimum touch target** requirement. This is NON-NEGOTIABLE for autism-friendly, child-accessible design.

### Why 96pt?

From the playbook:
- Standard recommendation: 44pt (too small for children)
- Our requirement: **96pt minimum** (2.18x larger)
- Ensures easy tapping for fine motor skill challenges
- Prevents frustration and accidental taps

---

## 📚 References

### Playbook
- **Section 1.1**: Brand personality - "Safe" means accessible
- **Section 5.2**: Touch target specifications
- **Section 7**: Quick reference - "TOUCH: >= 96pt"

### Design References
All screens in `C:\Users\christoph\Bennie und die Lemminge v3\design\references\screens\`:
- Verify reference screens follow 96pt rule
- Use as baseline for implementation

---

## 🎯 Implementation Steps

### Step 1: Create Touch Target Validation Tool

Create `Sources/Utilities/TouchTargetValidator.swift`:

```swift
import SwiftUI

/// Validates touch target sizes at compile-time and runtime
struct TouchTargetValidator {
    static let minimumSize: CGFloat = 96.0
    
    /// Debug overlay that shows touch target sizes
    static func debugOverlay(for view: some View, size: CGSize) -> some View {
        view.overlay(
            Rectangle()
                .stroke(size.width >= minimumSize && size.height >= minimumSize 
                    ? Color.green 
                    : Color.red, 
                    lineWidth: 2)
        )
    }
    
    /// Compile-time check for literal sizes
    static func validate(width: CGFloat, height: CGFloat, 
                        file: String = #file, 
                        line: Int = #line) {
        #if DEBUG
        if width < minimumSize || height < minimumSize {
            assertionFailure("""
                ⚠️ TOUCH TARGET VIOLATION ⚠️
                Size: \(width)x\(height)pt
                Minimum: \(minimumSize)x\(minimumSize)pt
                Location: \(file):\(line)
                """)
        }
        #endif
    }
}
```

### Step 2: Create Accessibility Button Component

Update `Sources/Design/Components/WoodButton.swift`:

```swift
struct WoodButton: View {
    let text: String?
    let icon: String?
    let action: () -> Void
    
    // ENFORCE 96pt minimum
    private let minimumSize: CGFloat = 96
    
    var body: some View {
        Button(action: action) {
            HStack {
                if let icon = icon {
                    Image(systemName: icon)
                }
                if let text = text {
                    Text(text)
                        .font(.sfRounded(size: 20, weight: .semibold))
                }
            }
            .padding(.horizontal, 20)
            .padding(.vertical, 12)
            .frame(minWidth: minimumSize, minHeight: minimumSize)
            .background(
                RoundedRectangle(cornerRadius: 12)
                    .fill(
                        LinearGradient(
                            colors: [Color(hex: "C4A574"), Color(hex: "A67C52")],
                            startPoint: .top,
                            endPoint: .bottom
                        )
                    )
            )
            .overlay(
                RoundedRectangle(cornerRadius: 12)
                    .stroke(Color(hex: "6B4423"), lineWidth: 2)
            )
        }
        .buttonStyle(WoodButtonStyle())
        #if DEBUG
        .overlay(
            TouchTargetValidator.debugOverlay(
                for: Rectangle().fill(Color.clear), 
                size: CGSize(width: minimumSize, height: minimumSize)
            )
        )
        #endif
    }
}
```

### Step 3: Audit All Screens

For **each screen**, verify touch targets:

#### Loading Screen
```
✅ Progress bar (non-interactive)
- No buttons, no interactive elements
```

#### Player Selection Screen
```
✅ Alexander button: 200x180pt (PASS)
✅ Oliver button: 200x180pt (PASS)
✅ Profile icon: 60x60pt → ENLARGE to 96x96pt
```

#### Home Screen (Waldabenteuer)
```
✅ Rätsel sign: Check actual tap area (not just visual)
✅ Zahlen sign: Check actual tap area
✅ Zeichnen sign: 96x96pt minimum
✅ Logik sign: 96x96pt minimum
✅ Treasure chest: 96x96pt minimum
✅ Settings icon: 96x96pt minimum
✅ Help icon: 96x96pt minimum
✅ Back button: 96x60pt minimum
```

#### Puzzle Matching Screen
```
✅ Grid cells: 96x96pt EACH
✅ Color picker buttons: 80x80pt → ENLARGE to 96x96pt
✅ Eraser button: 60x60pt → ENLARGE to 96x96pt
✅ Reset button: 60x60pt → ENLARGE to 96x96pt
✅ Home button: 96x60pt minimum
✅ Volume button: 60x60pt → ENLARGE to 96x96pt
```

#### Labyrinth Screen
```
✅ Path width: 44pt → INCREASE to 96pt touch tolerance
✅ Home button: 96x60pt minimum
✅ Volume button: 96x96pt minimum
```

#### Zahlen (Dice) Screen
```
✅ Dice area: 200x200pt (PASS)
✅ Number buttons: Check each (1-6)
✅ Home button: 96x60pt minimum
```

#### Zahlen (Choose Number) Screen
```
✅ Number buttons (1-10): Each 96x96pt minimum
✅ Color picker: 96x96pt minimum each
✅ Eraser: 96x96pt minimum
✅ Reset: 96x96pt minimum
```

#### Celebration Overlay
```
✅ "Weiter" button: 200x80pt minimum (PASS)
```

#### Treasure Screen
```
✅ "Zurück" button: 96x60pt minimum
✅ "5 Min YouTube" button: Check dimensions
✅ "10+2 Min YouTube" button: Check dimensions
```

#### Video Selection Screen
```
✅ Video thumbnail cards: 200x112pt minimum for tap area
✅ Back button: 96x60pt minimum
```

#### Video Player Screen
```
✅ (Minimal interaction - time runs automatically)
```

#### Parent Gate
```
✅ Number input field: 200x80pt minimum
✅ "Abbrechen" button: 120x60pt minimum
✅ "Bestätigen" button: 120x60pt minimum
```

#### Parent Dashboard
```
✅ All setting toggles: 96x60pt minimum
✅ Video management buttons: 96x60pt minimum
✅ Time limit controls: 96x60pt minimum
```

---

## 🔧 Implementation Checklist

### Pre-Audit
- [ ] Create `TouchTargetValidator.swift`
- [ ] Update `WoodButton.swift` to enforce 96pt
- [ ] Enable debug overlays in Development build
- [ ] Create audit spreadsheet

### Audit (Screen by Screen)
- [ ] Loading Screen
- [ ] Player Selection Screen
- [ ] Home Screen
- [ ] Puzzle Matching Screen
- [ ] Labyrinth Screen
- [ ] Zahlen (Dice) Screen
- [ ] Zahlen (Choose) Screen
- [ ] Celebration Overlay
- [ ] Treasure Screen
- [ ] Video Selection Screen
- [ ] Video Player Screen
- [ ] Parent Gate
- [ ] Parent Dashboard

### Fixes
- [ ] Document all violations
- [ ] Prioritize by severity
- [ ] Fix critical violations (< 50pt)
- [ ] Fix major violations (50-95pt)
- [ ] Re-audit after fixes
- [ ] Remove debug overlays from Production build

### Validation
- [ ] Run automated touch target check
- [ ] Manual testing on iPad
- [ ] Test with child users if possible
- [ ] Document all exceptions (if any)

---

## 📊 Audit Template

Use this for each screen:

```markdown
### Screen: [NAME]

| Element | Actual Size | Min Required | Status | Action |
|---------|-------------|--------------|--------|--------|
| Button 1 | 80x60pt | 96x96pt | ❌ FAIL | Enlarge |
| Button 2 | 100x100pt | 96x96pt | ✅ PASS | None |
| Icon 1 | 60x60pt | 96x96pt | ❌ FAIL | Add padding |
```

---

## 🚨 Common Violations & Fixes

### Violation: Icon buttons too small
```swift
// ❌ WRONG
Image(systemName: "gear")
    .frame(width: 44, height: 44)

// ✅ CORRECT
Image(systemName: "gear")
    .frame(width: 44, height: 44) // visual size
    .frame(minWidth: 96, minHeight: 96) // touch target
```

### Violation: Grid cells too small
```swift
// ❌ WRONG
GridItem(.fixed(60))

// ✅ CORRECT
GridItem(.fixed(96))
```

### Violation: Custom shapes
```swift
// ❌ WRONG
Circle()
    .frame(width: 50, height: 50)
    .onTapGesture { }

// ✅ CORRECT
Circle()
    .frame(width: 50, height: 50)
    .padding(23) // Total = 96pt
    .contentShape(Circle())
    .onTapGesture { }
```

---

## 📝 Documentation

Create audit report: `audits/touch_target_audit.md`

```markdown
# Touch Target Audit Report

**Date**: [DATE]
**Auditor**: [NAME]
**Build**: [VERSION]

## Summary
- Total interactive elements: X
- Passing (≥96pt): Y
- Failing (<96pt): Z
- Pass rate: Y/X %

## Violations

### Critical (< 50pt)
[List elements that are severely undersized]

### Major (50-95pt)
[List elements that don't meet minimum]

## Remediation Plan
[How violations will be fixed]

## Sign-off
- [ ] All violations documented
- [ ] Fixes prioritized
- [ ] No new violations introduced
```

---

## ✅ Success Criteria

This phase is complete when:

1. ✅ TouchTargetValidator utility exists
2. ✅ All screens audited and documented
3. ✅ Zero critical violations (< 50pt)
4. ✅ Zero major violations (50-95pt)
5. ✅ All interactive elements ≥ 96pt
6. ✅ Debug overlays show green on all elements
7. ✅ Manual testing confirms easy tapping
8. ✅ Audit report complete and reviewed

---

## 🔄 Maintenance

**After this phase**:
- Add touch target check to PR review process
- Every new button/interactive element MUST be ≥96pt
- Run automated validator in CI/CD
- Re-audit after any UI changes

---

*Next Phase*: 13.2 - VoiceOver Integration
*Previous Phase*: Phase 12 - Adaptive Difficulty
