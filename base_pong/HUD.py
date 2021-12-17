from GUI.clickable_component import ClickableComponent
from base_pong.utility_functions import draw_font
from base_pong.important_variables import (
    screen_length,
    screen_height,
    game_window
)
from base_pong.velocity_calculator import VelocityCalculator
import pygame
pygame.init()

# TODO clean up code pronto
class HUD:
    y_coordinate = VelocityCalculator.give_measurement(screen_height, 1)
    x_coordinate_1 = screen_length - \
        VelocityCalculator.give_measurement(screen_length, 4)
    x_coordinate_2 = x_coordinate_1 + \
        VelocityCalculator.give_measurement(screen_length, 2)
    length = VelocityCalculator.give_measurement(screen_length, .7)
    height = VelocityCalculator.give_measurement(screen_height, 5)
    color = (250, 250, 250)
    pause_button = None

    pause_font = pygame.font.Font('freesansbold.ttf', 53)
    normal_font = pygame.font.Font('freesansbold.ttf', 15)

    def render_pause_button():
        HUD.pause_button.run()

        pygame.draw.rect(game_window, (HUD.color), (HUD.x_coordinate_1,
                         HUD.y_coordinate, HUD.length, HUD.height))
        pygame.draw.rect(game_window, (HUD.color), (HUD.x_coordinate_2,
                         HUD.y_coordinate, HUD.length, HUD.height))

    def pause_got_clicked():
        return HUD.pause_button.got_clicked()

    def show_pause_screen():
        message = "Paused"
        draw_font(
            message, HUD.pause_font, is_center_of_screen=True)

    def initialize():
        HUD.pause_button = ClickableComponent()
        length = (HUD.x_coordinate_2 - HUD.x_coordinate_1) + HUD.length
        HUD.pause_button.number_set_bounds(HUD.x_coordinate_1, HUD.y_coordinate, length, HUD.height)




HUD.initialize()