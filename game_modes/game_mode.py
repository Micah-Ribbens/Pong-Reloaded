from abc import abstractmethod
class GameMode:
    @abstractmethod
    def run(ball, paddle1, paddle2):
        pass
    @abstractmethod
    def reset():
        pass