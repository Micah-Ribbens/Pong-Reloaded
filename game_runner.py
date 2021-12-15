from GUI.alter_sizes_screen import AlterSizesScreen
from GUI.text_box import TextBox
from GUI.drop_down_menu import DropDownMenu
import pygame
from base_pong.utility_classes import GameObject
from game_mechanics import GameRunner
from base_pong.important_variables import *
import time
from base_pong.velocity_calculator import VelocityCalculator
from GUI.start_screen import StartScreen
from GUI.alter_sizes_screen import AlterSizesScreen
from GUI.game_modes_screen import GameModesScreen
while True:
    start_time = time.time()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
    game_window.fill(background_color)
    StartScreen.run()
    pygame.display.update()
    VelocityCalculator.time = time.time() - start_time

    # Breaking ends this while loop allowing the code below- GameRunner.run_game() to run the game
    # if StartScreen.game_is_started():
    #     StartScreen.run_setup_before_game()
    #     break

GameRunner.run_game()
