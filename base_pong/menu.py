import pygame
from base_pong.important_variables import *
from base_pong.UtilityClasses import Button, GameObject, HistoryKeeper, UtilityFunctions
class MenuBar(GameObject):
    menu_items = []
    def __init__(self, height):
        self.x_coordinate = 0
        self.length = screen_length
        self.y = 0
        self.height = height
    def add(self, menu_item):
        self.menu_items.append(menu_item)
        menu_item.y_coordinate = self.y_coordinate
        menu_item.height = self.height
    def reset_clicked(self):
        for menu_item in self.menu_items:
            menu_item.is_selected = False
    def render(self):
        controlls = pygame.key.get_pressed()
        up_key = pygame.K_UP
        down_key = pygame.K_DOWN
        left_key = pygame.K_LEFT
        right_key = pygame.K_RIGHT
        HistoryKeeper.add(controlls[up_key] == 1, f"key{up_key}", False)
        HistoryKeeper.add(controlls[down_key] == 1, f"key{down_key}", False)
        HistoryKeeper.add(controlls[left_key] == 1, f"key{left_key}", False)
        HistoryKeeper.add(controlls[right_key] == 1, f"key{right_key}", False)
        for x in range(len(self.menu_items)):
            menu_item = self.menu_items[x]
            menu_item.length = self.length // len(self.menu_items)
            menu_item.x_coordinate = menu_item.length * x
            if menu_item.got_clicked():
                self.reset_clicked()
                menu_item.is_selected = True

            menu_item.render()


class MenuItem(Button):
    values = []
    label = ""
    properties_modifying = []
    is_selected = False
    increase_by = 0
    is_held_in = {pygame.K_UP: False, pygame.K_DOWN: False, pygame.K_LEFT: False, pygame.K_RIGHT: False}
    

    def __init__(self, label, default_values, properties_modifying, increase_by):
        self.properties_modifying = properties_modifying
        self.label = label
        self.values = default_values
        self.increase_by = increase_by

    def render(self):
        text = (f"{self.label}: ({self.values[0]}, {self.values[1]})" if self.values.__len__() == 2
                else f"{self.label}: {self.values[0]}")
    
        UtilityFunctions.draw_font(text, pygame.font.Font('freesansbold.ttf', 12), 
                                   x_coordinate=self.x_coordinate, y_coordinate=self.y_coordinate)
        controlls = pygame.key.get_pressed()
        if self.can_add_value(pygame.K_UP, False, self.values[0]) and controlls[pygame.K_UP]:
            self.values[0] += self.increase_by
        if self.can_add_value(pygame.K_DOWN, True, self.values[0]) and controlls[pygame.K_DOWN]:
            self.values[0] -= self.increase_by
        if self.values.__len__() == 1:
            return
        if self.can_add_value(pygame.K_LEFT, True, self.values[1]) and controlls[pygame.K_LEFT]:
            self.values[1] -= self.increase_by
        if self.can_add_value(pygame.K_RIGHT, False, self.values[1]) and controlls[pygame.K_RIGHT]:
            self.values[1] += self.increase_by

    def can_add_value(self, key, is_substracting, value):
        controlls = pygame.key.get_pressed()
        if self.time_based_activity_is_done(f"held in{key}", 1, not controlls[key], controlls[key]):
            self.is_held_in[key] = True
        if not controlls[key]:
            self.is_held_in[key] = False
        if is_substracting and value - self.increase_by <= 0:
            return False
        is_click = not HistoryKeeper.get_last(f"key{key}") and controlls[key] == 1
        is_held__in_increase = self.time_based_activity_is_done(f"held {key}", .05, not controlls[key], controlls[key]) and self.is_held_in[key]
        return self.is_selected and (is_click or is_held__in_increase)
