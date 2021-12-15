import pygame
from GUI.text_box import TextBox
from base_pong.important_variables import *
from base_pong.utility_classes import GameObject, Event, HistoryKeeper, TimedEvent
from base_pong.colors import *
from base_pong.important_variables import *
from base_pong.velocity_calculator import VelocityCalculator

class MenuItem(TextBox):
    values = []
    label = ""
    properties_modifying = []
    key_events = {}
    # Important Note: This class doesn't modify this property; the AlterSizesScreen does
    # I did this because the menu_item(s) are unselected if another item gets clicked
    is_selected = True
    increase_by = 0

    def __init__(self, label, default_values, properties_modifying, increase_by):
        self.properties_modifying = properties_modifying
        self.label = label
        self.values = default_values
        self.increase_by = increase_by

        # Text is assigned in the render method
        super().__init__("", 15, False, white, blue)

    def render(self):
        self.text = (f"{self.label}: ({self.values[0]}, {self.values[1]})" if self.values.__len__() == 2
                else f"{self.label}: {self.values[0]}")

        # Saving the length and height, so I can draw a section of the text box normally then add a buffer at the right_edge and bottom
        # The length and height will be modified below, then reverted back
        length = self.length
        height = self.height
        buffer_length = VelocityCalculator.give_measurement(screen_length, 1)
        buffer_height = VelocityCalculator.give_measurement(screen_height, 2)

        self.length -= buffer_length
        self.height -= buffer_height
        TextBox.render(self)

        GameObject.draw(GameObject(self.right_edge, self.y_coordinate, height, buffer_length, background_color))
        GameObject.draw(GameObject(self.x_coordinate, self.bottom, buffer_height, length, background_color))

        self.length = length
        self.height = height



    def instantiate_needed_objects(self, key):
        if not self.key_events.__contains__(f"held in{key}"):
            self.key_events[f"held in{key}"] = TimedEvent(1, False)

        if not self.key_events.__contains__(f"held increase{key}"):
            self.key_events[f"held increase{key}"] = TimedEvent(.1, True)

    def can_add_value(self, key, is_substracting, value, key_click_event):
        controlls = pygame.key.get_pressed()

        self.instantiate_needed_objects(key)

        key_held_in_event: TimedEvent = self.key_events.get(f"held in{key}")
        held_in_increase_event: TimedEvent = self.key_events.get(
            f"held increase{key}")

        restart_event = not controlls[key]
        key_held_in_event.run(restart_event, controlls[key])
        held_in_increase_event.run(restart_event, key_held_in_event.is_done())

        is_click = not key_click_event.is_continuous(controlls[key])

        if is_substracting and value - self.increase_by <= 0:
            return False

        return self.is_selected and (is_click or held_in_increase_event.is_done())
    
    def do_multiple_value_logic(self, left_key_event, right_key_event):
        controlls = pygame.key.get_pressed()

        if self.can_add_value(pygame.K_LEFT, True, self.values[1], left_key_event) and controlls[pygame.K_LEFT]:
            self.values[1] -= self.increase_by

        if self.can_add_value(pygame.K_RIGHT, False, self.values[1], right_key_event) and controlls[pygame.K_RIGHT]:
            self.values[1] += self.increase_by

    def run(self, up_key_event, down_key_event, left_key_event, right_key_event):
        controlls = pygame.key.get_pressed()
        
        # IMPORTANT NOTE: self.can_add_value() must be first in the if statement followed by controlls[key]
        # Otherwise the pause between holding the key down and repeatedly adding values doesn't work
        if self.can_add_value(pygame.K_UP, False, self.values[0], up_key_event) and controlls[pygame.K_UP]:
            self.values[0] += self.increase_by

        if self.can_add_value(pygame.K_DOWN, True, self.values[0], down_key_event) and controlls[pygame.K_DOWN]:
            self.values[0] -= self.increase_by

        # Some menu items can alter multiple values, but others don't
        has_multiple_values = len(self.values) == 2

        if has_multiple_values:
            self.do_multiple_value_logic(left_key_event, right_key_event)

        self.render()
