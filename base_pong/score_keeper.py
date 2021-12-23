import pygame
from base_pong.utility_functions import draw_font
from base_pong.important_variables import *
from base_pong.ball import Ball


class ScoreKeeper:
    def show_score(player1_score, player2_score):
        draw_font(f"Player 1: {player1_score} Player 2: {player2_score}",
                  pygame.font.Font('freesansbold.ttf', 30), is_center_of_screen=True, y_coordinate=screen_height*.02)

    def player_has_scored(ball: Ball, player_is_leftside):
        return ball.right_edge <= 0 if player_is_leftside else ball.x_coordinate >= screen_length
