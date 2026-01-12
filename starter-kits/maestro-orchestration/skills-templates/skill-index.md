# Skill Organization Guide

> How to organize, create, and maintain skills in Maestro.

## Skill Directory Structure

```
.claude/skills/
├── SKILL-INDEX.md              # This file
├── README.md                   # Skills overview
│
├── development/                # Code & build skills
│   ├── ios-dev/
│   │   ├── SKILL.md
│   │   ├── MCP-SETUP.md
│   │   └── RECURSIVE-TESTING.md
│   ├── swiftui-ipad.md
│   └── testing.md
│
├── design/                     # Visual & UX skills
│   ├── visual-design.md
│   ├── design-autism.md
│   └── website-review.md
│
├── animation/                  # Motion & animation
│   ├── animation-system.md
│   └── ludo-automation/
│       ├── SKILL.md
│       └── config/
│
├── content/                    # Story & media
│   ├── story-characters.md
│   ├── audio-voice.md
│   ├── image-generation.md
│   └── gameplay.md
│
└── infrastructure/             # Settings & admin
    └── parent-dashboard.md
```

## Creating a New Skill

### 1. Choose Location

| Category | Use For |
|----------|---------|
| `development/` | Build, test, deploy workflows |
| `design/` | Visual design, UX, accessibility |
| `animation/` | Motion, sprites, Lottie |
| `content/` | Characters, story, media generation |
| `infrastructure/` | Settings, admin, security |

### 2. Pick Template

- **Basic skill**: Use `skill-template.md`
- **MCP-dependent skill**: Use `mcp-skill-template.md`

### 3. Fill In Template

Required sections:
- [ ] One-line description
- [ ] When to Use triggers
- [ ] Prerequisites
- [ ] Workflow steps
- [ ] Examples
- [ ] Error handling

### 4. Register Skill

Add to `config/capabilities.json`:

```json
{
  "skills": [
    "existing-skills...",
    "your-new-skill"
  ]
}
```

## Skill Naming Conventions

| Pattern | Example | Use For |
|---------|---------|---------|
| `domain-task` | `ios-dev` | Single responsibility |
| `domain-subtask` | `design-autism` | Specialized variant |
| `tool-automation` | `ludo-automation` | Tool-specific |

### Good Names

- `image-generation` - Clear domain + action
- `animation-system` - Domain + scope
- `visual-regression` - Domain + technique

### Bad Names

- `stuff` - Too vague
- `ios-dev-build-test-deploy-screenshot` - Too long
- `MySkill` - Wrong case, not descriptive

## Skill File Naming

| Type | Pattern | Example |
|------|---------|---------|
| Single file | `skill-name.md` | `testing.md` |
| Complex skill | `skill-name/SKILL.md` | `ios-dev/SKILL.md` |
| Sub-docs | `skill-name/TOPIC.md` | `ios-dev/MCP-SETUP.md` |
| Config | `skill-name/config/` | `ludo-automation/config/` |

## Skill Quality Checklist

Before publishing a skill, verify:

### Documentation

- [ ] Clear one-line description
- [ ] Specific "When to Use" triggers
- [ ] All prerequisites listed
- [ ] Step-by-step workflow
- [ ] Working examples
- [ ] Error handling table
- [ ] Best practices section

### Technical

- [ ] All tool calls documented
- [ ] Parameters and return types specified
- [ ] Configuration templates provided
- [ ] Environment variables listed
- [ ] Related skills linked

### Usability

- [ ] Can be used without reading entire doc
- [ ] Quick Start section works standalone
- [ ] Examples are copy-paste ready
- [ ] Troubleshooting covers common issues

## Maintaining Skills

### When to Update

- MCP tool changes
- New best practices discovered
- User feedback received
- Workflow improved
- Dependencies updated

### Version Tracking

Add changelog to each skill:

```markdown
## Changelog

| Version | Date | Changes |
|---------|------|---------|
| 1.2 | 2025-01-10 | Added QA gate workflow |
| 1.1 | 2025-01-05 | Fixed timing configuration |
| 1.0 | 2025-01-01 | Initial release |
```

### Deprecation

To deprecate a skill:

1. Add warning at top:
   ```markdown
   > **DEPRECATED**: This skill is replaced by [new-skill].
   > It will be removed in version X.X.
   ```

2. Keep working for transition period
3. Update `capabilities.json` to remove
4. Archive file (don't delete)

## Cross-Skill Dependencies

When skills depend on each other:

```markdown
## Prerequisites

- Skill: `image-generation` - For generating keyframes
- Skill: `ludo-automation` - For animation pipeline
```

Document the dependency chain to help users understand the full workflow.

## Skill Categories Reference

### Development Skills

| Skill | Purpose | MCP |
|-------|---------|-----|
| `ios-dev` | iPad build/test loop | iOS Simulator |
| `swiftui-ipad` | SwiftUI patterns | - |
| `testing` | Test writing/running | iOS Simulator |

### Design Skills

| Skill | Purpose | MCP |
|-------|---------|-----|
| `visual-design` | UI design patterns | - |
| `design-autism` | Accessibility design | - |
| `website-review` | Web QA | Chrome DevTools |

### Animation Skills

| Skill | Purpose | MCP |
|-------|---------|-----|
| `animation-system` | Lottie integration | - |
| `ludo-automation` | Sprite generation | Chrome DevTools |

### Content Skills

| Skill | Purpose | MCP |
|-------|---------|-----|
| `image-generation` | Character art | Image Generator |
| `story-characters` | Character design | - |
| `audio-voice` | Voice generation | - |
| `gameplay` | Activity design | - |

### Infrastructure Skills

| Skill | Purpose | MCP |
|-------|---------|-----|
| `parent-dashboard` | Admin UI | - |
