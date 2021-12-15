from base_pong.utility_classes import HistoryKeeper
from base_pong.engines import CollisionsEngine
import abc
# from game_modes.normal_pong import NormalPong


class PongType(abc.ABC):
    @abc.abstractmethod
    def run(ball, paddle1, paddle2):
        pass

    @abc.abstractmethod
    def reset(ball, paddle1, paddle2):
        pass

    @abc.abstractmethod
    def ball_collisions(ball, paddle1, paddle2):
        pass

    def draw_game_objects(ball, paddle1, paddle2):
        paddle1.draw()
        paddle2.draw()
        ball.draw()

    def add_needed_objects(ball, paddle1, paddle2):
        HistoryKeeper.add(paddle1, paddle1.name, True)
        HistoryKeeper.add(paddle2, paddle2.name, True)
        HistoryKeeper.add(ball, "ball", True)
