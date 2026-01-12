# 13.2: VoiceOver Integration

**Status**: 🔵 Ready to Start
**Duration**: 2 days
**Priority**: HIGH
**Dependencies**: Phase 13.1 (Touch Targets)

---

## 📋 Overview

Implement comprehensive VoiceOver support with **German accessibility labels** for all interactive elements, ensuring the app is fully accessible to visually impaired children.

### Requirements from Playbook Section 5.7

| Element | Accessibility Label (German) |
|---------|------------------------------|
| Activity buttons | "Rätsel spielen" / "Zahlen spielen" |
| Grid cells | "Reihe [N], Spalte [N], [Farbe/leer]" |
| Progress bar | "[N] von 10 Münzen gesammelt" |
| Chest | "Schatzkiste, [N] Münzen" |
| Video card | "[Video title], zum Abspielen tippen" |

---

## 📚 References

### Playbook
- **Section 5.7**: VoiceOver support table
- **Section 3**: Voice script (for consistent language)
- **Section 1.4**: Language rules (German only, literal, max 7 words)

### Apple Documentation
- [Accessibility for UIKit](https://developer.apple.com/documentation/uikit/accessibility_for_uikit)
- [Accessibility for SwiftUI](https://developer.apple.com/documentation/swiftui/view-accessibility)
- [VoiceOver Programming Guide](https://developer.apple.com/library/archive/featuredarticles/ViewControllerPGforiPhoneOS/Accessibility.html)

---

## 🎯 Implementation Steps

### Step 1: Create Accessibility Labels Utility

Create `Sources/Utilities/AccessibilityLabels.swift`:

```swift
import Foundation

/// Centralized accessibility labels in German
/// All labels follow playbook language rules:
/// - German only
/// - Literal language (no metaphors)
/// - Max 7 words
/// - Positive framing
struct AccessibilityLabels {
    
    // MARK: - Navigation
    static let backButton = "Zurück zur vorherigen Seite"
    static let homeButton = "Zurück zum Waldabenteuer"
    static let settingsButton = "Einstellungen öffnen"
    static let helpButton = "Hilfe anzeigen"
    static let volumeButton = "Lautstärke ändern"
    
    // MARK: - Player Selection
    static func playerButton(_ name: String, coins: Int) -> String {
        "\(name), \(coins) Münzen, antippen zum Spielen"
    }
    static let playerSelectionTitle = "Wähle deinen Namen"
    
    // MARK: - Activity Selection
    static let raetselButton = "Rätsel spielen"
    static let zahlenButton = "Zahlen 1, 2, 3 spielen"
    static let zeichnenButton = "Zeichnen, noch gesperrt"
    static let logikButton = "Logik, noch gesperrt"
    
    // MARK: - Progress
    static func progressBar(coins: Int, max: Int = 10) -> String {
        "\(coins) von \(max) Münzen gesammelt"
    }
    static func coinIcon(count: Int) -> String {
        "\(count) Münze\(count == 1 ? "" : "n")"
    }
    
    // MARK: - Treasure
    static func treasureChest(coins: Int) -> String {
        "Schatzkiste, \(coins) Münzen"
    }
    static let youtube5Min = "5 Minuten YouTube schauen, kostet 10 Münzen"
    static let youtube10Min = "10 plus 2 Bonusminuten YouTube, kostet 20 Münzen"
    
    // MARK: - Grid Cells
    static func gridCell(row: Int, column: Int, color: String?) -> String {
        if let color = color {
            return "Reihe \(row), Spalte \(column), \(color)"
        } else {
            return "Reihe \(row), Spalte \(column), leer"
        }
    }
    
    // MARK: - Color Picker
    static let colorGreen = "Grüne Farbe wählen"
    static let colorYellow = "Gelbe Farbe wählen"
    static let colorGray = "Graue Farbe wählen"
    static let eraser = "Radierer, Farbe entfernen"
    static let reset = "Neustart, alles löschen"
    
    // MARK: - Numbers
    static func numberButton(_ number: Int) -> String {
        "Zahl \(number) wählen"
    }
    static func numberTrace(_ number: Int) -> String {
        "Zahl \(number) nachzeichnen"
    }
    
    // MARK: - Video
    static func videoCard(title: String) -> String {
        "\(title), zum Abspielen tippen"
    }
    static func videoTime(minutes: Int) -> String {
        "\(minutes) Minute\(minutes == 1 ? "" : "n") übrig"
    }
    
    // MARK: - Celebration
    static func celebration(coins: Int) -> String {
        "Super! \(coins) Münzen gesammelt!"
    }
    static let continueButton = "Weiter spielen"
    
    // MARK: - Parent Gate
    static let parentGateTitle = "Elternbereich, Rechenaufgabe lösen"
    static let parentGateInput = "Antwort eingeben"
    static let parentGateCancel = "Abbrechen"
    static let parentGateConfirm = "Bestätigen"
    
    // MARK: - Parent Dashboard
    static func dailyLimit(minutes: Int) -> String {
        "Tägliche Spielzeit, \(minutes) Minuten"
    }
    static func activityLock(name: String, locked: Bool) -> String {
        "\(name), \(locked ? "gesperrt" : "freigegeben")"
    }
}
```

### Step 2: Apply Labels to Components

Update `WoodButton.swift`:

```swift
struct WoodButton: View {
    let text: String?
    let icon: String?
    let accessibilityLabel: String? // Add this
    let action: () -> Void
    
    var body: some View {
        Button(action: action) {
            // ... existing code
        }
        .accessibilityLabel(accessibilityLabel ?? text ?? "")
        .accessibilityHint("Doppeltippen zum Aktivieren")
        .accessibilityAddTraits(.isButton)
    }
}
```

### Step 3: Implement Per-Screen Labels

#### Loading Screen
```swift
struct LoadingView: View {
    var body: some View {
        VStack {
            // Progress bar
            ProgressBar(progress: loadingProgress)
                .accessibilityLabel("Spielewelt lädt")
                .accessibilityValue("\(Int(loadingProgress * 100)) Prozent")
                .accessibilityAddTraits(.updatesFrequently)
            
            // Loading text
            Text("Lade Spielewelt...")
                .accessibilityHidden(true) // Redundant with progress bar
            
            // Bennie character
            BennieView(expression: loadingProgress < 1.0 ? .idle : .waving)
                .accessibilityLabel("Bennie der Bär")
                .accessibilityHidden(true) // Decorative
        }
    }
}
```

#### Player Selection Screen
```swift
struct PlayerSelectionView: View {
    var body: some View {
        VStack {
            Text("Wer spielt heute?")
                .accessibilityLabel(AccessibilityLabels.playerSelectionTitle)
                .accessibilityAddTraits(.isHeader)
            
            HStack {
                PlayerButton(
                    player: alexander,
                    action: { selectPlayer(alexander) }
                )
                .accessibilityLabel(
                    AccessibilityLabels.playerButton(
                        alexander.name, 
                        coins: alexander.coins
                    )
                )
                
                PlayerButton(
                    player: oliver,
                    action: { selectPlayer(oliver) }
                )
                .accessibilityLabel(
                    AccessibilityLabels.playerButton(
                        oliver.name, 
                        coins: oliver.coins
                    )
                )
            }
        }
    }
}
```

#### Home Screen
```swift
struct HomeView: View {
    var body: some View {
        VStack {
            // Title
            Text("Waldabenteuer")
                .accessibilityLabel("Waldabenteuer, Hauptmenü")
                .accessibilityAddTraits(.isHeader)
            
            // Activity signs
            HStack {
                ActivitySign(activity: .raetsel)
                    .accessibilityLabel(AccessibilityLabels.raetselButton)
                    .accessibilityAddTraits(.isButton)
                
                ActivitySign(activity: .zahlen)
                    .accessibilityLabel(AccessibilityLabels.zahlenButton)
                    .accessibilityAddTraits(.isButton)
                
                ActivitySign(activity: .zeichnen)
                    .accessibilityLabel(AccessibilityLabels.zeichnenButton)
                    .accessibilityAddTraits(.isButton)
                    .accessibilityAddTraits(.isNotEnabled) // Locked
                
                ActivitySign(activity: .logik)
                    .accessibilityLabel(AccessibilityLabels.logikButton)
                    .accessibilityAddTraits(.isButton)
                    .accessibilityAddTraits(.isNotEnabled) // Locked
            }
            
            // Progress bar
            ProgressBar(coins: player.coins)
                .accessibilityLabel(
                    AccessibilityLabels.progressBar(coins: player.coins)
                )
            
            // Treasure chest
            TreasureChest(coins: player.coins)
                .accessibilityLabel(
                    AccessibilityLabels.treasureChest(coins: player.coins)
                )
                .accessibilityAddTraits(.isButton)
                .accessibilityHint(
                    player.coins >= 10 
                    ? "Doppeltippen um YouTube zu schauen"
                    : "Du brauchst \(10 - player.coins) mehr Münzen"
                )
            
            // Characters (decorative)
            BennieView(expression: .pointing)
                .accessibilityHidden(true)
            
            LemmingeView(expression: .hiding)
                .accessibilityHidden(true)
        }
    }
}
```

#### Puzzle Matching Screen
```swift
struct PuzzleMatchingView: View {
    var body: some View {
        VStack {
            HStack {
                // Target grid
                GridView(grid: targetGrid, title: "ZIEL")
                    .accessibilityLabel("Zielvorlage")
                    .accessibilityHint("Das musst du nachbauen")
                
                // Player grid
                GridView(grid: playerGrid, title: "DU") { row, col in
                    tapCell(row: row, col: col)
                }
                .accessibilityLabel("Dein Spielfeld")
                .accessibilityHint("Tippe auf Felder um Farben zu setzen")
                
                // Grid cells individual labels
                ForEach(0..<3) { row in
                    ForEach(0..<3) { col in
                        GridCell(row: row, col: col, color: playerGrid[row][col])
                            .accessibilityLabel(
                                AccessibilityLabels.gridCell(
                                    row: row + 1,
                                    column: col + 1,
                                    color: playerGrid[row][col]
                                )
                            )
                    }
                }
            }
            
            // Color picker
            HStack {
                ColorButton(color: .green)
                    .accessibilityLabel(AccessibilityLabels.colorGreen)
                
                ColorButton(color: .yellow)
                    .accessibilityLabel(AccessibilityLabels.colorYellow)
                
                ColorButton(color: .gray)
                    .accessibilityLabel(AccessibilityLabels.colorGray)
                
                EraserButton()
                    .accessibilityLabel(AccessibilityLabels.eraser)
                
                ResetButton()
                    .accessibilityLabel(AccessibilityLabels.reset)
                    .accessibilityHint("Löscht alle Farben")
            }
        }
    }
}
```

#### Treasure Screen
```swift
struct TreasureView: View {
    var body: some View {
        VStack {
            // Chest visual
            TreasureChestOpen(coins: player.coins)
                .accessibilityLabel(
                    AccessibilityLabels.treasureChest(coins: player.coins)
                )
                .accessibilityHidden(true) // Decorative
            
            // YouTube buttons
            YouTubeButton(duration: 5, cost: 10)
                .accessibilityLabel(AccessibilityLabels.youtube5Min)
                .accessibilityAddTraits(
                    player.coins >= 10 ? .isButton : .isNotEnabled
                )
            
            YouTubeButton(duration: 12, cost: 20)
                .accessibilityLabel(AccessibilityLabels.youtube10Min)
                .accessibilityAddTraits(
                    player.coins >= 20 ? .isButton : .isNotEnabled
                )
        }
    }
}
```

---

## 🔧 Implementation Checklist

### Utilities
- [ ] Create `AccessibilityLabels.swift`
- [ ] Test all label strings in German
- [ ] Verify max 7 words per label
- [ ] Verify literal language (no metaphors)

### Components
- [ ] Update `WoodButton` with accessibility
- [ ] Update `WoodSign` with accessibility
- [ ] Update `ProgressBar` with accessibility
- [ ] Update `GridCell` with accessibility
- [ ] Update `ColorPicker` with accessibility

### Screens (Apply Labels)
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

### Navigation Flow
- [ ] Define accessibility navigation order
- [ ] Test tab navigation with VoiceOver
- [ ] Verify logical reading order
- [ ] Add accessibility containers where needed

### Testing
- [ ] Enable VoiceOver on iPad
- [ ] Navigate through each screen
- [ ] Verify all labels are spoken
- [ ] Verify hints are helpful
- [ ] Test with eyes closed
- [ ] Document any issues

---

## 📊 Validation Criteria

### Each Screen Must Have

```swift
✅ All interactive elements have labels
✅ All labels are in German
✅ All labels are descriptive (child understands)
✅ Decorative elements marked as hidden
✅ Logical navigation order
✅ Appropriate traits (.isButton, .isHeader, etc.)
✅ Helpful hints where needed
```

### Common Patterns

```swift
// Button
.accessibilityLabel("Klare Beschreibung")
.accessibilityHint("Was passiert beim Tippen")
.accessibilityAddTraits(.isButton)

// Decorative image
.accessibilityHidden(true)

// Dynamic value
.accessibilityLabel("Beschreibung")
.accessibilityValue("Aktueller Wert")
.accessibilityAddTraits(.updatesFrequently)

// Header
.accessibilityLabel("Titel")
.accessibilityAddTraits(.isHeader)

// Disabled
.accessibilityAddTraits(.isNotEnabled)
```

---

## 🚨 Common Issues & Solutions

### Issue: Label too long
```swift
// ❌ WRONG (> 7 words)
.accessibilityLabel("Tippe hier um die Aktivität Rätsel zu starten und Münzen zu verdienen")

// ✅ CORRECT (≤ 7 words)
.accessibilityLabel("Rätsel spielen")
.accessibilityHint("Münzen verdienen")
```

### Issue: Using English
```swift
// ❌ WRONG
.accessibilityLabel("Tap to play")

// ✅ CORRECT
.accessibilityLabel("Antippen zum Spielen")
```

### Issue: Not descriptive enough
```swift
// ❌ WRONG
.accessibilityLabel("Button")

// ✅ CORRECT
.accessibilityLabel("Zurück zum Waldabenteuer")
```

### Issue: Redundant information
```swift
// ❌ WRONG
Text("Rätsel")
    .accessibilityLabel("Text Rätsel") // Redundant "Text"

// ✅ CORRECT
Text("Rätsel")
    .accessibilityLabel("Rätsel spielen")
```

---

## 📝 Documentation

Create VoiceOver audit: `audits/voiceover_audit.md`

```markdown
# VoiceOver Audit Report

**Date**: [DATE]
**Auditor**: [NAME]
**Device**: iPad with VoiceOver enabled

## Navigation Test Results

### Loading Screen
- [ ] Screen title announced
- [ ] Progress announced
- [ ] Percentage spoken correctly

### Player Selection
- [ ] Title announced
- [ ] Both player buttons accessible
- [ ] Coin counts spoken

[... continue for all screens]

## Issues Found
1. [Issue description]
   - Screen: [Screen name]
   - Element: [Element name]
   - Expected: [Expected label]
   - Actual: [Actual behavior]
   - Fix: [How to fix]

## Sign-off
- [ ] All screens tested
- [ ] All issues documented
- [ ] Critical issues fixed
- [ ] Retest after fixes
```

---

## ✅ Success Criteria

This phase is complete when:

1. ✅ All interactive elements have German labels
2. ✅ All labels follow language rules (≤7 words, literal)
3. ✅ Decorative elements marked as hidden
4. ✅ Navigation order is logical
5. ✅ VoiceOver can navigate entire app
6. ✅ Child tester can use app with VoiceOver
7. ✅ No accessibility warnings in Xcode
8. ✅ Audit report complete

---

## 🔄 Maintenance

**After this phase**:
- Every new element needs accessibility label
- PR checklist includes VoiceOver test
- Labels in German only
- Follow AccessibilityLabels utility pattern

---

*Next Phase*: 13.3 - Color Blindness Accommodations
*Previous Phase*: 13.1 - Touch Target Audit
