from base_pong.important_variables import screen_length, screen_height
from base_pong.utility_functions import percentage_to_number
from gui_components.drop_down_menu import DropDownMenu
from gui_components.sub_screen import SubScreen
from base_pong.colors import *
from pong_types.game_mode_selector import GameModeSelector


class GameModesScreen(SubScreen):
    """The screen that allows the user to select the game mode"""

    pong_type_menu = DropDownMenu(
        "Pong Types", GameModeSelector.all_pong_types, white, blue, 15, GameModeSelector.all_pong_types.index(GameModeSelector.pong_type))
    player_menu = DropDownMenu(
        "Number Of Players", GameModeSelector.all_player_options, white, blue, 15, GameModeSelector.all_player_options.index(GameModeSelector.number_of_players))
    game_mode_menu = DropDownMenu(
        "Game Modes", GameModeSelector.all_game_modes, white, blue, 15, GameModeSelector.all_game_modes.index(GameModeSelector.game_mode))
    components = [game_mode_menu, player_menu, pong_type_menu]
    length_used_up = 0
    height_used_up = 0
    name = "Game Modes"

    def __init__(self, length_used_up, height_used_up):
        """ summary: initializes the object

            params:
                length_used_up: int; the amount of length that the main screen takes up
                height_used_up: int; the amount of height the main screen takes up

            returns: None
        """

        menu_lengths = percentage_to_number(30, screen_length)
        menu_heights = percentage_to_number(6, screen_height)
        buffer_between_menus = percentage_to_number(5, screen_length)

        self.game_mode_menu.number_set_dimensions(length_used_up, height_used_up, menu_lengths, menu_heights)
        self.player_menu.number_set_dimensions(self.game_mode_menu.right_edge + buffer_between_menus, height_used_up, menu_lengths, menu_heights)
        self.pong_type_menu.number_set_dimensions(self.player_menu.right_edge + buffer_between_menus, height_used_up,menu_lengths, menu_heights)

        GameModeSelector.pong_type = self.pong_type_menu.selected_item
        GameModeSelector.game_mode = self.game_mode_menu.selected_item
        
    def run(self):
        """ summary: runs all the necessary logic in order for the game modes screen to work
            params: None
            returns: None
        """

        GameModeSelector.game_mode = self.game_mode_menu.get_selected_item()

        if self.game_mode_menu.get_selected_item() == "Pick Pong Type":
            GameModeSelector.pong_type = self.pong_type_menu.get_selected_item()
        
        # The user gets to choose between certain game modes or choose a specific Pong Type like "Gravity Pong"
        # The Pong Types should only be displayed if they want to pick a specific Pong Type
        if self.game_mode_menu.get_selected_item() == "Pick Pong Type":
            self.pong_type_menu.is_visible = True

        else:
            self.pong_type_menu.is_visible = False

        
