from GUI.button import Button
from GUI.clickable_component import ClickableComponent
from GUI.grid import Grid
from base_pong.utility_functions import draw_font, percentage_to_number, percentages_to_numbers
from GUI.menu_item import MenuItem
from base_pong.players import Player
from base_pong.ball import Ball
from base_pong.important_variables import *
from base_pong.velocity_calculator import VelocityCalculator
from game_screen import GameScreen
from base_pong.colors import *
from base_pong.drawable_objects import Dimensions
from base_pong.events import Event
from GUI.sub_screen import SubScreen
# Paddle Dimension and Ball Dimensions

class AlterSizesScreen(SubScreen):
    paddle = Player()
    paddle1 = Player()
    paddle2 = Player()
    up_key_event = None
    down_key_event = None
    left_key_event = None
    right_key_event = None
    ball = Ball()
    menus = None
    name = "Alter Sizes"

    def initiate(length_used_up, height_used_up):
        AlterSizesScreen.paddle2.x_coordinate = screen_length - \
            AlterSizesScreen.paddle2.length
        paddle_y_coordinate = height_used_up
        AlterSizesScreen.paddle1.y_coordinate, AlterSizesScreen.paddle2.y_coordinate = paddle_y_coordinate, paddle_y_coordinate

        AlterSizesScreen.ball.reset()

        AlterSizesScreen.up_key_event = Event()
        AlterSizesScreen.down_key_event = Event()
        AlterSizesScreen.left_key_event = Event()
        AlterSizesScreen.right_key_event = Event()

        AlterSizesScreen.menus = [MenuItem("Paddle Dimensions", [Player().height, Player().length], ["height", "length"], 5),
                                  MenuItem("Ball Dimensions", [Ball().height, Ball().length], [
                                           "height", "length"], 5),
                                  MenuItem("Paddle Power", [
                                           Player().power], ["power"], .25),
                                  MenuItem("Ball Speed", [Ball().base_forwards_velocity], ["base_velocity"], int(VelocityCalculator.give_velocity(screen_length, 2)))]

        x_coordinate, y_coordinate, length, height = percentages_to_numbers(0, 0, 100, 100, screen_length, screen_height)

        grid = Grid(Dimensions(x_coordinate, y_coordinate, length, height), 2, None, False)

        max_height = VelocityCalculator.give_measurement(screen_height, 10)
        grid.turn_into_grid(AlterSizesScreen.menus, None, max_height)

    def do_menu_item_logic():
        controlls = pygame.key.get_pressed()
        AlterSizesScreen.up_key_event.run(controlls[pygame.K_UP])
        AlterSizesScreen.down_key_event.run(controlls[pygame.K_DOWN])
        AlterSizesScreen.right_key_event.run(controlls[pygame.K_RIGHT])
        AlterSizesScreen.left_key_event.run(controlls[pygame.K_LEFT])

        for menu_item in AlterSizesScreen.menus:

            if menu_item.got_clicked():
                AlterSizesScreen.reset_clicked()
                menu_item.is_selected = True

    def run():
        AlterSizesScreen.do_menu_item_logic()
        AlterSizesScreen.change_properties()
        AlterSizesScreen.change_class_attributes()

        AlterSizesScreen.render()

    def render():
        AlterSizesScreen.ball.draw()
        AlterSizesScreen.paddle1.draw()
        AlterSizesScreen.paddle2.draw()

        for menu_item in AlterSizesScreen.menus:
            menu_item.run(AlterSizesScreen.up_key_event, AlterSizesScreen.down_key_event,
                          AlterSizesScreen.left_key_event, AlterSizesScreen.right_key_event)

    def reset_clicked():
        for menu_item in AlterSizesScreen.menus:
            menu_item.is_selected = False

    def change_properties():
        for menu in AlterSizesScreen.menus:
            object_modifying = AlterSizesScreen.paddle if menu.label.__contains__(
                "Paddle") else AlterSizesScreen.ball
            object_modifying.__dict__[
                menu.properties_modifying[0]] = menu.values[0]

            if menu.properties_modifying.__len__() == 2:
                object_modifying.__dict__[
                    menu.properties_modifying[1]] = menu.values[1]

        modified_properties = ["length", "height", "power"]
        AlterSizesScreen.paddle2.change_properties(
            modified_properties, AlterSizesScreen.paddle)
        AlterSizesScreen.paddle1.change_properties(
            modified_properties, AlterSizesScreen.paddle)
        AlterSizesScreen.paddle2.x_coordinate = screen_length - \
            AlterSizesScreen.paddle2.length

    def change_class_attributes():
        modified_properties = ["length", "height", "power"]
        GameScreen.player1.change_properties(
            modified_properties, AlterSizesScreen.paddle)
        GameScreen.player2.change_properties(
            modified_properties, AlterSizesScreen.paddle)
        GameScreen.ball = AlterSizesScreen.ball
