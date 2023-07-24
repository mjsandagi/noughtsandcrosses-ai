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

    def final_state(self):
        """
        @return 0 if there is no win yet
        @return 1 if player 1 wins
        @return 2 if player 2 wins
        """

        # Vertical wins
        for col in range(COLS):
            if self.squares[0][col] == self.squares[1][col] == self.squares[2][col] != 0: # != 0 so that it ignores wholly empty columns 
                return self.squares[0][col]
            
        # Horizontal wins
        for row in range(ROWS):
            if self.squares[row][0] == self.squares[row][1] == self.squares[row][1] != 0: # != 0 so that it ignores wholly empty columns 
                return self.squares[row][0]
            
        # Descending diagonal wins
        if self.squares[0][0] == self.squares[1][1] == self.squares[2][2] != 0:
            return self.squares[1][1]

        # Ascending diagonal wins
        if self.squares[2][0] == self.squares[1][1] == self.squares[0][2] != 0:
            return self.squares[1][1]
        
        # No wins yet
        return 0

    def mark_sqr(self, row, col, player):
        self.squares[row][col] = player
        self.marked_sqrs += 1
    
    def empty_sqr(self, row, col):
        return self.squares[row][col] == 0

    def get_empty_sqrs(self):
        empty_sqrs = []
        for row in range(ROWS):
            for col in range(COLS):
                if self.empty_sqr(row, col):
                    empty_sqrs.append((row, col))
        return empty_sqrs

    def isfull(self):
        return self.marked_sqrs == 9
    
    def isempty(self):
        return self.marked_sqrs == 0
    
class Game:
    def __init__(self):
        self.board = Board()
        self.player = 1 # P1-Crosses and P2-Noughts
        self.show_lines()

    def show_lines(self):
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

def main():
    # Objects
    game = Game()
    board = game.board

    # Main "loop"
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                # print(event.pos) => (66, 17)
                pos = event.pos
                col = pos[0] // SQSIZE # Converts from Cartesian co-ordinates to (columns, rows).
                row = pos[1] // SQSIZE  

                if board.empty_square(row, col):
                    board.mark_sqr(row, col, game.player)
                    game.draw_fig(row, col)
                    game.next_turn()

        pygame.display.update()

main()