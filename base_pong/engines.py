from base_pong.utility_classes import HistoryKeeper
from base_pong.important_variables import (
    screen_height,
    screen_length
)


class CollisionsFinder:
    def is_collision(object1, object2):
        return (CollisionsFinder.is_x_collision(object1, object2)
                and CollisionsFinder.is_object_height_collision(object1, object2))

    def ball_collisions(ball, paddle, speed_multiplier):
        # So it doesn't collide two times in a row
        if CollisionsFinder.is_collision(ball, paddle):
            ball.color = paddle.outline_color
            ball.forwards_velocity *= speed_multiplier

        if CollisionsFinder.is_left_collision(ball, paddle):
            ball.x_coordinate = paddle.right_edge
            ball.is_moving_right = True
        if CollisionsFinder.is_right_collision(ball, paddle):
            ball.x_coordinate = paddle.x_coordinate - ball.length
            ball.is_moving_right = False

    def is_right_collision(object1, object2):
        prev_object1 = HistoryKeeper.get_last(object1.name)
        prev_object2 = HistoryKeeper.get_last(object2.name)
        if prev_object1 is None or prev_object2 is None:
            return False

        return (prev_object1.right_edge < prev_object2.x_midpoint and
                object1.right_edge > object2.x_coordinate) and CollisionsFinder.is_object_height_collision(object1, object2)

    def is_left_collision(object1, object2):
        prev_object1 = HistoryKeeper.get_last(object1.name)
        prev_object2 = HistoryKeeper.get_last(object2.name)
        if prev_object1 is None or prev_object2 is None:
            return False
        return (prev_object1.x_coordinate > prev_object2.x_midpoint and
                object1.x_coordinate < object2.right_edge) and CollisionsFinder.is_object_height_collision(object1, object2)

    def is_object_height_collision(object1, object2):
        return (object1.bottom >= object2.y_coordinate and
                object1.y_coordinate <= object2.bottom)

    def is_object_length_collision(object1, object2):
        return (object1.right_edge >= object2.x_coordinate
                and object1.x_coordinate <= object2.right_edge)

    def is_x_collision(object1, object2):
        return (CollisionsFinder.is_left_collision(object1, object2)
                or CollisionsFinder.is_right_collision(object1, object2)
                or object1.x_coordinate == object2.right_edge
                or object2.x_coordinate == object1.right_edge
                or CollisionsFinder.is_object_length_collision(object1, object2))


class CollisionsEngine:
    def ball_collisions(ball, paddle1, paddle2):
        CollisionsFinder.ball_collisions(ball, paddle1, paddle1.power / 10)
        CollisionsFinder.ball_collisions(ball, paddle2, paddle2.power / 10)

    def paddle_movements(paddle):
        paddle.can_move_down = False if paddle.bottom >= screen_height else True
        paddle.can_move_up = False if paddle.y_coordinate <= 0 else True
        paddle.can_move_right = False if paddle.right_edge >= screen_length else True
        paddle.can_move_left = False if paddle.x_coordinate <= 0 else True
        if paddle.y_coordinate <= 0:
            paddle.y_coordinate = 0

        if paddle.bottom >= screen_height:
            paddle.y_coordinate = screen_height - paddle.height
