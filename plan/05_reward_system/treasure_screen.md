# Treasure Screen Implementation

**📚 Playbook Reference**: [FULL_ARCHIVE.md Part 4.8](../../docs/playbook/FULL_ARCHIVE.md#48-treasure-screen)  
**🎨 Design Reference**: [Reference_Treasure_Screen.png](../../design/references/screens/Reference_Treasure_Screen.png)  
**🐻 Character Assets Required**:
- [bennie_encouraging.png](../../design/references/character/bennie/bennie_encouraging.png) - Bennie gesturing to options
- [lemminge_excited.png](../../design/references/character/lemminge/lemminge_excited.png) - Left Lemminge
- [lemminge_curious.png](../../design/references/character/lemminge/lemminge_curious.png) - Right Lemminge
- [lemminge_hiding.png](../../design/references/character/lemminge/lemminge_hiding.png) - Peeking from log

**🧩 Component Dependencies**:
- [NavigationHeader](../../Design/Components/NavigationHeader.swift) - With back button and volume
- [WoodButton](../../Design/Components/WoodButton.swift) - For redemption cards
- [BennieView](../../Design/Characters/BennieView.swift) - Character display
- [LemmingeView](../../Design/Characters/LemmingeView.swift) - Character display

**🎬 Animation Assets**:
- [treasure_chest_open.png](../../Resources/Assets.xcassets/treasure_chest_open.imageset/) - Open chest with glow
- [coins_spilling.json](../../Resources/Lottie/coins_spilling.json) - Coin animation

**🔊 Audio Files Required**:
- `bennie_treasure_under10.aac` - "Wir haben [X] Münzen. Noch [Y] bis YouTube!"
- `bennie_treasure_over10.aac` - "Wir können fünf Minuten schauen!"
- `bennie_treasure_over20.aac` - "Wir können zwölf Minuten schauen!"
- `narrator_film_ab.aac` - "Film ab!"
- `bennie_not_enough_coins.aac` - "Noch [X] Münzen bis YouTube!"

**🎨 UI Elements**:
- `youtube_icon.png` - YouTube logo for redemption cards
- `coin.png` - Coin icon for cost display
- `padlock.png` - Lock icon for disabled cards

---

## 🏴‍☠️ Overview

The Treasure Screen is where children exchange earned coins for YouTube time. It features an open treasure chest, coin display, and redemption options.

## Navigation Flow

> **Playbook Reference**: Part 2.2 - State Machine Definition

```
Activity Complete → +1 Coin → Celebration (if milestone) → Check Coins:
    If coins >= 10: Can navigate to Treasure
    If coins < 10: Return to activity
    
From Home Screen: Tap chest (only if coins >= 10)
From Celebration: Auto-navigate at 10+ coins after dismiss
```

## Screen Layout

> **Design Reference**: See Reference_Treasure_Screen.png for exact layout
> **Playbook**: Part 4.8 - Layout diagram

```swift
struct TreasureScreen: View {
    @EnvironmentObject var coinManager: CoinManager
    @State private var selectedTier: YouTubeTier? = nil
    
    var body: some View {
        ZStack {
            // Playbook: "Forest background with golden light"
            ForestBackground(style: .treasure)
            
            VStack {
                // Header with back button and coin count
                NavigationHeader(
                    showHome: true,
                    showVolume: true,
                    currentCoins: coinManager.currentCoins
                )
                
                Spacer()
                
                // Main content
                VStack(spacing: 40) {
                    // Treasure chest
                    TreasureChest(coins: coinManager.currentCoins)
                    
                    // Redemption options
                    HStack(spacing: 40) {
                        RedemptionCard(
                            tier: .fiveMinutes,
                            isEnabled: coinManager.currentCoins >= 10
                        )
                        
                        RedemptionCard(
                            tier: .tenPlusTwoMinutes,
                            isEnabled: coinManager.currentCoins >= 20
                        )
                    }
                }
                
                Spacer()
                
                // Characters
                // Playbook Part 4.8: Character positions and expressions
                HStack {
                    // Left Lemminge (excited)
                    LemmingeView(expression: .excited)
                        .frame(width: 80, height: 100)
                    
                    Spacer()
                    
                    // Bennie gesturing to options
                    BennieView(expression: .encouraging)
                        .frame(width: 200, height: 300)
                    
                    Spacer()
                    
                    // Right Lemminge (curious)
                    LemmingeView(expression: .curious)
                        .frame(width: 80, height: 100)
                }
                .padding(.horizontal, 60)
            }
        }
        .onAppear {
            playVoiceGreeting()
        }
    }
    
    func playVoiceGreeting() {
        // Playbook Part 4.8 - Voice Triggers
        let voiceFile: String
        if coinManager.currentCoins < 10 {
            voiceFile = "bennie_treasure_under10.aac"
        } else if coinManager.currentCoins >= 20 {
            voiceFile = "bennie_treasure_over20.aac"
        } else {
            voiceFile = "bennie_treasure_over10.aac"
        }
        
        AudioManager.shared.playBennie(voiceFile)
    }
}
```

## Treasure Chest Component

> **Design Reference**: treasure_chest_open.png
> **Color Reference**: BennieColors.coinGold (#D9C27A) for glow

```swift
struct TreasureChest: View {
    let coins: Int
    @State private var isGlowing = false
    
    var body: some View {
        ZStack {
            // Open chest image
            Image("treasure_chest_open")
                .resizable()
                .frame(width: 300, height: 250)
            
            // Glowing effect
            // Playbook: "Golden glow when coins >= 10"
            if coins >= 10 {
                Circle()
                    .fill(BennieColors.coinGold.opacity(0.3))
                    .frame(width: 320, height: 320)
                    .blur(radius: 30)
                    .scaleEffect(isGlowing ? 1.1 : 1.0)
                    .animation(
                        .easeInOut(duration: 1.5).repeatForever(autoreverses: true),
                        value: isGlowing
                    )
            }
            
            // Coins spilling out
            CoinsSpillingAnimation()
                .frame(width: 300, height: 100)
                .offset(y: 100)
        }
        .onAppear {
            isGlowing = true
        }
    }
}

struct CoinsSpillingAnimation: View {
    var body: some View {
        LottieView(
            animation: "coins_spilling",
            loopMode: .loop
        )
    }
}
```

## Redemption Card Component

> **Playbook Reference**: Part 4.8 - Button States table

```swift
enum YouTubeTier {
    case fiveMinutes
    case tenPlusTwoMinutes
    
    var title: String {
        switch self {
        case .fiveMinutes: return "5 Min YouTube"
        case .tenPlusTwoMinutes: return "10+2 Min YouTube"
        }
    }
    
    var cost: Int {
        switch self {
        case .fiveMinutes: return 10
        case .tenPlusTwoMinutes: return 20
        }
    }
    
    var duration: Int {
        switch self {
        case .fiveMinutes: return 5
        case .tenPlusTwoMinutes: return 12 // 10 + 2 bonus
        }
    }
}

struct RedemptionCard: View {
    let tier: YouTubeTier
    let isEnabled: Bool
    
    var body: some View {
        Button {
            handleRedemption()
        } label: {
            VStack(spacing: 16) {
                // YouTube icon
                Image("youtube_icon")
                    .resizable()
                    .frame(width: 80, height: 60)
                
                // Title
                Text(tier.title)
                    .font(.sfRounded(size: 24, weight: .bold))
                    .foregroundColor(BennieColors.bark)
                
                // Cost
                HStack(spacing: 8) {
                    Image("coin")
                        .resizable()
                        .frame(width: 30, height: 30)
                    
                    Text("\(tier.cost) Münzen")
                        .font(.sfRounded(size: 20, weight: .semibold))
                        .foregroundColor(BennieColors.coinGold)
                }
                
                // Bonus badge for tier 2
                // Playbook: "BONUS! badge for 20-coin option"
                if case .tenPlusTwoMinutes = tier {
                    Text("+ 2 Min BONUS!")
                        .font(.sfRounded(size: 16, weight: .bold))
                        .foregroundColor(.white)
                        .padding(.horizontal, 12)
                        .padding(.vertical, 6)
                        .background(
                            Capsule()
                                .fill(BennieColors.success)
                        )
                }
            }
            .frame(width: 250, height: 280)
            .padding(24)
            .background(
                RoundedRectangle(cornerRadius: 20)
                    .fill(BennieColors.cream)
                    .overlay(
                        RoundedRectangle(cornerRadius: 20)
                            .strokeBorder(
                                isEnabled ? BennieColors.woodMedium : Color.gray.opacity(0.5),
                                lineWidth: 4
                            )
                    )
                    .shadow(radius: isEnabled ? 8 : 0)
            )
            .opacity(isEnabled ? 1.0 : 0.5)
            .overlay(
                // Lock chains if disabled
                // Playbook: "X-pattern chains for locked content"
                Group {
                    if !isEnabled {
                        LockedChains()
                    }
                }
            )
        }
        .disabled(!isEnabled)
        .buttonStyle(WoodButtonStyle())
    }
    
    func handleRedemption() {
        // Playbook Part 4.8 - Redemption Logic
        
        // Play narrator voice
        AudioManager.shared.playNarrator("narrator_film_ab.aac")
        
        // Deduct coins
        CoinManager.shared.deduct(tier.cost)
        
        // Navigate to video selection
        NavigationCoordinator.shared.navigate(
            to: .videoSelection(duration: tier.duration)
        )
    }
}

struct LockedChains: View {
    var body: some View {
        ZStack {
            // X-pattern chains
            Rectangle()
                .fill(Color.gray)
                .frame(width: 4, height: 300)
                .rotationEffect(.degrees(45))
            
            Rectangle()
                .fill(Color.gray)
                .frame(width: 4, height: 300)
                .rotationEffect(.degrees(-45))
            
            // Padlock
            Image(systemName: "lock.fill")
                .resizable()
                .frame(width: 40, height: 50)
                .foregroundColor(.gray)
        }
    }
}
```

## Voice Lines

> **Playbook Reference**: Part 3.4 - Treasure Screen Script

```swift
struct TreasureVoiceLines {
    static func getGreeting(coins: Int) -> String {
        if coins < 10 {
            return "bennie_treasure_under10.aac"
            // Playbook: "Wir haben [X] Münzen. Noch [Y] bis YouTube!"
        } else if coins >= 20 {
            return "bennie_treasure_over20.aac"
            // Playbook: "Wir können zwölf Minuten schauen!"
        } else {
            return "bennie_treasure_over10.aac"
            // Playbook: "Wir können fünf Minuten schauen!"
        }
    }
}
```

**Voice Line Table** (from Playbook Part 3.4):

| Condition | Speaker | German | File Name |
|-----------|---------|--------|-----------|
| coins < 10 | Bennie | "Wir haben [X] Münzen. Noch [Y] bis YouTube!" | bennie_treasure_under10.aac |
| coins 10-19 | Bennie | "Wir können fünf Minuten schauen!" | bennie_treasure_over10.aac |
| coins ≥ 20 | Bennie | "Wir können zwölf Minuten schauen!" | bennie_treasure_over20.aac |
| Tap YouTube button | Narrator | "Film ab!" | narrator_film_ab.aac |

## Coin Deduction Logic

> **Playbook Reference**: Part 4.8 - Redemption Logic

```swift
extension CoinManager {
    func deduct(_ amount: Int) {
        guard currentCoins >= amount else {
            print("Error: Not enough coins")
            return
        }
        
        withAnimation(.spring()) {
            currentCoins -= amount
        }
        
        // Save to persistence
        PlayerDataStore.shared.updateCoins(currentCoins)
        
        // Play coin sound
        AudioManager.shared.playEffect("coin_spend.aac")
    }
}
```

## Chest Button State (Home Screen)

> **Playbook Reference**: Part 4.3 - Home Screen - Chest Behavior

**Chest State Table** (from Playbook):

| Coins | Chest State | Visual | Tap Action |
|-------|-------------|--------|------------|
| 0-9 | Closed | Dull wood, no glow | Bennie: "Noch [X] Münzen!" |
| 10-19 | Open | Golden glow, coins visible | → Treasure Screen |
| 20+ | Open + sparkles | Extra glow, 2 chest icons | → Treasure Screen |

```swift
struct ChestButton: View {
    @EnvironmentObject var coinManager: CoinManager
    let onTap: () -> Void
    @State private var isGlowing = false
    
    var body: some View {
        Button(action: handleTap) {
            ZStack {
                Image("treasure_chest_closed")
                    .resizable()
                    .frame(width: 120, height: 100)
                
                // Glowing effect if >= 10 coins
                // Playbook: "Golden glow when coins >= 10"
                if coinManager.currentCoins >= 10 {
                    Circle()
                        .fill(BennieColors.coinGold.opacity(0.3))
                        .frame(width: 140, height: 140)
                        .blur(radius: 20)
                        .scaleEffect(isGlowing ? 1.1 : 1.0)
                        .animation(
                            .easeInOut(duration: 1.5).repeatForever(autoreverses: true),
                            value: isGlowing
                        )
                }
                
                // Coin count badge
                VStack {
                    Spacer()
                    HStack {
                        Spacer()
                        CoinBadge(count: coinManager.currentCoins)
                    }
                }
            }
        }
        .disabled(coinManager.currentCoins < 10)
        .onAppear {
            isGlowing = true
        }
    }
    
    func handleTap() {
        if coinManager.currentCoins >= 10 {
            onTap()
        } else {
            AudioManager.shared.playBennie("bennie_not_enough_coins.aac")
            // Playbook: "Noch [X] Münzen bis YouTube!"
        }
    }
}
```

## Testing Checklist

> **Playbook Reference**: Part 10.2 - QA Verification Matrix

```
NAVIGATION:
□ Screen appears when coins >= 10 (from celebration or home)
□ Cannot access when coins < 10
□ Back button returns to home
□ Proper state restoration on return

VISUAL:
□ Chest glows with golden light (#D9C27A @ 30% opacity)
□ Coins spilling animation plays smoothly (loop)
□ 5 Min option enabled at 10+ coins
□ 10+2 Min option enabled at 20+ coins
□ Disabled cards show X-pattern lock chains
□ Touch targets >= 96pt (both cards)
□ Characters animate properly (bennie_encouraging, lemminge_excited, lemminge_curious)

INTERACTION:
□ Tapping enabled card:
  □ Plays "Film ab!" narrator voice
  □ Deducts correct coin amount (10 or 20)
  □ Updates coin display immediately
  □ Navigates to video selection
  □ Passes correct duration (5 or 12 minutes)
□ Tapping disabled card does nothing
□ Haptic feedback on successful redemption

VOICE:
□ Bennie voice plays correct greeting based on coins
□ Voice ducks music to 15%
□ Music returns to 30% after voice

PERFORMANCE:
□ Frame rate maintains 60fps during animations
□ Memory usage stays under 200MB
□ Chest glow animation is smooth
□ No lag when navigating to video selection

ACCESSIBILITY:
□ VoiceOver labels correct for all elements
□ Color contrast meets 4.5:1 minimum
□ Touch targets clearly defined
□ Screen scales properly on all iPad sizes
```

## Accessibility

> **Playbook**: Part 5.7 - VoiceOver Support

```swift
// Redemption cards
.accessibilityLabel("\(tier.title) für \(tier.cost) Münzen")
.accessibilityHint(isEnabled ? "Tippen um YouTube zu schauen" : "Nicht genug Münzen")
.accessibilityValue(isEnabled ? "Verfügbar" : "Gesperrt")

// Chest button (home screen)
.accessibilityLabel("Schatzkiste, \(coinManager.currentCoins) Münzen")
.accessibilityHint(coinManager.currentCoins >= 10 ? "Tippen um Münzen einzutauschen" : "Sammle mehr Münzen um YouTube zu schauen")
```

---

## 📋 Implementation Checklist

**Phase 5B - Treasure Screen**:
- [ ] Create TreasureScreen.swift
- [ ] Import treasure_chest_open.png
- [ ] Import coins_spilling.json Lottie animation
- [ ] Import youtube_icon.png
- [ ] Record all voice lines with ElevenLabs:
  - [ ] bennie_treasure_under10.aac
  - [ ] bennie_treasure_over10.aac
  - [ ] bennie_treasure_over20.aac
  - [ ] narrator_film_ab.aac
  - [ ] bennie_not_enough_coins.aac
- [ ] Implement RedemptionCard component
- [ ] Implement TreasureChest component with glow
- [ ] Implement LockedChains component
- [ ] Add CoinManager.deduct() method
- [ ] Update ChestButton on home screen
- [ ] Test navigation from celebration overlay
- [ ] Test navigation from home screen
- [ ] Verify accessibility with VoiceOver
- [ ] Performance test (60fps, <200MB)

**Asset Dependencies**:
- [ ] Reference_Treasure_Screen.png reviewed
- [ ] bennie_encouraging.png (static)
- [ ] lemminge_excited.png (static)
- [ ] lemminge_curious.png (static)
- [ ] All voice files recorded and imported

**Integration Points**:
- [ ] CelebrationOverlay (auto-navigate at 10+ coins)
- [ ] HomeScreen (chest button)
- [ ] VideoSelectionView (navigation target)
- [ ] CoinManager (deduction logic)
