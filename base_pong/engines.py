from base_pong.drawable_objects import GameObject
from base_pong.utility_classes import HistoryKeeper
from base_pong.important_variables import (
    screen_height,
    screen_length
)
from base_pong.utility_functions import lists_share_an_item


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
            # The objects couldn't have collided at that point if object2 doesn't have object1's x_coordinate
            if not object2_x_coordinates.__contains__(x_coordinate):
                continue

            object1_y_coordinates = object1.get_y_coordinates_from_x_coordinate(
                x_coordinate)
            object2_y_coordinates = object2.get_y_coordinates_from_x_coordinate(
                x_coordinate)

            # If the two object's share an x_coordinate and a y_coordinate then they must have collided
            if lists_share_an_item(object1_y_coordinates, object2_y_coordinates):
                is_collision = True

        return is_collision
