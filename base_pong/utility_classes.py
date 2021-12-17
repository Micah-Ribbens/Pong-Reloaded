import pygame
from base_pong.important_variables import game_window
from base_pong.velocity_calculator import VelocityCalculator
from base_pong.important_variables import screen_height, background_color, screen_length, game_window
from base_pong.utility_functions import percentage_to_number
from copy import deepcopy


class Segment:
    is_percentage = False
    color = (0, 0, 0)
    amount_from_top = 0
    amount_from_left = 0
    length_amount = 0
    width_amount = 0

    def __init__(self, **kwargs):
        """is_percentage, color, amount_from_top, amount_from_left, length_amount, width_amount"""
        self.is_percentage, self.color = kwargs.get(
            "is_percentage"), kwargs.get("color"),
        self.amount_from_top, self.amount_from_left = kwargs.get(
            "amount_from_top"), kwargs.get("amount_from_left")
        self.length_amount, self.width_amount = kwargs.get(
            "length_amount"), kwargs.get("width_amount")

class Dimensions:
    x_coordinate = 0
    y_coordinate = 0
    height = 0 
    length = 0

    def __init__(self, x_coordinate, y_coordinate, length, height):
        self.x_coordinate, self.y_coordinate = x_coordinate, y_coordinate
        self.length, self.height = length, height
    
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

    @property
    def y_midpoint(self):
        return self.y_coordinate + self.height / 2

class GameObject:
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

    @property
    def y_midpoint(self):
        return self.y_coordinate + self.height / 2

    def __init__(self, x_coordinate=0, y_coordinate=0, height=0, length=0, color=(0, 0, 0)):
        self.x_coordinate, self.y_coordinate = x_coordinate, y_coordinate
        self.height, self.length, self.color = height, length, color

    def draw(self):
        pygame.draw.rect(game_window, (self.color), (self.x_coordinate,
                                                     self.y_coordinate, self.length, self.height))

    def draw_circle(self):
        pygame.draw.ellipse(game_window, self.color, (self.x_coordinate,
                            self.y_coordinate, self.length, self.height))
    # Purely for debugging purposes; so you can see the location and size of game objects

    def str(self):
        print(f"name {self.name} x {self.x_coordinate} y {self.y_coordinate} length {self.length} height {self.height} bottom {self.bottom} right_edge {self.right_edge}\n")

    def draw_in_segments(object, segments):
        GameObject.draw(object)
        for segment in segments:
            if segment.is_percentage:
                x_coordinate = percentage_to_number(
                    segment.amount_from_left, object.length) + object.x_coordinate
                y_coordinate = percentage_to_number(
                    segment.amount_from_top, object.height) + object.y_coordinate
                height = percentage_to_number(
                    segment.width_amount, object.height)
                length = percentage_to_number(
                    segment.length_amount, object.length)
                GameObject.draw(GameObject(
                    x_coordinate, y_coordinate, height, length, segment.color))


class TimedEvent:
    time_needed = 0
    is_started = False
    restarts_upon_completion = False
    current_time = 0

    def __init__(self, time_needed, restarts_upon_completion):
        self.time_needed = time_needed
        self.restarts_upon_completion = restarts_upon_completion

    def is_done(self):
        is_finished = self.is_started

        if self.current_time < self.time_needed:
            is_finished = False

        if is_finished and self.restarts_upon_completion:
            self.start()
            self.current_time = 0

        return is_finished

    def run(self, reset_event, start_event):
        if reset_event:
            self.reset()

        elif start_event:
            self.start()

        if self.is_started:
            self.current_time += VelocityCalculator.time

    def start(self):
        self.is_started = True

    def reset(self):
        self.is_started = False
        self.current_time = 0


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


class Event:
    def is_continuous(self, event):
        if HistoryKeeper.get_last(id(self)) and event:
            return True
        return False

    def run(self, event):
        HistoryKeeper.add(event, id(self), False)
