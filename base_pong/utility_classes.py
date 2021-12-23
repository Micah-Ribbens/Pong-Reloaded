import pygame
from base_pong.important_variables import game_window
from base_pong.velocity_calculator import VelocityCalculator
from base_pong.important_variables import screen_height, background_color, screen_length, game_window
from base_pong.utility_functions import percentage_to_number
from copy import deepcopy
from math import sqrt, pow

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

class Fraction:
    numerator = None
    denominator = None
    
    def __init__(self, numerator, denominator):
        self.numerator = numerator
        self.denominator = denominator

    def get_reciprocal(self):
        return Fraction(self.denominator, self.numerator)
    
    def get_number(self):
        return self.numerator / self.denominator
    
    def get_fraction_to_power(self, power):
        return Fraction(pow(self.numerator, power), pow(self.denominator, power))
    
    # Gets the other part of the fraction to make it one
    # For instance for 3/4 it would do 4 - 3/4 which would be 1/4 and 1/4 + 3/4 = 1
    def get_fraction_to_become_one(self):
        return Fraction(self.denominator - self.numerator, self.denominator)
        

    def __str__(self):
        return f"{self.numerator}/{self.denominator}"

