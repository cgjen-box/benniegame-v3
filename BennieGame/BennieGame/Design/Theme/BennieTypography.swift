import SwiftUI

// ═══════════════════════════════════════════════════════════════════════════
// BennieTypography - Design System Font Styles
// ═══════════════════════════════════════════════════════════════════════════
// Uses SF Rounded (built into iOS) - no custom fonts required
// All text should use these functions for consistency
// ═══════════════════════════════════════════════════════════════════════════

enum BennieFont {

    // ═══════════════════════════════════════════════════════════════════
    // PRIMARY FONT STYLES
    // ═══════════════════════════════════════════════════════════════════

    /// Titles and headers - 32-48pt Bold
    /// Use for screen titles, activity names, celebratory messages
    /// Default: 40pt
    static func title(_ size: CGFloat = 40) -> Font {
        .system(size: size, weight: .bold, design: .rounded)
    }

    /// Body text - 17-24pt Regular
    /// Use for instructions, descriptions, narrator text
    /// Default: 20pt
    static func body(_ size: CGFloat = 20) -> Font {
        .system(size: size, weight: .regular, design: .rounded)
    }

    /// Button labels - 20-28pt Semibold
    /// Use for all interactive button text
    /// Default: 24pt
    static func button(_ size: CGFloat = 24) -> Font {
        .system(size: size, weight: .semibold, design: .rounded)
    }

    /// Small labels - 14-17pt Medium
    /// Use for captions, hints, secondary information
    /// Default: 16pt
    static func label(_ size: CGFloat = 16) -> Font {
        .system(size: size, weight: .medium, design: .rounded)
    }

    /// Large numbers - 40-72pt Bold
    /// Use for dice, coin counts, scores, number displays
    /// Default: 56pt
    static func number(_ size: CGFloat = 56) -> Font {
        .system(size: size, weight: .bold, design: .rounded)
    }

    // ═══════════════════════════════════════════════════════════════════
    // SPECIALIZED STYLES
    // ═══════════════════════════════════════════════════════════════════

    /// Screen header - slightly smaller than title
    /// Use for section headers within screens
    /// Default: 32pt Bold
    static func screenHeader(_ size: CGFloat = 32) -> Font {
        .system(size: size, weight: .bold, design: .rounded)
    }

    /// Speech bubble text - friendly size for character dialogue
    /// Max 7 words per sentence (German, literal language)
    /// Default: 22pt Regular
    static func speech(_ size: CGFloat = 22) -> Font {
        .system(size: size, weight: .regular, design: .rounded)
    }

    /// Celebration text - extra large for success moments
    /// Use for "Super!", "Toll gemacht!" etc.
    /// Default: 48pt Bold
    static func celebration(_ size: CGFloat = 48) -> Font {
        .system(size: size, weight: .bold, design: .rounded)
    }
}
