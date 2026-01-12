# Phase 07.1: Parent Gate

## 📚 Playbook References

### Primary References
- **Playbook**: `docs/playbook/FULL_ARCHIVE.md` → Part 4.11 "Parent Dashboard" (Parent Gate section)
- **Condensed Playbook**: `docs/playbook/PLAYBOOK_CONDENSED.md` → Quick Reference Card
- **Design Rules**: CRITICAL - No reference screens exist for Parent Gate (new design)

### Color Palette (CRITICAL)
Reference: `PLAYBOOK_CONDENSED.md` - Color System
- **Background**: `#FAF5EB` (Cream) @ 90% opacity
- **Text**: `#8C7259` (Bark)
- **Input Border**: `#8C7259` (Bark)
- **Error State**: Use system red sparingly
- **Overlay Dimming**: `#000000` @ 60% opacity

### Components Required
- `WoodButton` - See `design/references/components/settings-button-wooden_20260110_123306.png`
- `BennieColors` - All colors from playbook color palette
- `BennieFont` - SF Rounded system

---

## Overview
Math question gate that prevents children from accessing parent settings while remaining simple enough for parents to solve quickly.

## Component Location
```
Features/Parent/ParentGateView.swift
```

## Design Philosophy

```
╔══════════════════════════════════════════════════════════════════╗
║              PARENT GATE IS A SIMPLE BARRIER                     ║
║                                                                  ║
║  🎯 Goal: Prevent ages 4-5 from accessing settings               ║
║  ⚡ Speed: Parents solve in 5-15 seconds                         ║
║  🔒 Security: Randomized questions, no pattern learning          ║
║                                                                  ║
║  Addition (5-15 range) is the sweet spot:                       ║
║  ✅ Too hard for 4-5 year olds                                    ║
║  ✅ Fast for all parents (no calculator needed)                   ║
║  ✅ No frustration (universal skill)                              ║
╚══════════════════════════════════════════════════════════════════╝
```

## Purpose
- Prevent accidental access to parent settings by children
- Simple enough for parents (5-15 second solve time)
- Generate new questions on each attempt
- Allow 3 attempts before generating new question

