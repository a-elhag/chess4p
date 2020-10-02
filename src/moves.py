import numpy as np
import pygame
import main
import board

class Moves(board.ChessBoard):

    '''
    This class is responsbile for generating all legal moves
    '''

    def __init__(self):
        board.ChessBoard.__init__(self)
        self.turn_sequence = ['r', 'b', 'y', 'g']
        self.turn_direction = {
            "r": [-1, 0],
            "b": [0, 1],
            "y": [1, 0],
            "g": [0, -1]
        }

        self.log_move = []
        self.log_before = []
        self.log_after = []
        self.log_turn_sequence = []
        self.log_turn_sequence.append(self.turn_sequence)


    def get_moves(self):
        self.moves_ava = []
        self.get_team()
        self.get_opponents()
        self.get_moves_pawn()
        self.get_moves_rook()


    def get_team(self):
        self.team = self.board_turn = np.core.defchararray.find(
                    self.board, self.turn_sequence[0])
        self.team = (self.team == 0)


    def get_opponents(self):
        opponent1 = self.board_turn = np.core.defchararray.find(
                    self.board, self.turn_sequence[1])
        opponent1 = (opponent1 == 0)

        opponent2 = self.board_turn = np.core.defchararray.find(
            self.board, self.turn_sequence[2])
        opponent2 = (opponent2 == 0)

        opponent3 = self.board_turn = np.core.defchararray.find(
            self.board, self.turn_sequence[3])
        opponent3 = (opponent3 == 0)

        self.opponent = np.logical_or(opponent1, opponent2)
        self.opponent = np.logical_or(self.opponent, opponent3)


    def get_moves_pawn(self):
        # Finding the pawn and color
        idx_pawn = self.turn_sequence[0] + 'P' 
        board_pawns = self.board_turn = np.core.defchararray.find(
            self.board, idx_pawn)
        board_pawns = (board_pawns == 0)
        idx_add = np.array(self.turn_direction[self.turn_sequence[0]])

        # Available moves
        for row in range(self.dimension):
            for col in range(self.dimension):
                loc_before = [row, col]

                # Normal Movements
                if board_pawns[row, col]:
                    idx_next = np.array([row, col])
                    idx_next = idx_next + idx_add
                    if self.board[idx_next[0], idx_next[1]] == '--':
                        loc_after = [idx_next[0], idx_next[1]]
                        self.moves_ava.append([loc_before, loc_after])

                        idx_next = idx_next + idx_add

                        if ((idx_pawn[0] == "r") and (row == 12) and 
                            (self.board[idx_next[0], idx_next[1]] == '--')):
                            loc_after = [idx_next[0], idx_next[1]]
                            self.moves_ava.append([loc_before, loc_after])

                        if ((idx_pawn[0] == "b") and (col == 1) and 
                            (self.board[idx_next[0], idx_next[1]] == '--')):
                            loc_after = [idx_next[0], idx_next[1]]
                            self.moves_ava.append([loc_before, loc_after])

                        if ((idx_pawn[0] == "y") and (row == 1) and 
                            (self.board[idx_next[0], idx_next[1]] == '--')):
                            loc_after = [idx_next[0], idx_next[1]]
                            self.moves_ava.append([loc_before, loc_after])

                        if ((idx_pawn[0] == "g") and (col == 12) and 
                            (self.board[idx_next[0], idx_next[1]] == '--')):
                            loc_after = [idx_next[0], idx_next[1]]
                            self.moves_ava.append([loc_before, loc_after])

                # See if we can capture an opponent
                if board_pawns[row, col]:
                    idx_base = np.array([row, col]) + idx_add
                    idx_left = np.copy(idx_base)
                    idx_right = np.copy(idx_base)

                    for _ in range(2):
                        if idx_add[_] == 0:
                            idx_left[_] = idx_left[_] - 1
                            idx_right[_] = idx_right[_] + 1

                            piece_left = self.opponent[idx_left[0], idx_left[1]]
                            piece_right = self.opponent[idx_right[0], idx_right[1]]

                            if piece_left:
                                loc_after = [idx_left[0], idx_left[1]]
                                self.moves_ava.append([loc_before, loc_after])

                            if piece_right:
                                loc_after = [idx_right[0], idx_right[1]]
                                self.moves_ava.append([loc_before, loc_after])

    
    def get_moves_rook(self):
        idx_rook = self.turn_sequence[0] + 'R'
        board_rooks = self.board_turn = np.core.defchararray.find(
            self.board, idx_rook)
        board_rooks = (board_rooks == 0)

        for row in range(self.dimension):
            for col in range(self.dimension):
                loc_before = [row, col]
                idx_before = np.array(loc_before)
                idx_movement_rook = np.array([
                    [-1, 0], #up
                    [1, 0], #down
                    [0, 1], # right
                    [0, -1], #left
                ])

                if board_rooks[row, col]:
                    for movement in range(4):
                        idx_after = np.copy(loc_before)
                        flag_allowed = True
                        while(flag_allowed):
                            idx_after = (idx_after +
                                         idx_movement_rook[movement, :])
                            loc_after = [idx_after[0], idx_after[1]]

                            if not ((0 <= idx_after[0] < self.dimension) and
                                    (0 <= idx_after[1] < self.dimension)):
                                flag_allowed = False
                                break

                            if self.team[loc_after[0], loc_after[1]]:
                                flag_allowed = False
                            else:
                                self.moves_ava.append([loc_before, loc_after])
                                if self.opponent[loc_after[0], loc_after[1]]:
                                    flag_allowed = False
                        

    

    def turn_next(self):
        self.turn_sequence = self.turn_sequence[1:] + self.turn_sequence[:1]
        self.log_turn_sequence.append(self.turn_sequence)


    def move_piece(self, player_clicks):
        self.player_clicks = player_clicks
        loc_before = self.player_clicks[0]
        loc_after = self.player_clicks[1]

        self.get_moves()

        if self.is_valid():
            piece_before = self.board[loc_before]
            piece_after = self.board[loc_after]

            self.board[loc_before] = '--'
            self.board[loc_after] = piece_before

            self.turn_next()

            self.log_move.append(self.player_clicks)
            self.log_before.append(piece_before)
            self.log_after.append(piece_after)

    def move_undo(self):
        '''
        Undos moves
        '''

        if self.log_move:
            player_clicks_now = self.log_move.pop()
            piece_before = self.log_before.pop()
            piece_after = self.log_after.pop()
            self.log_turn_sequence.pop()
            self.turn_sequence = self.log_turn_sequence[-1]
            
            loc_before = player_clicks_now[0]
            loc_after = player_clicks_now[1]

            self.board[loc_before] = piece_before
            self.board[loc_after] = piece_after


    def is_valid(self):
        '''
        Check if the move is valid
        '''
        loc_before = self.player_clicks[0]
        loc_after = self.player_clicks[1]

        flag_move = [list(loc_before), list(loc_after)] in self.moves_ava

        return flag_move


    def print_moves(self):
        self.get_moves()
        print('Start: ', self.turn_sequence[0])
        for move in self.moves_ava:
            print(move)


if __name__ == "__main__":
    import ipdb; dbg1 = ipdb.set_trace  # BREAKPOINT
    chess_board = Moves()
    main.run_game(chess_board)
    pygame.display.quit()
