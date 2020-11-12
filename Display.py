import configparser
from Colour import Colour
import Pawn
import pygame
from pygame.locals import *
import King
import sys

class Display:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        self.board_size = int(config['Board_parameters']['BOARD_SIZE'])
        self.window_width = int(config['Window']['WINDOW_WIDTH'])
        self.window_height = int(config['Window']['WINDOW_HEIGHT'])
        self.field_size = int(config['Board_parameters']['FIELD_SIZE'])
        self.displaysurf = pygame.display.set_mode((self.window_width, self.window_height))
        self.xmargin = int((self.window_height - (self.board_size * self.field_size)) / 2)
        self.ymargin = int((self.window_width - (self.board_size * self.field_size)) / 2)
        self.basic_font_size = int(config['Font']['FONT_SIZE'])
        self.basic_font = pygame.font.Font('freesansbold.ttf', self.basic_font_size)

    def get_left_top_of_field(self, fieldy, fieldx):
        """Return left-top X&Y pixel coordinates of given field.

        :param fieldy: Board vertical coordinate, equivalent to row no. in board 2D-list
        :param fieldx: Board horizontal coordinate, equivalent to column no. in board 2D-list
        :return: Vertical and horizontal pixel coordinates
        """
        left_top_Xcoord = (fieldx * self.field_size) + self.ymargin
        left_top_Ycoord = (fieldy * self.field_size) + self.xmargin
        return (left_top_Ycoord, left_top_Xcoord)

    def draw_field(self, fieldy, fieldx):
        """Draw rect object on Surface object at given field.

        :param fieldy: Board vertical coordinate, equivalent to row no. in board 2D-list
        :param fieldx: Board horizontal coordinate, equivalent to column no. in board 2D-list
        """
        left_top_Ycoord, left_top_Xcoord = self.get_left_top_of_field(fieldy, fieldx)
        pygame.draw.rect(self.displaysurf, Colour.BLACK.value, (left_top_Xcoord, left_top_Ycoord, self.field_size, self.field_size))

    def draw_empty_board(self):
        """Draw Rect objects on Surface object, forming checkers board.

        """
        self.displaysurf.fill(Colour.WHITE.value)
        self.board_dim = self.board_size * self.field_size

        left_top_Ycoord, left_top_Xcoord = self.get_left_top_of_field(0, 0)
        pygame.draw.rect(self.displaysurf, Colour.BROWN.value, (left_top_Xcoord, left_top_Ycoord, self.board_dim, self.board_dim))
        counter = 0
        for fieldy in range(self.board_size):
            for fieldx in range(self.board_size):
                if counter % 2 == 0:
                    self.draw_field(fieldy, fieldx)
                counter += 1
            counter += 1

    def draw_pawn(self, fieldy, fieldx, colour):
        """Draw Circle object on Surface object at given field.

        :param fieldy: Board vertical coordinate, equivalent to row no. in board 2D-list
        :param fieldx: Board horizontal coordinate, equivalent to column no. in board 2D-list
        :param colour: Colour of given pawn
        """
        half = int(self.field_size * 0.5)

        left_top_Ycoord, left_top_Xcoord = self.get_left_top_of_field(fieldy, fieldx)
        pygame.draw.circle(self.displaysurf, colour, (left_top_Xcoord + half, left_top_Ycoord + half), half - 5)

    def draw_king_overlay(self, fieldy, fieldx):
        """Draw Cirle object on Surface object at given field.

        :param fieldy: Board vertical coordinate, equivalent to row no. in board 2D-list
        :param fieldx: Board horizontal coordinate, equivalent to column no. in board 2D-list
        """
        half = int(self.field_size * 0.5)
        quarter = int(self.field_size * 0.25)
        left_top_Ycoord, left_top_Xcoord = self.get_left_top_of_field(fieldy, fieldx)
        pygame.draw.circle(self.displaysurf, Colour.BLACK.value, (left_top_Xcoord + half, left_top_Ycoord + half), quarter - 5)

    def draw_pieces_on_board(self, board):
        """Call to draw_pawn method on fields with pawns in them.

        :param board: Board data structure
        """
        for fieldy in range(len(board)):
            for fieldx in range(len(board[0])):
                if isinstance(board[fieldy][fieldx], Pawn.Pawn):
                    self.draw_pawn(fieldy, fieldx, board[fieldy][fieldx].get_colour())
                elif isinstance(board[fieldy][fieldx], King.King):
                    self.draw_pawn(fieldy, fieldx, board[fieldy][fieldx].get_colour())
                    self.draw_king_overlay(fieldy, fieldx)

    def get_spot_clicked(self, board, mouse_posx, mouse_posy):
        """Convert pixel X&Y coordinates to board X&Y coordinates

        :param board: board data structure
        :param mouse_posx: Horizontal pixel coordinate
        :param mouse_posy: Vertical pixel coordinate
        :return: fieldx, fieldy representing board X&Y coordinates or None, None
        """
        for fieldy in range(len(board)):
            for fieldx in range(len(board)):
                left_top_Ycoord, left_top_Xcoord = self.get_left_top_of_field(fieldy, fieldx)
                field_Rect = pygame.Rect(left_top_Xcoord, left_top_Ycoord, self.field_size, self.field_size)
                if field_Rect.collidepoint(mouse_posx, mouse_posy):
                    return fieldy, fieldx
        return None, None

    def draw_highlight(self, fieldy, fieldx):
        """Draw Rect object on given field, serving as the field's border."""
        left_top_Ycoord, left_top_Xcoord = self.get_left_top_of_field(fieldy, fieldx)
        pygame.draw.rect(self.displaysurf, Colour.HIGHTLIGHTCOLOUR.value, (left_top_Xcoord, left_top_Ycoord,
                                                                           self.field_size - 3, self.field_size - 3), 4)

    def draw_computer_highlight(self, fieldy, fieldx):
        """Draw Rect object on given field, serving as the field's border."""
        left_top_Ycoord, left_top_Xcoord = self.get_left_top_of_field(fieldy, fieldx)
        pygame.draw.rect(self.displaysurf, Colour.RED.value, (left_top_Xcoord, left_top_Ycoord,
                                                                           self.field_size - 3, self.field_size - 3), 4)
    def highlight_available_moves(self, available_moves):
        """Iterate through list of available moves and call to draw_highlight() method on True values."""
        for fieldy in range(len(available_moves)):
            for fieldx in range(len(available_moves)):
                if available_moves[fieldy][fieldx] is True:
                    self.draw_highlight(fieldy, fieldx)
        pygame.display.update()

    def update_board(self, board):
        """Call to draw_empty_board and draw_pieces_on_board methods."""
        self.draw_empty_board()
        self.draw_pieces_on_board(board)

    def move_piece_animation(self, board, fieldy, fieldx, colour, posy, posx):
        """Call to draw_pawn/draw_king_overlay method at move location and draw_field method at piece's location.

        :param board: board data structure
        :param fieldy: Board vertical coordinate at move's destination
        :param fieldx: Board horizontal coordinate at move's destination
        :param colour: Colour of given pawn
        :param posy: Board vertical coordinate of piece's current location.
        :param posx: Board horizontal coordinate of piece's current location.
        """
        self.draw_pawn(fieldy, fieldx, colour)
        self.draw_field(posy, posx)
        if isinstance(board[posy][posx], King.King):
            self.draw_king_overlay(fieldy, fieldx)

    def attack_piece_animation(self, board, fieldy, fieldx, colour, posy, posx):
        """Call to draw_pawn method at move attack destination and draw_field method at pieces' locations.

        :param board: board data structure
        :param fieldy: Board vertical coordinate at move's destination
        :param fieldx: Board horizontal coordinate at move's destination
        :param colour: Colour of given pawn
        :param posy: Board vertical coordinate of piece's current location.
        :param posx: Board horizontal coordinate of piece's current location
        """
        attacked_piece_x = int((fieldx + posx) / 2)
        if fieldy < posy:
            attacked_piece_y = posy - 1
        else:
            attacked_piece_y = posy + 1

        self.draw_pawn(fieldy, fieldx, colour)
        if isinstance(board[posy][posx], King.King):
            self.draw_king_overlay(fieldy, fieldx)
        self.draw_field(posy, posx)
        self.draw_field(attacked_piece_y, attacked_piece_x)
        pygame.display.update()

    def victory_animation(self, colour):
        self.displaysurf.fill(colour)
        pygame.display.update()
        pygame.time.wait(3000)
        pygame.quit()
        sys.exit()

    def check_for_quit(self):
        """Look for QUIT event inputs and escape keys and if any are present, call to terminate method"""
        for event in pygame.event.get():
            if event.type == QUIT:
                self.terminate()
            pygame.event.post(event)
        for event in pygame.event.get(KEYUP):
            if event.key == K_ESCAPE:
                self.terminate()
            pygame.event.post(event)

    def terminate(self):
        """Quit pygame and shutdown program"""
        pygame.quit()
        sys.exit()

    def highlight_while_hovering(self, board, display, mouse_clicked, mousey, mousex):
        """Call to draw_highlight on not-clicked boxes."""
        if mouse_clicked is False:
            boxy, boxx = display.get_spot_clicked(board, mousey, mousex)
            if boxy is not None and boxx is not None:
                display.draw_highlight(boxy, boxx)