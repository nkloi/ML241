# ML241

# Chess AI Project

## Overview
This project implements a chess game with AI capabilities using Python. The AI employs optimization algorithms to calculate and execute moves. Users can play against the AI, against another player, or watch two AIs compete.

---

## Folder Structure
- **`sounds/`**: Contains all audio files for sound effects used during the game.
- **`images/`**: Contains image files for chess pieces.
- Ensure the file organization matches this structure to use relative paths correctly.

---

## Modules
### 1. `ChessMain.py`
Handles:
- Animations
- Game state visualization
- User interactions
- Chessboard rendering

### 2. `Engine.py`
Handles:
- Validation of moves
- Enforcement of chess rules
- Legal gameplay

### 3. `ChessAI.py`
Handles:
- Implementation of optimization algorithms
- Scoring positions and move evaluation
- Key algorithm: **NegaMax with Alpha-Beta Pruning and Null Move Heuristics**
- Includes customizable options for better performance and strategy.

---

## Key Features
- **Adjustable AI Configurations**:
  - Modify **scoring criteria** in `ChessAI.py` for improved AI strategies.
  - Customize **DEPTH** for various game stages:
    - **DEPTH = 1**: Simplistic, not effective.
    - **DEPTH = 2, 3**: Balanced performance and speed (recommended).
    - **DEPTH > 3**: Better calculations but slower performance.

- **Tiebreaking Strategies**:
  - Avoid repetitive moves leading to stalemates by enhancing endgame configurations (`pieceScores` and `DEPTH`).

---

## Game Modes
- **1**: Player as **White**, AI as **Black**.
- **2**: Player as **Black**, AI as **White**.
- **3**: Two-player local mode.
- **4**: Watch two AIs compete.

---

## Keyboard Shortcuts
- **`z`**: Undo the last move.
- **`i`**: Reset the board to the initial state.

---

## Performance Tips
- Use `DEPTH = 2` or `DEPTH = 3` for general play.
- Experiment with additional evaluation metrics in `ChessAI.py` to enhance decision-making.
- Adjust **endgame configurations** for improved results.

---

## Getting Started
1. Ensure the folder structure is intact (e.g., `sounds/`, `images/`).
2. Run `ChessMain.py` to start the game.

---

## Future Improvements
- Experiment with different scoring metrics in `ChessAI.py`.
- Enhance `DEPTH` in endgame scenarios for better AI performance.
- Optimize the AI evaluation function for faster and more accurate gameplay.

---

## Contributors
- Project by: [Khai Giang-Mien]

