from ball import Ball
from important_variables import (
    screen_height
)


class CollisionsFinder:
    def object_collision(object1, object2):
        return (CollisionsFinder.object_length_collision(object1, object2)
                and CollisionsFinder.object_height_collision(object1, object2))
    
    def object_length_collision(object1, object2):
        return (object1.x_coordinate <= object2.right_edge and
                object1.right_edge >= object2.x_coordinate)
    
    def object_height_collision(object1, object2):
        return (object1.bottom >= object2.y_coordinate and
                object1.y_coordinate <= object2.bottom)

class CollisionsEngine:
    def ball_collisions(ball: Ball, paddle1, paddle2):
        is_collision = CollisionsFinder.object_collision(ball, paddle1) or CollisionsFinder.object_collision(ball, paddle2)
        if is_collision:
            ball.is_moving_right = not ball.is_moving_right
            ball.velocity *= 1.1
        
        if ball.y_coordinate <= 0 or ball.bottom >= screen_height:
            ball.is_moving_down = not ball.is_moving_down

    def paddle_movements(paddle):
        if paddle.y_coordinate <= 0:
            paddle.y_coordinate = 0
            paddle.can_move_up = False
        else:
            paddle.can_move_up = True
        if paddle.bottom >= screen_height:
            paddle.y_coordinate = screen_height - paddle.height
            paddle.can_move_down = False
        else:
            paddle.can_move_down = True


        
