from Piece import Piece
import Pawn
from Colour import Colour


class Player:

    def __init__(self, colour, turn):
        self.turn = turn
        self.colour = colour

    def get_player_turn(self):
        """Return turn attribute value"""
        return self.turn

    def check_for_victory(self, board, main_display):
        """Check if player has won and if so, call to Display's class victory animation method.

        :param board: Board data structure
        :param main_display: Object of Display class
        """
        flattened_board = [y for x in board for y in x]
        pieces = [piece for piece in flattened_board if isinstance(piece, Piece) and piece.get_colour() != self.colour]
        if not pieces:
            main_display.victory_animation(self.colour)



    def is_piece_attacked(self, board):
        """Check if any of player's pieces are attackced and return either True or False."""
        all_attacks = []
        for fieldx in range(len(board)):
            for fieldy in range(len(board)):
                if isinstance(board[fieldy][fieldx], Piece) and board[fieldy][fieldx].get_colour() == self.colour:
                    available_attacks = board[fieldy][fieldx].get_available_attacks(board)
                    flattened_available_attacks = [y for x in available_attacks for y in x]
                    all_attacks.append(flattened_available_attacks)

        if any(True in sublist for sublist in all_attacks):
            return True
        else:
            return False

    @classmethod
    def select_player_with_turn(cls, player1, player2):
        """Returns Player's class object with turn attribute equating to True.

        :param player1: Player's class object
        :param player2: Player's class object
        :return: Player's class object with turn attribute set to True
        """
        players = (player1, player2)
        for player in players:
            if player.turn is True:
                return player

    def switch_turns(self, player1, player2):
        """Switches turn attributes of two Player's class objects."
        
        :param player1: Player's class object
        :param player2: Player's class object
        """""
        players = [player1, player2]
        for player in players:
            player.turn = not player.turn

    def get_moves_of_piece(self, board, posy, posx):
        """Return 4 or 5 item touple, depending on attack, with board coordinates as move positions. """
        piece_moves = []
        piece_attacks = []
        available_moves, attack = board[posy][posx].get_all_available_moves(board)
        for movex in range(len(available_moves)):
            for movey in range(len(available_moves)):
                if available_moves[movey][movex] is True and attack is True:

                        attacked_piece_x = int((posx + movex) / 2)
                        if movey < posy:
                            attacked_piece_y = posy - 1
                        else:
                            attacked_piece_y = posy + 1

                        attack_coordinates = (movey, movex, posy, posx, board[attacked_piece_y][attacked_piece_x])
                        piece_attacks.append(attack_coordinates)

                elif available_moves[movey][movex] is True and attack is False:
                    move_coordinates = (movey, movex, posy, posx)
                    piece_moves.append(move_coordinates)

        if not piece_attacks:
            attack = False
            return piece_moves, attack
        else:
            attack = True
            return piece_attacks, attack

    def get_ply(self, board):
        """Call to get_moves_of_piece on every piece on board in player's possession."""
        ply_attacks = []
        ply_moves = []
        for fieldx in range(len(board)):
            for fieldy in range(len(board)):
                if isinstance(board[fieldy][fieldx], Piece) and board[fieldy][fieldx].get_colour() == self.colour:

                    move_parameters, move_is_attack = self.get_moves_of_piece(board, fieldy, fieldx)
                    if move_is_attack is True:
                        ply_attacks.extend(move_parameters)
                    else:
                        ply_moves.extend(move_parameters)

        if not ply_attacks:
            move_is_attack = False
            return ply_moves, move_is_attack
        else:
            move_is_attack = True
            return ply_attacks, move_is_attack



