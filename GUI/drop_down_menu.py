import pygame
from GUI.clickable_component import ClickableComponent
from GUI.text_box import TextBox
from base_pong.drawable_objects import GameObject
from base_pong.colors import *
from base_pong.important_variables import *
from base_pong.utility_functions import percentage_to_number, percentages_to_numbers


class DropDownMenu(ClickableComponent):
    items = []
    text_color = None
    background_color = None
    font_size = 0
    is_expanded = False
    title = ""
    text = ""
    selected_item = ""
    # This is the part of the drop down menu that is supposed to be clicked
    clickable_component = None

    def get_selected_item(self):
        return self.selected_item

    def add_item(self, text):
        item = TextBox(text, self.font_size, False,
                       self.text_color, self.background_color)

        self.items.append(item)

    def __init__(self, title, item_names, text_color, background_color, font_size, selected_index):
        # Makes it so each drop down's menu items are unique
        self.items = []

        self.text_color = text_color
        self.background_color = background_color
        self.font_size = font_size
        self.title = title
        # This sets the text that is selected automatically without the user's input
        self.text = item_names[selected_index]
        self.selected_item = item_names[selected_index]

        for item_name in item_names:
            self.add_item(item_name)

        super().__init__()

    def run(self):
        # Stores height of the title portion of drop down menu which will need to be changed back- changing it, for seeing if it got clicked
        if self.got_clicked() or self.an_item_got_clicked():
            # Makes it so collapses when expanded and expands when collapsed
            self.is_expanded = not self.is_expanded

        for item in self.items:
            if item.got_clicked():
                self.text = item.text
                self.selected_item = item.text

        # if self.got_clicked():
        #     self.text = self.title

        self.render()

    def get_title_portion(self):
        title_portion = TextBox(
            self.title, self.font_size, False, self.text_color, background_color)
        title_portion.number_set_bounds(
            self.x_coordinate, self.y_coordinate, self.length, self.height)
        return title_portion

    def render(self):
        title_portion = self.get_title_portion()
        last_item = title_portion
        # Divided into two sections; the text portion and the arrow showing portion
        text_portion_length = self.length * .9
        text_portion = TextBox(
            self.text, self.font_size, False, self.text_color, self.background_color)

        text_portion.number_set_bounds(
            self.x_coordinate, last_item.bottom, text_portion_length, self.height)

        # So it doesn't reset the clickable component every cycle making it impossible to tell if the component got clicked
        # TODO set clickable part to entire drop down menu section not just text_portion
        if self.clickable_component is None:
            self.clickable_component = text_portion

        # Creates a divider between the text and the arrow
        divider_length = self.length * .02
        divider = GameObject(text_portion.right_edge, last_item.bottom,
                             self.height, divider_length, white)

        used_up_length = divider_length + text_portion_length

        remaining_length = self.length - used_up_length

        text_portion.run()
        divider.draw()
        self.draw_arrow_portion(
            remaining_length, divider.right_edge, last_item.bottom)
        title_portion.run()

        if self.is_expanded:
            self.render_items(last_item)

    def draw_arrow_portion(self, remaining_length, x_coordinate, y_coordinate):
        arrow_container = GameObject(x_coordinate, y_coordinate,
                                     self.height, remaining_length, self.background_color)

        # From here down is talking about the arrow part
        percent_down = 20
        percent_right = 20

        # The offset percent_down and percent_right should be equal on both sides
        # Thats what the code below does
        percent_length = 100 - (percent_right * 2)
        percent_height = 100 - (percent_down * 2)

        arrow_numbers = percentages_to_numbers(
            percent_right, percent_down, percent_length, percent_height, remaining_length, self.height)
        # number_to_right and number_downwards is how much right and how much down it should be in relation to the component
        number_to_right, number_downwards, length, height = arrow_numbers

        # The arrow is right after the divider
        start_x_coordinate = number_to_right + x_coordinate
        start_y_coordinate = number_downwards + y_coordinate

        # End x coordinate and y coordinate meaning the bottom point of the triangle
        end_y_coordinate = start_y_coordinate + height
        # This would be the halfway point of the vertices of the top of the triangle
        end_x_coordinate = start_x_coordinate + (length // 2)

        # arrow_container must be draw before the arrow, so the arrow can draw on top of the arrow_container
        arrow_container.draw()
        pygame.draw.polygon(surface=game_window, color=white,
                            points=[(start_x_coordinate, start_y_coordinate), (start_x_coordinate + length, start_y_coordinate), (end_x_coordinate, end_y_coordinate)])

    def render_items(self, last_item):
        for item in self.items:
            buffer_between_items = self.get_buffer_between_items(last_item)
            self.set_item_bounds(buffer_between_items, item)
            buffer_between_items.draw()
            item.run()

            last_item = item

    def get_buffer_between_items(self, last_item):
        return GameObject(last_item.x_coordinate, last_item.bottom, last_item.height * .1, last_item.length, white)

    def set_item_bounds(self, last_item, item: TextBox):
        item.number_set_bounds(
            self.x_coordinate, last_item.bottom, self.length, self.height)

    def an_item_got_clicked(self):
        is_clicked = False
        for item in self.items:
            if item.got_clicked():
                is_clicked = True

        return is_clicked

    def got_clicked(self):
        # The clickable component is set during the first cycle making it impossible to be clicked if it isn't set yet
        is_clicked = False if self.clickable_component is None else self.clickable_component.got_clicked()

        return is_clicked
