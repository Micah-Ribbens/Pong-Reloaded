from base_pong.important_variables import *
from base_pong.velocity_calculator import VelocityCalculator
from base_pong.engines import CollisionsEngine
from game_modes.game_mode import PongType


class NormalPong(PongType):
    def ball_collisions(ball, paddle1, paddle2):
        if ball.bottom >= screen_height:
            ball.is_moving_down = False
        if ball.y_coordinate <= 0:
            ball.is_moving_down = True
        CollisionsEngine.ball_collisions(ball, paddle1, paddle2)

    def ball_movement(ball):
        distance_change = VelocityCalculator.calc_distance(
            ball.forwards_velocity)
        ball.y_coordinate += distance_change if ball.is_moving_down else -distance_change
        ball.movement()
        # ball.x_coordinate += distance_change if ball.is_moving_right else -distance_change

    def run(ball, paddle1, paddle2):
        NormalPong.ball_collisions(ball, paddle1, paddle2)
        NormalPong.ball_movement(ball)

    def reset(ball, paddle1, paddle2):
        pass
