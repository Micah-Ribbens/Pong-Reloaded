import pygame
from base_pong.important_variables import game_window
from base_pong.velocity_calculator import VelocityCalculator
from base_pong.important_variables import screen_height, background_color, screen_length, game_window
from base_pong.utility_functions import percentage_to_number
from copy import deepcopy
from math import sqrt, pow

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
    def get_x_coordinates(self):
        return self.get_coordinates(self.x_coordinate, self.right_edge)
    
    def get_y_coordinates(self):
        return self.get_coordinates(self.y_coordinate, self.bottom)
    
    def get_coordinates(self, min, max):
        coordinates = [min, max]
        min = int(min) + 1
        max = int(max) + 1
        # Have to turn it into an int to make the code below work
        for x in range(max - min - 2):
            coordinates.append(x + min)

        return coordinates

    def get_y_coordinates_from_x_coordinate(self, x_coordinate):
        # Most GameObjects are going to be rectangular, but the elliptical ones override this method
        return self.get_y_coordinates()

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

    # Purely for debugging purposes; so you can see the location and size of game objects
    def str(self):
        print(f"name {self.name} x {self.x_coordinate} y {self.y_coordinate} length {self.length} height {self.height} bottom {self.bottom} right_edge {self.right_edge}\n")

    def draw_in_segments(object, segments):
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

class Ellipse(GameObject):
    def draw(self):
        pygame.draw.ellipse(game_window, self.color, (self.x_coordinate,
                            self.y_coordinate, self.length, self.height))

    def get_equation_variables(self):
        # x_center is the same as h and y_center is the same as k
        # x_center and y_center is a bit more descriptive here though
        x_center = self.x_coordinate + self.length / 2
        y_center = self.y_coordinate + self.height / 2
        a = x_center - self.x_coordinate
        b = y_center - self.y_coordinate

        return [x_center, y_center, a, b]

    def get_y_coordinates_from_x_coordinate(self, x_coordinate):
        # This is the equation for an ellipse (x - h)^2 / a^2 + (y - k)^2 / b^2 = 1
        # The math below I did by hand to solve for the y_min and y_max
        h, k, a, b = self.get_equation_variables()

        # right_side is the right side of the equation so starting out the side with the 1 and the left_side is the other side with x, y, k, etc.
        # This will make the left_side look like b^2 * (x - h)^2 + a^2 * (y - k)^2
        x_fraction = pow(x_coordinate - h, 2) / pow(a, 2)

        # Equation now looks like (y - k)^2 / b^2 = 1 - (x - h)^2 / a^2
        right_side = 1 - x_fraction
        # Equation now looks like (y - k)^2 = (1 - (x - h)^2 / a^2) * b^2
        right_side *= pow(b, 2)

        # Since a sqrt can either be positive or negative you have to do +-
        y_min = int(sqrt(right_side) + k)
        y_max = int(-sqrt(right_side) + k)

        return self.get_coordinates(y_min, y_max)