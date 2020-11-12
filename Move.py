from Pawn import Pawn
from King import King


class Move:
    """Methods of this class are used solely by A.I. In contrary to movement methods of pieces, these
    methods take all the pawn's positions on board as arguments and can undo those movements."""
    def __init__(self):
        pass

    def attack(self, board, destination_y, destination_x, posy, posx, attacked_piece):
        board[attacked_piece.posy][attacked_piece.posx] = None
        board[posy][posx], board[destination_y][destination_x] = board[destination_y][destination_x], \
                                                                             board[posy][posx]
        board[destination_y][destination_x].posy = destination_y
        board[destination_y][destination_x].posx = destination_x

    def move(self, board, destination_y, destination_x, posy, posx):
        board[posy][posx], board[destination_y][destination_x] = board[destination_y][destination_x], \
                                                                             board[posy][posx]
        board[destination_y][destination_x].posy = destination_y
        board[destination_y][destination_x].posx = destination_x

    def undo_move(self, board, destination_y, destination_x, posy, posx):
        board[posy][posx], board[destination_y][destination_x] = board[destination_y][destination_x], \
                                                                                 board[posy][posx]
        board[posy][posx].posy = posy
        board[posy][posx].posx = posx

    def undo_attack(self, board, destination_y, destination_x, posy, posx, attacked_piece):
          board[attacked_piece.posy][attacked_piece.posx] = attacked_piece
          board[posy][posx], board[destination_y][destination_x] = board[destination_y][destination_x], \
                                                                           board[posy][posx]
          board[posy][posx].posy = posy
          board[posy][posx].posx = posx
