from copy import deepcopy

from base_pong.velocity_calculator import VelocityCalculator
from base_pong.important_variables import *
from base_pong.engines import CollisionsFinder
from pong_types.pong_type import PongType
from pong_types.normal_pong import NormalPong
from pong_types.math import *


class GravityPong(PongType):
    """Pong with the ball's motion following gravity"""

    normal_pong = None
    time = 0
    physics_equation = None
    base_physics_equation = None
    vertex_increase = 0
    hits = 0

    def __init__(self, player1, player2, ball):
        """ summary: Initializes the PongType with the needed objects to run its methods

            params:
                player1: Paddle; the player on the leftmost side on the screen
                player2: Paddle; the player on the rightmost side on the screen
                ball: Ball; the ball that the players hit

            returns: None
        """

        super().__init__(player1, player2, ball)
        self.normal_pong = NormalPong(player1, player2, ball)
        self.physics_equation = PhysicsEquation()
        self.physics_equation.set_all_variables(250, 1, 250, screen_height - self.ball.height)
        self.ball.y_coordinate = screen_height - self.ball.height
        self.velocity_increase = self.get_velocity_increase(7, 1, 0)

    def get_velocity_increase(self, amount_of_hits_to_double, time, vertex):
        """ summary: finds the velocity increase by using the equation d = vit + 1/2 * at^2 where d is displacement, vi is initial velocity,
                     a is acceleration, and t is time

            params:
                amount_of_hits_to_double: int; the amount of hits it takes for the vertex of the equation to double
                time: double; the same time that was used when calling PhysicsEquation.set_all_variables()
                vertex; double; double the vertex (in relation to screen; top is 0 and bottom is 500) that was used when calling PhysicsEquation.set_all_variables()

            returns: double; the velocity increase
        """

        equation = self.physics_equation
        return (vertex - equation.initial_velocity * time - 1/2 * equation.acceleration * pow(time, 2)) / amount_of_hits_to_double

    def ball_collisions(self):
        """ summary: does the ball collisions (interactions with the paddles)
            params: None
            returns: None
        """

        ball_has_collided = CollisionsFinder.is_collision(self.ball, self.player1) or CollisionsFinder.is_collision(self.ball, self.player2)

        if ball_has_collided:
            self.ball.is_moving_right = not self.ball.is_moving_right
            # If the ball is going upwards then its velocity should become more negative moving it higher on the screen
            # The screen's top is at 0 and bottom is at 500 and vice versa if it's going downwards
            amount_changed = -self.velocity_increase if self.physics_equation.initial_velocity < 0 else self.velocity_increase

            self.physics_equation.set_variables(initial_velocity=self.physics_equation.initial_velocity+amount_changed)

        if CollisionsFinder.is_collision(self.ball, self.player1):
            self.ball.x_coordinate = self.player1.right_edge

        if CollisionsFinder.is_collision(self.ball, self.player2):
            self.ball.x_coordinate = self.player2.x_coordinate - self.ball.length

    def ball_movement(self):
        """ summary: does the horizontal and vertical movement of the ball and the logic that goes into
                     making the ball be affected by gravity

            params: None
            returns: None
        """

        if self.ball.y_coordinate <= 0 and self.time > 0:
            # Not making it negative because get_velocity_using_displacement gets the seconds number, which is when it is falling
            # Making it already to the sign (+/-) it should be
            initial_velocity = self.physics_equation.get_velocity_using_displacement(-screen_height + self.ball.height)
            self.physics_equation.set_variables(initial_velocity=initial_velocity, initial_distance=self.ball.height)
            self.ball.y_coordinate = 0

        elif self.ball.bottom >= screen_height and self.time > 0:
            time_to_vertex = self.physics_equation.get_time_to_vertex()
            displacement = screen_height - self.ball.height if self.physics_equation.get_distance(time_to_vertex) < 0 else 0

            # Making it negative to make it go the opposite direction
            initial_velocity = -self.physics_equation.get_velocity_using_displacement(displacement)
            self.physics_equation.set_variables(initial_velocity=initial_velocity, initial_distance=screen_height-self.ball.height)

            self.ball.y_coordinate = screen_height - self.ball.height

        if self.ball.bottom >= screen_height or self.ball.y_coordinate <= 0:
            self.time = 0

        # IMPORTANT: must be below the if statement(s) otherwise the ball's y_coordinate
        self.time += VelocityCalculator.time

        self.ball.y_coordinate = self.physics_equation.get_distance(self.time)

        x_change = VelocityCalculator.calc_distance(self.ball.forwards_velocity)
        self.ball.x_coordinate += x_change if self.ball.is_moving_right else -x_change

    def run(self):
        """ summary: runs all the code that is necessary for this pong type
            params: None
            returns: None
        """

        self.ball_movement()
        self.ball_collisions()
        self.time += VelocityCalculator.time

    def reset(self):
        """ summary: resets everything necessary after each time someone scores
            params: None
            returns: None
        """
        self.time = 0
        self.ball.y_coordinate = screen_height - self.ball.height
        self.physics_equation.set_all_variables(250, 1, 250, screen_height - self.ball.height)
