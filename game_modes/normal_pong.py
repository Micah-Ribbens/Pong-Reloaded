from base_pong.important_variables import *
from base_pong.velocity_calculator import VelocityCalculator
from game_modes.game_mode import GameMode
class NormalPong(GameMode):
    def ball_collisions(ball):
        if ball.bottom >= screen_height:
            ball.is_moving_down = False
        if ball.y_coordinate <= 0:
            ball.is_moving_down = True
    
    def ball_movement(ball):
        y_change = VelocityCalculator.calc_distance(ball.forwards_velocity)
        ball.y_coordinate += y_change if ball.is_moving_down else -y_change

    def run(ball, paddle1, paddle2):
        NormalPong.ball_collisions(ball)
        NormalPong.ball_movement(ball)
    def reset():
        pass