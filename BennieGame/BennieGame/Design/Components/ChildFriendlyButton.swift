import SwiftUI
import UIKit

// ═══════════════════════════════════════════════════════════════════════════
// ChildFriendlyButton - Base component for all interactive elements
// ═══════════════════════════════════════════════════════════════════════════
// CRITICAL: Enforces 96pt minimum touch target (NON-NEGOTIABLE)
// All buttons in the app MUST use this as their base
// ═══════════════════════════════════════════════════════════════════════════

/// Base button wrapper that enforces autism-friendly touch targets
/// All interactive elements in the app should use this component
struct ChildFriendlyButton<Label: View>: View {
    let action: () -> Void
    @ViewBuilder let label: () -> Label

    /// Minimum touch target for autism-friendly design (96pt × 96pt)
    /// This is NON-NEGOTIABLE - never reduce this value
    static var minimumTouchTarget: CGFloat { 96 }

    var body: some View {
        Button(action: {
            // Gentle haptic feedback
            let impact = UIImpactFeedbackGenerator(style: .light)
            impact.impactOccurred()
            action()
        }) {
            label()
                .frame(
                    minWidth: Self.minimumTouchTarget,
                    minHeight: Self.minimumTouchTarget
                )
                .contentShape(Rectangle())
        }
        .buttonStyle(ChildButtonStyle())
    }
}

/// Button style with gentle press animation
/// Animation is subtle: 0.95 scale over 0.1s (never use shaking or flashing)
struct ChildButtonStyle: ButtonStyle {
    func makeBody(configuration: Configuration) -> some View {
        configuration.label
            .scaleEffect(configuration.isPressed ? 0.95 : 1.0)
            .animation(.easeOut(duration: 0.1), value: configuration.isPressed)
    }
}

// MARK: - Previews

#Preview("ChildFriendlyButton - Text") {
    ChildFriendlyButton(action: { print("Tapped") }) {
        Text("Spielen")
            .font(BennieFont.button())
            .foregroundColor(BennieColors.textOnWood)
            .padding()
            .background(BennieColors.woodMedium)
            .cornerRadius(12)
    }
}

#Preview("ChildFriendlyButton - Icon") {
    ChildFriendlyButton(action: { print("Tapped") }) {
        Image(systemName: "house.fill")
            .font(.system(size: 40))
            .foregroundColor(BennieColors.textOnWood)
            .padding()
            .background(BennieColors.woodMedium)
            .cornerRadius(12)
    }
}
