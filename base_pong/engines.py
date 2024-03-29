from copy import deepcopy

from base_pong.ball import Ball
from base_pong.drawable_objects import GameObject, Ellipse
from base_pong.engine_utility_classes import CollisionsUtilityFunctions, CollisionData
from base_pong.equations import Point, LineSegment
from base_pong.path import Path, ObjectPath
from base_pong.utility_classes import HistoryKeeper
from base_pong.utility_functions import rounded

class CollisionsFinder:
    """Gives a series of methods to find if two (or more objects) have collided"""

    objects_to_data = {}

    # Simple Collision Code I put in to ensure that the collisions don't break as often 11/25/2023 (added much after project
    # development to ensure the game was still playable)

    def is_height_collision(object1, object2):
        return (object1.bottom >= object2.y_coordinate and
                object1.y_coordinate <= object2.bottom)

    def is_length_collision(object1, object2):
        return (object1.x_coordinate <= object2.right_edge and
                object1.right_edge >= object2.x_coordinate)

    @staticmethod
    def is_box_collision(object1, object2):
        """:returns: bool; whether object1 and object2 have collided vertically and horizontally (box collision)"""

        return CollisionsFinder.is_length_collision(object1, object2) and CollisionsFinder.is_height_collision(object1, object2)

    @staticmethod
    def simple_is_left_collision(object1, object2, is_collision=None, last_time=None):
        """ :returns: bool; if object1 has collided with object2's left edge"""

        objects_are_touching = object1.right_edge == object2.x_coordinate and CollisionsFinder.is_height_collision(
            object1, object2)
        is_moving_left_collision = CollisionsFinder.simple_is_moving_left_collision(object1, object2, is_collision, last_time)

        return is_moving_left_collision or objects_are_touching

    @staticmethod
    def simple_is_right_collision(object1, object2, is_collision=None, last_time=None):
        """:returns: bool; if object1 has collided with object2's right_edge"""

        is_moving_right_collision = CollisionsFinder.simple_is_moving_right_collision(object1, object2, is_collision,
                                                                               last_time)

        objects_are_touching = object1.x_coordinate == object2.right_edge and CollisionsFinder.is_height_collision(
            object1, object2)

        return is_moving_right_collision or objects_are_touching

    @staticmethod
    def simple_is_moving_right_collision(object1, object2, is_collision=None, last_time=None):
        """ :returns: bool; if object1 has collided with object2's right_edge because one of the objects has moved
            (the object1 did not collide with object2 horizontally last cycle)"""

        prev_object1 = HistoryKeeper.get_last(object1.name)
        prev_object2 = HistoryKeeper.get_last(object2.name)

        if prev_object1 is None or prev_object2 is None:
            return False

        is_collision = is_collision if is_collision is not None else CollisionsFinder.is_box_collision(object1, object2)
        object1_has_moved_into_object2 = (
                prev_object1.x_coordinate > prev_object2.right_edge and object1.x_coordinate < object2.right_edge)

        return is_collision and object1_has_moved_into_object2

    @staticmethod
    def simple_is_moving_left_collision(object1, object2, is_collision=None, last_time=None):
        """ :returns: bool; if object1 has hit object2's x_coordinate because one of the objects has moved
            (the object1 did not collide with object2 horizontally last cycle)"""

        prev_object1 = HistoryKeeper.get_last(object1.name)
        prev_object2 = HistoryKeeper.get_last(object2.name)

        if prev_object1 is None or prev_object2 is None:
            return False

        is_collision = is_collision if is_collision is not None else CollisionsFinder.is_box_collision(object1, object2)

        object1_has_moved_into_object2 = prev_object1.right_edge < prev_object2.x_coordinate and object1.right_edge > object2.x_coordinate
        return is_collision and object1_has_moved_into_object2

    @staticmethod
    def simple_is_bottom_collision(object1, object2, is_collision=None, time=None):
        """ :returns: bool; whether object1 has collided with object2's bottom
        """

        prev_object1 = HistoryKeeper.get_last(object1.name)
        prev_object2 = HistoryKeeper.get_last(object2.name)

        if prev_object1 is None or prev_object2 is None:
            return False

        objects_are_touching = object1.y_coordinate == object2.bottom and CollisionsFinder.is_length_collision(
            object1,
            object2)
        is_collision = is_collision if is_collision is not None else CollisionsFinder.is_collision(object1, object2)

        # Meaning that it isn't the bottom object anymore
        return (is_collision and prev_object1.y_coordinate > prev_object2.bottom and
                object1.y_coordinate < object2.bottom) or objects_are_touching

    @staticmethod
    def simple_is_top_collision(object1, object2, is_collision=None, time=None):
        """:returns: bool; whether object1 has collided with object2's y_coordinate"""

        prev_object1 = HistoryKeeper.get_last(object1.name)
        prev_object2 = HistoryKeeper.get_last(object2.name)

        if prev_object1 is None or prev_object2 is None:
            return False

        # So rounding doesn't cause any issues
        objects_are_touching = int(object1.bottom) == int(
            object2.y_coordinate) and CollisionsFinder.is_length_collision(object1, object2)
        is_collision = is_collision if is_collision is not None else CollisionsFinder.is_collision(object1, object2)

        # Meaning that it isn't the bottom object anymore
        return (is_collision and prev_object1.bottom < prev_object2.y_coordinate
                and object1.bottom > object2.y_coordinate) or objects_are_touching

    @staticmethod
    def simple_is_bottom_collision(object1, object2, is_collision=None, time=None):
        """ :returns: bool; whether object1 has collided with object2's bottom
        """

        prev_object1 = HistoryKeeper.get_last(object1.name)
        prev_object2 = HistoryKeeper.get_last(object2.name)

        if prev_object1 is None or prev_object2 is None:
            return False

        objects_are_touching = object1.y_coordinate == object2.bottom and CollisionsFinder.is_length_collision(
            object1,
            object2)
        is_collision = is_collision if is_collision is not None else CollisionsFinder.is_collision(object1, object2)

        # Meaning that it isn't the bottom object anymore
        return (is_collision and prev_object1.y_coordinate > prev_object2.bottom and
                object1.y_coordinate < object2.bottom) or objects_are_touching

    @staticmethod
    def simple_is_top_collision(object1, object2, is_collision=None, time=None):
        """:returns: bool; whether object1 has collided with object2's y_coordinate"""

        prev_object1 = HistoryKeeper.get_last(object1.name)
        prev_object2 = HistoryKeeper.get_last(object2.name)

        if prev_object1 is None or prev_object2 is None:
            return False

        # So rounding doesn't cause any issues
        objects_are_touching = int(object1.bottom) == int(
            object2.y_coordinate) and CollisionsFinder.is_length_collision(object1, object2)
        is_collision = is_collision if is_collision is not None else CollisionsFinder.is_collision(object1, object2)

        # Meaning that it isn't the bottom object anymore
        return (is_collision and prev_object1.bottom < prev_object2.y_coordinate
                and object1.bottom > object2.y_coordinate) or objects_are_touching

    # End code that I added on 11/25/2023 to faithfully "restore" the project into a working state

    def is_collision(object1, object2):
        # Old Code Below before switching to simpler (and more "robust" code)
        CollisionsFinder.update_data(object1, object2)
        return CollisionsFinder.objects_to_data.get(f"{id(object1)} {id(object2)}").is_collision

    def is_moving_collision(object1, object2):
        CollisionsFinder.update_data(object1, object2)
        return CollisionsFinder.objects_to_data.get(f"{id(object1)} {id(object2)}").is_moving_collision

    def is_left_collision(object1, object2):
        """ returns: boolean; if object1 has hit object2's x_coordinate"""

        CollisionsFinder.update_data(object1, object2)
        collision_data: CollisionData = CollisionsFinder.get_collision_data(object1, object2)
        return collision_data.is_moving_collision and collision_data.is_left_collision

    def get_collision_data(object1, object2) -> CollisionData:
        """returns: CollisionData; the data for the collision for 'object1' and 'object2'"""
        return CollisionsFinder.objects_to_data.get(f"{id(object1)} {id(object2)}")

    def get_objects_xy(object1, object2):
        """returns: List of Point; [object1's xy, object2's xy]"""
        CollisionsFinder.update_data(object1, object2)
        return [CollisionsFinder.get_collision_data(object1, object2).object_xy,
                CollisionsFinder.get_collision_data(object2, object1).object_xy]

    def is_right_collision(object1, object2):
        """returns: boolean; if object1 has collided with object2's right_edge"""

        CollisionsFinder.update_data(object1, object2)
        collision_data: CollisionData = CollisionsFinder.objects_to_data.get(f"{id(object1)} {id(object2)}")
        return collision_data.is_moving_collision and collision_data.is_right_collision

    def make_dimensions_match(prev_object, current_object):
        """Makes the height and length of the objects match; changes prev_object to match current_object"""

        height_difference = current_object.height - prev_object.height
        length_difference = current_object.length - prev_object.length

        prev_object.height = current_object.height
        prev_object.length = current_object.length
        prev_object.x_coordinate -= length_difference
        prev_object.y_coordinate -= height_difference

    def update_data(object1: GameObject, object2: GameObject):
        """ summary: uses get_x_coordinates() and get_y_coordinates_from_x_coordinate() (methods from GameObject)
            to check if the objects share a point(s) (x_coordinate, y_coordinate)

            params:
                object1: GameObject; one of the objects that is used to see if the two objects provided have collided
                object2: GameObject; one of the objects that is used to see if the two objects provided have collided

            returns: boolean; if the two objects provided have collided
        """

        prev_object1 = HistoryKeeper.get_last(object1.name)
        prev_object2 = HistoryKeeper.get_last(object2.name)

        # Prevents None Type Error and saving these coordinates because they have to be modified if the length or height of the object has changed
        prev_object1_dimensions = [prev_object1.x_coordinate, prev_object1.y_coordinate, prev_object1.length, prev_object1.height] if prev_object1 is not None else [0,0,0,0]
        prev_object2_dimensions = [prev_object2.x_coordinate, prev_object2.y_coordinate, prev_object2.length, prev_object2.height] if prev_object2 is not None else [0,0,0,0]

        object1_has_moved, object2_has_moved = False, False

        if prev_object1 is None or prev_object2 is None:
            # There couldn't have been a collision since both either object1 or object2 didn't exist before this, so
            # objects_to_data should reflect that there is no collision
            CollisionsFinder.objects_to_data[f"{id(object2)} {id(object1)}"] = CollisionData(False, False, False, (0, 0), (0, 0))
            CollisionsFinder.objects_to_data[f"{id(object1)} {id(object2)}"] = CollisionData(False, False, False, (0, 0), (0, 0))
            return

        else:
            CollisionsFinder.make_dimensions_match(prev_object1, object1)
            CollisionsFinder.make_dimensions_match(prev_object2, object2)
            object1_has_moved = CollisionsFinder.object_has_moved(prev_object1, object1)
            object2_has_moved = CollisionsFinder.object_has_moved(prev_object2, object2)
        # if CollisionsFinder.objects_to_data.__contains__(f"{id(object1)} {id(object2)}"):
        #     return


        object1_path = ObjectPath(prev_object1, object1)
        object2_path = ObjectPath(prev_object2, object2)
        collision_time = -1
        is_moving_collision = False
        
        if object2_has_moved and object1_has_moved:
            # 4 cases because there are two paths for the objects - 2^2 possible combinations
            collision_time = CollisionsUtilityFunctions.get_path_collision_time(object1_path, object2_path)
            # If the time is functionally zero it can be discounted
            # if is_within_range(0, collision_time, pow(10, -6)):
            #     collision_time = -1
            is_moving_collision = collision_time != -1

        elif object2_has_moved or object1_has_moved:
            stationary_object = object1 if not object1_has_moved else object2
            moving_object_path = object1_path if object1_has_moved else object2_path
            # 2 cases: one for the x coordinate path and the other for the right edge path
            collision_time = CollisionsUtilityFunctions.get_moving_collision_time(moving_object_path, stationary_object)

            # If they started out touching then it was not a moving collision; they were already collided beforehand
            if CollisionsFinder.objects_are_touching(prev_object1, prev_object2):
                collision_time = -1

            is_moving_collision = collision_time != -1

        if CollisionsFinder.objects_are_touching(object1, object2):
            # The last case where neither object has moved and is checking if the objects are touching each other
            collision_time = 0

        CollisionsFinder.objects_to_data[f"{id(object1)} {id(object2)}"] = CollisionsUtilityFunctions.get_collision_data(object1, object2, collision_time, is_moving_collision)
        CollisionsFinder.objects_to_data[f"{id(object2)} {id(object1)}"] = CollisionsUtilityFunctions.get_collision_data(object2, object1, collision_time, is_moving_collision)

        prev_object1.x_coordinate, prev_object1.y_coordinate, prev_object1.length, prev_object1.height = prev_object1_dimensions
        prev_object2.x_coordinate, prev_object2.y_coordinate, prev_object2.length, prev_object2.height = prev_object2_dimensions

    def objects_are_touching(object1, object2):
        """returns: booolean; if the objects are touching"""

        objects_were_touching_horizontally = (object1.x_coordinate == object2.right_edge or
                                              object2.x_coordinate == object1.right_edge) and CollisionsFinder.is_height_collision(object1, object2)
        objects_were_touching_vertically = (object1.y_coordinate == object2.bottom or
                                            object2.y_coordinate == object1.bottom) and CollisionsFinder.is_length_collision(object1, object2)

        return objects_were_touching_horizontally or objects_were_touching_vertically

    def is_a_bottom_collision(object1, object2):
        """returns: boolean; if either object1 or object2 collided with the other one's bottom"""

        return CollisionsFinder.is_bottom_collision(object1, object2) or CollisionsFinder.is_bottom_collision(object2, object1)

    def is_a_top_collision(object1, object2):
        """returns: boolean; if either object1 or object2 collided with the other one's top"""

        return CollisionsFinder.is_top_collision(object1, object2) or CollisionsFinder.is_top_collision(object2, object1)

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
            print("ERROR NO PREVIOUS GAME OBJECTS FOUND")
            return False
        
        return (CollisionsFinder.is_collision(object1, object2) and prev_object1.y_coordinate > prev_object2.bottom and
                object1.y_coordinate <= object2.bottom) # Meaning that it isn't the bottom object anymore

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
            print("ERROR NO PREVIOUS GAME OBJECTS FOUND")
            return False

        return (CollisionsFinder.is_collision(object1, object2) and prev_object1.bottom < prev_object2.y_coordinate
                and object1.bottom > object2.y_coordinate) # Meaning that it isn't the bottom object anymore

    def get_path_line_collision(path, line):
        """returns: Point; the point with the smallest x coordinate in CollisionUtilityFunctions.get_path_line_collision_points()"""

        smallest_point = None
        smallest_x_coordinate = float("inf")
        for point in CollisionsUtilityFunctions.get_path_line_collision_point(line, path):
            if point.x_coordinate < smallest_x_coordinate:
                smallest_point = point
                smallest_x_coordinate = point.x_coordinate
        return smallest_point

    def is_line_ellipse_collision(line, ellipse):
        return len(CollisionsUtilityFunctions.get_line_ellipse_collision_points(line, ellipse)) != 0

    def object_has_moved(prev_obect, object):
        """returns: boolean; if the object has moved"""

        # Have to round the numbers otherwise there is a weird python rounding thing with floats
        return (rounded(prev_obect.x_coordinate - object.x_coordinate, 4) != 0 or
                rounded(prev_obect.y_coordinate - object.y_coordinate, 4) != 0)




        