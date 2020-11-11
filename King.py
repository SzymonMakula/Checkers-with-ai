import configparser
from Colour import Colour
from Piece import Piece


class King(Piece):

    def is_valid_attack(self, board, fieldy, fieldx):
        if fieldy < self.posy:
            piece_position_y = self.posy - 1
        else:
            piece_position_y = self.posy + 1
        piece_position_x = int((self.posx + fieldx) / 2)

        if abs(self.posx - fieldx) == 2 and abs(self.posy - fieldy) == 2 and not isinstance(board[fieldy][fieldx], Piece):
            if isinstance(board[piece_position_y][piece_position_x], Piece) and board[piece_position_y][piece_position_x].get_colour() != self.colour:
                return True
            else:
                return False
        else:
            return False

    def attack_piece(self, board, fieldy, fieldx):
        if fieldy < self.posy:
            piece_position_y = self.posy - 1
        else:
            piece_position_y = self.posy + 1
        piece_position_x = int((self.posx + fieldx) / 2)

        board[piece_position_y][piece_position_x] = None
        board[self.posy][self.posx], board[fieldy][fieldx] = board[fieldy][fieldx], board[self.posy][self.posx]
        self.posy = fieldy
        self.posx = fieldx

    def is_valid_move(self, board, fieldy, fieldx):
        if isinstance(board[fieldy][fieldx], Piece):
            return False
        if abs(self.posy - fieldy) == 1 and abs(self.posx - fieldx) == 1:
            return True
        else:
            return False
