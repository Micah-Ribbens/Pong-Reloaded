from important_variables import window
import pygame
from abc import abstractmethod
from velocity_calculator import VelocityCalculator
from important_variables import screen_height, background, screen_length, window
import random
from utility_functions import *
import pickle
class GameObject:
    white = (255, 255, 255)
    light_gray = (190, 190, 190)
    gray = (127, 127, 127)
    dark_gray = (63, 63, 63)
    black = (0, 0, 0)
    red = (255, 0, 0)
    green = (0, 255, 0)
    blue = (0, 0, 255)
    yellow = (255, 255, 0)
    magenta = (255, 0, 255)
    cyan = (0, 255, 255)
    orange = (255, 100, 0)
    x_coordinate = 0
    y_coordinate = 0
    height = 0
    length = 0
    color = (0, 0, 250)
    name = ""
    attributes = []

    def find_all_attributes(object):
        attributes = []
        for key in object.__dict__.keys():
            if not key.__contains__("__") and not callable(key):
                attributes.append(key)
        return attributes

    # @property automatically changes this "attribute" when the x_coordinate or length changes
    # Can be treated as an attribute
    @property 
    def right_edge(self):
        return self.x_coordinate + self.length
    @property
    def bottom(self):
        return self.y_coordinate + self.height
    def draw(self):
        pygame.draw.rect(window, (self.color), (self.x_coordinate,
                        self.y_coordinate, self.length, self.height))

class UtilityFunctions:
    def validate_kwargs_has_all_fields(kwargs_fields, kwargs):
        for field in kwargs_fields:
            if not kwargs.__contains__(field):
                raise ValueError(f"Field {field} was not provided for kwargs")
    
    def draw_font(message, font, **kwargs):
        """x_coordinate and y_coordinate or 
        is_center_of_screen"""
        foreground = (255, 255, 255)
        text = font.render(message, True, foreground, background)
        text_rect = text.get_rect()
        if not kwargs.get("is_center_of_screen"):
            UtilityFunctions.validate_kwargs_has_all_fields(["x_coordinate", "y_coordinate"], kwargs)
            text_rect.left = kwargs.get("x_coordinate")
            text_rect.top = kwargs.get("y_coordinate")
        if kwargs.get("is_center_of_screen") and kwargs.get("y_coordinate"):
            text_rect.center = (screen_length / 2,
                                kwargs.get("y_coordinate"))
        elif kwargs.get("is_center_of_screen"):
            text_rect.center = (screen_length / 2,
                                screen_height / 2)
        window.blit(text, text_rect)

class HistoryKeeper:
    memento_list = {}
    def reset():
        HistoryKeeper.memento_list = {}
    def copy(object):
        return pickle.loads(pickle.dumps(object, -1))
    def add(object, name, is_game_object):
        if is_game_object:
            object = deepcopy(object)

        HistoryKeeper._add(object, name)
        
    def _add(object, name):
        try: 
            HistoryKeeper.memento_list[name].append(object)
        except KeyError:
            HistoryKeeper.memento_list[name] = [object]


    def get(name):
        if HistoryKeeper.memento_list.get(name) is None:
            return []
        return HistoryKeeper.memento_list.get(name)

    def get_last(name):
        mementos = HistoryKeeper.get(name)
        if len(mementos) == 0:
            return None
        if len(mementos) == 1:
            return mementos[0]
        return mementos[len(mementos) - 2]
