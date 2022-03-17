import pygame.display

from base_pong.engines import CollisionsFinder
from base_pong.path import *
from base_pong.utility_classes import HistoryKeeper
from gui.main_screen import MainScreen
from gui.pause_screen import PauseScreen
from gui.game_screen import GameScreen
from base_pong.important_variables import *
import time
from base_pong.velocity_calculator import VelocityCalculator

game_screen = GameScreen()
start_screen = MainScreen(game_screen)
pause_screen = PauseScreen()

game_window.add_screen(game_screen)
game_window.add_screen(start_screen)
game_window.add_screen(pause_screen)
game_window.set_screen_visible(game_screen, False)
game_window.set_screen_visible(pause_screen, False)
# game_window.set_screen_visible(start_screen, False)


def get_screen(current_screen):
    action_to_screen = {
        game_screen.pause_button.got_clicked(): pause_screen,
        pause_screen.continue_game_button.got_clicked(): game_screen,
        start_screen.start_button.got_clicked(): game_screen,
        pause_screen.go_to_start_screen_button.got_clicked(): start_screen
    }

    screen = action_to_screen.get(True)
    # If none of the actions are True then action_to_screen.get will return None, so the screen stays
    # As the current_screen
    return screen if screen is not None else current_screen

current_screen = start_screen

while True:
    start_time = time.time()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    game_window.run()
    screen = get_screen(current_screen)

    if screen != current_screen:
        current_screen.un_setup()

    if screen != current_screen:
        screen.setup()
        game_window.display_screen(screen)

    current_screen = screen
    # if HistoryKeeper.get_last(game_screen.ball) is not None:
    #     print(game_screen.ball.x_coordinate, HistoryKeeper.get_last(game_screen.ball.name).x_coordinate)
    CollisionsFinder.objects_to_data = {}
    # if CollisionsFinder.sim_collision(game_screen.player1, game_screen.ball) or CollisionsFinder.is_collision(game_screen.player1, game_screen.ball):
    #     CollisionsFinder.is_collision(game_screen.player1, game_screen.ball)
    VelocityCalculator.time = time.time() - start_time
    function_runner.run()
    changer.run_changes()
    HistoryKeeper.last_time = HistoryKeeper.get_last_time()
