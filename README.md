# Noughts and Crosses AI

This is a simple implementation of the classic Noughts and Crosses (also known as Tic Tac Toe) game with an unbeatable AI opponent. The AI opponent uses the Minimax algorithm to make its moves, ensuring that it will always tie or win the game, never losing.

## Requirements

-   Python 3.x
-   Pygame library

## How to Play

1. Ensure you have Python 3.x installed on your system.
2. Install the Pygame library by running: `pip install pygame`.
3. Clone this repository or download the ZIP file and extract it.
4. Open a terminal or command prompt and navigate to the project directory.
5. Run the following command to start the game: `python src/noughts_and_crosses.py`.

## Rules of Noughts and Crosses

Noughts and Crosses is a two-player game played on a 3x3 grid. Players take turns to place their symbol (Nought or Cross) in an empty cell. The player who succeeds in placing three of their symbols in a horizontal, vertical, or diagonal row wins the game.

## Controls

-   **"G":** Changes the game mode (player vs. player or player vs. AI).
-   **"0":** Sets the AI level to 0 (easy - random moves).
-   **"1":** Sets the AI level to 1 (hard - unbeatable).
-   **"R":** Restarts the game.

## Changing Themes

To change the themes of the game, you need to modify the `constants.py` file. In this file, you will find different colour combinations for different themes.

Simply comment out the current theme and uncomment the theme you would like to switch to.

## An unbeatable AI using the Minimax Algorithm

The Minimax algorithm is a decision-making algorithm used in two-player games, such as Noughts and Crosses, to determine the best possible move for a player. It explores all possible moves by simulating the game to the end and assigning a score to each possible outcome. The AI player chooses the move with the highest score when it's its turn and the lowest score when it's the opponent's turn.

### How the Minimax Algorithm works

1. The algorithm takes the current state of the Noughts and Crosses board as input.
2. If the game has reached a terminal state (win, lose, or draw), the algorithm returns a score based on the outcome (positive score for AI win, negative score for AI loss, and 0 for a draw).
3. If it's the AI's turn (maximizer), the algorithm tries all possible moves on the board and calls itself recursively with the opponent's turn (minimizer).
4. If it's the opponent's turn (minimizer), the algorithm tries all possible moves on the board and calls itself recursively with the AI's turn (maximizer).
5. The algorithm returns the maximum or minimum score from the recursive calls, depending on whether it's the AI's or opponent's turn, respectively.

By following these steps, the AI can determine the best move to make in any given state of the game and ensure it never loses.

Have fun playing against the AI! If you find any issues or have suggestions for improvements, feel free to submit them.

**Buena Suerte!!**
