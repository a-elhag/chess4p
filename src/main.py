'''
Name: Al-Baraa El-Hag
Date: Sept 29 2019
'''

## Part 0: Importing
import numpy as np
import pygame as p

class ChessBoard():

    '''
    This class is responsible for storing all the information about the current state
    of a chess game. It will also be responsible for determining the valid
    moves at the current state. It will also keep a move log
    '''

    def __init__(self):
        self.board = np.array([
            ['xx', 'xx', 'xx', 'yR', 'yN', 'yB', 'yQ', 'yK', 'yB', 'yN', 'yR', 'xx', 'xx', 'xx'],
            ['xx', 'xx', 'xx', 'yP', 'yP', 'yP', 'yP', 'yP', 'yP', 'yP', 'yP', 'xx', 'xx', 'xx'],
            ['xx', 'xx', 'xx', '--', '--', '--', '--', '--', '--', '--', '--', 'xx', 'xx', 'xx'],

            ['bR', 'bP', '--', '--', '--', '--', '--', '--', '--', '--', '--', '--', 'gP', 'gR'],
            ['bN', 'bP', '--', '--', '--', '--', '--', '--', '--', '--', '--', '--', 'gP', 'gN'],
            ['bB', 'bP', '--', '--', '--', '--', '--', '--', '--', '--', '--', '--', 'gP', 'gB'],
            ['bK', 'bP', '--', '--', '--', '--', '--', '--', '--', '--', '--', '--', 'gP', 'gQ'],
            ['bQ', 'bP', '--', '--', '--', '--', '--', '--', '--', '--', '--', '--', 'gP', 'gK'],
            ['bB', 'bP', '--', '--', '--', '--', '--', '--', '--', '--', '--', '--', 'gP', 'gB'],
            ['bN', 'bP', '--', '--', '--', '--', '--', '--', '--', '--', '--', '--', 'gP', 'gN'],
            ['bR', 'bP', '--', '--', '--', '--', '--', '--', '--', '--', '--', '--', 'gP', 'gR'],

            ['xx', 'xx', 'xx', '--', '--', '--', '--', '--', '--', '--', '--', 'xx', 'xx', 'xx'],
            ['xx', 'xx', 'xx', 'rP', 'rP', 'rP', 'rP', 'rP', 'rP', 'rP', 'rP', 'xx', 'xx', 'xx'],
            ['xx', 'xx', 'xx', 'rR', 'rN', 'rB', 'rQ', 'rK', 'rB', 'rN', 'rR', 'xx', 'xx', 'xx']])

        self.redToMove = True
        self.moveLog = []

        self.dimension = 14
        self.sq_size = 50
        self.width = self.height = self.sq_size * self.dimension
        self.max_fps = 15
        self.bg = "#3C3A36"


    def load_images(self):
        '''
        Initialize a global dictionary of images. This will be called once in the main
        '''
        self.images = {}

        colors = ['r', 'b', 'y', 'g']
        pieces = ['P', 'R', 'N', 'B', 'Q', 'K']

        for color in colors:
            for piece in pieces:
                folder_loc = "../resources/png/"
                piece_label = color+piece
                piece_loc = folder_loc + piece_label + ".png"

                self.images[piece_label] = p.transform.scale(
                    p.image.load(piece_loc), (self.sq_size, self.sq_size))


    def draw_board(self, screen):
        colors = [p.Color("white"), p.Color("gray")]
        for row in range(self.dimension):
            for col in range(self.dimension):
                if self.board[row, col] != 'xx':
                    color = colors[((row + col) % 2)]
                    p.draw.rect(screen, color, 
                                p.Rect((col*self.sq_size, row*self.sq_size, self.sq_size, self.sq_size)))
                else:
                    p.draw.rect(screen, p.Color(self.bg),
                        p.Rect((col*self.sq_size, row*self.sq_size, self.sq_size, self.sq_size)))


    def draw_pieces(self, screen):
        for row in range(self.dimension):
            for col in range(self.dimension):
                piece = self.board[row, col]

                if piece != '--' and piece != 'xx':
                    screen.blit(self.images[piece],
                                p.Rect(col*self.sq_size, row*self.sq_size, self.sq_size, self.sq_size))


class Move():
    def __init__(self, start_sq, end_sq, board):
        self.start_row = start_sq[0]
        self.start_col = start_sq[1]
        self.end_row = end_sq[0]
        self.end_col = end_sq[1]
        self.piece_moved = board[self.start_row, self.start_col]
        self.piece_captured = board[self.end_row, self.end_col]

def main():
    A = ChessBoard()
    A.load_images()
    screen = p.display.set_mode((A.width, A.height))
    clock = p.time.Clock()
    screen.fill(p.Color(A.bg))
    running = True
    sq_selected = () # no square is selected, keep track of last click
    player_clicks = [] # keep track of the player clicks (two tuples [(6, 4), (4, 4)])
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                # p.display.quit()
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos() # (x, y) location of mouse
                col = location[0]//A.sq_size
                row = location[1]//A.sq_size

                # the user clicked the same square twice (undo)
                if sq_selected == (row, col): 
                    sq_selected = () # deselect
                    player_clicks = []

                # append for first and second clicks
                else:
                    sq_selected = (row, col)
                    player_clicks.append(sq_selected) 

                # after the users second click
                if len(player_clicks) == 2: 
                    pass

        A.draw_board(screen)
        A.draw_pieces(screen)
        clock.tick(A.max_fps)
        p.display.flip()

if __name__ == "__main__":
    main()
    p.display.quit()
