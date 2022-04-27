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
    new_physics_equation = None
    # The physics equation that would be the 'normal' parabola of the ball- just makes increasing parabola height easier
    unaltered_physics_equation = None
    total_time = None

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
        self.velocity_increase = self.get_velocity_increase(4, 1, 0)
        self.unaltered_physics_equation = deepcopy(self.physics_equation)

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
            self.new_physics_equation = deepcopy(self.unaltered_physics_equation)

            if self.new_physics_equation is not None and self.unaltered_physics_equation != self.new_physics_equation:
                # Because the other increase that should have happened was not accounted for
                self.new_physics_equation.set_variables(initial_velocity=self.unaltered_physics_equation.initial_velocity-self.velocity_increase * 2)


            else:
                self.new_physics_equation.set_variables(initial_velocity=self.unaltered_physics_equation.initial_velocity-self.velocity_increase)

        if CollisionsFinder.is_collision(self.ball, self.player1):
            self.ball.x_coordinate = self.player1.right_edge
            self.data += f"""{self.s}unaltered_physics_equation:{self.unaltered_physics_equation}
{self.s}new_physics_equation:{self.new_physics_equation}
{self.s}current_physics_equation:{self.physics_equation}\n"""
            print("IS COLLISION STARTING AI LOGIC PLAYER1 !!!! !!!!\n\n")
            self.total_time = VelocityCalculator.time

        if CollisionsFinder.is_collision(self.ball, self.player2):
            self.ball.x_coordinate = self.player2.x_coordinate - self.ball.length

    def ball_movement(self):
        """ summary: does the horizontal and vertical movement of the ball and the logic that goes into
                     making the ball be affected by gravity

            params: None
            returns: None
        """

        if self.ball.bottom > screen_height and self.new_physics_equation is not None and self.unaltered_physics_equation != self.new_physics_equation:
            self.time = self.get_overshoot_time()
            print("HIT BOTTOM", self.total_time, self.get_overshoot_time())
            self.physics_equation, self.unaltered_physics_equation = deepcopy(self.new_physics_equation), deepcopy(self.new_physics_equation)
            self.ball.y_coordinate = screen_height - self.ball.height
            self.new_physics_equation = None

        elif self.ball.y_coordinate < 0 and self.time > 0:
            self.time = self.get_overshoot_time()

            # Not making it negative because get_velocity_using_displacement gets the seconds number, which is when it is falling
            # Making it already to the sign (+/-) it should be
            initial_velocity = self.physics_equation.get_velocity_using_displacement(-screen_height + self.ball.height)
            self.physics_equation.set_variables(initial_velocity=initial_velocity, initial_distance=0)
            self.ball.y_coordinate = 0

        elif self.ball.bottom > screen_height and self.time > 0:
            print("HIT BOTTOM", self.total_time, self.get_overshoot_time())
            self.time = self.get_overshoot_time()

            # If the ball has not hit the top of the screen from start -> end it's y coordinate has not changed
            displacement = screen_height - self.ball.height if self.physics_equation.get_vertex() < 0 else 0

            # Making it negative to make it go the opposite direction
            initial_velocity = -self.physics_equation.get_velocity_using_displacement(displacement)

            self.physics_equation.set_variables(initial_velocity=initial_velocity, initial_distance=screen_height-self.ball.height)
            self.unaltered_physics_equation = deepcopy(self.physics_equation)

            self.ball.y_coordinate = screen_height - self.ball.height

        # IMPORTANT: must be below the if statement(s) otherwise the ball's y_coordinate
        self.time += VelocityCalculator.time

        self.ball.y_coordinate = self.physics_equation.get_distance(self.time)
        print(f"Y {self.ball.y_coordinate} time {self.time} total time {self.total_time} pe {self.physics_equation}")

        x_change = VelocityCalculator.calc_distance(self.ball.forwards_velocity)
        self.ball.x_coordinate += x_change if self.ball.is_moving_right else -x_change

    def run(self):
        """ summary: runs all the code that is necessary for this pong type
            params: None
            returns: None
        """
        self.s = f"test_number{self.test_number}."

        # if self.ball.y_coordinate <= 0 or self.ball.bottom >= screen_height and self.time > 0 and self.get_overshoot_time() < 0:
        #     self.get_overshoot_time()

        self.ball_movement()
        self.ball_collisions()
        self.normal_pong.run_player_movement()
        if self.total_time is not None:
            self.total_time += VelocityCalculator.time

        if self.ball.right_edge >= self.player2.x_coordinate:
            self.data += f"{self.s}actual_y_coordinate:{self.ball.y_coordinate}\n"
            print("END TIME", self.total_time)
            self.test_number += 1

        if pygame.key.get_pressed()[pygame.K_SPACE] and not self.has_written:
            self.has_written = True
            self.data += f"number_of_tests:{self.test_number}"
            file_writer = open("data.txt", "w+")
            file_writer.write(self.data)

    def reset(self):
        """ summary: resets everything necessary after each time someone scores
            params: None
            returns: None
        """
        self.time = 0
        self.ball.y_coordinate = screen_height - self.ball.height
        self.physics_equation.set_all_variables(250, 1, 250, screen_height - self.ball.height)

    def get_overshoot_time(self):
        """returns: double; the amount of time that has passed between when the ball should have hit the floor/ceiling"""

        # Meaning the ball has hit the top of the screen
        if self.physics_equation.get_vertex() <= 0 and self.ball.y_coordinate < 0:
            return_value = self.time - self.physics_equation.get_times_to_point(0)[0]

        # Meaning the ball is coming from hitting the top of the screen
        elif self.physics_equation.initial_velocity > 0 and self.ball.bottom > screen_height:
            return_value = self.time - self.physics_equation.get_times_to_point(screen_height - self.ball.height)[1]

        # Meaning the ball is not coming from the top of the screen: like "normal"
        else:
            return_value = self.time - self.physics_equation.get_full_cycle_time()

        return return_value

    def get_ball_path_from(self, ball_y_coordinate, ball_x_coordinate, end_x_coordinate, ball_is_moving_down):
        """ summary: finds the ball's y_coordinate and bottom at the next time it hits the x_coordinate
            IMPORTANT: this function should be called when the ball is going the desired horizontal direction

            params:
                x_coordinate: int; the number that is used to evaluate the ball's path

            returns: Path; the path of the ball from its current x_coordinate to the end x_coordinate
        """
        self.data += f"""{self.s}ball_y_coordinate:{ball_y_coordinate}
{self.s}ball_x_coordinate:{ball_x_coordinate}
{self.s}time:{self.time}
{self.s}end_x_coordinate:{end_x_coordinate}
{self.s}ball_forward_velocity:{self.ball.forwards_velocity}\n"""
        # return super().get_ball_path_from(ball_y_coordinate, ball_x_coordinate, end_x_coordinate, ball_is_moving_down)
        return_value = None

        time_to_travel_distance = abs(end_x_coordinate - ball_x_coordinate) / self.ball.forwards_velocity

        if self.physics_equation.get_vertex() > 0:
            return_value = self.get_normal_end_y_coordinate(time_to_travel_distance)

        else:
            return_value = self.get_abnormal_end_y_coordinate(time_to_travel_distance)

        return return_value
    def get_time_to_vertex(self):
        """returns: double; the time it will take for the ball to reach its vertex"""

        vertex = 0 if self.physics_equation.get_vertex() < 0 else self.physics_equation.get_vertex()

        # The first point is needed because that will be the vertex; there is only one point also
        return self.physics_equation.get_times_to_point(vertex)[0]

    def get_time_to_bottom(self):
        """returns: double; the time it will take for the ball to go from the vertex to the bottom"""

        return_value = None

        if self.physics_equation.get_vertex() < self.ball.height:
            return_value = self.get_downwards_physics_equation().get_times_to_point(screen_height - self.ball.height)[1]

        else:
            return_value = self.physics_equation.get_time_to_vertex() # Time to go to vertex is same as going from vertex -> bottom

        return return_value

    # def get_data(self, physics_equation, ball_y_coordinate, current_time):
    #     """returns: Object[]; [ball_y_coordinate, current_time] from this cycle"""
    #
    #     if ball_y_coordinate <= 0:
    #         current_time = self.get_overshoot_time()
    #
    #         # Not making it negative because get_velocity_using_displacement gets the seconds number, which is when it is falling
    #         # Making it already to the sign (+/-) it should be
    #         initial_velocity = self.physics_equation.get_velocity_using_displacement(-screen_height + self.ball.height)
    #         physics_equation.set_variables(initial_velocity=initial_velocity, initial_distance=self.ball.height)
    #         self.ball.y_coordinate = 0
    #
    #     elif self.ball.bottom >= screen_height:
    #         current_time = self.get_overshoot_time()
    #
    #         time_to_vertex = physics_equation.get_time_to_vertex()
    #         displacement = screen_height - self.ball.height if physics_equation.get_distance(time_to_vertex) < 0 else 0
    #
    #         # Making it negative to make it go the opposite direction
    #         initial_velocity = -physics_equation.get_velocity_using_displacement(displacement)
    #         physics_equation.set_variables(initial_velocity=initial_velocity, initial_distance=screen_height-self.ball.height)
    #
    #         self.ball.y_coordinate = screen_height - self.ball.height
    #
    #     return [ball_y_coordinate, current_time]

    def get_downwards_physics_equation(self):
        """returns: PhysicsEquation; the physics equation will the ball has just hit the top"""

        physics_equation = deepcopy(self.physics_equation)
        initial_velocity = physics_equation.get_velocity_using_displacement(-screen_height + self.ball.height)
        physics_equation.set_variables(initial_velocity=initial_velocity, initial_distance=self.ball.height)
        return physics_equation

    def get_time_to_next_point(self):
        """returns: double; the time to the next major point (the vertex or bottom)"""

        time_at_next_point = None

        if self.get_next_point() == screen_height - self.ball.height:
            # Want the second one from the descent
            time_at_next_point = self.physics_equation.get_times_to_point(self.get_next_point())[1]

        else:
            time_at_next_point = self.physics_equation.get_times_to_point(self.get_next_point())[0]

        return time_at_next_point - self.time

    def get_next_point(self):
        """returns: double; the next major point (the vertex or bottom)"""

        return_value = None
        if self.time < self.physics_equation.get_time_to_vertex():
            ball_vertex = self.physics_equation.get_vertex()
            return_value = ball_vertex if ball_vertex > 0 else 0

        else:
            return_value = screen_height - self.ball.height

        return return_value

    def get_normal_end_y_coordinate(self, time_to_travel_distance):
        """returns: double; the normal end y coordinate of the ball- normal being not bouncing off the ceiling"""

        return_value = None

        time_to_bottom = self.physics_equation.get_full_cycle_time() - self.time

        if time_to_bottom >= time_to_travel_distance:
            return_value = self.physics_equation.get_distance(time_to_travel_distance + self.time)

        else:
            time_to_travel_distance -= time_to_bottom

        # So the first if statement has not been triggered allowing to move on to new physics equation
        if return_value is None:
            time_to_travel_distance %= self.new_physics_equation.get_full_cycle_time()
            return_value = self.new_physics_equation.get_distance(time_to_travel_distance)

        return return_value

    def get_abnormal_end_y_coordinate(self, time_to_travel_distance):
        """returns: double; the end y coordinate when the ball touches the ceiling"""

        return_value = None

        # time_from_top_to_bottom =















