from base_pong.important_variables import *
from base_pong.velocity_calculator import VelocityCalculator
from base_pong.engines import CollisionsEngine, CollisionsFinder
from game_modes.game_mode import PongType
from base_pong.drawable_objects import GameObject
from base_pong.ball import Ball
from base_pong.players import Paddle
import pygame


class NormalPong(PongType):
    is_tip_hit = True
    def ball_collisions(ball, paddle1, paddle2):
        controlls = pygame.key.get_pressed()
        if controlls[pygame.K_m]:
            NormalPong.is_tip_hit = False
        if controlls[pygame.K_t]:
            NormalPong.is_tip_hit = True
        if ball.bottom >= screen_height:
            ball.is_moving_down = False

        if ball.y_coordinate <= 0:
            ball.is_moving_down = True
        
        if CollisionsFinder.is_collision(paddle1, ball):
            NormalPong.paddle_collisions(paddle1, ball)
        
        if CollisionsFinder.is_collision(paddle2, ball):
            NormalPong.paddle_collisions(paddle2, ball)

    def paddle_collisions(paddle: Paddle, ball: Ball):
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
    

    def ball_movement(ball):
        distance_change = VelocityCalculator.calc_distance(
            ball.upwards_velocity)
        ball.y_coordinate += distance_change if ball.is_moving_down else -distance_change
        ball.movement()
        # ball.x_coordinate += distance_change if ball.is_moving_right else -distance_change

    def run(ball, paddle1, paddle2):
        NormalPong.ball_collisions(ball, paddle1, paddle2)
        NormalPong.ball_movement(ball)

    def reset(ball, paddle1, paddle2):
        ball.reset()
