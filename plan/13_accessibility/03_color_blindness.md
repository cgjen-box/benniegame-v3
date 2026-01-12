# Phase 13.3: Color Blindness Accommodations

**Status**: 🔵 Not Started
**Priority**: Critical
**Estimated Time**: 2 days
**Dependencies**: Phase 2 (Design System), Phase 4 (Activities)

---

## 📋 Overview

Implement shape indicators and texture patterns to ensure color-dependent information is accessible to children with color blindness.

**Playbook Reference**: `C:\Users\christoph\Bennie und die Lemminge v3\docs\playbook\05-technical-requirements.md` Section 5.7 "Color Blindness Considerations"

---

## 🎯 Requirements from Playbook

### Primary Concerns

| Issue | Solution (from Playbook) |
|-------|--------------------------|
| Green/Yellow confusion | Add shape indicators (circle/square) |
| Progress bar | Texture pattern in fill |
| Grid colors | Different shape overlays per color |

### Reference
- **Playbook**: `C:\Users\christoph\Bennie und die Lemminge v3\docs\playbook\05-technical-requirements.md` (Section 5.7)
- **Color System**: `C:\Users\christoph\Bennie und die Lemminge v3\docs\playbook\01-brand-identity.md` (Section 1.3)

---

## 🎯 Implementation Plan

### 13.3.1: Shape Indicator System

Create visual alternatives for all color-dependent information.

#### Color-Shape Mapping

```swift
// File: BennieGame/Design/Accessibility/ColorShapeIndicators.swift

import SwiftUI

enum ColorShapeIndicator {
    case green      // Circle ●
    case yellow     // Square ■
    case gray       // Triangle ▲
    
    var shape: some Shape {
        switch self {
        case .green:
            return AnyShape(Circle())
        case .yellow:
            return AnyShape(RoundedRectangle(cornerRadius: 4))
        case .gray:
            return AnyShape(Triangle())
        }
    }
    
    var texture: Image {
        switch self {
        case .green: 
            return Image("texture_dots")      // Dotted pattern
        case .yellow: 
            return Image("texture_stripes")   // Diagonal stripes
        case .gray: 
            return Image("texture_crosshatch") // Crosshatch
        }
    }
    
    var accessibilityLabel: String {
        switch self {
        case .green: return "Grün, runde Form"
        case .yellow: return "Gelb, quadratische Form"
        case .gray: return "Grau, dreieckige Form"
        }
    }
}

// Custom triangle shape
struct Triangle: Shape {
    func path(in rect: CGRect) -> Path {
        var path = Path()
        path.move(to: CGPoint(x: rect.midX, y: rect.minY))
        path.addLine(to: CGPoint(x: rect.maxX, y: rect.maxY))
        path.addLine(to: CGPoint(x: rect.minX, y: rect.maxY))
        path.closeSubpath()
        return path
    }
}

// Type-erased shape for enum
struct AnyShape: Shape {
    private let _path: (CGRect) -> Path
    
    init<S: Shape>(_ shape: S) {
        _path = { rect in
            shape.path(in: rect)
        }
    }
    
    func path(in rect: CGRect) -> Path {
        _path(rect)
    }
}
```

---

### 13.3.2: Puzzle Grid Enhancement

Add shape overlays to puzzle grid cells.

**Reference Screen**: `C:\Users\christoph\Bennie und die Lemminge v3\design\references\screens\Reference_Matching_Game_Screen.png`

#### Enhanced Grid Cell

```swift
// File: BennieGame/Features/Activities/Raetsel/Components/PuzzleGridCell.swift

struct PuzzleGridCell: View {
    let color: BennieColors.PuzzleColor?
    let shapeIndicator: ColorShapeIndicator?
    
    var body: some View {
        ZStack {
            // Background color
            Rectangle()
                .fill(color?.color ?? Color.clear)
            
            // Shape indicator overlay (20% opacity)
            if let indicator = shapeIndicator {
                indicator.shape
                    .fill(Color.white.opacity(0.2))
                    .padding(8)
            }
            
            // Texture pattern (subtle)
            if let indicator = shapeIndicator {
                indicator.texture
                    .resizable()
                    .scaledToFill()
                    .opacity(0.15)
            }
        }
        .frame(width: 96, height: 96)
        .cornerRadius(8)
        .accessibilityLabel(shapeIndicator?.accessibilityLabel ?? "Leere Zelle")
    }
}
```

---

### 13.3.3: Progress Bar Texture

Add texture pattern to progress fill.

**Reference**: Playbook Section 4.3 "Progress Bar Component"

```swift
// File: BennieGame/Design/Components/ProgressBar.swift

struct ProgressBarView: View {
    let currentCoins: Int
    let maxCoins: Int = 10
    
    var body: some View {
        HStack {
            // Berry decoration left
            Image("berry_cluster_left")
            
            // Wood trough progress bar
            ZStack(alignment: .leading) {
                // Empty state (dark wood interior)
                RoundedRectangle(cornerRadius: 8)
                    .fill(Color(hex: "6B4423"))
                
                // Fill state with texture
                ZStack(alignment: .leading) {
                    // Base color
                    RoundedRectangle(cornerRadius: 8)
                        .fill(BennieColors.success)
                        .frame(width: progressWidth)
                    
                    // Texture overlay for color blindness
                    Image("texture_diagonal_stripes")
                        .resizable()
                        .scaledToFill()
                        .opacity(0.2)
                        .frame(width: progressWidth)
                        .clipShape(RoundedRectangle(cornerRadius: 8))
                }
                
                // Coin slots overlay
                CoinSlotsView(filled: currentCoins % 10)
            }
            .frame(height: 40)
            
            // Berry decoration right
            Image("berry_cluster_right")
            
            // Chest icon(s)
            ChestIndicator(chests: currentCoins / 10)
        }
        .accessibilityLabel("\(currentCoins) von \(maxCoins) Münzen gesammelt")
    }
    
    var progressWidth: CGFloat {
        let progress = CGFloat(currentCoins % maxCoins) / CGFloat(maxCoins)
        return 400 * progress  // Total bar width
    }
}
```

