from base_pong.equations import Point, LineSegment
from base_pong.important_variables import screen_height
from base_pong.path import Path, PathLine
from base_pong.utility_classes import HistoryKeeper
from base_pong.score_keeper import ScoreKeeper
import abc
from base_pong.utility_functions import mod


class PongType(abc.ABC):
    player1 = None
    player2 = None
    ball = None

    def __init__(self, player1, player2, ball):
        """ summary: Initializes the PongType with the needed objects to run its methods
            
            params: 
                player1: Paddle; the player on the leftmost side on the screen
                player2: Paddle; the player on the rightmost side on the screen
                ball: Ball; the ball that the players hit

            returns: None
        """
        self.player1 = player1
        self.player2 = player2
        self.ball = ball

    @abc.abstractmethod
    def run(self):
        pass

    @abc.abstractmethod
    def reset(self):
        pass

    def draw_game_objects(self):
        """ summary: draws all the game objects (paddles and ball) onto the screen
            params: None
            returns: None
        """

        self.player1.render()
        self.player2.render()
        self.ball.render()

    def add_needed_objects(self):
        """ summary: adds all the games objects (paddle and ball) onto the screen
            params: None
            returns: None
        """

        HistoryKeeper.add(self.player1, self.player1.name, True)
        HistoryKeeper.add(self.player2, self.player2.name, True)
        HistoryKeeper.add(self.ball, self.ball.name, True)
    
    def player1_has_scored(self):
        """ summary: finds out if the ball has gone beyond the screens right boundary
            params: None
            returns: boolean; if player1 has scored
        """
        return ScoreKeeper.player_has_scored(self.ball, True)
    
    def player2_has_scored(self):
        """ summary: finds out if the ball has gone beyond the screens left boundary
            params: None
            returns: boolean; if player2 has scored
        """
        return ScoreKeeper.player_has_scored(self.ball, False)

    def set_paddles_movements(self, paddle):
        """ summary: sets all the ways the player can move (up and down)

            params:
                paddle: Paddle; the paddle will have its movement directions it can move set

            returns: None
        """

        paddle.can_move_down = False if paddle.bottom >= screen_height else True
        paddle.can_move_up = False if paddle.y_coordinate <= 0 else True

        if paddle.y_coordinate <= 0:
            paddle.y_coordinate = 0

        if paddle.bottom >= screen_height:
            paddle.y_coordinate = screen_height - paddle.height

    def get_path(self, x_coordinate):
        """ summary: finds the ball's y_coordinate and bottom at the next time it hits the x_coordinate
            IMPORTANT: this function should be called when the ball is going the desired horizontal direction

            params:
                x_coordinate: int; the number that is used to evaluate the ball's path

            returns: Path; the path of the ball from its current x_coordinate to the end x_coordinate
        """

        path = Path([])
        time_to_travel_distance = abs(x_coordinate - self.ball.x_coordinate) / self.ball.forwards_velocity

        ball_y_coordinate = self.ball.y_coordinate
        ball_is_moving_down = self.ball.is_moving_down
        ball_x_coordinate = self.ball.x_coordinate
        displacement = 0

        while time_to_travel_distance > 0:
            ball_bottom = ball_y_coordinate + self.ball.height

            if ball_is_moving_down:
                displacement = screen_height - ball_bottom

            else:
                displacement = -ball_y_coordinate

            time = abs(displacement / self.ball.upwards_velocity)

            if time_to_travel_distance - time < 0:
                distance = self.ball.upwards_velocity * time_to_travel_distance
                displacement = distance if ball_is_moving_down else -distance
                time = time_to_travel_distance

            end_ball_y_coordinate = ball_y_coordinate + displacement
            end_ball_x_coordinate = ball_x_coordinate + time * self.ball.forwards_velocity
            y_coordinate_line = LineSegment(Point(ball_x_coordinate, ball_y_coordinate),
                                                    Point(end_ball_x_coordinate, end_ball_y_coordinate))

            path.add(PathLine(y_coordinate_line, self.ball.height))
            ball_is_moving_down = not ball_is_moving_down
            
            ball_y_coordinate = end_ball_y_coordinate
            ball_x_coordinate = end_ball_x_coordinate

            time_to_travel_distance -= time

        return path





