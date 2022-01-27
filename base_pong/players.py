import pygame
from base_pong.drawable_objects import GameObject
from base_pong.velocity_calculator import VelocityCalculator
from base_pong.utility_functions import change_attributes
from base_pong.important_variables import *
from base_pong.colors import *


class Paddle(GameObject):
    """The paddle that dimensions can be changed and drawn"""

    can_move_up = True
    can_move_down = True
    velocity = VelocityCalculator.give_velocity(screen_height, 1500)
    power = 10.5
    attributes = ["x_coordinate", "y_coordinate"]

    def __init__(self):
        """ summary: initializes the paddle with predetermined values
            params: None
            returns: None
        """

        self.y_coordinate = 0
        self.x_coordinate = 0
        self.length = VelocityCalculator.give_measurement(screen_length, 3)
        # TODO change back to 30
        self.height = VelocityCalculator.give_measurement(screen_height, 100)
        self.color = white
        self.outline_color = red

    def draw(self):
        """ summary: draws the paddle onto the game window
            params: None
            returns: None
        """

        self.color = white
        GameObject.render(self)
        pygame.draw.rect(game_window.get_window(), (self.outline_color), (self.x_coordinate,
                         self.y_coordinate, self.length, self.height), 8)


class Player(Paddle):
    """Extends Paddle and provides movement options and a way to change the classes properties"""

    up_key = pygame.K_UP
    down_key = pygame.K_DOWN

    def movement(self):
        """ summary: moves the paddle up and down if those keys were hit
            params: None
            returns: None
        """

        controls = pygame.key.get_pressed()
        if controls[self.up_key] and self.can_move_up:
            self.y_coordinate -= VelocityCalculator.calc_distance(
                self.velocity)

        if controls[self.down_key] and self.can_move_down:
            self.y_coordinate += VelocityCalculator.calc_distance(
                self.velocity)


