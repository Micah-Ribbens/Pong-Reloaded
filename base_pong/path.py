import pygame.draw_py


class PathLine:
    """Made up of two lines start y_coordinate to end y_coordinate and start bottom to end bottom"""

    y_coordinate_line = None
    bottom_line = None

    def __init__(self, y_coordinate_line, bottom_line):
        """ summary: initializes the object

            params:
                y_coordinate_line: Line; the line from the start y_coordinate to the end y_coordinate
                bottom_line: Line; the line from the start bottom to the end bottom

            returns: None
        """
        self.y_coordinate_line = y_coordinate_line
        self.bottom_line = bottom_line


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

        print("STARTING")
        for path_line in self.path_lines:
            path_line.y_coordinate_line.render()
            path_line.bottom_line.render()
        print("ENDING\n=========")



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

