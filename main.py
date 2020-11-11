import pygame, sys
from pygame.locals import *
from Colour import Colour
from Piece import Piece
from Board import Board
from Display import Display
import configparser
from Player import Player
from Pawn import Pawn
from Computer import Computer
from Move import Move
import math

config = configparser.ConfigParser()
config.read('config.ini')
fps = int(config['Window']['FPS'])


def main():
    pygame.init()
    fps_clock = pygame.time.Clock()
    pygame.display.set_caption('Checkers')

    main_board = Board()
    main_display = Display()

    spoty = 0
    spotx = 0
    mousex = 0
    mousey = 0
    mouse_clicked = False
    board = main_board.get_newboard()
    human_player = Player(Colour.WHITE.value, True)
    ai_player = Player(Colour.RED.value, False)
    computer = Computer(ai_player, human_player, Colour.RED.value)
    move = Move()

    while True:  # Main game loop
        player = Player.select_player_with_turn(human_player, ai_player)
        main_display.update_board(board)

        if human_player.turn is True:  # human player turn
            is_attacked = player.is_piece_attacked(board) # checks if piece is attacked
            main_display.check_for_quit()

            for event in pygame.event.get():  # event handling loop
                if event.type == MOUSEMOTION:
                    mousey, mousex = event.pos
                if event.type == MOUSEBUTTONUP:
                    spoty, spotx = main_display.get_spot_clicked(board, event.pos[0], event.pos[1])
                    mouse_clicked = True
            main_display.highlight_while_hovering(board, main_display, mouse_clicked, mousey, mousex)
            piece = board[spoty][spotx]

            if isinstance(piece, Piece) and piece.colour == player.colour and mouse_clicked is True:
                available_moves, attack = piece.get_all_available_moves(board)
                has_attacked = False
    
                # While loop for handling attack moves. If there's no attack available, this loop is skipped.
                while any(True in sublist for sublist in available_moves) and attack is True:
                    main_display.highlight_available_moves(available_moves)  # displays available attacks
                    event = pygame.event.wait()
                    main_display.check_for_quit()
    
                    if event.type == MOUSEBUTTONUP:
                        field_to_move_y, field_to_move_x = main_display.get_spot_clicked(board, event.pos[0], event.pos[1])

                        if available_moves[field_to_move_y][field_to_move_x] is True:
                            main_display.attack_piece_animation(board, field_to_move_y, field_to_move_x,
                                                                piece.colour, spoty, spotx)
                            piece.attack_piece(board, field_to_move_y, field_to_move_x)

                            spoty, spotx = field_to_move_y, field_to_move_x

                            if isinstance(piece, Pawn):
                                piece.check_for_promotion(board)

                            available_moves, attack = piece.get_all_available_moves(board)
                            has_attacked = True

                        elif has_attacked is False:
                            break  # return to piece selection

                while any(True in sublist for sublist in available_moves) and not has_attacked and not is_attacked:
                    main_display.highlight_available_moves(available_moves)
                    event = pygame.event.wait()
                    main_display.check_for_quit()

                    if event.type == MOUSEBUTTONUP:  # event handling statement for mouseclicks
                        field_to_move_y, field_to_move_x = main_display.get_spot_clicked(board, event.pos[0], event.pos[1])

                        if available_moves[field_to_move_y][field_to_move_x] is True:
                            main_display.move_piece_animation(board, field_to_move_y, field_to_move_x,
                                                              piece.colour, spoty, spotx)
                            piece.make_move(board, field_to_move_y, field_to_move_x)
                            spoty, spotx = field_to_move_y, field_to_move_x

                            if isinstance(piece, Pawn):
                                piece.check_for_promotion(board)

                            # end his turn
                            player.switch_turns(human_player, ai_player)
                            mousey, mousex = event.pos
                            available_moves = [[]]
                        else:
                            break  # return to piece selection

                if has_attacked:  # end his turn
                    player.switch_turns(human_player, ai_player)
                    mousey, mousex = event.pos


        else:  # Computer turn
            value, best_move = computer.alpha_beta(5, True, -math.inf, math.inf, board)
            try:
                move.attack(board, best_move[0], best_move[1], best_move[2], best_move[3], best_move[4])
                main_display.draw_computer_highlight(best_move[0], best_move[1])
                piece = board[best_move[0]][best_move[1]]
                if isinstance(piece, Pawn):
                    piece.check_for_promotion(board)

                available_moves, attack = piece.get_all_available_moves(board)
                while attack is True: # can move after multi-attack, check this function
                    value, best_move = computer.alpha_beta(5, True, math.inf, -math.inf, board)
                    move.attack(board, best_move[0], best_move[1], best_move[2], best_move[3], best_move[4])
                    main_display.draw_computer_highlight(best_move[0], best_move[1])

                    if isinstance(piece, Pawn):
                        piece.check_for_promotion(board)
                    available_moves, attack = piece.get_all_available_moves(board)

            except IndexError:
                move.move(board, best_move[0], best_move[1], best_move[2], best_move[3])
                main_display.draw_computer_highlight(best_move[0], best_move[1])
                piece = board[best_move[0]][best_move[1]]

                if isinstance(piece, Pawn):
                    piece.check_for_promotion(board)

            player.switch_turns(human_player, ai_player)
            pygame.display.update()
            pygame.time.wait(300)

        # Redraw screen and wait a clock tick.
        player.check_for_victory(board, main_display)
        mouse_clicked = False
        pygame.display.update()
        fps_clock.tick()


if __name__ == '__main__':
    main()

