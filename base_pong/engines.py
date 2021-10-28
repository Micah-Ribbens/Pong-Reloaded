from base_pong.UtilityClasses import HistoryKeeper
from base_pong.important_variables import (
    screen_height,
    screen_length
)

class CollisionDirection:
    is_collision = False
    is_right = False
    def __init__(self, is_collision, is_right):
        self.is_collision = is_collision
        self.is_right = is_right
class CollisionsFinder:
    def is_collision(object1, object2):
        return (CollisionsFinder.is_x_collision(object1, object2) 
                and CollisionsFinder.object_height_collision(object1, object2))
    def ball_collisions(ball, paddle):
        if not CollisionsFinder.is_collision(ball, paddle):
            return
        
        ball.color = paddle.outline_color
        ball.forwards_velocity *= paddle.power / 10

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
                object1.right_edge > object2.x_coordinate)
    def is_left_collision(object1, object2):
        prev_object1 = HistoryKeeper.get_last(object1.name)
        prev_object2 = HistoryKeeper.get_last(object2.name)
        if prev_object1 is None or prev_object2 is None:
             return False
        return (prev_object1.x_coordinate > prev_object2.x_midpoint and 
                object1.x_coordinate < object2.right_edge)
    
    def object_height_collision(object1, object2):
        return (object1.bottom >= object2.y_coordinate and
                object1.y_coordinate <= object2.bottom)
    
    def is_x_collision(object1, object2):
        return (CollisionsFinder.is_left_collision(object1, object2) 
                or CollisionsFinder.is_right_collision(object1, object2)
                or object1.x_coordinate == object2.right_edge
                or object2.x_coordinate == object1.right_edge)
    

class CollisionsEngine:
    def ball_collisions(ball, paddle1, paddle2):
        CollisionsFinder.ball_collisions(ball, paddle1)
        CollisionsFinder.ball_collisions(ball, paddle2)

    def paddle_movements(paddle):
        paddle.can_move_down = False if paddle.bottom >= screen_height else True
        paddle.can_move_up = False if paddle.y_coordinate <= 0 else True
        paddle.can_move_right = False if paddle.right_edge >= screen_length else True
        paddle.can_move_left = False if paddle.x_coordinate <= 0 else True
        if paddle.y_coordinate <= 0:
            paddle.y_coordinate = 0

        if paddle.bottom >= screen_height:
            paddle.y_coordinate = screen_height - paddle.height
        




        
