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

# Game Screen as in where the game is actually played not selection screens and the sort
class GameScreen:
    game_mode = None
    pause_is_held_down = False
    game_paused = False
    ball = Ball()
    player1 = Player()
    player2 = Player()

    def reset_variables():
        GameScreen.game_mode = GameModeSelector.get_pong_type()
        GameScreen.ball.reset()
        GameScreen.game_mode.reset(GameScreen.ball, GameScreen.player1,
                                   GameScreen.player2)
        GameScreen.ball.name = "ball"
        GameScreen.player2.color, GameScreen.player2.outline_color = blue, blue
        GameScreen.player1.name = "player1"
        GameScreen.player2.name = "player2"
        GameScreen.player1.up_key = pygame.K_w
        GameScreen.player1.down_key = pygame.K_s
        GameScreen.player1.right_key = pygame.K_d
        GameScreen.player1.left_key = pygame.K_a
        GameScreen.player2.x_coordinate = screen_length - GameScreen.player2.length

    def reset_after_scoring():
        HistoryKeeper.reset()
        GameScreen.ball.reset()
        GameScreen.game_mode.reset(GameScreen.ball, GameScreen.player1,
                                   GameScreen.player2)

    def game_is_paused():
        pause_clicked = HUD.pause_clicked()
        # TODO can_pause? Isn't this used to pause and unpause?
        can_pause = not GameScreen.pause_is_held_down and pause_clicked

        if pause_clicked:
            GameScreen.pause_is_held_down = True

        else:
            GameScreen.pause_is_held_down = False
        if can_pause:
            GameScreen.game_paused = not GameScreen.game_paused
        return GameScreen.game_paused

    def run():
        run = True
        GameScreen.reset_variables()
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
            if not GameScreen.game_is_paused():
                GameScreen.game_mode.add_needed_objects(
                    GameScreen.ball, GameScreen.player1, GameScreen.player2)

                ScoreKeeper.show_score()
                GameScreen.game_mode.draw_game_objects(
                    GameScreen.ball, GameScreen.player1, GameScreen.player2)
                GameScreen.game_mode.ball_collisions(
                    GameScreen.ball, GameScreen.player1, GameScreen.player2)

                GameScreen.player1.movement()
                GameScreen.player2.movement()
                CollisionsEngine.paddle_movements(GameScreen.player1)
                CollisionsEngine.paddle_movements(GameScreen.player2)
                ScoreKeeper.figure_out_scoring(GameScreen.ball)
                GameScreen.game_mode.run(GameScreen.ball, GameScreen.player1,
                                         GameScreen.player2)
            HUD.render_pause_button(GameScreen.game_is_paused())
            if ScoreKeeper.has_scored(GameScreen.ball):
                GameScreen.reset_after_scoring()

            pygame.display.update()
            end_time = time.time()
            time_taken = end_time - start_time
            if time_taken > 0:
                VelocityCalculator.time = time_taken

        GameScreen.reset_variables()
        GameScreen.run()