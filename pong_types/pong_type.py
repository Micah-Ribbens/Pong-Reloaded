from base_pong.important_variables import screen_height
from base_pong.utility_classes import HistoryKeeper
from base_pong.score_keeper import ScoreKeeper
import abc

# TODO replace all places with Pong2
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
