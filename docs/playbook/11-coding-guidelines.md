# Part 11: Coding Guidelines Reference

> **Chapter 11** of the Bennie Brand Playbook
>
> Covers: Companion document reference, critical rules

---

## 11.1 Companion Document

This playbook has a companion technical document:

**SWIFTUI_CODING_GUIDELINES.md**

The coding guidelines provide:
- Complete SwiftUI code implementations for every component
- Copy-paste ready code blocks for Claude Code
- Memory management patterns (200MB target)
- Touch target enforcement (96pt minimum)
- Color system as Swift enum
- Animation presets matching this playbook
- QA checklist for every PR

---

## 11.2 How to Use Together

| Document | Purpose | Audience |
|----------|---------|----------|
| **BENNIE_BRAND_PLAYBOOK** | Design specs, screens, flow, assets | Designers, PM, QA |
| **SWIFTUI_CODING_GUIDELINES** | Implementation code, patterns | Claude Code, Developers |

### For Claude Code:

```
When implementing screens:
1. Read PLAYBOOK for design specs and behavior
2. Read CODING_GUIDELINES for exact code patterns
3. Use ONLY BennieColors enum values
4. Use ONLY BennieFont enum values
5. Use ONLY BennieAnimation presets
6. Enforce 96pt minimum touch targets
```

---

## 11.3 Critical Rules (Both Documents)

These rules appear in BOTH documents because they are **NON-NEGOTIABLE**:

| Rule | Violation Impact |
|------|------------------|
| Touch targets >= 96pt | Children can't tap, frustration |
| Bennie NO clothing | Character inconsistency |
| Lemminge BLUE #6FA8DC | Character inconsistency |
| German only UI | Children confusion |
| No "Falsch"/"Fehler" | Psychological harm |
| No flashing/shaking | Seizure/anxiety risk |
| No red #FF0000 | Overstimulation |

---

## 11.4 Color System Reference

```swift
enum BennieColors {
    // Primary
    static let woodland = Color(hex: "738F66")
    static let bark = Color(hex: "8C7259")
    static let sky = Color(hex: "B3D1E6")
    static let cream = Color(hex: "FAF5EB")

    // Characters
    static let bennieBrown = Color(hex: "8C7259")
    static let bennieTan = Color(hex: "C4A574")
    static let lemmingeBlue = Color(hex: "6FA8DC")

    // UI
    static let success = Color(hex: "99BF8C")
    static let coinGold = Color(hex: "D9C27A")
    static let woodLight = Color(hex: "C4A574")
    static let woodMedium = Color(hex: "A67C52")
    static let woodDark = Color(hex: "6B4423")
}
```

---

## 11.5 Touch Target Enforcement

```swift
extension View {
    func ensureMinimumTouchTarget() -> some View {
        self.frame(minWidth: 96, minHeight: 96)
    }
}

// Usage
Button("Tap") { }
    .ensureMinimumTouchTarget()
```

---

*Document Version: 3.1*
*Created: January 2026*
*For: Bennie und die Lemminge - iPad App*
*Target Audience: Alexander (5) & Oliver (4)*