## UI Layout

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  [Dimmed Forest Background - 60% opacity]                       │
│                                                                 │
│                     ╭────────────────────────────╮              │
│                     │                            │              │
│                     │   🔒 Elternbereich         │              │
│                     │                            │              │
│                     │   Bitte löse diese Aufgabe:│              │
│                     │                            │              │
│                     │        7 + 8 = ?           │              │
│                     │      (36pt bold)           │              │
│                     │                            │              │
│                     │   ╭──────────────────────╮ │              │
│                     │   │                      │ │              │
│                     │   │  [Number Input]      │ │ ← 100pt wide│
│                     │   │     (24pt)           │ │   96pt tall │
│                     │   │                      │ │              │
│                     │   ╰──────────────────────╯ │              │
│                     │                            │              │
│                     │   ╭──────────╮ ╭──────────╮│              │
│                     │   │Abbrechen │ │Bestätigen││ ← WoodButtons│
│                     │   │  96x60pt │ │  96x60pt ││   (≥96pt)   │
│                     │   ╰──────────╯ ╰──────────╯│              │
│                     │                            │              │
│                     ╰────────────────────────────╯              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**Design Notes:**
- Modal appears over current screen (no navigation)
- Cream background (#FAF5EB) @ 90% opacity
- Rounded corners: 24pt
- Shadow: radius 20pt
- Touch targets: ALL buttons ≥ 96pt (critical for parent usability)

## Math Question Logic

### Question Generation
```swift
struct MathQuestion {
    let a: Int
    let b: Int
    var answer: Int { a + b }
    
    static func generate() -> MathQuestion {
        MathQuestion(
            a: Int.random(in: 5...15),
            b: Int.random(in: 5...15)
        )
    }
}
```

**Why addition only?**
- Quick to solve (5-15 seconds)
- No calculator needed
- Universal skill for all parents
- Prevents children ages 4-5 from accessing

**Number range: 5-15**
- Results: 10-30 (easy mental math)
- Not too simple (prevents guessing)
- Not too complex (parents solve quickly)

### Answer Validation

```swift
struct ParentGate: View {
    @State private var question = MathQuestion.generate()
    @State private var userAnswer: String = ""
    @State private var attempts: Int = 0
    @State private var showError: Bool = false
    @Environment(\.dismiss) private var dismiss
    
    // CRITICAL: Store reference to success handler
    let onSuccess: () -> Void
    
    var body: some View {
        ZStack {
            // Dimmed forest background
            Color.black.opacity(0.6)
                .ignoresSafeArea()
            
            VStack(spacing: 24) {
                Text("🔒 Elternbereich")
                    .font(.sfRounded(size: 28, weight: .bold))
                    .foregroundColor(BennieColors.bark)
                
                Text("Bitte löse diese Aufgabe:")
                    .font(.sfRounded(size: 18))
                    .foregroundColor(BennieColors.bark)
                
                // Question display
                Text("\(question.a) + \(question.b) = ?")
                    .font(.sfRounded(size: 36, weight: .bold))
                    .foregroundColor(BennieColors.bark)
                
                // Number input - CRITICAL: 100pt wide for easy tapping
                TextField("", text: $userAnswer)
                    .keyboardType(.numberPad)
                    .font(.sfRounded(size: 24))
                    .multilineTextAlignment(.center)
                    .frame(width: 100, height: 96) // ≥96pt touch target
                    .padding()
                    .background(Color.white)
                    .cornerRadius(12)
                    .overlay(
                        RoundedRectangle(cornerRadius: 12)
                            .stroke(showError ? Color.red : BennieColors.bark, lineWidth: 2)
                    )
                    .accessibilityLabel("Antwortfeld. Gib die Lösung ein.")
                
                if showError {
                    Text("Versuch es nochmal")
                        .font(.sfRounded(size: 14))
                        .foregroundColor(.red)
                }
                
                // Action buttons - CRITICAL: ≥96pt touch targets
                HStack(spacing: 20) {
                    Button("Abbrechen") {
                        dismiss()
                    }
                    .buttonStyle(WoodButtonStyle())
                    .frame(minWidth: 96, minHeight: 60) // Enforce minimum
                    
                    Button("Bestätigen") {
                        checkAnswer()
                    }
                    .buttonStyle(WoodButtonStyle(isPrimary: true))
                    .frame(minWidth: 96, minHeight: 60) // Enforce minimum
                }
            }
            .padding(40)
            .background(
                RoundedRectangle(cornerRadius: 24)
                    .fill(BennieColors.cream)
            )
            .shadow(radius: 20)
        }
        .onAppear {
            // Auto-focus input field
            DispatchQueue.main.asyncAfter(deadline: .now() + 0.5) {
                // Trigger keyboard
            }
        }
    }
    
    func checkAnswer() {
        if Int(userAnswer) == question.answer {
            // Success! Navigate to parent dashboard
            dismiss()
            onSuccess()
        } else {
            attempts += 1
            showError = true
            
            if attempts >= 3 {
                // Generate new question after 3 failed attempts
                question = MathQuestion.generate()
                attempts = 0
            }
            
            // Clear input
            userAnswer = ""
            
            // Hide error after 2 seconds
            DispatchQueue.main.asyncAfter(deadline: .now() + 2) {
                showError = false
            }
        }
    }
}
```

## Access Flow

### From Home Screen
```
Home Screen
    ↓
    Tap ⚙️ Settings button
    ↓
    ParentGateView appears (modal)
    ↓
    [Success] → Navigate to ParentDashboardView
    [Cancel] → Dismiss back to Home Screen
```

### State Management
```swift
// In HomeView
@State private var showParentGate = false
@State private var showParentDashboard = false

// Settings button (reference: settings-button-wooden_20260110_123306.png)
Button {
    showParentGate = true
} label: {
    Image(systemName: "gear")
        .font(.system(size: 24))
}
.frame(width: 96, height: 96) // CRITICAL: ≥96pt touch target
.sheet(isPresented: $showParentGate) {
    ParentGateView(
        onSuccess: {
            showParentGate = false
            showParentDashboard = true
        }
    )
}
.sheet(isPresented: $showParentDashboard) {
    ParentDashboardView()
}
```

## Security Considerations

### Why This Approach Works
✅ **Children ages 4-5 cannot solve addition problems with numbers 5-15**
✅ **Parents solve in 5-15 seconds (not frustrating)**
✅ **No memorization possible (randomized each time)**
✅ **Three attempts prevent accidental lockout from typos**
✅ **New question after 3 failures prevents brute force**

### Why NOT Use These Alternatives
❌ **Simple tap sequence** - Children learn patterns
❌ **PIN code** - Parents forget, frustration
❌ **Slider puzzle** - Children can solve visually
❌ **Long press (3-5 seconds)** - Children can hold button
❌ **Subtraction/Multiplication** - Slower for parents
❌ **Text password** - Typing takes too long on iPad

## Accessibility

### VoiceOver
```swift
// Question
.accessibilityLabel("Elternbereich. Löse die Rechenaufgabe: \(question.a) plus \(question.b)")
.accessibilityHint("Gib die richtige Antwort ein um fortzufahren")

// Input field
.accessibilityLabel("Antwortfeld")
.accessibilityValue(userAnswer.isEmpty ? "Leer" : userAnswer)

// Buttons
.accessibilityLabel("Abbrechen und zurück")
.accessibilityLabel("Antwort bestätigen")
```

### Keyboard
- Number pad only (no letters)
- Auto-focus input field on appear
- Return key submits answer (if enabled)

## Testing Checklist

### ✅ Playbook Compliance
```
□ Background is Cream (#FAF5EB)?
□ Text is Bark (#8C7259)?
□ WoodButton component used?
□ ALL touch targets ≥ 96pt?
□ No red colors except error state?
□ SF Rounded font used?
□ German text only?
```

### Functional Tests
```
□ Question generates within range (5-15)
□ Correct answer navigates to dashboard
□ Wrong answer shows error message
□ Error clears after 2 seconds
□ New question after 3 failed attempts
□ Cancel button returns to home
□ Input field accepts numbers only
□ Input field has focus on appear
```

### Edge Cases
```
□ Empty input (button should work, validate answer)
□ Non-numeric input (prevented by number pad)
□ Very large numbers (input validation max 2-3 digits)
□ Rapid tap confirm button (debounce not needed - validation is instant)
□ Dismiss while error showing (clears state on reappear)
□ Rotation (should stay in landscape, but test)
```

### Accessibility Tests
```
□ VoiceOver reads question correctly
□ VoiceOver reads error message
□ Input field is focusable
□ Buttons have descriptive labels
□ Touch targets ≥ 96pt (measure)
□ Color contrast meets 4.5:1 (cream + bark)
```

## File Dependencies

### Imports
```swift
import SwiftUI
```

### Required Components
- `WoodButtonStyle` - Wooden button styling
- `BennieColors` - Color palette enum
- `BennieFont` - Typography helper
- Navigation to `ParentDashboardView`

### Required Services
- None (standalone component)

## Performance Considerations

- **No animations** - Gate appears instantly (avoid startling parents)
- **Lightweight** - Simple math, no complex UI
- **No network** - Entirely local
- **No persistence** - Fresh question each time (security)

## Analytics (Optional - Phase 2)

Consider tracking (privacy-safe):
- Number of failed attempts before success
- Time to solve (for difficulty adjustment)
- Cancel rate (do parents give up?)

But **never track**:
- The questions asked (privacy)
- The answers given (privacy)
- When parents access settings (privacy)

---

## 🎯 Success Criteria

**This phase is complete when:**
1. ✅ Parents can access settings via math gate
2. ✅ Children ages 4-5 cannot solve the math
3. ✅ All touch targets ≥ 96pt
4. ✅ Colors match playbook exactly
5. ✅ VoiceOver works correctly
6. ✅ No crashes or freezes

---

**Status**: Ready for Implementation
**Dependencies**: WoodButtonStyle, BennieColors from Phase 02
**Next**: Phase 07.2 - Parent Dashboard
