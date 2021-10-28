import pygame
from base_pong.UtilityClasses import HistoryKeeper, UtilityFunctions
from base_pong.important_variables import *
from base_pong.ball import Ball
class ScoreKeeper:
    player1_score = 0
    player2_score = 0
    def show_score():
        UtilityFunctions.draw_font(f"Player 1: {ScoreKeeper.player1_score} Player 2: {ScoreKeeper.player2_score}", 
                                   pygame.font.Font('freesansbold.ttf', 30), is_center_of_screen=True, y_coordinate=screen_height*.02)
    def figure_out_scoring(ball: Ball):
        if ball.right_edge <= 0:
            ScoreKeeper.player2_score += 1

        if ball.x_coordinate >= screen_length:
            ScoreKeeper.player1_score += 1

    def has_scored(ball: Ball):
        return ball.right_edge <= 0 or ball.x_coordinate >= screen_length






                        