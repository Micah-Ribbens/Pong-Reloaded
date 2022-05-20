from base_pong.equations import Point
from base_pong.events import Event
from base_pong.path import VelocityPath
from base_pong.players import AI
from base_pong.utility_classes import HistoryKeeper
from base_pong.engines import CollisionsFinder
from base_pong.ball import Ball
from base_pong.velocity_calculator import VelocityCalculator
from pong_types.pong_type import PongType
from pong_types.normal_pong import NormalPong
from base_pong.score_keeper import ScoreKeeper
from base_pong.colors import red, white
from copy import deepcopy


class AIData:
    """A utility class for storing data making the AI for Split Pong easier"""

    time = 0
    y_coordinate = 0

    def __init__(self, time, y_coordinate):
        """Initializes the object"""

        self.time, self.y_coordinate = time, y_coordinate

    def __str__(self):
        return f"time {self.time} y coordinate {self.y_coordinate}"

class SplitPong(PongType):
    """Pong where the balls size increases until it doubles in size and after that it splits"""
    balls = []
    base_ball_length = 0
    normal_pong = None
    total_time = None

    ai_data = {} # ball to ball data

    def __init__(self, player1, player2, ball):
        """ summary: Initializes with the PongType with the needed objects to run its methods

            params:
                player1: Paddle; the player on the leftmost side on the screen
                player2: Paddle; the player on the rightmost side on the screen
                ball: Ball; the ball that the players hit

            returns: None
        """

        super().__init__(player1, player2, ball)
        self.normal_pong = NormalPong(player1, player2, ball)
        
        self.balls.append(ball)
        ball.color = red

        if type(player2) == AI:
            # Don't want it to do anything; I want the AI code to be executed in a very specific spot
            player2.set_action(lambda: [].__contains__(0))

    def increase_ball_size(self, ball):
        """ summary: increases the ball's size

            params:
                ball: Ball; the ball which size should increase

            returns: None
        """

        # The ball's right edge will change from the length increase making a collision that didn't happen becuase the
        # Ball will move into player2; this prevents that
        if ball.right_edge == self.player2.x_coordinate:
            ball.x_coordinate -= (self.base_ball_length * .25)

        ball.length += (self.base_ball_length * .25)
        ball.height += (self.base_ball_length * .25)


    def ball_is_ready_to_split(self, ball):
        """ summary: finds out if the ball's size is double the size of its base length

            params:
                ball: Ball; the ball that this function is testing if it is ready to split

            returns: boolean; if the ball is ready to split
        """

        return ball.length >= self.base_ball_length * 2

    def split(self, ball: Ball, new_balls, ball_has_collided_with_player1):
        """ summary: splits the ball

            params:
                ball: Ball; the ball that should be split
                new_balls: List of Ball; the new_balls that were created from splitting this cycle
                ball_has_collided_with_player1: boolean; the ball has collided with the first player

            returns: None
        """

        ball.length = self.base_ball_length
        ball.height = self.base_ball_length
        new_ball: Ball = deepcopy(ball)
        new_ball.color = white
        new_ball.is_moving_down = not ball.is_moving_down
        new_ball.forwards_velocity *= 1.2
        distance_change = new_ball.forwards_velocity * .1

        new_ball.is_moving_right = True if ball_has_collided_with_player1 else False

        new_ball.x_coordinate += distance_change if ball_has_collided_with_player1 else -distance_change
        new_balls.append(new_ball)

    def ball_collisions(self):
        """ summary: does all the collisions with the paddles for the ball
            params: None
            returns: None
        """

        new_balls = []
        for ball in self.balls:
            ball_has_collided_with_paddle1 = CollisionsFinder.is_collision(ball, self.player1)

            ball.render()
            self.normal_pong.ball_screen_boundary_collisions(ball)
            ball_has_collided = self.ball_has_collided(ball)

            # if ball_has_collided:
            #     ball.is_moving_right = True if ball_has_collided_with_paddle1 else False
            #     ball.x_coordinate = self.player1.right_edge if ball_has_collided_with_paddle1 else self.player2.x_coordinate - ball.length

            self.normal_pong._ball_collisions(ball, self.player1, self.player2)

            # if ball_has_collided and ball.right_edge == 776.0000000001:
            #     self.increase_ball_size(ball)
            # This has to be done later because the ball changing size messes up the collisions
            if ball_has_collided:
                self.increase_ball_size(ball)

            print("BRC1", ball.right_edge, ball.x_coordinate)

            if self.ball_is_ready_to_split(ball):
                self.split(ball, new_balls, ball_has_collided_with_paddle1)

            print("BRC2", ball.right_edge, ball.x_coordinate)

        for new_ball in new_balls:
            self.balls.append(new_ball)

    def ball_has_collided(self, ball):
        """returns: boolean; if the ball has collided with a player"""

        # The ball has to be going to opposite direction of the player to have collided with the weird splitting mechanics
        return ((CollisionsFinder.is_collision(ball, self.player1) and not ball.is_moving_right)
                or (CollisionsFinder.is_collision(ball, self.player2) and ball.is_moving_right))

    def run(self):
        self.run_ai()
        self.add_needed_objects()

        for x in range(len(self.balls)):
            ball = self.balls[x]
            # ball.name = f"ball #{x + 1}"
            self.normal_pong._ball_movement(ball)

        self.normal_pong.run_player_movement()

        self.ball_collisions()

        if self.total_time is not None:
            self.total_time += VelocityCalculator.time

        for ball in self.balls:
            print("BR", ball.right_edge, ball.x_coordinate)

    def add_needed_objects(self):
        """Adds all the objects to the History Keeper that need to be there"""

        super().add_needed_objects()

        for ball in self.balls:
            ball.name = id(ball)
            HistoryKeeper.add(ball, ball.name, True)

    def reset(self):
        """ summary: resets everything necessary after each time someone scores
            params: None
            returns: None
        """

        # Meaning the base_pong self.ball length has not been assigned yet
        if self.base_ball_length == 0:
            self.base_ball_length = self.ball.length

        self.balls = [self.ball]
        self.ball.length = self.base_ball_length
        self.ball.height = self.base_ball_length
        self.ball.forwards_velocity = self.ball.base_forwards_velocity
        self.ai_data = {}

    def draw_game_objects(self):
        """ summary: draws all the game objects (paddles and ball) onto the screen
            params: None
            returns: None
        """

        self.player1.render()
        self.player2.render()
        for ball in self.balls:
            ball.render()
    
    def player1_has_scored(self):
        """ summary: finds out if a ball has gone beyond the screens left boundary
            params: None
            returns: boolean; if player2 has scored
        """
        return self.player_has_scored(False)
    
    def player2_has_scored(self):
        """ summary: finds out if a ball has gone beyond the screens right boundary
            params: None
            returns: boolean; if player2 has scored
        """

        return self.player_has_scored(True)
    
    def player_has_scored(self, player_is_leftside):
        """ summary: iterates over every ball in balls and calls ScoreKeeper.player_has_scored()

            params:
                player_is_leftside: boolean; the player is on the left side of the screen

            returns: None
        """

        has_scored = False

        for ball in self.balls:
            if ScoreKeeper.player_has_scored(ball, player_is_leftside):
                CollisionsFinder.is_collision(ball, self.player1 if not player_is_leftside else self.player2)
                has_scored = True

        return has_scored

    def add_ball_to_ai_path(self, ball):
        """Adds the ball to the ai's path, so it will hit it"""

        ball_path, unused, times = self._get_ball_path_data(ball.y_coordinate, ball.x_coordinate, self.player2.x_coordinate - ball.length, ball.is_moving_down, ball.forwards_velocity)

        time_to_ai = times[len(times) - 1]
        end_y_coordinate = ball_path.get_end_points()[0].y_coordinate

        self.ai_data[ball] = AIData(time_to_ai, end_y_coordinate)

        # Sorting the keys of the ai data so the it goes least to greatest time
        sorted_ai_data_keys = sorted(self.ai_data.keys(), key=lambda item: self.ai_data.get(item).time)

        self.player2.path = VelocityPath(Point(self.player2.x_coordinate, self.player2.y_coordinate), [], self.player2.velocity)

        current_time = 0

        for key in sorted_ai_data_keys:
            data = self.ai_data.get(key)

            self.player2.move_towards_ball(data.y_coordinate, data.time - current_time, False)
            current_time = data.time

    def run_ai(self):
        """Runs the code that makes the ai to work"""

        for ball in self.balls:
            # Meaning the ball has not been added to the ai path and it should be
            if ball.is_moving_right and not self.ai_data.__contains__(ball):
                self.add_ball_to_ai_path(ball)

                if self.total_time is None:
                    self.total_time = 0

            if CollisionsFinder.is_collision(ball, self.player2) and self.ai_data.__contains__(ball):
                self.ai_data.pop(ball)

        for data in self.ai_data.values():
            data.time -= VelocityCalculator.time
        self.player2.run_hitting_balls_logic()





