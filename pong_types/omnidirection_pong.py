import pygame.key

from base_pong.engines import CollisionsFinder
from base_pong.equations import Point, LineSegment
from base_pong.events import Event
from base_pong.important_variables import screen_height, screen_length
from base_pong.path import VelocityPath, Path, PathLine
from base_pong.players import AI
from base_pong.utility_classes import HistoryKeeper
from base_pong.velocity_calculator import VelocityCalculator
from pong_types.normal_pong import NormalPong
from pong_types.pong_type import PongType
from base_pong.utility_functions import key_is_hit

# TODO fix code so you don't have to assume player2 is the ai
class OmnidirectionalPong(NormalPong):
    """Pong where the player can move 4 directions"""''
    # States for the AI
    class States:
        GOING_TOWARDS_GOAL = 1
        GOING_TOWARDS_BALL = 2
        INIT = 3
        GOING_TOWARDS_CENTER = 4
        WAITING = 5

    current_state = States.GOING_TOWARDS_GOAL

    ball_sandwiched_event = Event()

    # Stores the value of the ball at the start of the cycle; the ball gets modified in the code making this necesary
    last_ball = None
    debug = False

    player_who_hit_ball_key = "player who hit ball"
    player_path = None

    def __init__(self, player1, player2, ball):
        """ summary: Initializes the PongType with the needed objects to run its methods

            params:
                player1: Paddle; the player on the leftmost side on the screen
                player2: Paddle; the player on the rightmost side on the screen
                ball: Ball; the ball that the players hit

            returns: None
        """

        super().__init__(player1, player2, ball)
        self.last_ball = self.ball
        self.player1.can_move_left, self.player2.can_move_left = False, False
        self.player1.can_move_right, self.player2.can_move_right = False, False

        self.player2.action = self.run_ai
        self.player2: AI = self.player2
        distance_to_goal = self.player2.x_coordinate
        time_to_goal = distance_to_goal / self.player2.velocity

        ball_path: Path = self.get_ball_y_coordinates(time_to_goal)

        self.player_path = VelocityPath(Point(self.player2.x_coordinate, self.player2.y_coordinate), [], self.player2.velocity)

        for time in self.get_important_times(ball_path):
            x_coordinate = self.player2.x_coordinate - time * self.player2.velocity

            y_coordinate = ball_path.get_y_coordinate(time)

            if y_coordinate >= screen_height - self.player2.height:
                y_coordinate = screen_height - self.player2.height

            self.player_path.add_time_point(Point(x_coordinate, y_coordinate), time)

    def run(self):
        """ summary: runs all the code that is necessary for this pong type
            params: None
            returns: None
        """
        self.last_ball = self.ball
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            self.ball.can_move = True

        self.ball_collisions(self.player1)
        self.ball_collisions(self.player2)
        self.paddle_collisions()
        self.horizontal_player_movements(self.player1, pygame.K_a, pygame.K_d)
        self.horizontal_player_movements(self.player2, pygame.K_LEFT, pygame.K_RIGHT)
        self.ball_sandwiched_event.run(self.ball_is_sandwiched())
        self.run_ball_sandwiching()

        if self.ball.can_move:
            self.ball_movement()
        self.run_player_movement()
        self.run_player_boundaries(self.player2)
        self.run_player_boundaries(self.player1)

    def paddle_collisions(self):
        """ summary: runs all the collisions between paddles
            params: None
            returns: None
        """

        if CollisionsFinder.is_right_collision(self.player1, self.player2) or CollisionsFinder.is_left_collision(self.player1, self.player2):
            leftmost_player = self.get_leftmost_player()
            rightmost_player = self.get_rightmost_player()
            leftmost_player.can_move_right = False
            rightmost_player.can_move_left = False
            rightmost_player.x_coordinate = leftmost_player.right_edge
            leftmost_player.x_coordinate = rightmost_player.x_coordinate - rightmost_player.length

        self.run_player_boundaries(self.player1)
        self.run_player_boundaries(self.player2)

    def run_ball_sandwiching(self):
        """ summary: runs all the logic necessary for the ball to stop when it's "sandwiched" between two players
            params: None
            returns: None
        """

        if self.ball_is_sandwiched():
            self.ball.can_move = False
            self.ball.x_coordinate = self.get_leftmost_player().right_edge

        if self.ball_is_sandwiched() and not self.ball_sandwiched_event.happened_last_cycle():
            rightmost_player = self.get_rightmost_player()
            leftmost_player = self.get_leftmost_player()

            rightmost_player.x_coordinate = self.ball.right_edge
            leftmost_player.x_coordinate = self.ball.x_coordinate - leftmost_player.length

            rightmost_player.can_move_left = False
            leftmost_player.can_move_right = False

        if not self.ball_is_sandwiched() and not self.ball.can_move:
            self.debug = True
            self.ball_is_sandwiched()
            self.ball.can_move = True
            self.debug = False

    def ball_collisions(self, player):
        """ summary: runs the collisions between the ball and that player

            params:
                player: Player; the player that will have its collisions between it and the ball run

            returns: None
        """
        if CollisionsFinder.is_collision(self.ball, player):
            HistoryKeeper.add(player, self.player_who_hit_ball_key, True)
            velocity_reduction = .8
            player.velocity = player.base_velocity * velocity_reduction

        else:
            player.velocity = player.base_velocity

        if CollisionsFinder.is_left_collision(self.ball, player) and not self.ball_is_sandwiched():
            self.ball.x_coordinate = player.right_edge
            self.ball.is_moving_right = True
            HistoryKeeper.add(player, self.player_who_hit_ball_key, True)

        if CollisionsFinder.is_right_collision(self.ball, player) and not self.ball_is_sandwiched():
            self.ball.x_coordinate = player.x_coordinate - self.ball.length
            self.ball.is_moving_right = False
            HistoryKeeper.add(player, self.player_who_hit_ball_key, True)

        if self.ball.bottom >= screen_height:
            self.ball.is_moving_down = False

        if self.ball.y_coordinate <= 0:
            self.ball.is_moving_down = True

    def horizontal_player_movements(self, player, left_key, right_key):
        controls = pygame.key.get_pressed()

        if player.can_move_left and controls[left_key]:
            player.x_coordinate -= VelocityCalculator.calc_distance(player.velocity)

        if player.can_move_right and controls[right_key] and not controls[left_key]:
            player.x_coordinate += VelocityCalculator.calc_distance(player.velocity)


    def run_player_boundaries(self, player):
        """ summary: sets the players can move left and right based on if the player is within the screens bounds

            params:
                player: Player; the player that the boundaries will be checked for

            returns: None
        """
        is_collision = CollisionsFinder.is_collision(self.player1, self.player2) or self.ball_is_sandwiched()

        if player.right_edge >= screen_length:
            player.x_coordinate = screen_length - player.length
            player.can_move_right = False

        elif not is_collision:
            player.can_move_right = True

        if player.x_coordinate <= 0:
            player.x_coordinate = 0
            player.can_move_left = False

        elif not is_collision:
            player.can_move_left = True

        bottom_player = CollisionsFinder.get_bottommost_object(self.player1, self.player2)
        top_player = CollisionsFinder.get_topmost_object(self.player1, self.player2)

        if CollisionsFinder.is_bottom_collision(self.player1, self.player2) or CollisionsFinder.is_top_collision(self.player1, self.player2):
            bottom_player.can_move_up = False
            top_player.can_move_down = False

            bottom_player.y_coordinate = top_player.bottom
            top_player.y_coordinate = bottom_player.y_coordinate - top_player.height

        elif player.y_coordinate <= 0:
            player.can_move_up = False
            player.y_coordinate = 0

        elif player.bottom >= screen_height:
            player.can_move_down = False
            player.y_coordinate = screen_height - player.height

        elif not CollisionsFinder.is_collision(self.player1, self.player2):
            self.player1.can_move_up, self.player2.can_move_up = True, True
            self.player1.can_move_down, self.player2.can_move_down = True, True

    def ball_is_sandwiched(self):
        """ summary: finds out if the ball is a within a certain distance between the two players and is within their height (sandwiched)
            params: None
            returns: boolean; if the ball is sandwiched
        """
        leftmost_player = self.get_leftmost_player()
        rightmost_player = self.get_rightmost_player()

        distance_between_players = rightmost_player.x_coordinate - leftmost_player.right_edge

        distance_needed = self.ball.length

        ball_is_between_players = (self.last_ball.x_coordinate >= leftmost_player.x_coordinate
                                           and self.last_ball.right_edge <= rightmost_player.right_edge)

        return distance_between_players <= distance_needed and self.ball_is_between_players() and ball_is_between_players

    def ball_is_between_players(self):
        """ summary: finds out if the players are at the same height and the ball's y coordinates are between the players
            params: None
            returns: boolean; the ball is between the players
        """

        leftmost_player = self.get_leftmost_player()
        rightmost_player = self.get_rightmost_player()

        players_are_at_same_height = CollisionsFinder.is_height_collision(leftmost_player, rightmost_player)
        ball_y_coordinate_is_between_players = (CollisionsFinder.is_height_collision(self.last_ball, rightmost_player)
                                                and CollisionsFinder.is_height_collision(self.last_ball, leftmost_player))

        return players_are_at_same_height and ball_y_coordinate_is_between_players

    def get_leftmost_player(self):
        """ summary: finds the player that is the most left on the screen and returns it
            params: None
            returns: Player; the leftmost player
        """
        return self.player1 if self.player1.x_coordinate < self.player2.x_coordinate else self.player2

    def get_rightmost_player(self):
        """ summary: finds the player that is the most right on the screen and returns it
            params: None
            returns: Player; the rightmost player
        """
        return self.player1 if self.player1.x_coordinate > self.player2.x_coordinate else self.player2

    # From here down is the code for AI
    def run_ai(self):
        # TODO change back
        # state_to_function = {
        #     self.States.GOING_TOWARDS_GOAL: self.go_towards_goal,
        #     self.States.GOING_TOWARDS_BALL: self.go_towards_ball,
        #     self.States.GOING_TOWARDS_CENTER: self.go_towards_center
        # }
        # function = state_to_function.get(self.current_state)
        #
        # if function is not None:
        #     function()
        #
        # if self.ball_is_sandwiched():
        #     self.current_state = self.States.WAITING
        #
        # if self.current_state == self.States.WAITING and not self.ball_is_sandwiched():
        #     self.current_state = self.States.GOING_TOWARDS_BALL

        self.go_towards_goal()

    def go_towards_goal(self):
        """Moves the AI towards the ball and should only be called if moving directly to the ball
        means going towards the goal and the ball is being hit by the AI"""

        # distance_to_goal = self.player2.x_coordinate
        # time_to_goal = distance_to_goal / self.player2.velocity
        #
        # ball_path: Path = self.player2.pong_type.get_ball_y_coordinates(time_to_goal)
        #
        # player_path = VelocityPath(Point(self.player2.x_coordinate, self.player2.y_coordinate), [], self.player2.velocity)
        #
        # for time in self.get_important_times(ball_path):
        #     x_coordinate = self.player2.x_coordinate - time * self.player2.velocity
        #
        #     y_coordinate = ball_path.get_y_coordinate(time)
        #
        #     if y_coordinate >= screen_height - self.player2.height:
        #         y_coordinate = screen_height - self.player2.height
        #
        #     print(x_coordinate, y_coordinate, time)
        #     player_path.add_time_point(Point(x_coordinate, y_coordinate), time)

        # print(player_path)
        self.player2.x_coordinate, self.player2.y_coordinate = self.player_path.get_coordinates()
        # self.player2.add_path(player_path)

    def get_important_times(self, ball_path):
        """Finds and returns the important times for the players path; important is being defined by points where a major
        change happens. The major changes are transitioning into the bottom of the screen and transitioning out of the bottom of the screen"""

        important_times = []
        for path_line in ball_path.path_lines:
            line: LineSegment = path_line.y_coordinate_line

            # Or more accurately the player transitions into the bottom of the screen or out of the bottom of the screen
            time_at_bottom = line.get_x_coordinate(screen_height - self.player2.height)
            min_time = line.start_point.x_coordinate
            max_time = line.end_point.x_coordinate

            player_is_at_bottom = time_at_bottom > min_time and time_at_bottom < max_time

            if player_is_at_bottom and line.slope_is_positive():
                important_times.append(time_at_bottom)

            elif player_is_at_bottom:
                important_times.append(time_at_bottom)

            if not important_times.__contains__(max_time):
                important_times.append(max_time)

        return important_times

    def go_towards_ball(self):
        distance = VelocityCalculator.calc_distance(self.player2.velocity)
        # displacement = distance if self.player2.x_coordinate <
        if self.ball.y_coordinate > self.player2.y_coordinate:
            self.player2.y_coordinate += VelocityCalculator.calc_distance(self.player2.velocity)

        else:
            self.player2.y_coordinate += VelocityCalculator.calc_distance(self.player2.velocity)

    def intercept_opponent(self):
        self.player2.x_coordinate += VelocityCalculator.calc_distance(self.player2.velocity)

        if self.ball.y_coordinate > self.player2.y_coordinate:
            self.player2.y_coordinate += VelocityCalculator.calc_distance(self.player2.velocity)

        else:
            self.player2.y_coordinate += VelocityCalculator.calc_distance(self.player2.velocity)

        distance_to_cover = self.ball.right_edge - self.player2.x_coordinate
        velocities_difference = self.player2.velocity - self.player1.velocity

        # Prevents a dividing by 0 error
        if velocities_difference == 0:
            return

        # NOTE: Code under this point won't be executed if velocities_difference == 0
        time_to_reach_opponent = distance_to_cover / velocities_difference

        if time_to_reach_opponent * self.player2.velocity >= screen_height:
            self.current_state = self.States.GOING_TOWARDS_CENTER

    def go_towards_center(self):
        center = screen_length / 2

        is_at_center = self.player2.x_coordinate >= center and self.player2 <= center + screen_length * .05

        # So it is close to the center, but doesn't have to be right on
        if not is_at_center and self.player2.x_coordinate >= center:
            self.player2.x_coordinate -= VelocityCalculator.calc_distance(self.player2.velocity)

        elif not is_at_center:
            self.player2.x_coordinate += VelocityCalculator.calc_distance(self.player2.velocity)

        if self.last_ball.x_coordinate == center:
            self.current_state = self.States.GOING_TOWARDS_BALL







