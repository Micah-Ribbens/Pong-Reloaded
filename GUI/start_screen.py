from GUI.game_modes_screen import GameModesScreen
from GUI.alter_sizes_screen import AlterSizesScreen
from GUI.button import Button
from GUI.grid import Grid
from base_pong.colors import *
from base_pong.velocity_calculator import VelocityCalculator
from base_pong.important_variables import *
from GUI.screen import Screen
from base_pong.utility_classes import Dimensions
from base_pong.utility_functions import percentages_to_numbers


class StartScreen(Screen):
    selected_screen = None
    is_initiated = False
    sub_screens = [AlterSizesScreen, GameModesScreen]
    sub_screen_buttons = []
    start_button = Button("Start", 20, white, green)
    back_button = Button("Back", 20, white, green)

    # Each button is associated with a sub screen
    def get_sub_screen(sub_screen_button: Button):
        for sub_screen in StartScreen.sub_screens:
            if sub_screen_button.text == sub_screen.name:
                return sub_screen

    def run():
        if not StartScreen.is_initiated:
            StartScreen.initiate()

        for button in StartScreen.sub_screen_buttons:
            # Despite the buttons not being rendered they can still be clicked, so this prevents that from happening
            if button.got_clicked() and StartScreen.selected_screen == StartScreen:
                StartScreen.selected_screen = StartScreen.get_sub_screen(
                    button)

        if StartScreen.back_button.got_clicked():
            StartScreen.selected_screen = StartScreen

        StartScreen.render()

    def render():
        for screen in StartScreen.sub_screens:
            if screen == StartScreen.selected_screen:
                screen.run()
                break

        if StartScreen.selected_screen == StartScreen:
            StartScreen.render_sub_screen_buttons()

        StartScreen.back_button.run()
        StartScreen.start_button.run()

    def render_sub_screen_buttons():
        for button in StartScreen.sub_screen_buttons:
            button.run()

    def initiate():
        StartScreen.selected_screen = StartScreen
        StartScreen.is_initiated = True

        for x in range(len(StartScreen.sub_screens)):
            button = Button(StartScreen.sub_screens[x].name, 20, white, green)
            StartScreen.sub_screen_buttons.append(button)

        x_coordinate, y_coordinate, length, height = percentages_to_numbers(0, 20, 100, 90, screen_length, screen_height)
        sub_screen_button_gird = Grid(Dimensions(x_coordinate, y_coordinate, length, height), 3, None, True)

        max_height = VelocityCalculator.give_measurement(screen_height, 20)
        sub_screen_button_gird.turn_into_grid(StartScreen.sub_screen_buttons, None, max_height)

        x_coordinate, y_coordinate, length, height = percentages_to_numbers(0, 0, 30, 10, screen_length, screen_height)
        button_grid = Grid(Dimensions(x_coordinate, y_coordinate, length, height), 2, None, True)
        button_grid.turn_into_grid([StartScreen.start_button, StartScreen.back_button], None, None)
        
        for sub_screen in StartScreen.sub_screens:
            sub_screen.initiate(0, button_grid.dimensions.height)
        

