from base_pong.important_variables import *
from base_pong.velocity_calculator import VelocityCalculator
from game_modes.game_mode import PongType
from base_pong.players import Player
from base_pong.engines import CollisionsEngine, CollisionsFinder
from base_pong.utility_classes import GameObject, Segment
from game_modes.normal_pong import NormalPong
from base_pong.colors import *


class ShatterPong(PongType):
    def shatter_pongs(ball, paddle):
        if not CollisionsFinder.is_collision(ball, paddle):
            return
        ball_has_hit_top = ball.y_coordinate <= paddle.y_midpoint
        shatter_function = ShatterPong.shatter_top if ball_has_hit_top else ShatterPong.shatter_bottom
        shatter_function(ball, paddle)

    def shatter_top(ball, paddle):
        height_change = ball.bottom - paddle.y_coordinate
        paddle.height -= height_change
        paddle.y_coordinate += height_change

    def shatter_bottom(ball, paddle):
        paddle.height -= (ball.y_coordinate - paddle.y_midpoint)

    def ball_movement(ball):
        y_change = VelocityCalculator.calc_distance(ball.forwards_velocity)
        ball.y_coordinate += y_change if ball.is_moving_down else -y_change

    def run(ball, paddle1, paddle2):
        ShatterPong.ball_movement(ball)
        ShatterPong.shatter_pongs(ball, paddle1)
        ShatterPong.shatter_pongs(ball, paddle2)
        CollisionsEngine.ball_collisions(ball, paddle1, paddle2)
        NormalPong.ball_collisions(ball, paddle1, paddle2)

    def reset(ball, player1, player2):
        player1.height = VelocityCalculator.give_measurement(50, screen_height)
        player2.height = VelocityCalculator.give_measurement(50, screen_height)

    def draw_game_objects(ball, paddle1, paddle2):
        ShatterPong.draw_paddle(paddle1)
        ShatterPong.draw_paddle(paddle2)
        ball.draw()

    def draw_paddle(paddle):
        middle_segment = Segment(
            is_percentage=True,
            color=white,
            amount_from_top=50,
            amount_from_left=0,
            length_amount=100,
            width_amount=5
        )
        paddle.draw_in_segments([middle_segment])
