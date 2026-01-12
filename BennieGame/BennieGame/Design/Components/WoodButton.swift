import SwiftUI

// ═══════════════════════════════════════════════════════════════════════════
// WoodButton - Primary interactive button component
// ═══════════════════════════════════════════════════════════════════════════
// Uses ChildFriendlyButton as base (inherits 96pt touch target enforcement)
// Wood gradient background with dark border, matching reference images
// ═══════════════════════════════════════════════════════════════════════════

/// Wood-styled button for main menu actions and navigation
/// Always meets 96pt minimum touch target via ChildFriendlyButton base
struct WoodButton: View {
    let title: String
    var icon: String? = nil
    let action: () -> Void

    var body: some View {
        ChildFriendlyButton(action: action) {
            VStack(spacing: 8) {
                if let icon = icon {
                    Image(systemName: icon)
                        .font(.system(size: 32))
                }
                Text(title)
                    .font(BennieFont.button(24))
            }
            .foregroundColor(BennieColors.textOnWood)
            .frame(minWidth: 160, minHeight: 140)
            .padding(16)
            .background(
                RoundedRectangle(cornerRadius: 12)
                    .fill(
                        LinearGradient(
                            colors: [BennieColors.woodLight, BennieColors.woodMedium],
                            startPoint: .top,
                            endPoint: .bottom
                        )
                    )
            )
            .overlay(
                RoundedRectangle(cornerRadius: 12)
                    .stroke(BennieColors.woodDark, lineWidth: 3)
            )
            .shadow(color: .black.opacity(0.2), radius: 4, x: 0, y: 2)
        }
    }
}

// MARK: - Convenience Initializers

extension WoodButton {
    /// Create a WoodButton with just a title
    init(_ title: String, action: @escaping () -> Void) {
        self.title = title
        self.icon = nil
        self.action = action
    }

    /// Create a WoodButton with an icon and title
    init(_ title: String, icon: String, action: @escaping () -> Void) {
        self.title = title
        self.icon = icon
        self.action = action
    }
}

// MARK: - Previews

#Preview("WoodButton - Title Only") {
    WoodButton("Spielen") {
        print("Play tapped")
    }
    .padding()
}

#Preview("WoodButton - With Icon") {
    WoodButton("Rätsel", icon: "puzzlepiece.fill") {
        print("Puzzle tapped")
    }
    .padding()
}

#Preview("WoodButton - Multiple") {
    HStack(spacing: 20) {
        WoodButton("Rätsel", icon: "puzzlepiece.fill") { }
        WoodButton("Zahlen", icon: "number") { }
    }
    .padding()
}
