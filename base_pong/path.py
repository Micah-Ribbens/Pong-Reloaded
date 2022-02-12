from math import sqrt

import pygame.draw_py
from base_pong.equations import LineSegment, Point
from base_pong.velocity_calculator import VelocityCalculator


class PathLine:
    """Made up of two lines start y_coordinate to end y_coordinate and start bottom to end bottom"""

    y_coordinate_line: LineSegment = None
    bottom_line = None

    def __init__(self, y_coordinate_line, height):
        """ summary: initializes the object

            params:
                y_coordinate_line: LineSegment; the line from the start y_coordinate to the end y_coordinate
                height: double; the distance from the y_coordinate line to the bottom_line

            returns: None
        """
        self.y_coordinate_line = y_coordinate_line

        # The y_coordinate_line and bottom_line's y_coordinate are off by height
        self.bottom_line = LineSegment(Point(self.y_coordinate_line.start_point.x_coordinate, self.y_coordinate_line.start_point.y_coordinate + height),
                                       Point(self.y_coordinate_line.end_point.x_coordinate, self.y_coordinate_line.end_point.y_coordinate + height))


class Path:
    """Stores the path of an object"""

    path_lines = []

    def __init__(self, path_lines):
        """ summary: initializes the object

            params:
                path_lines: List of PathLine; the path lines for this path

            returns: None
        """

        self.path_lines = path_lines

    def add(self, path_line):
        """Adds the path_line to the attribute 'path_lines'"""

        self.path_lines.append(path_line)

    def render(self):
        """Renders all the path lines"""
        distinct_colors = [(230, 25, 75), (60, 180, 75), (255, 225, 25), (0, 130, 200), (245, 130, 48), (145, 30, 180), (70, 240, 240), (240, 50, 230), (210, 245, 60), (250, 190, 212), (0, 128, 128), (220, 190, 255), (170, 110, 40), (255, 250, 200), (128, 0, 0), (170, 255, 195), (128, 128, 0), (255, 215, 180), (0, 0, 128), (128, 128, 128), (255, 255, 255), (0, 0, 0)]

        for x in range(len(self.path_lines)):
            y_coordinate_line = self.path_lines[x].y_coordinate_line
            bottom_line = self.path_lines[x].bottom_line

            y_coordinate_line.color = distinct_colors[x]
            bottom_line.color = distinct_colors[x]
            y_coordinate_line.render()
            bottom_line.render()


    def get_start_points(self):
        """returns: List of Point; [y_coordinate start point, bottom start point] for the first y_coordinate_line and bottom_line
        in the attribute 'path_lines'"""
        y_coordinate_point = self.path_lines[0].y_coordinate_line.start_point
        bottom_point = self.path_lines[0].bottom_line.start_point
        return [y_coordinate_point, bottom_point]

    def get_end_points(self):
        """returns: List of Point; [y_coordinate end point, bottom end point] for the last y_coordinate_line and bottom_line
        in the attribute 'path_lines'"""

        last_index = len(self.path_lines) - 1
        y_coordinate_point = self.path_lines[last_index].y_coordinate_line.end_point
        bottom_point = self.path_lines[last_index].bottom_line.end_point
        return [y_coordinate_point, bottom_point]

    def get_y_coordinate(self, x_coordinate):
        """returns: double; the y_coordinate at that x_coordinate"""

        for path_line in self.path_lines:
            start_point = path_line.y_coordinate_line.start_point
            end_point = path_line.y_coordinate_line.end_point

            if x_coordinate <= start_point.x_coordinate and x_coordinate >= end_point.x_coordinate:
                print(path_line.y_coordinate_line)
                return path_line.y_coordinate_line.get_y_coordinate(x_coordinate)

        return -1

class VelocityPath(Path):
    """A path that takes into account velocity"""

    velocity = 0
    x_coordinate_lines = []
    y_coordinate_lines = []
    last_end_time = 0

    times = []  # Stores the times that the get_coordinates() function was called
    total_time = 0

    def __init__(self, start_point, other_points, velocity, height):
        """Initializes the object"""

        self.velocity = velocity

        last_point = start_point

        for point in other_points:
            path_line = PathLine(LineSegment(last_point, point), height)
            self.add(path_line)
            last_point = point

    def add(self, path_line: PathLine):
        super().add(path_line)

        line = path_line.y_coordinate_line
        x_distance = line.start_point.x_coordinate - line.end_point.x_coordinate
        y_distance = line.start_point.y_coordinate - line.end_point.y_coordinate

        # Using formula sqrt of (x1 - x2)^2 + (y1 - y2)^2
        distance = sqrt(pow(x_distance, 2) + pow(y_distance, 2))

        end_time = self.last_end_time + (distance / self.velocity)

        x_coordinate_line = LineSegment(Point(self.last_end_time, line.start_point.x_coordinate),
                                        Point(end_time, line.end_point.x_coordinate))

        y_coordinate_line = LineSegment(Point(self.last_end_time, line.start_point.y_coordinate),
                                        Point(end_time, line.end_point.y_coordinate))

        self.x_coordinate_lines.append(x_coordinate_line)
        self.y_coordinate_lines.append(y_coordinate_line)
        self.last_end_time = end_time

    def get_coordinates(self):
        """returns: [x_coordinate, y_coordinate] for that time"""

        if not self.times.__contains__(VelocityCalculator.time):
            self.times.append(VelocityCalculator.time)
            self.total_time += VelocityCalculator.time

        for x in range(len(self.path_lines)):
            y_coordinate_line: LineSegment = self.y_coordinate_lines[x]
            x_coordinate_line: LineSegment = self.x_coordinate_lines[x]
            start_point = y_coordinate_line.start_point
            end_point = y_coordinate_line.end_point

            if self.total_time >= start_point.x_coordinate and self.total_time <= end_point.x_coordinate:
                return [x_coordinate_line.get_y_coordinate(self.total_time), y_coordinate_line.get_y_coordinate(self.total_time)]

        return [0, 0] # Invalid input

