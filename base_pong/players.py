from random import randint

import pygame
from base_pong.drawable_objects import GameObject
from base_pong.engines import CollisionsFinder
from base_pong.path import Path, VelocityPath
from base_pong.score_keeper import ScoreKeeper
from base_pong.utility_classes import Fraction, HistoryKeeper
from base_pong.velocity_calculator import VelocityCalculator
from base_pong.utility_functions import change_attributes
from base_pong.important_variables import *
from base_pong.colors import *
from pong_types.pong_type import PongType


class Paddle(GameObject):
    """The paddle that dimensions can be changed and drawn"""

    can_move_up = True
    can_move_down = True
    velocity = VelocityCalculator.give_velocity(screen_height, 1500)
    power = 10.5
    attributes = ["x_coordinate", "y_coordinate"]

    def __init__(self):
        """ summary: initializes the paddle with predetermined values
            params: None
            returns: None
        """

        self.y_coordinate = 0
        self.x_coordinate = 0
        self.length = VelocityCalculator.give_measurement(screen_length, 3)
        self.height = VelocityCalculator.give_measurement(screen_height, 30)
        self.color = white
        self.outline_color = red

    def get_top_tip_of_paddle(self):
        return GameObject(self.x_coordinate, self.y_coordinate, self.height * .1, self.length)

    def get_bottom_tip_of_paddle(self):
        tip_height = self.height * .1
        return GameObject(self.x_coordinate, self.bottom - tip_height, tip_height, self.length)

    def render(self):
        paddle_image = pygame.transform.scale(pygame.image.load("images/paddle.png"), (int(self.length), int(self.height)))
        game_window.get_window().blit(paddle_image, (self.x_coordinate, self.y_coordinate))


class Player(Paddle):
    """Extends Paddle and provides movement options and a way to change the classes properties"""

    up_key = pygame.K_UP
    down_key = pygame.K_DOWN

    def run(self):
        """ summary: moves the paddle up and down if those keys were hit
            params: None
            returns: None
        """

        controls = pygame.key.get_pressed()

        if controls[self.up_key] and self.can_move_up:
            self.y_coordinate -= VelocityCalculator.calc_distance(
                self.velocity)

        if controls[self.down_key] and self.can_move_down:
            self.y_coordinate += VelocityCalculator.calc_distance(
                self.velocity)


