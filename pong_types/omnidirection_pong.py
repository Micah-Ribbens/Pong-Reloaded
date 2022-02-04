import pygame.key

from base_pong.engines import CollisionsFinder
from base_pong.events import Event
from base_pong.important_variables import screen_height, screen_length
from base_pong.utility_classes import HistoryKeeper
from base_pong.velocity_calculator import VelocityCalculator
from pong_types.normal_pong import NormalPong
from pong_types.pong_type import PongType

# TODO add ball sandwiching and make it so the player can't move beyond the screen boundaries
class OmnidirectionalPong(NormalPong):
    """Pong where the player can move 4 directions"""''

    ball_sandwiched_event = Event()

    # Stores the value of the ball at the start of the cycle; the ball gets modified in the code making this necesary
    last_ball = None
    debug = False

    player_who_hit_ball_key = "player who hit ball"

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
        self.player1.is_moving_left, self.player2.is_moving_left = False, False
        self.player1.is_moving_right, self.player2.is_moving_right = False, False

    def set_paddles_movements(self, player):
        """ summary: sets all the ways the player can move (up and down)

            params:
                paddle: Paddle; the paddle will have its movement directions it can move set

            returns: None
        """

        self.run_player_boundaries(player)

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

        if CollisionsFinder.is_left_collision(self.ball, player) and not self.ball_is_sandwiched():
            self.ball.x_coordinate = player.right_edge + self.ball.length * .2
            self.ball.is_moving_right = True
            HistoryKeeper.add(player, self.player_who_hit_ball_key, True)

        if CollisionsFinder.is_right_collision(self.ball, player) and not self.ball_is_sandwiched():
            self.ball.x_coordinate = player.x_coordinate - self.ball.length * 1.2
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
            player.is_moving_left = True

        else:
            player.is_moving_left = False

        if player.can_move_right and controls[right_key] and not controls[left_key]:
            player.x_coordinate += VelocityCalculator.calc_distance(player.velocity)
            player.is_moving_right = True

        else:
            player.is_moving_right = False

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

    def ball_went_through_a_player(self):
        """ summary: finds out if the ball went through a player because its movement in one cycle made it phase through/into a player
            NOTE: this function is only concerned about the x_coordinates and doesn't take into consideration y_coordinates

            params: None
            returns: boolean; if the ball went through the player
        """

        ball_went_through_a_player = False

        leftmost_player = self.get_leftmost_player()
        rightmost_player = self.get_rightmost_player()

        last_cycle_ball = HistoryKeeper.get_last(self.ball.name)

        if last_cycle_ball is None:
            return False

        if last_cycle_ball.x_coordinate > leftmost_player.right_edge and self.last_ball.x_coordinate <= leftmost_player.right_edge:
            ball_went_through_a_player = True

        if last_cycle_ball.right_edge < rightmost_player.x_coordinate and self.last_ball.right_edge >= rightmost_player.x_coordinate:
            ball_went_through_a_player = True

        return ball_went_through_a_player

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


