from base_pong.UtilityClasses import GameObject, HistoryKeeper
from base_pong.velocity_calculator import VelocityCalculator
from base_pong.important_variables import *
class Ball(GameObject):
    is_moving_right = False
    is_moving_down = True
    base_forwards_velocity = VelocityCalculator.give_velocity(screen_length, 300)
    forwards_velocity = base_forwards_velocity
    can_move = True
    height = VelocityCalculator.give_measurement(screen_height, 5)
    time_since_ground = 0
    attributes = ["x_coordinate", "y_coordinate"]
    def __init__(self):
        self.length = VelocityCalculator.give_measurement(screen_height, 5)
        self.name = "ball"
    def reset(self):
        self.x_coordinate = screen_length // 2
        self.y_coordinate = screen_height // 2
        self.forwards_velocity = self.base_forwards_velocity
        self.color = self.white
    def movement(self):
        HistoryKeeper.add(self, "ball", True)
        x_change = VelocityCalculator.calc_distance(self.forwards_velocity)
        self.x_coordinate += x_change if self.is_moving_right else -x_change
    def draw(self):
        pygame.draw.ellipse(window, self.color, (self.x_coordinate, self.y_coordinate, self.length, self.height))


