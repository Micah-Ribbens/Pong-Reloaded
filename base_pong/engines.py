from base_pong.ball import Ball
from base_pong.drawable_objects import GameObject
from base_pong.utility_classes import HistoryKeeper
from base_pong.important_variables import (
    screen_height,
    screen_length
)
from base_pong.utility_functions import lists_share_an_item

# TODO make collisions better
class CollisionsFinder:
    """Gives a series of methods to find if two (or more objects) have collided"""
    def is_right_collision(object1, object2):
        """ summary: uses CollisionsFinder.is_collision() to check if there was a collision and HistoryKeeper to
            get the objects from the previous cycle

            params: 
                object1: GameObject; one of the objects that is used to see if the two objects provided have collided
                object2: GameObject; one of the objects that is used to see if the two objects provided have collided

            returns: boolean; if the object1 was previously to the left of object2, but now isn't and if the objects have collided
        """

        prev_object1 = HistoryKeeper.get_last(object1.name)
        prev_object2 = HistoryKeeper.get_last(object2.name)

        if prev_object1 is None or prev_object2 is None:
            # Don't want to actually abort the code if this happens since it does on the first cycle; but it is a message to fix something
            print("ERROR NO PREVIOUS GAME OBJECTS FOUND")
            return False

        return prev_object1.right_edge < prev_object2.right_edge and CollisionsFinder.is_collision(object1, object2)

    def is_left_collision(object1, object2):
        """ summary: uses CollisionsFinder.is_collision() to check if there was a collision and HistoryKeeper to
            get the objects from the previous cycle

            params: 
                object1: GameObject; one of the objects that is used to see if the two objects provided have collided
                object2: GameObject; one of the objects that is used to see if the two objects provided have collided

            returns: boolean; if the object1 was previously to the right of object2, but now isn't and if the objects have collided
        """

        prev_object1 = HistoryKeeper.get_last(object1.name)
        prev_object2 = HistoryKeeper.get_last(object2.name)
        if prev_object1 is None or prev_object2 is None:
            # Don't want to actually abort the code if this happens since it does on the first cycle; but it is a message to fix something
            print("ERROR NO PREVIOUS GAME OBJECTS FOUND")
            return False
        return prev_object1.x_coordinate > prev_object2.x_coordinate and CollisionsFinder.is_collision(object1, object2)

    def is_collision(object1: GameObject, object2: GameObject):
        """ summary: uses get_x_coordinates() and get_y_coordinates_from_x_coordinate() (methods from GameObject)
            to check if the objects share a point(s) (x_coordinate, y_coordinate)

            params: 
                object1: GameObject; one of the objects that is used to see if the two objects provided have collided
                object2: GameObject; one of the objects that is used to see if the two objects provided have collided

            returns: boolean; if the two objects provided have collided        
        """
        object1_x_coordinates = object1.get_x_coordinates()
        object2_x_coordinates = object2.get_x_coordinates()

        is_collision = False
        for x_coordinate in object1_x_coordinates:
            if not object2_x_coordinates.__contains__(x_coordinate):
                continue

            is_y_coordinate_collision = (object1.get_y_coordinate_max(x_coordinate) >= object2.get_y_coordinate_min(x_coordinate)
                                         and object1.get_y_coordinate_min(x_coordinate) <= object2.get_y_coordinate_max(x_coordinate))

            # If the two object's share an x_coordinate and a y_coordinate then they must have collided
            if is_y_coordinate_collision:
                is_collision = True
                break

        return is_collision

    def is_height_collision(object1, object2):
        """ summary: finds out if the object's y_coordinates have collided

            params:
                object1: GameObject; one of the objects that is used to see if the two objects provided have collided
                object2: GameObject; one of the objects that is used to see if the two objects provided have collided

            returns: boolean; if the two object's y_coordinates have collided
        """

        return (object1.bottom >= object2.y_coordinate and
                object1.y_coordinate <= object2.bottom)

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
            print("ERROR NO PREVIOUS GAME OBJECTS FOUND")
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
            print("ERROR NO PREVIOUS GAME OBJECTS FOUND")
            return False

        prev_bottom_object = CollisionsFinder.get_bottommost_object(prev_object1, prev_object2)
        prev_top_object = CollisionsFinder.get_topmost_object(prev_object1, prev_object2)

        top_object = CollisionsFinder.get_topmost_object(object1, object2)
        bottom_object = CollisionsFinder.get_bottommost_object(object1, object2)

        return (CollisionsFinder.is_collision(object1, object2)
                and prev_top_object.bottom < prev_bottom_object.y_coordinate and top_object.bottom >= bottom_object.y_coordinate)
        
        