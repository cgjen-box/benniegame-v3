import SwiftUI
import Lottie

// ═══════════════════════════════════════════════════════════════════════════
// LottieView - SwiftUI wrapper for Lottie animations
// ═══════════════════════════════════════════════════════════════════════════
// Displays Lottie JSON animations for Bennie Bear and Lemminge characters
// Supports looping, autoplay, and playback control
// ═══════════════════════════════════════════════════════════════════════════

/// SwiftUI view wrapper for Lottie animations
struct LottieView: UIViewRepresentable {
    // MARK: - Properties

    /// Name of the Lottie JSON file (without .json extension)
    let animationName: String

    /// Whether the animation should loop continuously
    var loopMode: LottieLoopMode = .loop

    /// Animation playback speed (1.0 = normal)
    var animationSpeed: CGFloat = 1.0

    /// Whether to start playing automatically
    var autoplay: Bool = true

    /// Content mode for the animation view
    var contentMode: UIView.ContentMode = .scaleAspectFit

    // MARK: - UIViewRepresentable

    func makeUIView(context: Context) -> LottieAnimationView {
        let animationView: LottieAnimationView

        // Try to load from bundle with explicit name
        if let animation = LottieAnimation.named(animationName, bundle: .main) {
            animationView = LottieAnimationView(animation: animation)
        } else {
            // Fallback to named initializer
            animationView = LottieAnimationView(name: animationName)
        }

        animationView.loopMode = loopMode
        animationView.animationSpeed = animationSpeed
        animationView.contentMode = contentMode
        animationView.backgroundBehavior = .pauseAndRestore

        // Configure for proper sizing in SwiftUI
        animationView.setContentCompressionResistancePriority(.defaultLow, for: .horizontal)
        animationView.setContentCompressionResistancePriority(.defaultLow, for: .vertical)
        animationView.setContentHuggingPriority(.defaultLow, for: .horizontal)
        animationView.setContentHuggingPriority(.defaultLow, for: .vertical)

        // Allow autolayout to work
        animationView.translatesAutoresizingMaskIntoConstraints = false

        if autoplay {
            animationView.play()
        }

        return animationView
    }

    func updateUIView(_ animationView: LottieAnimationView, context: Context) {
        // Update properties if they change
        animationView.loopMode = loopMode
        animationView.animationSpeed = animationSpeed
        animationView.contentMode = contentMode
    }
}

// MARK: - Character Animation Names

/// Animation names for Bennie Bear character
enum BennieAnimation: String, CaseIterable {
    case idle = "bennie_idle"
    case happy = "bennie_happy"
    case thinking = "bennie_thinking"
    case encouraging = "bennie_encouraging"
    case celebrating = "bennie_celebrating"
    case waving = "bennie_waving"
    case pointing = "bennie_pointing"

    /// Get LottieView for this animation
    var view: LottieView {
        LottieView(animationName: rawValue)
    }
}

/// Animation names for Lemminge character
enum LemmingeAnimation: String, CaseIterable {
    case idle = "lemminge_idle"
    case curious = "lemminge_curious"
    case excited = "lemminge_excited"
    case celebrating = "lemminge_celebrating"
    case hiding = "lemminge_hiding"
    case mischievous = "lemminge_mischievous"

    /// Get LottieView for this animation
    var view: LottieView {
        LottieView(animationName: rawValue)
    }
}

// MARK: - Animated Character View

/// A higher-level view for displaying character animations with easy state switching
struct AnimatedCharacter: View {
    // MARK: - Character Type

    enum CharacterType {
        case bennie(BennieAnimation)
        case lemminge(LemmingeAnimation)

        var animationName: String {
            switch self {
            case .bennie(let animation):
                return animation.rawValue
            case .lemminge(let animation):
                return animation.rawValue
            }
        }
    }

    // MARK: - Properties

    let character: CharacterType
    var loopMode: LottieLoopMode = .loop
    var animationSpeed: CGFloat = 1.0

    // MARK: - Body

    var body: some View {
        LottieView(
            animationName: character.animationName,
            loopMode: loopMode,
            animationSpeed: animationSpeed
        )
    }
}

// MARK: - Previews

#Preview("LottieView - Bennie") {
    VStack(spacing: 20) {
        Text("Bennie Bear Animations")
            .font(BennieFont.title())

        HStack(spacing: 20) {
            VStack {
                LottieView(animationName: "bennie_idle")
                    .frame(width: 150, height: 150)
                Text("Idle")
                    .font(BennieFont.label())
            }

            VStack {
                LottieView(animationName: "bennie_happy")
                    .frame(width: 150, height: 150)
                Text("Happy")
                    .font(BennieFont.label())
            }

            VStack {
                LottieView(animationName: "bennie_waving")
                    .frame(width: 150, height: 150)
                Text("Waving")
                    .font(BennieFont.label())
            }
        }
    }
    .padding()
    .background(BennieColors.cream)
}

#Preview("LottieView - Lemminge") {
    VStack(spacing: 20) {
        Text("Lemminge Animations")
            .font(BennieFont.title())

        HStack(spacing: 20) {
            VStack {
                LottieView(animationName: "lemminge_idle")
                    .frame(width: 120, height: 120)
                Text("Idle")
                    .font(BennieFont.label())
            }

            VStack {
                LottieView(animationName: "lemminge_curious")
                    .frame(width: 120, height: 120)
                Text("Curious")
                    .font(BennieFont.label())
            }

            VStack {
                LottieView(animationName: "lemminge_excited")
                    .frame(width: 120, height: 120)
                Text("Excited")
                    .font(BennieFont.label())
            }
        }
    }
    .padding()
    .background(BennieColors.cream)
}

#Preview("AnimatedCharacter") {
    VStack(spacing: 30) {
        AnimatedCharacter(character: .bennie(.celebrating))
            .frame(width: 200, height: 200)

        AnimatedCharacter(character: .lemminge(.mischievous))
            .frame(width: 150, height: 150)
    }
    .padding()
    .background(BennieColors.cream)
}
