from base_pong.utility_classes import GameObject, Event
from base_pong.utility_functions import percentage_to_number
from base_pong.important_variables import *
from base_pong.velocity_calculator import VelocityCalculator
from base_pong.utility_classes import HistoryKeeper
import pygame


class ClickableComponent(GameObject):
    click_event = None

    def __init__(self):
        self.click_event = Event()
    
    def run(self):
        self.run_click_event()

    def got_clicked(self):
        # This is just a safety net in case components of this don't call run_click_event
        # The issue with it being here though it that it assumes the got_clicked() is called every cycle
        # So it's ideal if components of this call run()
        self.run_click_event()

        is_clicked = True
        area = pygame.Rect(self.x_coordinate, self.y_coordinate, self.length,
                           self.height)

        mouse_x, mouse_y = pygame.mouse.get_pos()
        mouse_clicked = pygame.mouse.get_pressed()[0]
        # Otherwise if the mouse is held down this is going to be called over and over again
        if self.click_event.is_continuous(mouse_clicked):
            is_clicked = False

        if not area.collidepoint(mouse_x, mouse_y) or not mouse_clicked:
            is_clicked = False

        return is_clicked

    # Things that inherit from it must call this method otherwise seeing if component got clicked won't work
    # Code won't see if this component got clicked in the past
    def run_click_event(self):
        # Implementation detail; assumes that two run cycle times can't be equal, so it can be used to see if it was called this cycle
        # If it was then it won't call click_event.run
        HistoryKeeper.add(VelocityCalculator.time, id(self), False)
        was_called_this_cycle = HistoryKeeper.get_last(
            id(self)) == VelocityCalculator.time

        if not was_called_this_cycle:
            mouse_clicked = pygame.mouse.get_pressed()[0]
            self.click_event.run(mouse_clicked)

    def percentage_set_bounds(self, percent_right, percent_down, percent_length, percent_height):
        self.x_coordinate = percentage_to_number(percent_right, screen_length)
        self.y_coordinate = percentage_to_number(percent_down, screen_height)
        self.length = percentage_to_number(percent_length, screen_length)
        self.height = percentage_to_number(percent_height, screen_height)

    def number_set_bounds(self, x, y, length, height):
        self.x_coordinate, self.y_coordinate = x, y
        self.length, self.height = length, height
