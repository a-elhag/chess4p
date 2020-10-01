import numpy as np
import pygame
import main

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

        self.turn_sequence = ['r', 'b', 'y', 'g']

        self.log_move = []
        self.log_before = []
        self.log_after = []
        self.log_turn_sequence = []
        self.log_turn_sequence.append(self.turn_sequence)

        self.dimension = 14
        self.sq_size = 50
        self.width = self.height = self.sq_size * self.dimension
        self.max_fps = 15
        self.bg = "#3C3A36"

        self.load_images()

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

                self.images[piece_label] = pygame.transform.scale(
                    pygame.image.load(piece_loc), (self.sq_size, self.sq_size))


    def draw_board(self, screen):
        colors = [pygame.Color("white"), pygame.Color("gray")]
        for row in range(self.dimension):
            for col in range(self.dimension):
                # Draw real squares
                if self.board[row, col] != 'xx':
                    color = colors[((row + col) % 2)]
                    pygame.draw.rect(screen, color, 
                                pygame.Rect((col*self.sq_size, row*self.sq_size, self.sq_size, self.sq_size)))

                # Draw squares that are not playable
                else:
                    pygame.draw.rect(screen, pygame.Color(self.bg),
                        pygame.Rect((col*self.sq_size, row*self.sq_size, self.sq_size, self.sq_size)))


    def draw_pieces(self, screen):
        for row in range(self.dimension):
            for col in range(self.dimension):
                piece = self.board[row, col]

                if piece != '--' and piece != 'xx':
                    screen.blit(self.images[piece],
                                pygame.Rect(col*self.sq_size, row*self.sq_size, self.sq_size, self.sq_size))

    def draw_all(self, screen):
        self.draw_board(screen)
        self.draw_pieces(screen)

    def turn_next(self):
        self.turn_sequence = self.turn_sequence[1:] + self.turn_sequence[:1]
        self.log_turn_sequence.append(self.turn_sequence)


    def move_piece(self, player_clicks):
        loc_before = player_clicks[0]
        loc_after = player_clicks[1]

        if self.is_valid(loc_before, loc_after):
            piece_before = self.board[loc_before]
            piece_after = self.board[loc_after]

            self.board[loc_before] = '--'
            self.board[loc_after] = piece_before

            self.turn_next()

            self.log_move.append(player_clicks)
            self.log_before.append(piece_before)
            self.log_after.append(piece_after)

    def move_undo(self):
        '''
        Undos moves
        Doesn't work for multiple undo
        '''

        if self.log_move:
            player_clicks = self.log_move.pop()
            piece_before = self.log_before.pop()
            piece_after = self.log_after.pop()
            self.log_turn_sequence.pop()
            self.turn_sequence = self.log_turn_sequence[-1]
            
            loc_before = player_clicks[0]
            loc_after = player_clicks[1]

            self.board[loc_before] = piece_before
            self.board[loc_after] = piece_after


    def is_valid(self, loc_before, loc_after):
        '''
        Check if the move is valid
        '''
        piece_before = self.board[loc_before]
        piece_after = self.board[loc_after]
        piece_id = piece_before[1]

        flag_turn = self.is_valid_turn(piece_before)

        if piece_id == 'P':
            flag_move = self.is_valid_pawn()
        else:
            flag_move = False

        print(flag_turn, flag_move)

        return flag_turn and flag_move


    def is_valid_turn(self, piece_before):
        turn_now = self.turn_sequence[0]
        turn_made = piece_before[0]

        if turn_now == turn_made:
            return True
        else:
            return False


    def is_valid_pawn(self):
        return True


if __name__ == "__main__":
    chess_board = ChessBoard()
    main.run_game(chess_board)
    pygame.display.quit()

