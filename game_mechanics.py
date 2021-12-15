import pygame
from base_pong.engines import CollisionsEngine
from base_pong.utility_classes import GameObject, HistoryKeeper
from base_pong.score_keeper import ScoreKeeper
from base_pong.players import Player
from base_pong.ball import Ball
from base_pong.HUD import HUD
from base_pong.important_variables import *
from base_pong.velocity_calculator import VelocityCalculator
import time
from game_modes.portal_pong import PortalPong
from base_pong.colors import *
from game_modes.game_mode_selector import GameModeSelector

nameOfGame = "robowars"
pygame.display.set_caption(f'{nameOfGame}')


class GameRunner:
    game_mode = None
    pause_is_held_down = False
    game_paused = False
    ball = Ball()
    player1 = Player()
    player2 = Player()

    def reset_variables():
        GameRunner.game_mode = GameModeSelector.get_pong_type()
        GameRunner.ball.reset()
        GameRunner.game_mode.reset(GameRunner.ball, GameRunner.player1,
                                   GameRunner.player2)
        GameRunner.ball.name = "ball"
        GameRunner.player2.color, GameRunner.player2.outline_color = blue, blue
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
        GameRunner.game_mode.reset(GameRunner.ball, GameRunner.player1,
                                   GameRunner.player2)

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

            # Has to be above all the drawing because it paints the screen the color of the background_color
            game_window.fill(background_color)

            # Draw Everything has to be here so it can populate history keeper allowing the engines to see the last_platform object
            if not GameRunner.game_is_paused():
                GameRunner.game_mode.add_needed_objects(
                    GameRunner.ball, GameRunner.player1, GameRunner.player2)

                ScoreKeeper.show_score()
                GameRunner.game_mode.draw_game_objects(
                    GameRunner.ball, GameRunner.player1, GameRunner.player2)
                GameRunner.game_mode.ball_collisions(
                    GameRunner.ball, GameRunner.player1, GameRunner.player2)

                GameRunner.player1.movement()
                GameRunner.player2.movement()
                CollisionsEngine.paddle_movements(GameRunner.player1)
                CollisionsEngine.paddle_movements(GameRunner.player2)
                ScoreKeeper.figure_out_scoring(GameRunner.ball)
                GameRunner.game_mode.run(GameRunner.ball, GameRunner.player1,
                                         GameRunner.player2)
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
