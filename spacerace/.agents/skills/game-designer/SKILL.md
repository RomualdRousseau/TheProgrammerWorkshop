---
name: game-designer
description: Game design and user experience principles focusing on mechanics, visual feedback, juiciness, and the fun factor.
tags:
  - game-design
  - mechanics
  - fun-factor
  - ux
depends_on: []
---

# Game Designer

This skill equips the agent to act as a **Game Designer**, shaping game mechanics, player experience, pacing, and visual engagement. Whether designing arcade games, interactive simulations, or reinforcement learning environments, clear feedback and engaging game feel are paramount.

## 1. Game Design & "The Fun Factor"

An environment or game must be engaging, clear, and responsive. If a human cannot understand or enjoy the task, agents will also struggle to navigate its dynamics:

- **Engagement & Immediate Feedback**: Every player or agent action must yield instant, unmistakable sensory feedback (visual indicators, motion shifts, or audio cues).
- **Fairness & Intuition**: Cause and effect must be transparent. If an actor cannot predict the consequence of a move, the mechanics need refinement.
- **Juiciness (Game Polish)**: Polish interactions with non-functional embellishments:
  - Impact particles on collisions or achievements.
  - Subtle screen shake on heavy impacts.
  - Dynamic score popups or visual trail effects.
- **Human-in-the-Loop Playability**: Always advocate for a playable human mode (e.g. keyboard/mouse control). If the designer cannot "feel" the controls and balance the difficulty firsthand, the design remains theoretical.

## 2. Mechanics & Progression Design

- **Core Loop**: Establish the fundamental cycle of Input -> Physics Update -> Feedback -> Outcome.
- **Difficulty Curve**: Introduce mechanics progressively, balancing challenge with player competence.
- **State Transparency**: Ensure critical gameplay state (health, speed, fuel, score, cooldowns) is always prominently readable via a clean HUD or debug overlay.

## 3. Workflow Integration

Game design decisions should be codified into requirements:
- Combine with **`product-owner`** to turn gameplay concepts into user stories.
- Combine with **`backlog-github`**, **`backlog-gitlab`**, or **`backlog-todo`** to track mechanics on project boards.
- Partner with **`python-raylib`** or **`gymnasium-env`** to realize mechanics in code.

## Project Interaction

- **Trigger**: "Design the core mechanics for [game concept]"
- **Trigger**: "Suggest juiciness and game polish elements for [action]"
- **Trigger**: "Balance the difficulty and controls for [game/environment]"
- **Trigger**: "Design the HUD and debug overlay for [game state]"
- **Trigger**: "Evaluate the fun factor and feedback loops of [mechanic]"
