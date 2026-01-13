import SwiftUI

// ═══════════════════════════════════════════════════════════════════════════
// ForestBackground - Parallax forest background for all screens
// ═══════════════════════════════════════════════════════════════════════════
// 4-layer parallax depth with warm golden light from upper-left
// Uses forest_layer_far, forest_layer_mid, forest_layer_near, forest_layer_glow
// ═══════════════════════════════════════════════════════════════════════════

/// Parallax forest background with 4 layers
/// Consistent across all screens for magical forest theme
struct ForestBackground: View {
    var body: some View {
        GeometryReader { geometry in
            ZStack {
                // Base gradient (sky to forest floor)
                LinearGradient(
                    colors: [
                        BennieColors.sky.opacity(0.6),
                        BennieColors.cream
                    ],
                    startPoint: .top,
                    endPoint: .bottom
                )

                // Layer 1: Far trees (misty)
                Image("Backgrounds/forest_layer_far")
                    .resizable()
                    .aspectRatio(contentMode: .fill)
                    .frame(width: geometry.size.width, height: geometry.size.height)
                    .clipped()
                    .opacity(0.9)

                // Layer 2: Mid trees (sage)
                Image("Backgrounds/forest_layer_mid")
                    .resizable()
                    .aspectRatio(contentMode: .fill)
                    .frame(width: geometry.size.width, height: geometry.size.height)
                    .clipped()
                    .opacity(0.85)

                // Layer 3: Near foliage
                Image("Backgrounds/forest_layer_near")
                    .resizable()
                    .aspectRatio(contentMode: .fill)
                    .frame(width: geometry.size.width, height: geometry.size.height)
                    .clipped()
                    .opacity(0.8)

                // Layer 4: Light glow overlay
                Image("Backgrounds/forest_layer_glow")
                    .resizable()
                    .aspectRatio(contentMode: .fill)
                    .frame(width: geometry.size.width, height: geometry.size.height)
                    .clipped()
                    .blendMode(.softLight)
                    .opacity(0.3)

                // Warm golden light from upper-left
                RadialGradient(
                    colors: [
                        Color(hex: "F5E6C8").opacity(0.3),
                        Color.clear
                    ],
                    center: .topLeading,
                    startRadius: 0,
                    endRadius: geometry.size.width * 0.7
                )
            }
        }
        .ignoresSafeArea()
    }
}

// MARK: - Previews

#Preview("ForestBackground") {
    ForestBackground()
}
