from base_pong.ball import Ball
from base_pong.drawable_objects import GameObject, Ellipse
from base_pong.engine_utility_classes import CollisionsUtilityFunctions, CollisionData
from base_pong.equations import Point, LineSegment
from base_pong.path import Path, ObjectPath
from base_pong.utility_classes import HistoryKeeper
from base_pong.important_variables import (
    screen_height,
    screen_length
)
from base_pong.utility_functions import get_rightmost_object, get_leftmost_object
from base_pong.utility_functions import lists_share_an_item, solve_quadratic, min_value, is_within_range
from base_pong.velocity_calculator import VelocityCalculator

# TODO fix code with ball collision! At least collisions are working again for the most part! LEEEEETTTS GOOOOO!
class CollisionsFinder:
    """Gives a series of methods to find if two (or more objects) have collided"""

    objects_to_data = {}

    # def update_data(object1, object2):

    def is_collision(object1, object2):
        CollisionsFinder.update_data(object1, object2)
        return CollisionsFinder.objects_to_data.get(f"{id(object1)} {id(object2)}").is_collision

    def is_moving_collision(object1, object2):
        CollisionsFinder.update_data(object1, object2)
        return CollisionsFinder.objects_to_data.get(f"{id(object1)} {id(object2)}").is_moving_collision

    def is_left_collision(object1, object2):
        """ summary: uses CollisionsUtilityFunctions.is_collision() to check if there was a collision and HistoryKeeper to
            get the objects from the previous cycle

            params: 
                object1: GameObject; one of the objects that is used to see if the two objects provided have collided
                object2: GameObject; one of the objects that is used to see if the two objects provided have collided

            returns: boolean; if the object1 was previously to the left of object2, but now isn't and if the objects have collided
        """
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
        """ summary: uses CollisionsUtilityFunctions.is_collision() to check if there was a collision and HistoryKeeper to
            get the objects from the previous cycle

            params: 
                object1: GameObject; one of the objects that is used to see if the two objects provided have collided
                object2: GameObject; one of the objects that is used to see if the two objects provided have collided

            returns: boolean; if the object1 was previously to the right of object2, but now isn't and if the objects have collided
        """
        CollisionsFinder.update_data(object1, object2)
        collision_data: CollisionData = CollisionsFinder.objects_to_data.get(f"{id(object1)} {id(object2)}")
        return collision_data.is_moving_collision and collision_data.is_right_collision

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

        if prev_object1 is None or prev_object2 is None:
            # There couldn't have been a collision since both either object1 or object2 didn't exist before this, so
            # objects_to_data should reflect that there is no collision
            CollisionsFinder.objects_to_data[f"{id(object2)} {id(object1)}"] = CollisionData(False, False, False, (0, 0), (0, 0))
            CollisionsFinder.objects_to_data[f"{id(object1)} {id(object2)}"] = CollisionData(False, False, False, (0, 0), (0, 0))
            return

        # if CollisionsFinder.objects_to_data.__contains__(f"{id(object1)} {id(object2)}"):
        #     return

        object1_has_moved = prev_object1.x_coordinate != object1.x_coordinate or prev_object1.y_coordinate != object1.y_coordinate
        object2_has_moved = prev_object2.x_coordinate != object2.x_coordinate or prev_object2.y_coordinate != object2.y_coordinate

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

            objects_were_touching = (prev_object1.x_coordinate == prev_object2.right_edge or
                                     prev_object2.x_coordinate == prev_object1.right_edge)

            # If they started out touching then it was not a moving collision; they were already collided beforehand
            if objects_were_touching:
                collision_time = -1

            is_moving_collision = collision_time != -1

        # The other one's don't take into account if the objects are touching each other
        objects_are_touching = ((object1.x_coordinate == object2.right_edge or object2.x_coordinate == object1.right_edge)
                                and CollisionsFinder.is_height_collision(object1, object2))
        if objects_are_touching:
            # The last case where neither object has moved and is checking if the objects are touching each other
            collision_time = 0


        CollisionsFinder.objects_to_data[f"{id(object1)} {id(object2)}"] = CollisionsUtilityFunctions.get_collision_data(object1, object2, collision_time, is_moving_collision)
        CollisionsFinder.objects_to_data[f"{id(object2)} {id(object1)}"] = CollisionsUtilityFunctions.get_collision_data(object2, object1, collision_time, is_moving_collision)
        # if type(object1) == Ball:
        #     print(collision_time, is_moving_collision, CollisionsFinder.objects_to_data.get(f"{id(object1)} {id(object2)}").is_moving_collision, CollisionsFinder.objects_to_data.get(f"{id(object2)} {id(object1)}").is_moving_collision)

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
            # print("ERROR NO PREVIOUS GAME OBJECTS FOUND")
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
            # print("ERROR NO PREVIOUS GAME OBJECTS FOUND")
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

    def is_line_ellipse_equation(line, ellipse):
        return len(CollisionsUtilityFunctions.get_line_ellipse_collision_points(line, ellipse)) != 0


        