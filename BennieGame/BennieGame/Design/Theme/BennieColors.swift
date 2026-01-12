import SwiftUI

// ═══════════════════════════════════════════════════════════════════════════
// BennieColors - Design System Color Palette
// ═══════════════════════════════════════════════════════════════════════════
// Source of truth: PLAYBOOK_CONDENSED.md
// All colors MUST match exactly - no approximations
// ═══════════════════════════════════════════════════════════════════════════

enum BennieColors {

    // ═══════════════════════════════════════════════════════════════════
    // CHARACTER COLORS (NON-NEGOTIABLE)
    // ═══════════════════════════════════════════════════════════════════

    /// Bennie's fur color - warm brown
    /// CRITICAL: Bennie must NEVER have clothing, vest, or accessories
    static let bennieBrown = Color(hex: "8C7259")

    /// Bennie's snout/muzzle - lighter tan
    /// Only the snout should be this color, not belly
    static let bennieTan = Color(hex: "C4A574")

    /// Bennie's nose - dark brown
    static let bennieNose = Color(hex: "3D2B1F")

    /// Lemminge body color - soft blue
    /// CRITICAL: NEVER green, NEVER brown - always this exact blue
    static let lemmingeBlue = Color(hex: "6FA8DC")

    /// Lemminge nose and paw pads - soft pink
    static let lemmingePink = Color(hex: "E8A0A0")

    /// Lemminge belly - warm cream white
    static let lemmingeBelly = Color(hex: "FAF5EB")

    // ═══════════════════════════════════════════════════════════════════
    // UI COLORS
    // ═══════════════════════════════════════════════════════════════════

    /// Success state - muted forest green
    /// Used for correct answers, progress fill, positive feedback
    static let success = Color(hex: "99BF8C")

    /// Coin and treasure gold
    /// Used for coins, treasure highlights, rewards
    static let coinGold = Color(hex: "D9C27A")

    /// Light wood - buttons, signs (lighter areas)
    static let woodLight = Color(hex: "C4A574")

    /// Medium wood - buttons, signs (main areas)
    static let woodMedium = Color(hex: "A67C52")

    /// Dark wood - borders, shadows, accents
    static let woodDark = Color(hex: "6B4423")

    /// Rope/twine color for hanging signs
    static let rope = Color(hex: "B8956B")

    /// Chain color for locked content
    static let chain = Color(hex: "6B6B6B")

    // ═══════════════════════════════════════════════════════════════════
    // ENVIRONMENT COLORS
    // ═══════════════════════════════════════════════════════════════════

    /// General woodland green - mid-ground trees
    static let woodland = Color(hex: "738F66")

    /// Distant/far trees - blue-green muted
    static let farTrees = Color(hex: "4A6B5C")

    /// Near foliage - brighter forest green
    static let nearFoliage = Color(hex: "7A9973")

    /// Sky - soft blue
    static let sky = Color(hex: "B3D1E6")

    /// Cream background - warm off-white
    static let cream = Color(hex: "FAF5EB")

    /// Light rays through trees - warm yellow at 30% opacity
    static let lightRays = Color(hex: "F5E6C8").opacity(0.3)

    /// Moss on rocks and trees
    static let moss = Color(hex: "5D6B4D")

    /// Stone path/tablet color
    static let pathStone = Color(hex: "A8A090")

    // ═══════════════════════════════════════════════════════════════════
    // TEXT COLORS
    // ═══════════════════════════════════════════════════════════════════

    /// Text on wood surfaces - dark brown
    static let textOnWood = Color(hex: "4A4036")

    /// General dark text
    static let textDark = Color(hex: "2D2D2D")

    // ═══════════════════════════════════════════════════════════════════
    // FORBIDDEN COLORS - NEVER USE
    // ═══════════════════════════════════════════════════════════════════
    // - Pure Red #FF0000 (alarming, not autism-friendly)
    // - Pure White #FFFFFF for large areas (too harsh)
    // - Pure Black #000000 for large areas (too harsh)
    // - Any neon colors (overstimulating)
    // - Any color with saturation > 80% (overstimulating)
    // ═══════════════════════════════════════════════════════════════════
}
