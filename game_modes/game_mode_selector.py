from game_modes.utility_functions import *
from game_modes.gravity_pong import GravityPong
from game_modes.middle_paddle_pong import MiddlePaddlePong
from game_modes.normal_pong import NormalPong
from game_modes.portal_pong import PortalPong
from game_modes.shatter_pong import ShatterPong
from game_modes.split_pong import SplitPong
class GameModeSelector:
    # If a game mode isn't selected from the GUI, then the game mode will be Random
    game_mode = "Random"
    # If a pong_type isn't selected from the GUI, then the game mode will be Normal Pong
    pong_type = "Normal Pong"
    number_of_players = "2 Player"

    all_game_modes = ["Chaos", "Civilized", "Unique Twist", "Random", "Pick Pong Type"]
    all_player_options = ["Single Player", "2 Player"]
    all_pong_types = ["Gravity Pong", "Middle Paddle Pong", "Normal Pong", "Portal Pong", "Shatter Pong", "Split Pong"]
    
    def get_pong_type_class(pong_type):
        # Each pong type has its own class
        pong_type_to_class = {
            "Gravity Pong": GravityPong,
            "Middle Paddle Pong": MiddlePaddlePong, 
            "Normal Pong": NormalPong, 
            "Portal Pong": PortalPong,
            "Shatter Pong": ShatterPong, 
            "Split Pong": SplitPong
            }
        if not pong_type_to_class.__contains__(pong_type):
            raise ValueError("No such pong type exists: ")
        
        else:
            return pong_type_to_class.get(pong_type)

    def get_pong_type():
        # Each Game Mode has a list of possible pong types that are chosen at random after each reset
        # Reset meaning the start of the game or after someone scores
        print(GameModeSelector.pong_type)
        game_mode_to_pong_types = {
            "Chaos": ["Gravity Pong", "Portal Pong", "Split Pong"],
            "Civilized": ["Normal Pong", "Shatter Pong", "Gravity Pong"],
            "Unique Twist": ["Gravity Pong", "Middle Paddle Pong", "Portal Pong", "Shatter Pong", "Split Pong"],
            "Random": GameModeSelector.all_pong_types
        }
        pong_type = None

        if game_mode_to_pong_types.__contains__(GameModeSelector.game_mode):
            pong_types = game_mode_to_pong_types.get(GameModeSelector.game_mode)
            pong_type = GameModeSelector.get_random_pong_type(pong_types)

        elif GameModeSelector.game_mode == "Pick Pong Type":
            pong_type = GameModeSelector.get_pong_type_class(GameModeSelector.pong_type)

        return pong_type

    def get_random_pong_type(pong_types):
        pong_type = get_random_item(pong_types)
        return GameModeSelector.get_pong_type_class(pong_type)

