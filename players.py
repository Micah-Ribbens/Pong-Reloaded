from UtilityClasses import GameObject
import pygame

from velocity_calculator import VelocityCalculator
import pygame
from important_variables import *
class Paddle(GameObject):
    can_move_up = True
    can_move_down = True
    velocity = VelocityCalculator.give_velocity(screen_height, 1000)

    def __init__(self):
        self.y_coordinate = 0
        self.x_coordinate = 0
        self.length = VelocityCalculator.give_measurement(screen_length, 3)
        self.height = VelocityCalculator.give_measurement(screen_height, 30)
        self.color = self.white

class Player(Paddle):
    up_key = pygame.K_UP
    down_key = pygame.K_DOWN

    def movement(self):
        controlls = pygame.key.get_pressed()
        if controlls[self.up_key] and self.can_move_up:
            self.y_coordinate -= VelocityCalculator.calc_distance(self.velocity)

        elif controlls[self.down_key] and self.can_move_down:
            self.y_coordinate += VelocityCalculator.calc_distance(self.velocity)