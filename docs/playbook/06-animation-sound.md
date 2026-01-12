# Part 6: Animation & Sound Guide

> **Chapter 6** of the Bennie Brand Playbook
>
> Covers: Animation principles, transitions, character states

---

## 6.1 Animation Principles

| Property      | Value                    | Reason                           |
| ------------- | ------------------------ | -------------------------------- |
| **Duration**  | 0.3-0.5s typical         | Not too fast, not too slow       |
| **Easing**    | Spring (response: 0.3)   | Natural, organic feel            |
| **Breathing** | Scale 1.0->1.03 (2s loop)| Subtle, calming, for idle states |
| **UI hover**  | Gentle swing (0.5s)      | Playful, inviting                |

### Forbidden Animations

| Animation           | Reason          |
| ------------------- | --------------- |
| Flashing            | Seizure risk    |
| Shaking             | Anxiety trigger |
| Fast strobing       | Overstimulating |
| Sudden movements    | Startling       |
| Rapid color changes | Disorienting    |
| Bouncing text       | Distracting     |

---

## 6.2 Transition Animations

| Transition       | Animation                  | Duration  |
| ---------------- | -------------------------- | --------- |
| Screen to screen | Cross-fade                 | 0.3s      |
| Overlay appear   | Scale 0.8->1.0 + fade      | 0.4s      |
| Overlay dismiss  | Scale 1.0->0.9 + fade      | 0.3s      |
| Button press     | Scale 0.95                 | 0.1s      |
| Sign swing       | Rotation +/-3 degrees      | 0.5s loop |
| Coin fly         | Arc path to progress bar   | 0.8s      |
| Progress fill    | Left to right with sparkle | 0.5s      |

---

## 6.3 Character Animation States

### Bennie Animations

| State       | Animation        | Loop | Trigger       |
| ----------- | ---------------- | ---- | ------------- |
| Idle        | Gentle breathing | Yes  | Default       |
| Waving      | Wave gesture     | No   | Greeting      |
| Pointing    | Arm extend       | No   | Direction     |
| Thinking    | Paw to chin      | Yes  | Child working |
| Encouraging | Lean forward     | No   | Hint given    |
| Celebrating | Jump + arms up   | No   | Success       |

### Lemminge Animations

| State       | Animation    | Loop | Trigger      |
| ----------- | ------------ | ---- | ------------ |
| Idle        | Sway + blink | Yes  | Background   |
| Curious     | Head tilt    | Yes  | Watching     |
| Excited     | Bounce       | Yes  | Pre-success  |
| Celebrating | Jump         | No   | Success      |
| Hiding      | Peek in/out  | Yes  | Tree holes   |
| Mischievous | Scheme pose  | Yes  | Chaos moment |
