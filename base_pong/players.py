from random import randint

import pygame
from base_pong.drawable_objects import GameObject
from base_pong.engines import CollisionsFinder
from base_pong.equations import Point
from base_pong.events import TimedEvent
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
    base_velocity = VelocityCalculator.give_velocity(screen_height, 1500)
    velocity = base_velocity
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
        self.height = VelocityCalculator.give_measurement(screen_height, 35)
        self.color = white
        self.outline_color = red

    def get_top_tip_of_paddle(self):
        return GameObject(self.x_coordinate, self.y_coordinate, self.height * .1, self.length)

    def get_bottom_tip_of_paddle(self):
        tip_height = self.height * .1
        return GameObject(self.x_coordinate, self.bottom - tip_height, tip_height, self.length)

    # def render(self):
    #     paddle_image = pygame.transform.scale(pygame.image.load("images/paddle.png"), (int(self.length), int(self.height)))
    #     game_window.get_window().blit(paddle_image, (self.x_coordinate, self.y_coordinate))


class Player(Paddle):
    """Extends Paddle and provides movement options and a way to change the classes properties"""

    up_key = pygame.K_UP
    down_key = pygame.K_DOWN

    def movement(self):
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
    path: VelocityPath = None
    path_is_leftwards = False
    forwards_velocity = VelocityCalculator.give_velocity(400, screen_length)

    ai_path = None

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

    def move_towards_ball(self, ball_y_coordinate, ball_time_to_ai):
        """ summary: changes the property that tells the computer opponent where to move so it hits the ball

            params:
                ball: Ball; the ball the computer opponent should be moved towards

            returns: None
        """

        # Setting the player's y_midpoint to the ball's y_coordinate
        new_y_coordinate = (ball_y_coordinate - self.height / 2)

        if new_y_coordinate >= screen_height:
            new_y_coordinate = screen_height - self.height

        elif new_y_coordinate <= 0:
            new_y_coordinate = 0

        self.change_player_path(new_y_coordinate, ball_time_to_ai)

    def move_away_from_ball(self, ball_y_coordinate, ball_time_to_ai):
        """ summary: changes the property that tells the computer opponent where to move so it misses the ball

            params:
                ball: Ball; the ball the computer oponent should be moved away from

            returns: None
        """

        new_y_coordinate = None

        if ball_y_coordinate > screen_height / 2:
            new_y_coordinate = 0

        else:
            new_y_coordinate = screen_height - self.height

        self.change_player_path(new_y_coordinate, ball_time_to_ai)

    def change_player_path(self, new_y_coordinate, ball_time_to_ai):
        """Changes the player's path so it will go to the new_y_coordinate within the right amount of time"""

        distance_to_new_y_coordinate = abs(new_y_coordinate - self.y_coordinate)

        time_to_reach_new_y_coordinate = distance_to_new_y_coordinate / self.velocity

        # The player should beat the ball to the spot by a little bit
        time_buffer = .5

        self.path = VelocityPath(Point(self.x_coordinate, self.y_coordinate), [], self.velocity)

        self.path.add_time_point(Point(self.x_coordinate, self.y_coordinate),
                                 ball_time_to_ai - time_to_reach_new_y_coordinate - time_buffer)

        self.path.add_point(Point(self.x_coordinate, new_y_coordinate))

    def default_run(self):
        """summary: runs the logic for figuring out if the player should hit the ball and the players movement;
            default code if action isn't changed"""

        prev_ball = HistoryKeeper.get_last(self.ball.name)
        prev_ball_is_moving_left = False if prev_ball is None else not prev_ball.is_moving_right

        ball_has_hit_player1 = prev_ball_is_moving_left and self.ball.is_moving_right

        # I want to move the ai if the ball has hit off of another player or it is moving to player2 from respawning
        should_get_ball_coordinates = ball_has_hit_player1 or (self.path is None and self.ball.is_moving_right)

        if self.is_going_to_hit_ball and should_get_ball_coordinates:
            ball_y_coordinate, ball_time_to_ai = self.pong_type.get_ai_data(self.x_coordinate)
            self.move_towards_ball(ball_y_coordinate, ball_time_to_ai)
            # print("HIT BALL", self.number_of_hits)

        elif not self.is_going_to_hit_ball and should_get_ball_coordinates:
            ball_y_coordinate, ball_time_to_ai = self.pong_type.get_ai_data(self.x_coordinate)
            self.move_away_from_ball(ball_y_coordinate, ball_time_to_ai)
            # print("MISS BALL", self.number_of_hits)

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
        """Runs the logic for figuring out if the computer opponent should hit the next ball"""
        hit_ball_this_cycle = CollisionsFinder.is_collision(self.ball, self)

        if self.path is not None:
            self.x_coordinate, self.y_coordinate = self.path.get_coordinates()

        if hit_ball_this_cycle:
            self.number_of_hits += 1

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
        """Resets all the variables once a player scores"""

        self.number_of_hits = 0
        self.is_going_to_hit_ball = True
        self.is_moving = False
        self.path = None

    def render(self):
        """renders the ai"""

        paddle_image = pygame.transform.scale(pygame.image.load("images/paddle.png"), (int(self.length), int(self.height)))
        game_window.get_window().blit(paddle_image, (self.x_coordinate, self.y_coordinate))

        if self.path is not None:
            self.path.render()

    def add_path(self, path):
        """Makes the AI follow the specified path until it hits the path's end"""

        self.path = path
        self.path_is_leftwards = path.get_end_points()[0].x_coordinate < self.x_coordinate

    def remove_path(self):
        """Makes the AI stop following a path"""

        self.path = None

