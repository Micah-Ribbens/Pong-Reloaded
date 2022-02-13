from base_pong.quadratic_equations import *
from base_pong.important_variables import *
from base_pong.colors import *


class Point:
    x_coordinate = 0
    y_coordinate = 0

    """Stores the x and y coordinates of point"""

    def __init__(self, x_coordinate, y_coordinate):
        """ summary: initializes the object

            params:
                x_coordinate: double; the value of the point's x coordinate
                y_coordinate: double; the value of the point's y coordinate

            returns: None
        """

        self.x_coordinate, self.y_coordinate = x_coordinate, y_coordinate

    def __str__(self):
        return f"({self.x_coordinate}, {self.y_coordinate})"


class LineSegment:
    """Uses the equation y = mx + b where m is slope and b is y_intercept"""

    slope = 0
    y_intercept = 0
    start_point = 0
    end_point = 0
    color = purple

    def __init__(self, start_point: Point, end_point: Point):
        """ summary: initializes the object

            params:
                start_point: Point; a point on the line (different than end_point)
                end_point: Point; a point on the line (different than point1)

            returns: None
        """
        self.slope = (start_point.y_coordinate - end_point.y_coordinate) / (start_point.x_coordinate - end_point.x_coordinate)
        self.y_intercept = start_point.y_coordinate - self.slope * start_point.x_coordinate

        self.start_point = start_point
        self.end_point = end_point

    def render(self):
        """Renders the object"""

        pygame.draw_py.draw_line(game_window.get_window(), self.color,
                                 (int(self.start_point.x_coordinate), int(self.start_point.y_coordinate)),
                                 (int(self.end_point.x_coordinate), int(self.end_point.y_coordinate)), 9)

    def get_y_coordinate(self, x_coordinate):
        """ summary: finds the y_coordinate using the equation y = mx + b

            params:
                x_coordinate: the x coordinate which will be used to find the y_coordinate

            returns: double; the y coordinate
        """

        return self.slope * x_coordinate + self.y_intercept

    def get_x_coordinate(self, y_coordinate):
        """ summary: finds the x coordinate using the equation x = (y - b) / m

            params:
                y_coordinate: the y coordinate which will be used to find the x coordinate

            returns: double; the x coordinate
        """

        return (y_coordinate - self.y_intercept) / self.slope

    def slope_is_positive(self):
        """returns: boolean; if the slope is >= 0"""

        return self.slope >= 0

    def __str__(self):
        return f"{self.start_point} -> {self.end_point}"
