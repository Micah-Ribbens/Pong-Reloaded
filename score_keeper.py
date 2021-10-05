from UtilityClasses import UtilityFunctions
import pygame
from important_variables import *
from ball import Ball
class ScoreKeeper:
    player1_score = 0
    player2_score = 0
    def keep_score(ball: Ball):
        if ball.x_coordinate <= 0:
            ScoreKeeper.player1_score += 1
            ball.reset()
        if ball.x_coordinate >= screen_length:
            ScoreKeeper.player2_score += 1
            ball.reset()
        UtilityFunctions.draw_font(f"Player 1: {ScoreKeeper.player1_score} Player 2: {ScoreKeeper.player2_score}", 
                                   pygame.font.Font('freesansbold.ttf', 30), is_center_of_screen=True, y_coordinate=screen_height*.02)
                        