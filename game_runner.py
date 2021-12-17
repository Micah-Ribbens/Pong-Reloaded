from GUI.alter_sizes_screen import AlterSizesScreen
from GUI.pause_screen import PauseScreen
from GUI.text_box import TextBox
from GUI.drop_down_menu import DropDownMenu
import pygame
from base_pong.HUD import HUD
from base_pong.utility_classes import GameObject
from game_screen import GameScreen
from base_pong.important_variables import *
import time
from base_pong.velocity_calculator import VelocityCalculator
from GUI.start_screen import StartScreen
from GUI.alter_sizes_screen import AlterSizesScreen
from GUI.game_modes_screen import GameModesScreen

current_screen = StartScreen
current_screen.set_up()
while True:
    start_time = time.time()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
    game_window.fill(background_color)
    current_screen.run()

    if current_screen == GameScreen:
        HUD.render_pause_button()
    
    if current_screen == GameScreen and HUD.pause_button.got_clicked():
        current_screen = PauseScreen
        current_screen.set_up()    

    
    if current_screen == PauseScreen and PauseScreen.go_to_start_screen_button.got_clicked():
        current_screen = StartScreen
        current_screen.set_up()    


    if current_screen == PauseScreen and PauseScreen.continue_game_button.got_clicked():
        current_screen = GameScreen

    pygame.display.update()
    VelocityCalculator.time = time.time() - start_time

    if current_screen == StartScreen and StartScreen.start_button.got_clicked():
        current_screen = GameScreen
        current_screen.set_up()    