---

### 13.3.4: Color Picker Enhancement

Add shape previews to color picker.

**Reference Screen**: `C:\Users\christoph\Bennie und die Lemminge v3\design\references\screens\Reference_Matching_Game_Screen.png`

```swift
// File: BennieGame/Features/Activities/Raetsel/Components/ColorPicker.swift

struct ColorPickerButton: View {
    let color: BennieColors.PuzzleColor
    let indicator: ColorShapeIndicator
    let isSelected: Bool
    let action: () -> Void
    
    var body: some View {
        Button(action: action) {
            ZStack {
                // Leaf-shaped background
                Image("color_picker_leaf")
                    .renderingMode(.template)
                    .foregroundColor(color.color)
                
                // Shape indicator
                indicator.shape
                    .fill(Color.white)
                    .frame(width: 30, height: 30)
                
                // Selection ring
                if isSelected {
                    Circle()
                        .stroke(BennieColors.woodland, lineWidth: 4)
                        .frame(width: 76, height: 76)
                }
            }
            .frame(width: 80, height: 80)
        }
        .accessibilityLabel("\(color.germanName), \(indicator.accessibilityLabel)")
    }
}
```

---

### 13.3.5: Texture Asset Creation

Create texture pattern images for overlays.

**Asset Location**: `C:\Users\christoph\Bennie und die Lemminge v3\Resources\Assets.xcassets\Textures\`

#### Required Textures

| Texture | Pattern | Usage |
|---------|---------|-------|
| `texture_dots` | Small dots | Green elements |
| `texture_stripes` | Diagonal lines | Yellow elements |
| `texture_crosshatch` | Grid pattern | Gray elements |
| `texture_diagonal_stripes` | Wide diagonals | Progress bar |

**Specifications**:
- Format: PNG with alpha
- Size: 50x50pt @1x (tileable)
- Color: White (tinted at runtime)
- Opacity: 15-20% when applied

---

## 📋 Screen-by-Screen Checklist

### Puzzle Matching Screen
- [ ] Grid cells have shape indicators
- [ ] Grid cells have texture overlays
- [ ] Color picker shows shapes
- [ ] Selected state is clear
- [ ] VoiceOver describes shapes

### Numbers Screen
- [ ] Stone tablet numbers have subtle texture backgrounds
- [ ] Selected number has clear non-color indicator

### Progress Bar (All Screens)
- [ ] Progress fill has texture pattern
- [ ] Coin slots are visible regardless of fill
- [ ] Chest icons have proper contrast

---

## 🧪 Testing Requirements

### Manual Testing

Test with color blindness simulators:
1. **Protanopia** (red-blind): Green/yellow confusion
2. **Deuteranopia** (green-blind): Green/yellow confusion
3. **Tritanopia** (blue-blind): Blue/yellow confusion

**Tool**: Use iOS Accessibility Inspector's Color Filter feature
**Path**: Settings → Accessibility → Display & Text Size → Color Filters

### Validation Checklist

```
✅ All color-dependent information has shape alternative
✅ Texture patterns are visible but not overwhelming
✅ Shapes are distinguishable at 96pt size
✅ Color blindness simulators confirm clarity
✅ VoiceOver describes both color and shape
✅ Performance remains smooth with overlays
```

---

## 📊 Success Criteria

### Phase 13.3 Complete When:

1. ✅ ColorShapeIndicators.swift exists and is integrated
2. ✅ All texture assets are created
3. ✅ Puzzle grid cells show shape + texture
4. ✅ Progress bar has textured fill
5. ✅ Color picker shows shape previews
6. ✅ Tested with all 3 color blindness types
7. ✅ No functionality lost for color-blind users
8. ✅ VoiceOver includes shape descriptions

---

## 🔗 Integration Points

### Design System Updates
- Add ColorShapeIndicators to design system
- Add texture assets to asset catalog
- Update BennieColors enum with shape mappings

### Component Updates
- PuzzleGridCell: Add shape overlay support
- ProgressBarView: Add texture to fill
- ColorPickerButton: Add shape preview

### Testing Updates
- Add color blindness simulation tests
- Verify texture visibility
- Validate shape distinguishability

---

## 📚 References

### Playbook
- Section 5.7: Accessibility - Color Blindness Considerations
- Section 1.3: Color System
- Section 4.4: Puzzle Matching Screen

### Design References
- `Reference_Matching_Game_Screen.png`: Grid layout
- `Reference_Menu_Screen.png`: Progress bar

### External Resources
- [Apple Human Interface Guidelines: Color and Contrast](https://developer.apple.com/design/human-interface-guidelines/accessibility#Color-and-contrast)
- [WebAIM: Designing for Color Blindness](https://webaim.org/articles/visual/colorblind)

---

*Phase Owner*: Development Team
*Playbook Compliance*: Section 5.7
*Last Updated*: 2026-01-11
