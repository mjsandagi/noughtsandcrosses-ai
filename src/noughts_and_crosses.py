import copy
import random
import sys
import pygame
import numpy as np

from constants import *

# PYGAME SETUP
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Noughts and Crosses AI")
screen.fill(BG_COLOUR)

class Board:
    def __init__(self):
        self.squares = np.zeros((ROWS, COLS)) # => [[0. 0. 0.] [0. 0. 0.] [0. 0. 0.]]
        self.empty_sqrs = self.squares # [SQUARES]
        self.marked_sqrs = 0

    def final_state(self, show=False):
        """
        @param show: Flag to control whether to draw the winning line on the screen.

        @return 0 if there is no win yet
        @return 1 if player 1 wins
        @return 2 if player 2 wins
        """

        # Vertical wins
        for col in range(COLS):
            if self.squares[0][col] == self.squares[1][col] == self.squares[2][col] != 0: # != 0 so that it ignores wholly empty columns 
                if show:
                    colour = CIRCLE_COLOUR if self.squares[0][col] == 2 else CROSS_COLOUR
                    iPos = (col * SQSIZE + SQSIZE // 2, LINE_OFFSET)
                    fPos = (col * SQSIZE + SQSIZE // 2, HEIGHT - LINE_OFFSET)
                    pygame.draw.line(screen, colour, iPos, fPos, LINE_WIDTH)
                return self.squares[0][col]
            
        # Horizontal wins
        for row in range(ROWS):
            if self.squares[row][0] == self.squares[row][1] == self.squares[row][2] != 0: # != 0 so that it ignores wholly empty rows 
                if show:
                    colour = CIRCLE_COLOUR if self.squares[row][0] == 2 else CROSS_COLOUR
                    iPos = (LINE_OFFSET, row * SQSIZE + SQSIZE // 2)
                    fPos = (WIDTH - LINE_OFFSET, row * SQSIZE + SQSIZE // 2)
                    pygame.draw.line(screen, colour, iPos, fPos, LINE_WIDTH)
                return self.squares[row][0]
            
        # Descending diagonal wins
        if self.squares[0][0] == self.squares[1][1] == self.squares[2][2] != 0:
            if show:
                colour = CIRCLE_COLOUR if self.squares[1][1] == 2 else CROSS_COLOUR
                iPos = (LINE_OFFSET, LINE_OFFSET)
                fPos = (WIDTH - LINE_OFFSET, HEIGHT - OFFSET)
                pygame.draw.line(screen, colour, iPos, fPos, CROSS_WIDTH)
            return self.squares[1][1]

        # Ascending diagonal wins
        if self.squares[2][0] == self.squares[1][1] == self.squares[0][2] != 0:
            if show:
                colour = CIRCLE_COLOUR if self.squares[1][1] == 2 else CROSS_COLOUR
                iPos = (LINE_OFFSET, HEIGHT - LINE_OFFSET)
                fPos = (WIDTH - LINE_OFFSET, OFFSET)
                pygame.draw.line(screen, colour, iPos, fPos, CROSS_WIDTH)
            return self.squares[1][1]
        
        # No wins yet
        return 0

    def mark_sqr(self, row, col, player):
        """
        @param row: Row index of the square.
        @param col: Column index of the square.
        @param player: Player number (1 for Crosses, 2 for Noughts).
        """
        self.squares[row][col] = player
        self.marked_sqrs += 1
    
    def empty_sqr(self, row, col):
        """
        @param row: Row index of the square.
        @param col: Column index of the square.

        @return: True if the square is empty, False otherwise.
        """
        return self.squares[row][col] == 0

    def get_empty_sqrs(self):
        """
        @return: List of (row, col) tuples representing empty squares.
        """
        empty_sqrs = []
        for row in range(ROWS):
            for col in range(COLS):
                if self.empty_sqr(row, col):
                    empty_sqrs.append((row, col))
        return empty_sqrs

    def isfull(self):
        """
        @return: True if the board is full. False otherwise.
        """
        return self.marked_sqrs == 9
    
    def isempty(self):
        """
        @return: True if the board is empty, False otherwise.
        """
        return self.marked_sqrs == 0

class AI:
    def __init__(self, level=1, player=2):
        """
        @param level: AI level, 0 for random moves, 1 for minimax algorithm.
        @param player: Player number for the AI (2 for Noughts).
        """
        self.level = level
        self.player = player
    
    def rnd(self, board):
        """
        @param board: The current game board.

        @return: (row, col) tuple representing the chosen move coordinates.
        """
        empty_sqrs = board.get_empty_sqrs()
        idx = random.randrange(0, len(empty_sqrs))

        return empty_sqrs[idx] # [row, col]

    def minimax(self, board, maximising): 
        """
        @param board: The current game board.
        @param maximising: Flag to indicate if the AI is maximising its move.

        @return: Tuple (evaluation, move) representing the best evaluation score and corresponding move coordinates.
        """
        # Terminal cases
        case = board.final_state()

        # Terminal case 1: Player 1 wins
        if case == 1:
            return 1, None # eval, move
        
        # Terminal case 2: Player 2 wins (AI)
        if case == 2:
            return -1, None 
        
        elif board.isfull():
            return 0, None 
        
        if maximising:
            max_eval = -100
            best_move = None
            empty_sqrs = board.get_empty_sqrs()

            for (row, col) in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_sqr(row, col, 1)
                eval = self.minimax(temp_board, False)[0]
                if eval > max_eval:
                    max_eval = eval
                    best_move = (row, col)

            return max_eval, best_move

        else:
            min_eval = 100
            best_move = None
            empty_sqrs = board.get_empty_sqrs()

            for (row, col) in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_sqr(row, col, self.player)
                eval = self.minimax(temp_board, True)[0]
                if eval < min_eval:
                    min_eval = eval
                    best_move = (row, col)

            return min_eval, best_move

    def eval(self, main_board):
        """
        @param board: The current game board.
        @param maximising: Flag to indicate if the AI is maximising its move.

        @return: Tuple (evaluation, move) representing the best evaluation score and corresponding move coordinates.
        """
        if self.level == 0:
            # Random move
            eval = "random"
            move = self.rnd(main_board)
        else:
            # Make a move calculated by the minimax algorithm
            eval, move = self.minimax(main_board, False)
        # print(f"The AI has chosen to make a move at the co-ordinates {move}, with an eval of {eval}")
        print(f"AI move: {move}, evaluation: {eval}")
        return move

class Game:
    def __init__(self):
        self.board = Board()
        self.ai = AI()
        self.player = 1 # P1-Crosses and P2-Noughts [Change this to 2 if you want the AI to start (or 1 if you want the human player to start)]
        self.gamemode = "ai" # PvP or Ai
        self.running = True
        self.show_lines()

    def make_move(self, row, col):
        """
        @param row: Row index of the selected square.
        @param col: Column index of the selected square.
        """
        self.board.mark_sqr(row, col, self.player)
        self.draw_fig(row, col)
        self.next_turn()

    def show_lines(self):
        # Fill the game board with the background colour
        screen.fill(BG_COLOUR)
        # Vertical
        pygame.draw.line(screen, LINE_COLOUR, (SQSIZE, 0), (SQSIZE, HEIGHT), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOUR, (WIDTH - SQSIZE, 0), (WIDTH - SQSIZE, HEIGHT), LINE_WIDTH)

        # Horizontal
        pygame.draw.line(screen, LINE_COLOUR, (0, SQSIZE), (WIDTH, SQSIZE), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOUR, (0, HEIGHT - SQSIZE), (WIDTH, HEIGHT - SQSIZE), LINE_WIDTH)
    
    def draw_fig(self, row, col):
        if self.player == 1:
            # Draws a cross
            # Draws a line with a positive gradient
            start_asc = (col * SQSIZE + OFFSET, row * SQSIZE + SQSIZE - OFFSET)
            end_asc = (col * SQSIZE + SQSIZE - OFFSET, row * SQSIZE + OFFSET)
            pygame.draw.line(screen, CROSS_COLOUR, start_asc, end_asc, CROSS_WIDTH)
            # Draws a line with a negative gradient
            start_desc = (col * SQSIZE + OFFSET, row * SQSIZE + OFFSET)
            end_desc = (col * SQSIZE + SQSIZE - OFFSET, row * SQSIZE + SQSIZE - OFFSET)
            pygame.draw.line(screen, CROSS_COLOUR, start_desc, end_desc, CROSS_WIDTH)
        elif self.player == 2:
            # Draws a nought
            center = (col * SQSIZE + SQSIZE // 2, row * SQSIZE + SQSIZE // 2)
            pygame.draw.circle(screen, CIRCLE_COLOUR, center, RADIUS, CIRCLE_WIDTH)

    def next_turn(self):
        self.player = self.player % 2 + 1 # ((1P % 2 = 1) + 1 == 2P) and ((2P % 2 = 0) + 1 == 1P)

    def change_gamemode(self):
        self.gamemode = "ai" if self.gamemode == "pvp" else "pvp"

    def isover(self):
        return self.board.final_state(show=True) != 0 or self.board.isfull() and not self.board.final_state()

    def reset(self):
        self.__init__()

def main():
    # Objects
    game = Game()
    board = game.board
    ai = game.ai

    # Main "loop"
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                # "G": Change game mode
                if event.key == pygame.K_g:
                    game.change_gamemode()

                if event.key == pygame.K_r:
                    game.reset()
                    board = game.board
                    ai = game.ai

                # "0": Random AI
                if event.key == pygame.K_0:
                    ai.level = 0
                    print(f"AI level: {ai.level}")

                # "0": Random AI
                if event.key == pygame.K_1:
                    ai.level = 1
                    print(f"AI level: {ai.level}")

            if event.type == pygame.MOUSEBUTTONDOWN:
                # print(event.pos) => (66, 17)
                pos = event.pos
                col = pos[0] // SQSIZE # Converts from Cartesian co-ordinates to (columns, rows).
                row = pos[1] // SQSIZE  

                if board.empty_sqr(row, col) and game.running:
                    game.make_move(row, col)
                    
                    if game.isover():
                        game.running = False

        if game.gamemode == "ai" and game.player == ai.player and game.running:
            # AI methods
            row, col = ai.eval(board)
            game.make_move(row, col)

            if game.isover():
                game.running = False

        pygame.display.update()

if __name__ == "__main__":
    main()
