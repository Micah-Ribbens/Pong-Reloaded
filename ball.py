from UtilityClasses import GameObject
from velocity_calculator import VelocityCalculator
from important_variables import *
class Ball(GameObject):
    is_moving_right = True
    is_moving_down = True
    base_velocity = VelocityCalculator.give_velocity(screen_length, 200)
    velocity = base_velocity
    def __init__(self):
        self.length = VelocityCalculator.give_measurement(screen_height, 5)
        self.height = VelocityCalculator.give_measurement(screen_height, 5)
        self.x_coordinate = screen_length // 2
        self.y_coordinate = screen_height // 2
        self.color = self.white
        self.name = "ball"
    def reset(self):
        self.x_coordinate = screen_length // 2
        self.y_coordinate = screen_height // 2
        self.velocity = self.base_velocity
    def movement(self):
        x_change = VelocityCalculator.calc_distance(self.velocity)
        y_change = VelocityCalculator.calc_distance(self.velocity)
        self.x_coordinate += x_change if self.is_moving_right else -x_change
        self.y_coordinate += y_change if self.is_moving_down else -y_change