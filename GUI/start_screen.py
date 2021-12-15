from GUI.game_modes_screen import GameModesScreen
from GUI.alter_sizes_screen import AlterSizesScreen
from GUI.button import Button
from base_pong.colors import *
from base_pong.velocity_calculator import VelocityCalculator
from base_pong.important_variables import *


class StartScreen:
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
            # All of them are going to be in the same row, so each one must take up the total length divided by the number of sub_screen_buttons
            button_percent_length = 100 // len(StartScreen.sub_screens)

            button = Button(StartScreen.sub_screens[x].name, 20, white, green)
            # The first button doesn't have to have a buffer before it since there are no buttons before it
            buffer_percent = 3 if x > 0 else 0

            button.percentage_set_bounds(
                button_percent_length * x + buffer_percent, 30, button_percent_length, 20)
            StartScreen.sub_screen_buttons.append(button)

        button_percent_height = 10
        StartScreen.start_button.percentage_set_bounds(
            0, 0, 30, button_percent_height)
        StartScreen.back_button.percentage_set_bounds(
            35, 0, 30, button_percent_height)

        for sub_screen in StartScreen.sub_screens:
            # Buffer between the sub_screen and the back and start buttons
            height_buffer = VelocityCalculator.give_measurement(screen_height, 2)

            height_used_up = VelocityCalculator.give_measurement(
                screen_height, button_percent_height) + height_buffer

            sub_screen.initiate(0, height_used_up)
