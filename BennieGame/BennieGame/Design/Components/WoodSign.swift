import SwiftUI

// ═══════════════════════════════════════════════════════════════════════════
// WoodSign - Hanging wood sign for activity selection
// ═══════════════════════════════════════════════════════════════════════════
// Features rope decoration at top, locked/unlocked states
// Uses ChildFriendlyButton when tappable (inherits 96pt enforcement)
// ═══════════════════════════════════════════════════════════════════════════

/// Wood sign component with hanging rope decoration
/// Can be tappable or display-only, with locked/unlocked states
struct WoodSign: View {
    let title: String
    var isLocked: Bool = false
    var action: (() -> Void)? = nil

    var body: some View {
        VStack(spacing: 0) {
            // Rope at top
            RopeDecoration()

            // Sign content
            signContent
        }
    }

    @ViewBuilder
    private var signContent: some View {
        if let action = action {
            ChildFriendlyButton(action: action) {
                signBody
            }
        } else {
            signBody
        }
    }

    private var signBody: some View {
        ZStack {
            // Wood background
            RoundedRectangle(cornerRadius: 8)
                .fill(BennieColors.woodMedium)
                .overlay(
                    RoundedRectangle(cornerRadius: 8)
                        .stroke(BennieColors.woodDark, lineWidth: 2)
                )

            // Title text
            Text(title)
                .font(BennieFont.button(20))
                .foregroundColor(BennieColors.textOnWood)
                .multilineTextAlignment(.center)
                .padding(.horizontal, 12)

            // Locked overlay
            if isLocked {
                LockedOverlay()
            }
        }
        .frame(minWidth: 120, minHeight: 96)
    }
}

// MARK: - Rope Decoration

/// Simple rope connector for hanging signs
struct RopeDecoration: View {
    var body: some View {
        VStack(spacing: 0) {
            // Top attachment point
            Circle()
                .fill(BennieColors.rope)
                .frame(width: 12, height: 12)

            // Rope segment
            Rectangle()
                .fill(BennieColors.rope)
                .frame(width: 6, height: 24)
        }
    }
}

// MARK: - Locked Overlay

/// Overlay shown on locked activities/content
struct LockedOverlay: View {
    var body: some View {
        ZStack {
            // Darkened background
            BennieColors.woodDark.opacity(0.3)

            // Chain pattern + lock icon
            VStack(spacing: 4) {
                // Horizontal chain
                HStack(spacing: 2) {
                    ForEach(0..<3, id: \.self) { _ in
                        Capsule()
                            .stroke(BennieColors.chain, lineWidth: 2)
                            .frame(width: 16, height: 8)
                    }
                }

                // Lock icon
                Image(systemName: "lock.fill")
                    .font(.system(size: 24))
                    .foregroundColor(BennieColors.chain)
            }
        }
        .clipShape(RoundedRectangle(cornerRadius: 8))
    }
}

// MARK: - Previews

#Preview("WoodSign - Unlocked") {
    WoodSign(title: "Rätsel") {
        print("Rätsel tapped")
    }
    .padding()
}

#Preview("WoodSign - Locked") {
    WoodSign(title: "Zeichnen", isLocked: true) {
        print("Zeichnen tapped")
    }
    .padding()
}

#Preview("WoodSign - Display Only") {
    WoodSign(title: "Waldabenteuer")
        .padding()
}

#Preview("WoodSign - Activity Row") {
    HStack(spacing: 20) {
        WoodSign(title: "Rätsel") { }
        WoodSign(title: "Zahlen") { }
        WoodSign(title: "Zeichnen", isLocked: true) { }
        WoodSign(title: "Logik", isLocked: true) { }
    }
    .padding()
}
