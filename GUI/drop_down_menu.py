from GUI.clickable_component import ClickableComponent
from GUI.text_box import TextBox
from base_pong.utility_classes import GameObject
from base_pong.colors import *


class DropDownMenu(ClickableComponent):
    items = []
    text_color = None
    background_color = None
    font_size = 0
    is_expanded = False
    menu_title = ""
    text = ""
    selected_item = ""

    def get_selected_item(self):
        return self.selected_item

    def add_item(self, text):
        item = TextBox(text, self.font_size, False,
                       self.text_color, self.background_color)

        self.items.append(item)

    def __init__(self, menu_title, item_names, text_color, background_color, font_size):
        # Makes it so each drop down's menu items are unique
        self.items = []

        self.text_color = text_color
        self.background_color = background_color
        self.font_size = font_size
        self.menu_title = menu_title
        self.text = menu_title

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

        if self.got_clicked():
            self.text = self.menu_title

        self.render()

    def render(self):
        # Divided into two sections; the text portion and the arrow showing portion

        # TODO fix
        text_portion_length = self.length * .9
        text_portion = TextBox(
            self.text, self.font_size, False, self.text_color, self.background_color)
        text_portion.number_set_bounds(
            self.x_coordinate, self.y_coordinate, text_portion_length, self.height)
        # Creates a divider between the text and the arrow
        divider_length = self.length * .02
        divider = GameObject(text_portion.right_edge, self.y_coordinate,
                             self.height, divider_length, white)

        used_up_length = divider_length + text_portion_length
        arrow_portion = GameObject(divider.right_edge, self.y_coordinate,
                                   self.height, self.length - used_up_length, self.background_color)

        text_portion.run()
        arrow_portion.draw()
        divider.draw()

        if self.is_expanded:
            self.render_items()

    def render_items(self):
        # This object (self) is above all the other items; so its the starting item for last item
        last_item = self

        for item in self.items:
            # So if that item is selected then it doesn't render
            if self.text == item.text:
                continue

            divider = self.get_divider(last_item)
            self.set_item_bounds(divider, item)
            divider.draw()
            item.run()

            last_item = item

    def get_divider(self, last_item):
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
