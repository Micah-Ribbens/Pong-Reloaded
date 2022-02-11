from base_pong.important_variables import *
from base_pong.velocity_calculator import VelocityCalculator
from base_pong.engines import CollisionsFinder
from pong_types.pong_type import PongType
from base_pong.drawable_objects import GameObject
from base_pong.ball import Ball
from base_pong.players import Paddle
import pygame


class NormalPong(PongType):
    """The normal version of pong"""

    is_tip_hit = True

    def _ball_collisions(self, ball, player1, player2):
        """ summary: does the collisions of the ball off the players and screen bounds

            params:
                ball: Ball; the ball of the game
                player1: Player; the first player
                player2: Player; the second player

            returns: None
        """

        # TODO explain distance_change logic better
        if ball.bottom >= screen_height:
            distance_change = ball.bottom - screen_height
            ball.is_moving_down = False
            ball.y_coordinate = screen_height - distance_change - ball.height

        if ball.y_coordinate <= 0:
            distance_change = -ball.y_coordinate
            ball.y_coordinate = ball.y_coordinate + distance_change
            ball.is_moving_down = True

        if CollisionsFinder.is_collision(player1, ball):
            self.paddle_collisions(ball, player1)

        if CollisionsFinder.is_collision(player2, ball):
            self.paddle_collisions(ball, player2)

    def ball_collisions(self):
        """ summary: does the ball collisions by calling _ball_collisions()
            params: None
            returns: None
        """

        self._ball_collisions(self.ball, self.player1, self.player2)

    def paddle_collisions(self, ball, paddle):
        """ summary: does the logic for the ball bouncing off of a paddle

            params:
                ball: Ball; the ball that collided with the paddle
                paddle: Paddle; the paddle the ball collided into

            returns: None
        """

        top_tip_of_paddle = GameObject(paddle.x_coordinate, paddle.y_coordinate, paddle.height * .1, paddle.length)
        bottom_tip_of_paddle = GameObject(paddle.x_coordinate, paddle.y_coordinate, paddle.height * .1, paddle.length)
        used_up_height = top_tip_of_paddle.height + bottom_tip_of_paddle.height

        middle_part_of_paddle = GameObject(paddle.x_coordinate, top_tip_of_paddle.bottom, paddle.height - used_up_height, paddle.length)

        if ball.bottom >= middle_part_of_paddle.y_coordinate and ball.y_coordinate <=  middle_part_of_paddle.bottom:
            ball.middle_hit(paddle.power / 10)
        
        elif ball.y_coordinate >= top_tip_of_paddle.y_coordinate and top_tip_of_paddle.bottom <= top_tip_of_paddle.bottom:
            ball.tip_hit(paddle.power / 10)
            ball.is_moving_down = False
        
        # If the ball didn't hit the middle or top it must have hit the bottom
        else:
            ball.tip_hit(paddle.power / 10)
            ball.is_moving_down = True

        if CollisionsFinder.is_left_collision(ball, paddle):
            ball.x_coordinate = paddle.right_edge
            ball.is_moving_right = True

        if CollisionsFinder.is_right_collision(ball, paddle):
            ball.x_coordinate = paddle.x_coordinate - ball.length
            ball.is_moving_right = False

    def ball_movement(self):
        """ summary: does the horizontal and vertical movement of the ball by calling _ball_movement()
            params: None
            returns: None
        """

        self._ball_movement(self.ball)

    def run(self):
        """ summary: runs all the code that is necessary for this pong type
            params: None
            returns: None
        """
        self.ball_collisions()
        self.ball_movement()

    def reset(self):
        """ summary: resets everything necessary after each time someone scores
            params: None
            returns: None
        """
        self.ball.reset()

    def _ball_movement(self, ball):
        """ summary: does the horizontal and vertical movement of the ball

            params:
                ball: Ball; the ball that should be moved

            returns: None
        """

        distance_change = VelocityCalculator.calc_distance(ball.upwards_velocity)
        ball.y_coordinate += distance_change if ball.is_moving_down else -distance_change
        ball.movement()