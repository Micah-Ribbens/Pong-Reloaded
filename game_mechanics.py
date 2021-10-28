import pygame
from base_pong.engines import CollisionsEngine
from base_pong.UtilityClasses import GameObject, HistoryKeeper
from base_pong.score_keeper import ScoreKeeper
from base_pong.players import Player
from base_pong.ball import Ball
from base_pong.HUD import HUD
from base_pong.important_variables import *
from base_pong.velocity_calculator import VelocityCalculator
import time
# from game_modes import *
from game_modes.gravity_pong import GravityPong
from game_selector import GameSelector
GameSelector.game_mode = GravityPong
nameOfGame = "robowars"
pygame.display.set_caption(f'{nameOfGame}')

class GameRunner:
    pause_is_held_down = False
    game_paused = False
    ball = Ball()
    player1 = Player()
    player2 = Player()

    def reset_variables():
        GameRunner.ball.reset()
        GameSelector.reset()
        GameRunner.ball.name = "ball"
        GameRunner.player2.outline_color = GameObject.blue
        GameRunner.player1.name = "player1"
        GameRunner.player2.name = "player2"
        GameRunner.player1.up_key = pygame.K_w
        GameRunner.player1.down_key = pygame.K_s
        GameRunner.player1.right_key = pygame.K_d
        GameRunner.player1.left_key = pygame.K_a
        GameRunner.player2.x_coordinate = screen_length - GameRunner.player2.length
    def reset_after_scoring():
        HistoryKeeper.reset()
        GameRunner.ball.reset()
        GameSelector.reset()
    def game_is_paused():
        pause_clicked = HUD.pause_clicked()
        # TODO can_pause? Isn't this used to pause and unpause?
        can_pause = not GameRunner.pause_is_held_down and pause_clicked

        if pause_clicked:
            GameRunner.pause_is_held_down = True

        else:
            GameRunner.pause_is_held_down = False
        if can_pause:
            GameRunner.game_paused = not GameRunner.game_paused
        return GameRunner.game_paused

    def run_game():
        run = True
        GameRunner.reset_variables()
        while run:
            start_time = time.time()
            HUD.show_pause_screen()
            # If the player hits the exit button then the game closes
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            # Has to be above all the drawing because it paints the screen the color of the background
            window.fill(background)

            # Draw Everything has to be here so it can populate history keeper allowing the engines to see the last_platform object
            if not GameRunner.game_is_paused():
                HistoryKeeper.add(GameRunner.player1, GameRunner.player1.name, True)
                HistoryKeeper.add(GameRunner.player2, GameRunner.player2.name, True)
                HistoryKeeper.add(GameRunner.ball, "ball", True)
                # HistoryKeeper.add(GameRunner.player1, GameRunner.player1.name, True)
                # HistoryKeeper.add(GameRunner.player2, GameRunner.player2.name, True)

                ScoreKeeper.show_score()
                GameRunner.player1.draw()
                GameRunner.player2.draw()
                GameRunner.ball.draw()

                GameRunner.ball.movement()
                GameRunner.player1.movement()
                GameRunner.player2.movement()
                CollisionsEngine.ball_collisions(GameRunner.ball, GameRunner.player1, GameRunner.player2)
                CollisionsEngine.paddle_movements(GameRunner.player1)
                CollisionsEngine.paddle_movements(GameRunner.player2)
                ScoreKeeper.figure_out_scoring(GameRunner.ball)
                GameSelector.run(GameRunner.ball, GameRunner.player1, GameRunner.player2)
            HUD.render_pause_button(GameRunner.game_is_paused())
            if ScoreKeeper.has_scored(GameRunner.ball):
                GameRunner.reset_after_scoring()




            pygame.display.update()
            end_time = time.time()
            time_taken = end_time - start_time
            if time_taken > 0:
                VelocityCalculator.time = time_taken
        GameRunner.reset_variables()
        GameRunner.run_game()
