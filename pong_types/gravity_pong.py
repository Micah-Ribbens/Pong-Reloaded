from copy import deepcopy

import pygame

from base_pong.equations import Point
from base_pong.path import Path
from base_pong.velocity_calculator import VelocityCalculator
from base_pong.important_variables import *
from base_pong.engines import CollisionsFinder
from pong_types.pong_type import PongType
from pong_types.normal_pong import NormalPong
from base_pong.quadratic_equations import *


class GravityPong(PongType):
    """Pong with the ball's motion following gravity"""

    normal_pong = None
    time = 0
    physics_equation = None
    base_physics_equation = None
    vertex_increase = 0
    hits = 0
    is_writing = False
    data = ""
    test_number = 1
    has_written = False
    s = None

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
        self.s = f"test_number{self.test_number}."

        self.ball_movement()
        self.ball_collisions()
        self.normal_pong.run_player_movement()
        self.time += VelocityCalculator.time

        if self.ball.right_edge >= self.player2.x_coordinate:
            self.is_writing = False
            self.data += f"{self.s}actual_y_coordinate:{self.ball.y_coordinate}"
            self.test_number += 1

        if pygame.key.get_pressed()[pygame.K_SPACE] and not self.has_written:
            self.data += f"number_of_tests{self.test_number}"
            file_writer = open("data.txt", "w+")
            file_writer.write(self.data)
            self.has_written = True

    def reset(self):
        """ summary: resets everything necessary after each time someone scores
            params: None
            returns: None
        """
        self.time = 0
        self.ball.y_coordinate = screen_height - self.ball.height
        self.physics_equation.set_all_variables(250, 1, 250, screen_height - self.ball.height)

    def get_ball_path(self, x_coordinate):
        """ summary: finds the ball's y_coordinate and bottom at the next time it hits the x_coordinate
            IMPORTANT: this function should be called when the ball is going the desired horizontal direction

            params:
                x_coordinate: int; the number that is used to evaluate the ball's path

            returns: Path; the path of the ball from its current x_coordinate to the end x_coordinate
        """

        path = Path(Point(self.ball.x_coordinate, self.ball.y_coordinate), self.ball.height, self.ball.length)

        time_to_travel_distance = abs(x_coordinate - self.ball.x_coordinate) / self.ball.forwards_velocity
        ball_is_moving_down = self.ball.is_moving_down
        ball_y_coordinate = self.ball.y_coordinate
        ball_x_coordinate = self.ball.x_coordinate

        self.data += f"""{self.s}ball_y_coordinate:{ball_y_coordinate}
{self.s}ball_x_coordinate:{ball_x_coordinate}
{self.s}time:{self.time}
{self.s}x_coordinate:{x_coordinate}
{self.s}ball_forward_velocity:{self.ball.forwards_velocity}
{self.s}physics_equation:{self.physics_equation}\n
"""

        self.is_writing = True
        return super().get_ball_path(x_coordinate) # TODO do more later
        # while time_to_travel_distance > 0:
        #     if ball_is_moving_down:
        #         time = self.get_time_to_bottom()
        #         ball_y_coordinate = screen_height - self.ball.height
        #
        #     else:
        #         time = self.get_time_to_vertex()
        #         ball_y_coordinate = 0 if self.physics_equation.get_vertex() < 0 else self.physics_equation.get_vertex()
        #
        #
        #     if time_to_travel_distance - time < 0:
        #         time = time_to_travel_distance
        #         physics_equation = self.get_downwards_physics_equation() if self.physics_equation.get_vertex() < 0 else self.physics_equation
        #         ball_y_coordinate += physics_equation.get_displacement(time)
        #
        #     ball_x_coordinate += time * self.ball.forwards_velocity
        #
        #     path.add_point(Point(ball_x_coordinate, ball_y_coordinate))
        #     ball_is_moving_down = not ball_is_moving_down
        #
        #     time_to_travel_distance -= time
        #
        # print("END", ball_y_coordinate)
        # return path

    def get_time_to_vertex(self):
        """returns: double; the time it will take for the ball to reach its vertex"""

        vertex = 0 if self.physics_equation.get_vertex() < 0 else self.physics_equation.get_vertex()

        # The first point is needed because that will be the vertex
        return self.physics_equation.get_time_to_point(vertex)[0]

    def get_time_to_bottom(self):
        """returns: double; the time it will take for the ball to go from the vertex to the bottom"""

        return_value = None

        if self.physics_equation.get_vertex() < self.ball.height:
            return_value = self.get_downwards_physics_equation().get_time_to_point(screen_height - self.ball.height)

        else:
            return_value = self.get_time_to_bottom()

        return return_value

    def get_physics_equation(self):
        """returns: PhysicsEquation; the physics equation that will dictate the ball's movement"""

    def get_downwards_physics_equation(self):
        """returns: PhysicsEquation; the physics equation will the ball has just hit the top"""

        physics_equation = deepcopy(self.physics_equation)
        initial_velocity = physics_equation.get_velocity_using_displacement(-screen_height + self.ball.height)
        physics_equation.set_variables(initial_velocity=initial_velocity, initial_distance=self.ball.height)










