from base_pong.important_variables import *
from base_pong.engines import CollisionsEngine
from game_modes.game_mode import PongType
from game_modes.normal_pong import NormalPong
from base_pong.players import Paddle
from base_pong.velocity_calculator import VelocityCalculator
from base_pong.utility_classes import HistoryKeeper

middle_paddle = Paddle()
# TODO change back
middle_paddle.x_coordinate = screen_length // 2
middle_paddle.y_coordinate = 0
middle_paddle.name = "middle_paddle"
middle_paddle.height = VelocityCalculator.give_measurement(screen_height, 33)
middle_paddle.is_moving_down = False
middle_paddle.power = 10


class MiddlePaddlePong(PongType):
    def middle_paddle_movement():
        if middle_paddle.bottom >= screen_height:
            middle_paddle.is_moving_down = False
        if middle_paddle.y_coordinate <= 0:
            middle_paddle.is_moving_down = True
        y_change = VelocityCalculator.calc_distance(middle_paddle.velocity)
        middle_paddle.y_coordinate += y_change if middle_paddle.is_moving_down else -y_change

    def ball_collisions(ball, paddle1, paddle2):
        # Ball collisions changes colors if it hits middle_paddle
        # and I won't to change it back to color before hitting it
        prev_ball_color = ball.color
        CollisionsEngine.ball_collisions(ball, middle_paddle, 1.2)
        ball.color = prev_ball_color

    def run(ball, paddle1, paddle2):
        CollisionsEngine.ball_collisions(ball, paddle1, paddle2)
        NormalPong.run(ball, paddle1, paddle2)
        middle_paddle.draw()
        MiddlePaddlePong.middle_paddle_movement()
        MiddlePaddlePong.ball_collisions(ball, paddle1, paddle2)
        HistoryKeeper.add(middle_paddle, "middle_paddle", True)

    def add_needed_objects(ball, paddle1, paddle2):
        PongType.add_needed_objects(ball, paddle1, paddle2)
        HistoryKeeper.add(middle_paddle, middle_paddle.name, True)

    def reset(ball, paddle1, paddle2):
        pass
