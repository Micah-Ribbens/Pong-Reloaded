from math import ceil, floor
from base_pong.velocity_calculator import VelocityCalculator
from base_pong.important_variables import *
class Grid:
    dimensions = 0
    max_columns = 0
    max_rows = 0
    starts_at_top = False

    def __init__(self, dimensions, max_columns, max_rows, starts_at_top):
        self.dimensions = dimensions
        self.max_columns, self.max_rows = max_columns, max_rows
        self.starts_at_top = starts_at_top

        if max_columns is None and max_rows is None:
            raise ValueError("Max columns or max rows must have a value; they both can't be None")

    def turn_into_grid(self, items, item_max_length: int, item_max_height: int):
        length_buffer = VelocityCalculator.give_measurement(screen_length, 1)
        height_buffer = VelocityCalculator.give_measurement(screen_height, 1)

        rows = self.get_rows(len(items))
        columns = self.get_columns(len(items))
        item_length = self.get_item_length(columns, item_max_length, length_buffer, len(items))
        item_height = self.get_item_height(rows, item_max_height, height_buffer, len(items))
        base_y_coordinate = self.dimensions.y_coordinate if self.starts_at_top else self.dimensions.bottom - item_height

        for x in range(len(items)):
            # Both would start at 0 (0 is the first column and row)
            column_number = x % columns
            row_number = floor(x / columns)
            # Multiplying row_number by item_height because each row that is gone done increases the y_coordinate that a item should be at
            # For instance, if it is at the 2nd row then one item was before it so it'd be row_number * item_height
            y_coordinate_change = row_number * item_height if self.starts_at_top else -(row_number * item_height)

            # The row and column numbers are multiplied by the buffers to add the neccessary buffers. For instance, if it is in column 3
            # The item in column 1 and column 2 had a buffer, so it'd be the length_buffer * 2
            change_from_height_buffer = (row_number * height_buffer) if self.starts_at_top else -(row_number * height_buffer)
            change_from_length_buffer = (column_number * length_buffer)

            y_coordinate_change += change_from_height_buffer

            # Multiplying column_number by item_length because each column that is before it increases the x_coordinate that a item should be at
            # For instance, if it is at the 2nd column then one item was before it so it'd be column_number * item_length
            x_coordinate = (column_number * item_length) + change_from_length_buffer
            y_coordinate = base_y_coordinate + y_coordinate_change

            items[x].number_set_bounds(x_coordinate, y_coordinate, item_length, item_height)

        # TODO FIX
        for item in items:
            item.str()

    def get_item_length(self, columns, item_max_length, length_buffer, number_of_items):
        # Must minus the length buffer * (number_of_items - 2) from the regular length because
        # Every item has the length_buffer after it besides the first and last item, so hence the minus 2
        remaining_length = self.dimensions.length - (length_buffer * (number_of_items - 2))

        length = remaining_length // columns

        if item_max_length is not None and length > item_max_length:
            length = item_max_length
        
        return length

    def get_item_height(self, rows, item_max_height, height_buffer, number_of_items):
        # Must minus the height_buffer * (number_of_items - 2) from the regular height because
        # Every item has the height_buffer after it besides the first and last item, so hence the minus 2
        remaining_height = self.dimensions.height - (height_buffer * (number_of_items - 2))
        height = remaining_height // rows

        if item_max_height is not None and height > item_max_height:
            height = item_max_height
        
        return height

    def get_columns(self, number_of_items):
        rows = self.max_rows if self.max_rows is not None else self.get_rows(number_of_items)

        # The overfill of number_of_items / max_rows must be an additional column
        # For instance if they are 5 items and there are 2 rows there must be 3 columns
        columns = ceil(number_of_items / rows)

        if self.max_columns is not None and columns > self.max_columns:
            columns = self.max_columns
        
        return columns
    
    def get_rows(self, number_of_items):
        columns = self.max_columns if self.max_columns is not None else self.get_columns(number_of_items)
        # The overfill of number_of_items / max_columns must be an additional row
        # For instance if they are 5 items and there are 2 columns there must be 3 rows.
        rows = ceil(number_of_items / columns)

        if self.max_rows is not None and rows > self.max_rows:
            rows = self.max_rows
        
        return rows