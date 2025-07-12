# Space Race Game Tutorial in Python

Welcome to the step-by-step tutorial on creating the classic Atari game Space Race using Python! This tutorial will guide you through the process of developing the game, and we'll be using `uv`, `ruff`, and `pytest` throughout the tutorial to ensure code quality and testing.

## Table of Contents
1. [Introduction](#introduction)
2. [Prerequisites](#prerequisites)
3. [Installation](#installation)
4. [Project Structure](#project-structure)
5. [Step-by-Step Guide](#step-by-step-guide)
6. [Running Tests](#running-tests)
7. [Linting and Formatting](#linting-and-formatting)
8. [Contributing](#contributing)
9. [License](#license)

## Introduction
In this tutorial, you will learn how to create the Space Race game from scratch using Python. We will cover the basics of game development, including setting up the game loop, handling player input, and rendering graphics. By the end of this tutorial, you will have a fully functional Space Race game.

## Prerequisites
Before you start, ensure you have the following installed on your machine:
- Python 3.8 or higher
- `uv` for package management and installation
- `ruff` for linting and formating
- `pytest` for testing

## Installation
To get started, clone the repository and install the required dependencies using `uv`:
```bash
git clone https://github.com/romualdrousseau/theprogrammerworkshop.git
cd Spacerace
uv sync
```

## Project Structure
Here's an overview of the project structure:
```
spacerace/
├── README.md
├── data
│   ├── spaceship.png
│   └── title.png
├── pyproject.toml
├── src
│   └── spacerace
│       ├── __init__.py
│       ├── __main__.py
│       ├── entities
│       │   ├── __init__.py
│       │   ├── asteriod.py
│       │   ├── entity.py
│       │   └── player.py
│       ├── scenes
│       │   ├── __init__.py
│       │   ├── context.py
│       │   ├── game.py
│       │   ├── game_over.py
│       │   ├── scene_manager.py
│       │   └── title.py
│       └── utils
│           ├── graphic.py
│           └── resources.py
├── tests
│   └── spacerace
│       └── scenes
│           └── test_scene_manager.py
└── uv.lock
```

## Step-by-Step Guide
Follow the tutorial on YouTube to create the Space Race game step by step. Each video will cover a specific part of the development process:
1. [Setting Up the Project](#)
2. [Creating the Game Loop](#)
3. [Handling Player Input](#)
4. [Rendering Graphics](#)
5. [Adding Game Logic](#)
6. [Testing the Game](#)
7. [Refactoring and Optimization](#)

## Running Tests
To ensure your code is working correctly, run the tests using `pytest`:
```bash
uv run pytest
```

## Linting and Formatting
Keep your code clean and consistent by using `ruff` for linting:
```bash
uv run ruff check
```

## Running the game
Run the game:
```bash
uv run spacerace
```

## Contributing
Contributions are welcome! If you have any suggestions or improvements, please open an issue or submit a pull request.

## License
This project is licensed under the GNU General Public License v3.0. See the [LICENSE](LICENSE) file for details.
