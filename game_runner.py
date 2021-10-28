from base_pong.menu_screen import show_menu_screen, start_button
import pygame
from game_mechanics import GameRunner
from base_pong.important_variables import *
import time
from base_pong.velocity_calculator import VelocityCalculator

while True:
    start_time = time.time()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
    if start_button.game_is_started:
       break
    window.fill(background)
    show_menu_screen()
    pygame.display.update()
    VelocityCalculator.time = time.time() - start_time
GameRunner.run_game()