from GUI.grid import Grid
from GUI.screen import Screen
from GUI.button import Button
from GUI.text_box import TextBox 
from base_pong.colors import *
from base_pong.important_variables import *
from base_pong.velocity_calculator import VelocityCalculator
from base_pong.utility_functions import percentages_to_numbers
from GUI.grid import Grid
from base_pong.utility_classes import Dimensions

class PauseScreen(Screen):
    continue_game_button = Button("Continue Game", 30, white, green)
    go_to_start_screen_button = Button("Go Back to Start Screen", 30, white, green)
    game_paused_text_box = TextBox("Game Paused", 40, False, white, background_color)

    def set_up():
        print("PAUSE SET UP")
        PauseScreen.game_paused_text_box.percentage_set_bounds(0, 0, 100, 40)
        buffer = VelocityCalculator.give_measurement(screen_height, 5)

        x_coordinate = 0
        length = screen_length

        height_used_up = buffer + PauseScreen.game_paused_text_box.height
        y_coordinate = height_used_up
        height = screen_height - height_used_up

        grid = Grid(Dimensions(x_coordinate, y_coordinate, length, height), 2, None, True)
        grid.turn_into_grid([PauseScreen.go_to_start_screen_button, PauseScreen.continue_game_button], None, None)

    def run():
        PauseScreen.game_paused_text_box.run()
        PauseScreen.go_to_start_screen_button.run()
        PauseScreen.continue_game_button.run()
