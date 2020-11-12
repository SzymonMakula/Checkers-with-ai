from Piece import Piece
from Player import Player
from Colour import Colour
from Pawn import Pawn
from Move import Move
import math


class Computer:
    def __init__(self, computer, human, colour):
        self.computer = computer
        self.human = human
        self.colour = colour

    def evaluate_piece_prefer_promotion_edges(self, board, fieldy, fieldx):
        pawn_value = 10
        king_value = 40
        position_multiplier = 1

        if board[fieldy][fieldx] is None:
            return 0
        if fieldy == 0 or fieldy == len(board):
            position_multiplier = 1.2
        if isinstance(board[fieldy][fieldx], Pawn):
            return pawn_value * position_multiplier
        else:
            return king_value

    def evaluate_piece_prefer_vertical_borders(self, board, fieldy, fieldx):
        pawn_value = 10
        king_value = 40
        position_multiplier = 1

        if board[fieldy][fieldx] is None:
            return 0
        if fieldx == 0 or fieldx == len(board):
            position_multiplier = 1.2

        if isinstance(board[fieldy][fieldx], Pawn):
            return pawn_value * position_multiplier
        else:
            return king_value

    def evaluate_board(self, board, depth):
        score = 0
        for fieldx in range(len(board)):
            for fieldy in range(len(board)):
                if board[fieldy][fieldx] is not None:
                    if board[fieldy][fieldx].get_colour() == self.colour:
                        score = depth + score + \
                            (self.evaluate_piece_prefer_promotion_edges(board, fieldy, fieldx) +
                                self.evaluate_piece_prefer_vertical_borders(board, fieldy, fieldx))/2
                    else:
                        score = score - depth - \
                            (self.evaluate_piece_prefer_promotion_edges(board, fieldy, fieldx) +
                                self.evaluate_piece_prefer_vertical_borders(board, fieldy, fieldx))/2
        return score

    def alpha_beta(self, depth, is_maximizing, alpha, beta, board):
        move = Move()
        best_move = 0

        if depth == 0 or best_move is None:
            return self.evaluate_board(board, depth), best_move

        if is_maximizing:
            best_value = -math.inf
            ply, move_is_attack = self.computer.get_ply(board)
            value = -math.inf

            for child in ply:
                if move_is_attack:
                    move.attack(board, child[0], child[1], child[2], child[3], child[4])

                    has_to_attack_again = board[child[0]][child[1]].can_piece_attack(board)
                    if has_to_attack_again:
                        value, ply = self.alpha_beta(depth - 1, True, alpha, beta, board)
                        if value >= best_value:
                            best_value = value
                            best_move = child
                    else:  # attacks only once
                        value, ply = self.alpha_beta(depth - 1, False, alpha, beta, board)
                        if value >= best_value:
                            best_value = value
                            best_move = child
                    move.undo_attack(board, child[0], child[1], child[2], child[3], child[4])

                else:  # move is not attack
                    move.move(board, child[0], child[1], child[2], child[3])

                    value, ply = self.alpha_beta(depth - 1, False, alpha, beta, board)
                    if value >= best_value:
                        best_value = value
                        best_move = child

                    move.undo_move(board, child[0], child[1], child[2], child[3])

                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return value, best_move

        else:  # is minimizer
            best_value = math.inf
            value = math.inf
            ply, move_is_attack = self.human.get_ply(board)

            for child in ply:
                if move_is_attack is True:
                    move.attack(board, child[0], child[1], child[2], child[3], child[4])

                    has_to_attack_again = board[child[0]][child[1]].can_piece_attack(board)
                    if has_to_attack_again:
                        value, ply = self.alpha_beta(depth - 1, False, alpha, beta, board)
                        if value < best_value:
                            best_value = value
                            best_move = child
                    else:  # attacks only once
                        value, ply = self.alpha_beta(depth - 1, True, alpha, beta, board)
                        if value <= best_value:
                            best_value = value
                            best_move = child

                    move.undo_attack(board, child[0], child[1], child[2], child[3], child[4])

                else:  # move is not attack
                    move.move(board, child[0], child[1], child[2], child[3])
                    value, ply = self.alpha_beta(depth - 1, True, alpha, beta, board)
                    if value <= best_value:
                        best_value = value
                        best_move = child
                    move.undo_move(board, child[0], child[1], child[2], child[3])

                beta = min(beta, value)
                if alpha >= beta:
                    break

            return value, best_move