class AI(Paddle):
    """A player that isn't an actual person- it will be used for a single player option"""

    difficulty_level = 0
    is_going_to_hit_ball = True
    ball = None
    number_of_hits = 0
    pong_type: PongType = None

    # The function that it should run everytime run is called
    action = None

    y_coordinate_should_be_at = 0  # The y_coordinate the computer opponent should move to
    is_moving_down = False
    is_moving = False
    get_path_was_called = False
    path: VelocityPath = None
    path_is_leftwards = False
    forwards_velocity = VelocityCalculator.give_velocity(400, screen_length)

    def __init__(self, difficulty_level, ball):
        """ summary: initializes the object

            params:
                difficulty_level: int; the level of difficulty in the range 1-10
                ball: Ball; the ball that the game is played with

            returns: None
        """
        super().__init__()

        self.difficulty_level = difficulty_level
        self.ball = ball
        self.action = self.default_run

    def set_pong_type(self, pong_type):
        self.pong_type = pong_type

    def set_action(self, action):
        """ summary: sets the function that should be called every cycle for the computer opponent's movement

            params:
                action: function; the function that should be called every cycle

            returns: None
        """

        self.action = action

    def should_move_towards_ball(self, ball):
        """ summary: finds out if the top tip of the paddle or bottom tip of paddle would be hit if the paddle doesn't move

            params:
                ball: Ball; the ball that this function uses to decide if the computer opponent should move towards it

            returns: boolean; whether the paddle should move towards the ball
        """

        # Prevents oscillation from trying to move towards the ball, but then overshooting it in an unending cycle
        # If the tips of the paddle will be hit the paddle is in a "good enough" position
        return (CollisionsFinder.is_height_collision(self.get_top_tip_of_paddle(), ball)
                or CollisionsFinder.is_height_collision(self.get_bottom_tip_of_paddle(), ball))

    def move_towards_ball(self, ball_y_coordinate, ball_bottom):
        """ summary: changes the property that tells the computer opponent where to move so it hits the ball

            params:
                ball: Ball; the ball the computer opponent should be moved towards

            returns: None
        """

        buffer = VelocityCalculator.give_measurement(screen_height, 5)
        # Makes it so it will move away from the ball if it isn't going to hit the ball
        if ball_y_coordinate >= screen_height - self.height - buffer:
            self.y_coordinate_should_be_at = ball_y_coordinate - self.height + buffer

        else:
            self.y_coordinate_should_be_at = ball_y_coordinate

        self.is_moving_down = self.bottom < self.y_coordinate_should_be_at

    def move_away_from_ball(self, ball_y_coordinate, ball_bottom):
        """ summary: changes the property that tells the computer opponent where to move so it misses the ball

            params:
                ball: Ball; the ball the computer oponent should be moved away from

            returns: None
        """
        buffer = VelocityCalculator.give_measurement(screen_height, 5)
        # Makes it so it will move away from the ball if it isn't going to hit the ball
        if ball_bottom >= screen_height - self.height:
            self.y_coordinate_should_be_at = ball_y_coordinate - self.height - buffer

        else:
            self.y_coordinate_should_be_at = ball_bottom + buffer

        self.is_moving_down = self.y_coordinate < self.y_coordinate_should_be_at

    def default_run(self):
        """ summary: runs the logic for figuring out if the player should hit the ball and the players movement; default code if action isn't changed
            params: None
            returns: None
        """
        prev_ball = HistoryKeeper.get_last(self.ball.name)
        prev_ball_is_moving_left = False if prev_ball is None else not prev_ball.is_moving_right
        should_get_ball_coordinates = prev_ball_is_moving_left and self.ball.is_moving_right and not self.get_path_was_called

        if self.is_going_to_hit_ball and should_get_ball_coordinates:
            ball_path = self.pong_type.get_path(self.x_coordinate - self.ball.length)
            ball_y_coordinate, ball_bottom = self.get_ball_end_coordinates(ball_path)
            self.move_towards_ball(ball_y_coordinate, ball_bottom)
            self.get_path_was_called = True

        elif not self.is_going_to_hit_ball and should_get_ball_coordinates:
            ball_path = self.pong_type.get_path(self.x_coordinate - self.ball.length)
            ball_y_coordinate, ball_bottom = self.get_ball_end_coordinates(ball_path)
            self.move_away_from_ball(ball_y_coordinate, ball_bottom)
            self.get_path_was_called = True

        self.run_hitting_balls_logic()

    def get_ball_end_coordinates(self, ball_path: Path):
        """ summary: gets the balls end coordinates from the data inside ball_path

            params:
                ball_path: Path; the ball's path

            returns: List of Double; [ball_y_coordinate, ball_bottom]
        """

        ball_end_points = ball_path.get_end_points()
        return [ball_end_points[0].y_coordinate, ball_end_points[1].y_coordinate]

    def run_hitting_balls_logic(self):
        """ summary: runs the logic for figuring out if the computer opponent should hit the next ball
            params: None
            returns: None
        """
        hit_ball_this_cycle = CollisionsFinder.is_collision(self.ball, self)

        time_to_get_to_desired_y_coordinate = abs(self.y_coordinate - self.y_coordinate_should_be_at) / self.velocity

        ball_distance_from_paddle = self.x_coordinate - self.ball.right_edge
        time_for_ball_to_come_to_paddle = ball_distance_from_paddle / self.ball.forwards_velocity

        buffer = .4
        # The buffer is to prevent the paddle not having enough time to reach the ball
        if time_to_get_to_desired_y_coordinate >= time_for_ball_to_come_to_paddle - buffer:
            self.is_moving = True

        if hit_ball_this_cycle:
            self.number_of_hits += 1
            self.get_path_was_called = False

        if self.is_moving_down and self.y_coordinate >= self.y_coordinate_should_be_at and self.is_moving:
            self.is_moving = False

        elif self.y_coordinate <= self.y_coordinate_should_be_at and not self.is_moving_down and self.is_moving:
            self.is_moving = False

        if self.is_moving:
            distance = VelocityCalculator.calc_distance(self.velocity)
            displacement = distance if self.is_moving_down else -distance
            self.y_coordinate += displacement

        # The computer should hit the ball so many times before it misses
        if hit_ball_this_cycle and self.number_of_hits > self.difficulty_level // 2:
            self.is_going_to_hit_ball = self.is_random_chance(
                Fraction(self.difficulty_level, self.difficulty_level + 1))

    def run(self):
        self.action()

    def is_random_chance(self, probability: Fraction):
        """ summary: uses the probability for the random chance (for instance if the probability is 7/10 then 7 out of 10
            times it will return True and the other 3 times it will return False)

            params:
                probability: Fraction; the probability this function will return True

            returns: boolean; if the random number between 1-probability.denominator is >= probability.numerator

        """

        return randint(probability.numerator, probability.denominator) <= probability.numerator

    def reset(self):
        """ summary: resets all the variables once a player scores
            params: None
            returns: None
        """

        self.number_of_hits = 0
        self.is_going_to_hit_ball = True
        self.get_path_was_called = False
        self.is_moving = False

    def render(self):
        paddle_image = pygame.transform.scale(pygame.image.load("images/paddle.png"), (int(self.length), int(self.height)))
        game_window.get_window().blit(paddle_image, (self.x_coordinate, self.y_coordinate))

    def add_path(self, path):
        """Makes the AI follow the specified path until it hits the path's end"""

        self.path = path
        self.path_is_leftwards = path.get_end_points()[0].x_coordinate < self.x_coordinate

    def remove_path(self):
        """Makes the AI stop following a path"""

        self.path = None

