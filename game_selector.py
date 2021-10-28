from game_modes.game_mode import GameMode
class GameSelector:
    game_mode: GameMode = None
    def run(ball, paddle1, paddle2):
        GameSelector.game_mode.run(ball, paddle1, paddle2)
    def reset():
        GameSelector.game_mode.reset()