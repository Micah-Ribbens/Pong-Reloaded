import pygame
from base_pong.utility_classes import GameObject
from base_pong.velocity_calculator import VelocityCalculator
from base_pong.utility_functions import change_properties
from base_pong.important_variables import *
from base_pong.colors import *


class Paddle(GameObject):
    can_move_up = True
    can_move_down = True
    velocity = VelocityCalculator.give_velocity(screen_height, 1500)
    power = 10.5
    attributes = ["x_coordinate", "y_coordinate"]

    def __init__(self):
        self.y_coordinate = 0
        self.x_coordinate = 0
        self.length = VelocityCalculator.give_measurement(screen_length, 3)
        self.height = VelocityCalculator.give_measurement(screen_height, 30)
        self.color = red
        self.outline_color = red


class Player(Paddle):
    up_key = pygame.K_UP
    down_key = pygame.K_DOWN

    # TODO add outline to the player
    def draw(self):
        GameObject.draw(self)
        # pygame.draw.rect(game_window, (self.outline_color), (self.x_coordinate,
        #             self.y_coordinate, self.length, self.height), 8)

    def movement(self):
        controlls = pygame.key.get_pressed()
        if controlls[self.up_key] and self.can_move_up:
            self.y_coordinate -= VelocityCalculator.calc_distance(
                self.velocity)

        if controlls[self.down_key] and self.can_move_down:
            self.y_coordinate += VelocityCalculator.calc_distance(
                self.velocity)

    def change_properties(self, properties, object):
        self.attributes = properties
        change_properties(self, object)
