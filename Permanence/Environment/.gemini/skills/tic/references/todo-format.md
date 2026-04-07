# TODO.md Specification

The `TODO.md` file must always maintain three distinct sections to track the project's state.

## Required Sections

### 1. # Backlog
Contains all ideas, feature requests, and future user stories. These are not yet prioritized for development.
- [ ] Story: As a player, I want...
- [ ] Feature: Character Customization

### 2. # To Be Developed (In Progress)
Contains the current sprint's or task's active user stories and their sub-tasks.
- [ ] Story: Implement basic movement
  - [ ] Task: Handle WASD input
  - [ ] Task: Apply velocity to player state

### 3. # Done
Contains all completed stories and tasks. Move items here only when all acceptance criteria are met.
- [x] Task: Initialize project structure
- [x] Story: Setup Raylib window
