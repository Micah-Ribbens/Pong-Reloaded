from base_pong.important_variables import *
from random import randint


def change_properties(modified_object, object):
    for key in modified_object.attributes:
        modified_object.__dict__[key] = object.__dict__[key]
    return modified_object


def percentage_to_number(perecentage, percentage_of_number):
    return (perecentage / 100) * percentage_of_number


def validate_kwargs_has_all_fields(kwargs_fields, kwargs):
    for field in kwargs_fields:
        if not kwargs.__contains__(field):
            raise ValueError(f"Field {field} was not provided for kwargs")


def draw_font(message, font, **kwargs):
    """x_coordinate and y_coordinate or 
    is_center_of_screen (text_color and background_color are optional)"""
    foreground = (255, 255, 255) if not kwargs.get(
        "text_color") else kwargs.get("text_color")
    text_background = background_color if not kwargs.get(
        "background_color") else kwargs.get("background_color")
    text = font.render(message, True, foreground, text_background)
    text_rect = text.get_rect()
    if not kwargs.get("is_center_of_screen"):
        validate_kwargs_has_all_fields(
            ["x_coordinate", "y_coordinate"], kwargs)
        text_rect.left = kwargs.get("x_coordinate")
        text_rect.top = kwargs.get("y_coordinate")
    if kwargs.get("is_center_of_screen") and kwargs.get("y_coordinate"):
        text_rect.center = (screen_length / 2,
                            kwargs.get("y_coordinate"))
    elif kwargs.get("is_center_of_screen"):
        text_rect.center = (screen_length / 2,
                            screen_height / 2)
    game_window.blit(text, text_rect)

# length is what percent_right and percent_length are a percent of and height is what percent_down and percent_height are a percent of
def percentages_to_numbers(percent_right, percent_down, percent_length, percent_height, length, height):
    return [
        percentage_to_number(percent_right, length), 
        percentage_to_number(percent_down, height),
        percentage_to_number(percent_length, length),
        percentage_to_number(percent_height, height)
        ]