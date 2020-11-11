import configparser
import Pawn
from Colour import Colour


class Board:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        self.board_size = int(config['Board_parameters']['BOARD_SIZE'])


    def get_newboard(self):
        """Create an empty 2D list and instantiate Pawn objects in it.

        :return: 2D board data structure that stores positions of Pawn objects
        """
        new_board = [[None for j in range(self.board_size)] for i in range(self.board_size)]
        for i in range(self.board_size // 2 - 1):
            for j in range(0, self.board_size, 2):
                new_board[i][j + i % 2] = Pawn.Pawn(i, j + i % 2, Colour.WHITE.value)
        for i in range(self.board_size // 2 + 1, self.board_size):
            for j in range(0, self.board_size, 2):
                new_board[i][j + i % 2] = Pawn.Pawn(i, j + i % 2, Colour.RED.value)
        return new_board
