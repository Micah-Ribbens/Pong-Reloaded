import pygame
from base_pong.important_variables import window
from base_pong.velocity_calculator import VelocityCalculator
from base_pong.important_variables import screen_height, background, screen_length, window
from base_pong.utility_functions import *
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
    @property
    def x_midpoint(self):
        return self.x_coordinate + self.length / 2
    def draw(self):
        pygame.draw.rect(window, (self.color), (self.x_coordinate,
                        self.y_coordinate, self.length, self.height))
    def time_based_activity_is_done(self, name, time_needed, restart_condition, start_condition=True):
        if restart_condition:
            HistoryKeeper.add(0, name, False)
            return False

        if HistoryKeeper.get_last(name) is None:
            HistoryKeeper.add(VelocityCalculator.time, name, False)

        current_time = HistoryKeeper.get_last(name)
        if current_time >= time_needed:
            HistoryKeeper.add(0, name, False)
            return True

        elif start_condition:
            HistoryKeeper.add(current_time + VelocityCalculator.time, name, False)

        return False

class UtilityFunctions:
    def validate_kwargs_has_all_fields(kwargs_fields, kwargs):
        for field in kwargs_fields:
            if not kwargs.__contains__(field):
                raise ValueError(f"Field {field} was not provided for kwargs")
    
    def draw_font(message, font, **kwargs):
        """x_coordinate and y_coordinate or 
        is_center_of_screen (foreground and background are optional)"""
        foreground = (255, 255, 255) if not kwargs.get("foreground") else kwargs.get("foreground")
        text_background = background if not kwargs.get("background") else kwargs.get("background")
        text = font.render(message, True, foreground, text_background)
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

class Button(GameObject):
    def got_clicked(self):
        area = pygame.Rect(self.x_coordinate, self.y_coordinate, self.length,
                           self.height)
        mouse_x, mouse_y = pygame.mouse.get_pos()
        clicked = pygame.mouse.get_pressed()[0]
        if area.collidepoint(mouse_x, mouse_y) and clicked:
            return True

        return False

class HistoryKeeper:
    memento_list = {}
    def reset():
        HistoryKeeper.memento_list = {}
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
