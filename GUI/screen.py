import abc

from base_pong.utility_functions import percentage_to_number
from base_pong.important_variables import *


class SubScreen(abc.ABC):
    @abc.abstractmethod
    def run():
        pass

    @abc.abstractclassmethod
    def initiate(length_used_up, height_used_up):
        pass

    def set_item_bounds(item, length_used_up, height_used_up, percent_right, percent_down, percent_length, percent_height):
        x_coordinate = percentage_to_number(percent_right, screen_length)
        y_coordinate = percentage_to_number(percent_down, screen_height)
        length = percentage_to_number(percent_length, screen_length)
        height = percentage_to_number(percent_height, screen_height)

        # Changes values to max_value to still be within bounds
        if x_coordinate < length_used_up:
            x_coordinate = length_used_up

        if y_coordinate < height_used_up:
            y_coordinate = height_used_up

        item.number_set_bounds(x_coordinate, y_coordinate, length, height)
