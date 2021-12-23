from base_pong.drawable_objects import GameObject
from base_pong.utility_classes import HistoryKeeper
from base_pong.important_variables import (
    screen_height,
    screen_length
)
from base_pong.utility_functions import lists_share_an_item


class CollisionsFinder:
    def is_collision(object1, object2):
        return (CollisionsFinder.is_x_collision(object1, object2)
                and CollisionsFinder.is_object_height_collision(object1, object2))

    def is_right_collision(object1, object2):
        prev_object1 = HistoryKeeper.get_last(object1.name)
        prev_object2 = HistoryKeeper.get_last(object2.name)
        if prev_object1 is None or prev_object2 is None:
            # Don't want to actually abort the code if this happens since it does on the first cycle; but it is a message to fix something
            print("ERROR NO PREVIOUS GAME OBJECTS FOUND")
            return False

        return (prev_object1.right_edge < prev_object2.right_edge and
                object1.right_edge > object2.x_coordinate) and CollisionsFinder.is_object_height_collision(object1, object2)

    def is_left_collision(object1, object2):
        prev_object1 = HistoryKeeper.get_last(object1.name)
        prev_object2 = HistoryKeeper.get_last(object2.name)
        if prev_object1 is None or prev_object2 is None:
            # Don't want to actually abort the code if this happens since it does on the first cycle; but it is a message to fix something
            print("ERROR NO PREVIOUS GAME OBJECTS FOUND")
            return False
        return (prev_object1.x_coordinate > prev_object2.x_coordinate and
                object1.x_coordinate < object2.right_edge) and CollisionsFinder.is_object_height_collision(object1, object2)

    def is_object_height_collision(object1: GameObject, object2: GameObject):
        object1_x_coordinates = object1.get_x_coordinates()
        object2_x_coordinates = object2.get_x_coordinates()

        is_collision = False
        for x_coordinate in object1_x_coordinates:
            if not object2_x_coordinates.__contains__(x_coordinate):
                continue

            object1_y_coordinates = object1.get_y_coordinates_from_x_coordinate(
                x_coordinate)
            object2_y_coordinates = object2.get_y_coordinates_from_x_coordinate(
                x_coordinate)

            if lists_share_an_item(object1_y_coordinates, object2_y_coordinates):
                is_collision = True

        return is_collision

    def is_x_collision(object1, object2):
        # TODO maybe change to contain the last two with the ==, but this is breaking something rn
        return (CollisionsFinder.is_left_collision(object1, object2)
                or CollisionsFinder.is_right_collision(object1, object2))


class CollisionsEngine:
    def paddle_ball_collisions(ball, paddle, speed_multiplier):
        if CollisionsFinder.is_collision(ball, paddle):
            ball.color = paddle.outline_color
            ball.forwards_velocity *= speed_multiplier

        if CollisionsFinder.is_left_collision(ball, paddle):
            ball.x_coordinate = paddle.right_edge
            ball.is_moving_right = True

        if CollisionsFinder.is_right_collision(ball, paddle):
            ball.x_coordinate = paddle.x_coordinate - ball.length
            ball.is_moving_right = False

    def ball_collisions(ball, paddle1, paddle2):
        CollisionsEngine.paddle_ball_collisions(
            ball, paddle1, paddle1.power / 10)
        CollisionsEngine.paddle_ball_collisions(
            ball, paddle2, paddle2.power / 10)

    def paddle_movements(paddle):
        paddle.can_move_down = False if paddle.bottom >= screen_height else True
        paddle.can_move_up = False if paddle.y_coordinate <= 0 else True
        paddle.can_move_right = False if paddle.right_edge >= screen_length else True
        paddle.can_move_left = False if paddle.x_coordinate <= 0 else True
        if paddle.y_coordinate <= 0:
            paddle.y_coordinate = 0

        if paddle.bottom >= screen_height:
            paddle.y_coordinate = screen_height - paddle.height
