from base_pong.ball import Ball
from base_pong.drawable_objects import GameObject, Ellipse
from base_pong.equations import Point, LineSegment
from base_pong.path import Path
from base_pong.utility_classes import HistoryKeeper
from base_pong.important_variables import (
    screen_height,
    screen_length
)
from base_pong.utility_functions import get_rightmost_object, get_leftmost_object
from base_pong.utility_functions import lists_share_an_item, solve_quadratic

class CollisionsFinder:
    """Gives a series of methods to find if two (or more objects) have collided"""

    def largest_path_direction_is_leftwards(path1: Path, path2: Path):
        """returns: Path; if the path that has traveled the most x distance is leftwards"""

        path1_line = path1.path_lines[0].y_coordinate_line
        path2_line = path2.path_lines[0].y_coordinate_line
        path1_distance = abs(path1_line.start_point.x_coordinate - path1_line.end_point.x_coordinate)
        path2_distance = abs(path2_line.start_point.x_coordinate - path2_line.end_point.x_coordinate)

        largest_path_line = path1_line if path1_distance > path2_distance else path2_line
        return largest_path_line.start_point.x_coordinate > largest_path_line.end_point.x_coordinate

    def is_left_collision(object1, object2):
        """ summary: uses CollisionsFinder.is_collision() to check if there was a collision and HistoryKeeper to
            get the objects from the previous cycle

            params: 
                object1: GameObject; one of the objects that is used to see if the two objects provided have collided
                object2: GameObject; one of the objects that is used to see if the two objects provided have collided

            returns: boolean; if the object1 was previously to the left of object2, but now isn't and if the objects have collided
        """
        # TODO change back
        prev_object1 = HistoryKeeper.get_last(object1.name)
        prev_object2 = HistoryKeeper.get_last(object2.name)
        if prev_object1 is None or prev_object2 is None:
            # Don't want to actually abort the code if this happens since it does on the first cycle; but it is a message to fix something
            # print("ERROR NO PREVIOUS GAME OBJECTS FOUND")
            return False
        return prev_object1.x_coordinate > prev_object2.x_coordinate and CollisionsFinder.is_collision(object1, object2)
        # prev_object1 = HistoryKeeper.get_last(object1.name)
        # prev_object2 = HistoryKeeper.get_last(object2.name)
        #
        # if prev_object1 is None or prev_object2 is None:
        #     # Don't want to actually abort the code if this happens since it does on the first cycle; but it is a message to fix something
        #     # print("ERROR NO PREVIOUS GAME OBJECTS FOUND")
        #     return False
        # object1_path = Path.get_x_coordinate_path(prev_object1, object1)
        # object2_path = Path.get_x_coordinate_path(prev_object2, object2)
        # return not CollisionsFinder.largest_path_direction_is_leftwards(object1_path, object2_path) and CollisionsFinder.is_collision(object1, object2)

    def is_right_collision(object1, object2):
        """ summary: uses CollisionsFinder.is_collision() to check if there was a collision and HistoryKeeper to
            get the objects from the previous cycle

            params: 
                object1: GameObject; one of the objects that is used to see if the two objects provided have collided
                object2: GameObject; one of the objects that is used to see if the two objects provided have collided

            returns: boolean; if the object1 was previously to the right of object2, but now isn't and if the objects have collided
        """
        # TODO change back
        prev_object1 = HistoryKeeper.get_last(object1.name)
        prev_object2 = HistoryKeeper.get_last(object2.name)

        if prev_object1 is None or prev_object2 is None:
            # Don't want to actually abort the code if this happens since it does on the first cycle; but it is a message to fix something
            # print("ERROR NO PREVIOUS GAME OBJECTS FOUND")
            return False

        return prev_object1.right_edge < prev_object2.right_edge and CollisionsFinder.is_collision(object1, object2)
        # prev_object1 = HistoryKeeper.get_last(object1.name)
        # prev_object2 = HistoryKeeper.get_last(object2.name)
        # if prev_object1 is None or prev_object2 is None:
        #     # Don't want to actually abort the code if this happens since it does on the first cycle; but it is a message to fix something
        #     # print("ERROR NO PREVIOUS GAME OBJECTS FOUND")
        #     return False
        # object1_path = Path.get_x_coordinate_path(prev_object1, object1)
        # object2_path = Path.get_x_coordinate_path(prev_object2, object2)
        # # if CollisionsFinder.is_collision(object1, object2) and not CollisionsFinder.largest_path_direction_is_leftwards(object1_path, object2_path):
        # #     print("OH NO")
        # return CollisionsFinder.largest_path_direction_is_leftwards(object1_path, object2_path) and CollisionsFinder.is_collision(object1, object2)

    def is_collision(object1: GameObject, object2: GameObject):
        """ summary: uses get_x_coordinates() and get_y_coordinates_from_x_coordinate() (methods from GameObject)
            to check if the objects share a point(s) (x_coordinate, y_coordinate)

            params:
                object1: GameObject; one of the objects that is used to see if the two objects provided have collided
                object2: GameObject; one of the objects that is used to see if the two objects provided have collided

            returns: boolean; if the two objects provided have collided
        """
        # TODO change back
        return CollisionsFinder.sim_collision(object1, object2)

        prev_object1 = HistoryKeeper.get_last(object1.name)
        prev_object2 = HistoryKeeper.get_last(object2.name)

        if prev_object1 is None or prev_object2 is None:
            print("NO PREV GAME OBJECTS FOUND")
            return False

        object1_has_moved = prev_object1.x_coordinate != object1.x_coordinate or prev_object1.y_coordinate != object1.y_coordinate
        object2_has_moved = prev_object2.x_coordinate != object2.x_coordinate or prev_object2.y_coordinate != object2.y_coordinate

        object1_x_coordinate_path = Path.get_x_coordinate_path(prev_object1, object1)
        object1_right_edge_path = Path.get_right_edge_path(prev_object1, object1)
        object2_x_coordinate_path = Path.get_x_coordinate_path(prev_object2, object2)
        object2_right_edge_path = Path.get_right_edge_path(prev_object2, object2)

        return_value = False
        if object2_has_moved and object1_has_moved:
            # 4 cases because there are two paths for the objects - 2^2 possible combinations
            return_value = (CollisionsFinder.is_path_collision(object1_x_coordinate_path, object2_x_coordinate_path) or
                            CollisionsFinder.is_path_collision(object1_x_coordinate_path, object2_right_edge_path) or
                            CollisionsFinder.is_path_collision(object1_right_edge_path, object2_x_coordinate_path) or
                            CollisionsFinder.is_path_collision(object1_right_edge_path, object2_right_edge_path))

        elif object2_has_moved or object1_has_moved:
            stationary_object = object1 if not object1_has_moved else object2
            moving_x_coordinate_path = object1_x_coordinate_path if object1_has_moved else object2_x_coordinate_path
            moving_right_edge_path = object1_right_edge_path if object1_has_moved else object2_right_edge_path
            # 2 cases: one for the x coordinate path and the other for the right edge path
            return_value = (CollisionsFinder.is_moving_collision(moving_x_coordinate_path, stationary_object) or
                            CollisionsFinder.is_moving_collision(moving_right_edge_path, stationary_object))

        # The other one's don't take into account if the objects are touching each other
        objects_are_touching = ((object1.x_coordinate == object2.right_edge or object2.x_coordinate == object1.right_edge)
                                and CollisionsFinder.is_height_collision(object1, object2))
        if objects_are_touching:
            # The last case where neither object has moved and is checking if the objects are touching each other
            return_value = True

        return return_value

    def is_moving_collision(moving_object_path, stationary_object):
        """ summary: Calls is_line_ellipse_collision() or is_line_rectangle_collision()
                     depending on if the stationary object is elliptical or rectangular

            params:
                moving_object_path: Path; the moving object's path
                stationary_object: GameObject; the object that isn't moving

            returns: boolean; if the moving object's path collides with the stationary object
        """

        is_collision = False
        for line in moving_object_path.get_lines():
            if type(stationary_object) == Ellipse:
                is_collision = CollisionsFinder.is_line_ellipse_collision(stationary_object, line)

            # Assumes that if it isn't an ellipse it must be a rectangle
            else:
                is_collision = CollisionsFinder.is_line_rectangle_collision(stationary_object, line)

            if is_collision:
                break

        return is_collision

    def is_line_rectangle_collision(rectangle: GameObject, line: LineSegment):
        """returns: boolean; if the line and the rectangle have collided"""

        rectangle_lines = [
            LineSegment(Point(rectangle.x_coordinate, rectangle.y_coordinate), Point(rectangle.x_coordinate, rectangle.bottom)),
            LineSegment(Point(rectangle.x_coordinate, rectangle.bottom), Point(rectangle.right_edge, rectangle.bottom)),
            LineSegment(Point(rectangle.right_edge, rectangle.bottom), Point(rectangle.right_edge, rectangle.y_coordinate)),
            LineSegment(Point(rectangle.right_edge, rectangle.y_coordinate), Point(rectangle.x_coordinate, rectangle.y_coordinate))
        ]

        return_value = False

        for rectangle_line in rectangle_lines:
            if CollisionsFinder.is_line_collision(rectangle_line, line):
                return_value = True
                break

        return return_value

    def is_line_ellipse_collision(ellipse: Ellipse, line: LineSegment):
        """returns: boolean; if the line and the ellipse have collided"""

        # I'm using c in place of b since I have two b's one from the ellipse and the other from the line
        h, k, a, c = ellipse.get_equation_variables()

        m, b = line.slope, line.y_intercept

        # See documentation.md for where these numbers came from
        # quadratic_a = -(pow(a, 2) * pow(c, 2) - (pow(a, 2) * pow(m, 2) + pow(c, 2)))
        # quadratic_b = -2 * (pow(a, 2) * (b - k) * m - pow(c, 2) * h)
        # quadratic_c = -pow(a, 2) * (pow(b, 2) - 2 * b * k + pow(k, 2)) - pow(c, 2) * pow(h, 2)
        quadratic_a = pow(a, 2) * pow(m, 2) + pow(c, 2)
        quadratic_b = 2 * (pow(a, 2) * (b - k) * m - pow(c, 2) * h)
        quadratic_c = pow(a, 2) * pow(b - k, 2) + pow(c, 2) * pow(h, 2) - pow(a, 2) * pow(c, 2)

        answers = solve_quadratic(quadratic_a, quadratic_b, quadratic_c)
        return_value = True
        # solve_quadratic returns False if it gets an imaginary number meaning there isn't a collision
        if not answers:
            return_value = False

        else:
            x_coordinate1, x_coordinate2 = answers
            y_coordinate1, y_coordinate2 = line.get_y_coordinate(x_coordinate1), line.get_y_coordinate(x_coordinate2)
            return_value = line.contains_point(Point(x_coordinate1, y_coordinate1), 1) or line.contains_point(Point(x_coordinate2, y_coordinate2), 1)

        return return_value

    def is_path_collision(path1: Path, path2: Path):
        """returns: boolean; if the two paths have collided"""

        return_value = False

        path1_lines = path1.get_lines()
        path2_lines = path2.get_lines()

        for line1 in path1_lines:
            for line2 in path2_lines:
                if CollisionsFinder.is_line_collision(line1, line2):
                    return_value = True
                    break

        return return_value

    def get_line_collision_point(line1, line2):
        """returns: Point; the point at which line1 and line2 collide (None if they don't collide)"""

        # If the lines are parallel they couldn't have collided
        if line1.slope == line2.slope:
            return None

        x_collision_point = (line2.y_intercept - line1.y_intercept) / (line1.slope - line2.slope)
        collision_point = Point(x_collision_point, line1.get_y_coordinate(x_collision_point))

        # If one of the line segments doesn't contain that collision point then the lines couldn't have collided
        if not line1.contains_point(collision_point, 1) or not line2.contains_point(collision_point, 1):
            collision_point = None

        return collision_point

    def is_line_collision(line1: LineSegment, line2: LineSegment):
        """returns: boolean; if the two lines have crossed"""

        return CollisionsFinder.get_line_collision_point(line1, line2) is not None

    def get_path_line_collision_point(line: LineSegment, path: Path):
        """returns: Point; the x and y coordinate at which the line and path collide (None if they don't collide)"""

        collision_point = None

        for path_line in path.get_lines():
            collision_point = CollisionsFinder.get_line_collision_point(path_line, line)

            if collision_point is not None:
                break

        return collision_point

    def is_height_collision(object1, object2):
        """ summary: finds out if the object's y_coordinates have collided

            params:
                object1: GameObject; one of the objects that is used to see if the two objects provided have collided
                object2: GameObject; one of the objects that is used to see if the two objects provided have collided

            returns: boolean; if one of the object's y coordinates is within the other's y coordinates
        """

        return (object1.bottom >= object2.y_coordinate and
                object1.y_coordinate <= object2.bottom)

    def is_length_collision(object1, object2):
        """ summary: finds out if the object's x coordinates have collided

            params:
                object1: GameObject; one of the objects that is used to see if the two objects provided have collided
                object2: GameObject; one of the objects that is used to see if the two objects provided have collided

            returns: boolean; if one of the object's x coordinates is within the other's x coordinates
        """

        return (object1.x_coordinate <= object2.right_edge and
                object1.right_edge >= object2.x_coordinate)

    def sim_collision(object1, object2):
        return CollisionsFinder.is_height_collision(object1, object2) and CollisionsFinder.is_length_collision(object1, object2)

    def get_bottommost_object(object1, object2):
        """ summary: finds the object whose y_coordinate is the biggest (top of the screen is 0)

              params:
                 object1: GameObject; one of the objects that is used to see if the two objects provided have collided
                 object2: GameObject; one of the objects that is used to see if the two objects provided have collided

              returns: GameObject; the object that is on the bottom of the screen
         """
        return object1 if object1.y_coordinate > object2.y_coordinate else object2

    def get_topmost_object(object1, object2):
        """ summary: finds the object whose y_coordinate is the smallest (top of the screen is 0)

             params:
                object1: GameObject; one of the objects that is used to see if the two objects provided have collided
                object2: GameObject; one of the objects that is used to see if the two objects provided have collided

             returns: GameObject; the object that is on the top of the screen
        """

        return object1 if object1.y_coordinate < object2.y_coordinate else object2
    
    def is_bottom_collision(object1, object2):
        """ summary: finds out if the object's collided from the bottom
            
            params: 
                object1: GameObject; one of the objects that is used to see if the two objects provided have collided
                object2: GameObject; one of the objects that is used to see if the two objects provided have collided
            
            returns: boolean; if the object's collided from the bottom
        """
        
        prev_object1 = HistoryKeeper.get_last(object1.name)
        prev_object2 = HistoryKeeper.get_last(object2.name)

        if prev_object1 is None or prev_object2 is None:
            # print("ERROR NO PREVIOUS GAME OBJECTS FOUND")
            return False

        prev_bottom_object = CollisionsFinder.get_bottommost_object(prev_object1, prev_object2)
        prev_top_object = CollisionsFinder.get_topmost_object(prev_object1, prev_object2)

        top_object = CollisionsFinder.get_topmost_object(object1, object2)
        bottom_object = CollisionsFinder.get_bottommost_object(object1, object2)

        return (CollisionsFinder.is_collision(object1, object2)
                and prev_bottom_object.y_coordinate > prev_top_object.bottom and bottom_object.y_coordinate <= top_object.bottom)

    def is_top_collision(object1, object2):
        """ summary: finds out if the object's collided from the bottom

            params:
                object1: GameObject; one of the objects that is used to see if the two objects provided have collided
                object2: GameObject; one of the objects that is used to see if the two objects provided have collided

            returns: boolean; if the object's collided from the bottom
        """

        prev_object1 = HistoryKeeper.get_last(object1.name)
        prev_object2 = HistoryKeeper.get_last(object2.name)

        if prev_object1 is None or prev_object2 is None:
            # print("ERROR NO PREVIOUS GAME OBJECTS FOUND")
            return False

        prev_bottom_object = CollisionsFinder.get_bottommost_object(prev_object1, prev_object2)
        prev_top_object = CollisionsFinder.get_topmost_object(prev_object1, prev_object2)

        top_object = CollisionsFinder.get_topmost_object(object1, object2)
        bottom_object = CollisionsFinder.get_bottommost_object(object1, object2)

        return (CollisionsFinder.is_collision(object1, object2)
                and prev_top_object.bottom < prev_bottom_object.y_coordinate and top_object.bottom >= bottom_object.y_coordinate)
        
        