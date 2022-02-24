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
    last_point = None

    def __init__(self, start_point):
        """ summary: initializes the object

            params:
                path_lines: List of PathLine; the path lines for this path

            returns: None
        """

        self.last_point = start_point
        self.path_lines = []

    def get_x_coordinate_path(prev_game_object, game_object):
        """returns: Path; the path of the game object using the x coordinate"""
        path = Path(Point(prev_game_object.x_coordinate, prev_game_object.y_coordinate))
        path.add_point(Point(game_object.x_coordinate, game_object.y_coordinate), game_object.height)
        return path

    def get_right_edge_path(prev_game_object, game_object):
        """returns: Path; the path of the game object using the right edge"""

        path = Path(Point(prev_game_object.right_edge, prev_game_object.y_coordinate))
        path.add_point(Point(game_object.right_edge, game_object.y_coordinate), game_object.height)
        return path

    def add_point(self, point, height):
        """Adds the path_line to the attribute 'path_lines'"""

        path_line = PathLine(LineSegment(self.last_point, point), height)
        self.path_lines.append(path_line)
        self.last_point = point

    def render(self):
        """Renders all the path lines"""
        distinct_colors = [(230, 25, 75), (60, 180, 75), (255, 225, 25), (0, 130, 200), (245, 130, 48), (145, 30, 180), (70, 240, 240), (240, 50, 230), (210, 245, 60), (250, 190, 212), (0, 128, 128), (220, 190, 255), (170, 110, 40), (255, 250, 200), (128, 0, 0), (170, 255, 195), (128, 128, 0), (255, 215, 180), (0, 0, 128), (128, 128, 128), (255, 255, 255), (0, 0, 0)]

        for x in range(len(self.path_lines)):
            y_coordinate_line = self.path_lines[x].y_coordinate_line
            bottom_line = self.path_lines[x].bottom_line

            y_coordinate_line.color = distinct_colors[x % 22]
            bottom_line.color = distinct_colors[x % 22]
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
        try:
            last_index = len(self.path_lines) - 1
            y_coordinate_point = self.path_lines[last_index].y_coordinate_line.end_point
            bottom_point = self.path_lines[last_index].bottom_line.end_point
            return [y_coordinate_point, bottom_point]
        except:
            pass

    def get_y_coordinate(self, x_coordinate):
        """returns: double; the y_coordinate at that x_coordinate"""

        for path_line in self.path_lines:
            start_point = path_line.y_coordinate_line.start_point
            end_point = path_line.y_coordinate_line.end_point

            # TODO fix so it works for both a leftwards and a rightwards path
            if x_coordinate >= start_point.x_coordinate and x_coordinate <= end_point.x_coordinate:
                return path_line.y_coordinate_line.get_y_coordinate(x_coordinate)

        return -1

    def __str__(self):
        string = ""
        for x in range(len(self.path_lines)):
            string += f"{self.path_lines[x].y_coordinate_line}\n"

        return string

    def get_lines(self):
        """returns: List of LineSegment; all the lines that this path has"""

        lines = []

        for path_line in self.path_lines:
            y_line = path_line.y_coordinate_line
            bottom_line = path_line.bottom_line

            lines.append(y_line)
            lines.append(bottom_line)

            lines.append(LineSegment(y_line.start_point, bottom_line.start_point))
            lines.append(LineSegment(y_line.end_point, bottom_line.end_point))

        return lines




class VelocityPath(Path):
    """A path that takes into account velocity"""

    velocity = 0
    x_coordinate_lines = []
    y_coordinate_lines = []
    last_end_time = 0

    times = []  # Stores the times that the get_coordinates() function was called
    total_time = 0
    last_point = None

    def __init__(self, start_point, other_points, velocity):
        """Initializes the object"""

        self.velocity = velocity
        self.path_lines = []
        self.x_coordinate_lines = []
        self.y_coordinate_lines = []

        self.last_point = start_point

        for point in other_points:
            self.add_point(point)

    def add_point(self, point):
        """Does some calculations to find the time from the start of the last point to the end of the parameter 'point'
        and then calls add_time_point() to add the point"""
        x_distance = self.last_point.x_coordinate - point.x_coordinate
        y_distance = self.last_point.y_coordinate - point.y_coordinate

        end_time = max(x_distance / self.velocity, y_distance / self.velocity) + self.last_end_time
        self.add_time_point(point, end_time)

    def add_time_point(self, point, end_time):
        """Adds the point to the path using the end_time as the x_coordinate for the x and y coordinate lines"""
        x_coordinate_line = LineSegment(Point(self.last_end_time, self.last_point.x_coordinate),
                                        Point(end_time, point.x_coordinate))

        y_coordinate_line = LineSegment(Point(self.last_end_time, self.last_point.y_coordinate),
                                        Point(end_time, point.y_coordinate))

        self.x_coordinate_lines.append(x_coordinate_line)
        self.y_coordinate_lines.append(y_coordinate_line)
        self.last_end_time = end_time

        # The height for the path_line doesn't matter
        path_line = PathLine(LineSegment(self.last_point, point), 0)
        self.path_lines.append(path_line)

        self.last_point = point

    def get_coordinates(self):
        """returns: [x_coordinate, y_coordinate] for that time"""
        if not self.times.__contains__(VelocityCalculator.time):
            self.times.append(VelocityCalculator.time)
            self.total_time += VelocityCalculator.time


        # By default it starts out as the end of the path and if the time falls within the path uses those coordinates
        last_index = len(self.x_coordinate_lines) - 1
        end_x_coordinate = self.x_coordinate_lines[last_index].end_point.y_coordinate
        end_y_coordinate = self.y_coordinate_lines[last_index].end_point.y_coordinate
        coordinates = [end_x_coordinate, end_y_coordinate]

        for x in range(len(self.y_coordinate_lines)):
            y_coordinate_line: LineSegment = self.y_coordinate_lines[x]
            x_coordinate_line: LineSegment = self.x_coordinate_lines[x]
            start_point = y_coordinate_line.start_point
            end_point = y_coordinate_line.end_point

            if self.total_time >= start_point.x_coordinate and self.total_time <= end_point.x_coordinate:
                # print(x_coordinate_line, y_coordinate_line)
                coordinates = [x_coordinate_line.get_y_coordinate(self.total_time), y_coordinate_line.get_y_coordinate(self.total_time)]
        return coordinates

    def __str__(self):
        string = ""
        for x in range(len(self.y_coordinate_lines)):
            y_coordinate_line = self.y_coordinate_lines[x]
            x_coordinate_line = self.x_coordinate_lines[x]

            string += f"x {x_coordinate_line}, y {y_coordinate_line}\n"

        return string