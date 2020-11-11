from Colour import Colour


class Piece:
    def __init__(self, posy, posx, colour):
        self.posy = posy
        self.posx = posx
        self.colour = colour

        if self.colour == Colour.WHITE.value:
            self.direction = -1
        else:
            self.direction = 1

    def get_colour(self):
        """Return colour attribute value"""
        return self.colour

    def get_available_moves(self, board):
        """Iterate through sublists of board, call to is_valid_move method and append it's return values to a list.

        :param board: board data structure.
        :param posy: Board vertical coordinate at piece's location
        :param posx: Board horizontal coordinate at piece's location
        """
        available_moves = []
        for fieldx in range(len(board)):
            column = []
            for fieldy in range(len(board)):
                legit_move = board[self.posy][self.posx].is_valid_move(board, fieldx, fieldy)
                column.append(legit_move)
            available_moves.append(column)
        return available_moves

    def get_available_attacks(self, board):
        """Iterate through sublists of board, call to is_valid_attack method and append it's return values to a list.

        :param board: board data structure
        :param posy: Board vertical coordinate at piece's location.
        :param posx: Board horizontal coodinate at piece's location.
        :return:
        """
        available_attacks = []
        for fieldx in range(len(board)):
            column = []
            for fieldy in range(len(board)):
                legit_attack = board[self.posy][self.posx].is_valid_attack(board, fieldx, fieldy)
                column.append(legit_attack)
            available_attacks.append(column)
        return available_attacks

    def get_all_available_moves(self, board):
        """Return available_attacks and attack if there are any, else return available_moves and False attack value.

        :param board: Board data structure
        :param posy: Board vertical coordinate at piece's location.
        :param posx: Board horizontal coordinate at piece's location.
        :return: available_attacks, attack or available_moves, attack
        """
        available_attacks = self.get_available_attacks(board)
        if any(True in sublist for sublist in available_attacks):
            attack = True
            return available_attacks, attack
        else:
            available_moves = self.get_available_moves(board)
            attack = False
            return available_moves, attack

    def is_valid_move(self, board, fieldy, fieldx):
        """Check if move on specified location is valid.

        :param board: Board data structure.
        :param fieldy: Board vertical coordinate.
        :param fieldx: Board horizontal coordinate.
        :return: True or False
        """
        if isinstance(board[fieldy][fieldx], Piece):
            return False
        if self.posy - fieldy == self.direction and abs(self.posx - fieldx) == 1:
            return True
        else:
            return False

    def make_move(self, board, fieldy, fieldx):
        """Update board data structure and piece's attributes responsible for it's location.

        :param board: Board data structure
        :param fieldy: Board vertical coordinate at moves' destination.
        :param fieldx: Board horizontal coordinate at move's destination.
        :return:
        """
        board[self.posy][self.posx], board[fieldy][fieldx] = board[fieldy][fieldx], board[self.posy][self.posx]
        self.posy = fieldy
        self.posx = fieldx

