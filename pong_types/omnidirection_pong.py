import pygame.key

from base_pong.engines import CollisionsFinder
from base_pong.equations import Point, LineSegment
from base_pong.events import Event
from base_pong.important_variables import screen_height, screen_length
from base_pong.path import VelocityPath, Path, PathLine
from base_pong.players import AI
from base_pong.utility_classes import HistoryKeeper, StateChange
from base_pong.velocity_calculator import VelocityCalculator
from pong_types.normal_pong import NormalPong
from pong_types.pong_type import PongType
from base_pong.utility_functions import key_is_hit, get_leftmost_object, get_rightmost_object, get_displacement

# TODO fix code so you don't have to assume player2 is the ai
class OmnidirectionalPong(NormalPong):
    """Pong where the player can move 4 directions"""''
    # States for the AI
    class States:
        GOING_TOWARDS_GOAL = "GOING_TOWARDS_GOAL"
        INTERCEPTING_BALL = "INTERCEPTING_BALL"
        CENTERING = "CENTERING"
        BACKING_UP = "BACKING_UP"
        INTERCEPTING_PLAYER = "INTERCEPTING_PLAYER"
        WAITING = "WAITING"

    current_state = States.INTERCEPTING_BALL
    next_state = States.INTERCEPTING_BALL

    ball_sandwiched_event = Event()
    ball_is_spawned = False
    a_player_has_scored = False

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

        # TODO uncomment
        # self.player2.action = self.run_ai
        self.player2 = self.player2

    def run(self):
        """ summary: runs all the code that is necessary for this pong type
            params: None
            returns: None
        """
        self.last_ball = self.ball
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            self.ball.can_move = True

        self.paddle_collisions()
        self.horizontal_player_movements(self.player1, pygame.K_a, pygame.K_d)
        self.horizontal_player_movements(self.player2, pygame.K_LEFT, pygame.K_RIGHT)
        self.ball_sandwiched_event.run(self.ball_is_sandwiched())
        self.run_ball_sandwiching()

        # if self.ball.can_move:
        self.ball_movement()
        self.run_player_movement()
        self.ball_collisions(self.player1)
        self.ball_collisions(self.player2)
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
        if CollisionsFinder.sim_collision(self.last_ball, player) and not CollisionsFinder.is_collision(self.last_ball, player):
            CollisionsFinder.is_collision(self.last_ball, player)

        # if CollisionsFinder.is_collision(self.last_ball, player):
        #     print("COLLLISION")
        if CollisionsFinder.is_collision(self.last_ball, player):
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

    def reset(self):
        """Resets everything necessary after someone scored"""
        super().reset()
        self.ball_is_spawned = True
        self.a_player_has_scored = True

    # AI CODE
    def run_ai(self):
        # TODO uncomment lines
        # So when it is first initialized there is a player path
        if self.next_state != self.current_state or self.player_path is None:
            self.run_state_changes()

        # BACKING_UP
        self.run_state_change(self.States.BACKING_UP, [
            StateChange(self.is_done_backing_up(), self.States.WAITING)])
        # INTERCEPTING_PLAYER
        self.run_state_change(self.States.INTERCEPTING_PLAYER, [
            StateChange(not self.can_intercept_object(self.player1.velocity, self.player1), self.States.CENTERING),
            StateChange(not CollisionsFinder.is_collision(self.player1, self.last_ball), self.States.INTERCEPTING_BALL)])
        # CENTERING
        self.run_state_change(self.States.CENTERING, [
            StateChange(self.ball_is_spawned, self.States.INTERCEPTING_BALL)])
        # INTERCEPTING_BALL
        self.run_state_change(self.States.INTERCEPTING_BALL, [
            StateChange(CollisionsFinder.is_left_collision(self.player2, self.last_ball), self.States.GOING_TOWARDS_GOAL),
            StateChange(not self.can_intercept_object(self.ball.forwards_velocity, self.last_ball), self.States.CENTERING),
            StateChange(CollisionsFinder.is_collision(self.player1, self.last_ball), self.States.INTERCEPTING_PLAYER)
        ])
        # WAITING
        prev_player = HistoryKeeper.get_last(self.player1.name)
        opponent_has_moved = prev_player is not None and prev_player.x_coordinate != self.player1.x_coordinate
        opponent_is_touching_ball = CollisionsFinder.is_collision(self.player1, self.last_ball)
        self.run_state_change(self.States.WAITING, [
            StateChange(opponent_has_moved and opponent_is_touching_ball, self.States.INTERCEPTING_PLAYER),
            StateChange(self.ball.is_moving_right and self.ball.x_coordinate >= self.player2.right_edge, self.States.INTERCEPTING_BALL)])
        # State Changes no matter what State
        self.next_state = self.States.BACKING_UP if self.ball_is_sandwiched() else self.next_state
        self.next_state = self.States.INTERCEPTING_BALL if self.a_player_has_scored else self.next_state

        if self.player_path is not None:
            self.player2.x_coordinate, self.player2.y_coordinate = self.player_path.get_coordinates()

        # Done using this variable, so it should be False again
        self.a_player_has_scored = False

    def can_intercept_object(self, intercepted_object_velocity, intercepted_object):
        """returns: boolean; if the AI can intercept that object (assumes the object is going rightwards)"""
        return_value = True

        distance_needed = intercepted_object.right_edge - self.player2.x_coordinate

        velocity_difference = self.player2.velocity - intercepted_object_velocity

        if velocity_difference <= 0:
            return_value = False

        else:
            # The max amonut of time the AI has to travel the distance
            max_time = (screen_length - intercepted_object.right_edge) / intercepted_object_velocity

            return_value = (distance_needed / velocity_difference) <= max_time

        return return_value

    def is_done_backing_up(self):
        """returns: boolean; if the AI is done backing away from the ball"""
        return_value = False

        # Assumes the backing up path is one singular line
        start_x_coordinate: Point = self.player_path.x_coordinate_lines[0].start_point.y_coordinate
        end_x_coordinate: Point = self.player_path.x_coordinate_lines[0].end_point.y_coordinate

        path_is_leftwards = start_x_coordinate > end_x_coordinate

        if path_is_leftwards and self.player2.x_coordinate <= end_x_coordinate:
            return_value = True

        if not path_is_leftwards and self.player2.x_coordinate >= end_x_coordinate:
            return_value = True

        return return_value

    def run_state_change(self, needed_state, states_changes):
        """ summary: changes the attribute 'next_state' if one of the state change's condition is True

            params:
                needed_state: int; the state that the AI has to be in in order to change states
                state_changes: List of StateChange; the states that are allowed
        """

        for state_change in states_changes:
            if state_change.condition and self.current_state == needed_state:
                self.next_state = state_change.state

    def run_state_changes(self):
        """Runs all the code that should be done when the state changes"""

        self.current_state = self.next_state

        # GOING_TOWARDS_GOAL
        if self.current_state == self.States.GOING_TOWARDS_GOAL:
            self.go_to_goal()

        # INTERCEPTING_BALL
        if self.current_state == self.States.INTERCEPTING_BALL:
            self.intercept_object(self.ball.forwards_velocity, self.ball)

        # INTERCEPTING_PLAYER
        if self.current_state == self.States.INTERCEPTING_PLAYER:
            # The ball is touching the player so it has to intercept the ball that is touching the player
            self.intercept_object(self.player2.forwards_velocity, self.ball)

        # BACKING_UP
        if self.current_state == self.States.BACKING_UP:
            self.player_path = VelocityPath(Point(self.player2.x_coordinate, self.player2.y_coordinate), [], self.player2.velocity)
            self.player_path.add_point(Point(self.player2.x_coordinate + 50, self.player2.y_coordinate + 10))

        # CENTERING
        if self.current_state == self.States.CENTERING:
            self.player_path = VelocityPath(Point(self.player2.x_coordinate, self.player2.y_coordinate), [], self.player2.velocity)
            self.player_path.add_point(Point(screen_length / 2, screen_height / 2))

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

    def intercept_object(self, intercepted_objects_velocity, intercepted_object):
        """ summary: makes the AI's path intercept the other object using the parameters

            params:
                intercepted_objects_velocity: double; the velocity of the intercepted_object
                intercepted_object: GameObject; the object that will be intercepted

            returns: None
        """
        path_is_leftwards = get_rightmost_object(intercepted_object, self.player2) == self.player2
        self.player_path = VelocityPath(Point(self.player2.x_coordinate, self.player2.y_coordinate), [],
                                        self.player2.velocity)

        # Gets the horizontal distance for the rightwards path and if the path is leftwards then it changes the distance
        horizontal_buffer = VelocityCalculator.give_measurement(screen_length, 5)
        horizontal_distance = int(intercepted_object.right_edge - self.player2.x_coordinate + horizontal_buffer)
        if path_is_leftwards:
            horizontal_distance = int(self.player2.x_coordinate - intercepted_object.right_edge)

        velocity_difference = self.player2.velocity - intercepted_objects_velocity
        horizontal_time = horizontal_distance / velocity_difference

        ball_path = self.get_ball_y_coordinates(horizontal_time)
        vertical_buffer = VelocityCalculator.give_measurement(screen_height, 15)
        end_point: Point = ball_path.get_end_points()[0]

        intercepted_object_end_y_coordinate = end_point.y_coordinate
        # Starts out finding the vertical displacement if the AI is above the intercepted object at the end and if it
        # isn't then it changes the vertical displacement
        vertical_displacement = intercepted_object_end_y_coordinate + intercepted_object.height - self.player2.bottom
        if intercepted_object_end_y_coordinate < self.player2.x_coordinate:
            vertical_displacement = intercepted_object_end_y_coordinate - self.player2.y_coordinate

        vertical_time = abs(vertical_displacement) / self.player2.velocity

        if vertical_time > horizontal_time or path_is_leftwards:
            displacement = get_displacement(self.player2.velocity, horizontal_time, path_is_leftwards)
            self.add_path_point(intercepted_object.right_edge + displacement, end_point.y_coordinate, horizontal_time)

        else:
            # The time that the AI should go from moving only horizontally to a slant of vertical + horizontal movement
            time_vertical_ascent_should_start = horizontal_time - vertical_time
            displacement = get_displacement(self.player2.velocity, time_vertical_ascent_should_start, path_is_leftwards)

            self.add_path_point(intercepted_object.right_edge + displacement, self.player2.y_coordinate, time_vertical_ascent_should_start)

            displacement = get_displacement(self.player2.velocity, vertical_time, path_is_leftwards)

            self.add_path_point(intercepted_object.right_edge + displacement, end_point.y_coordinate, horizontal_time)
        print(f"PATH {self.player_path}\n")

    def add_path_point(self, x_coordinate, y_coordinate, time):
        """Adds a point to the attribute 'player_path' and makes sure the point is within the screens bounds"""
        if y_coordinate >= screen_height - self.player2.height:
            y_coordinate = screen_height - self.player2.height

        self.player_path.add_time_point(Point(x_coordinate, y_coordinate), time)

    def go_to_goal(self):
        """Changes the AI's path, so it will move towards the goal"""
        distance_to_goal = self.player2.x_coordinate
        time_to_goal = distance_to_goal / self.player2.velocity

        ball_path: Path = self.get_ball_y_coordinates(time_to_goal)

        self.player_path = VelocityPath(Point(self.player2.x_coordinate, self.player2.y_coordinate), [],
                                        self.player2.velocity)

        for time in self.get_important_times(ball_path):
            x_coordinate = self.player2.x_coordinate - time * self.player2.velocity

            self.add_path_point(x_coordinate, ball_path.get_y_coordinate(time), time)






