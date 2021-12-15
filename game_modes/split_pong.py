from base_pong.utility_classes import HistoryKeeper
from base_pong.engines import CollisionsFinder
from base_pong.ball import Ball
from game_modes.game_mode import PongType
from game_modes.normal_pong import NormalPong
from base_pong.score_keeper import ScoreKeeper
from copy import deepcopy


class SplitPong(PongType):
    balls = []
    base_ball_length = 0

    def increase_ball_size(ball):
        ball.length += (SplitPong.base_ball_length * .2)
        ball.height += (SplitPong.base_ball_length * .2)

    def ball_is_ready_to_split(ball):
        return ball.length >= SplitPong.base_ball_length * 2

    def split(ball: Ball, new_balls, ball_has_collided_with_paddle1):
        SplitPong.reset_ball(ball)
        new_ball: Ball = deepcopy(ball)
        new_ball.is_moving_down = not ball.is_moving_down
        new_ball.forwards_velocity *= 1.1
        distance_change = new_ball.forwards_velocity * .1

        new_ball.is_moving_right = True if ball_has_collided_with_paddle1 else False

        new_ball.x_coordinate += distance_change if ball_has_collided_with_paddle1 else -distance_change
        new_balls.append(new_ball)

    def ball_collisions(ball, paddle1, paddle2):
        new_balls = []
        for ball in SplitPong.balls:
            NormalPong.ball_collisions(ball, paddle1, paddle2)
            ball.draw()
            ball_has_collided_with_paddle1 = CollisionsFinder.is_collision(
                ball, paddle1)
            ball_has_collided_with_paddle2 = CollisionsFinder.is_collision(
                ball, paddle2)
            ball_has_collided = ball_has_collided_with_paddle1 or ball_has_collided_with_paddle2
            HistoryKeeper.add(ball_has_collided,
                              f"ball_has_collided{id(ball)}", False)

            # Makes sure that the ball doesn't collide into the same paddle mulitple times
            if not HistoryKeeper.get_last(f"ball_has_collided{id(ball)}") and ball_has_collided:
                SplitPong.increase_ball_size(ball)

            if SplitPong.ball_is_ready_to_split(ball):
                SplitPong.split(ball, new_balls,
                                ball_has_collided_with_paddle1)

        for new_ball in new_balls:
            ball_has_collided = SplitPong.ball_has_collided(
                ball, paddle1, paddle2)
            HistoryKeeper.add(ball_has_collided,
                              f"ball_has_collided{id(ball)}", False)
            SplitPong.balls.append(new_ball)

    def ball_has_collided(ball, paddle1, paddle2):
        return CollisionsFinder.is_collision(ball, paddle1) or CollisionsFinder.is_collision(ball, paddle2)

    def run(ball, paddle1, paddle2):
        if len(SplitPong.balls) == 0:
            SplitPong.balls.append(ball)

        for ball in SplitPong.balls:
            NormalPong.ball_movement(ball)
            ScoreKeeper.figure_out_scoring(ball)

    def reset(ball, paddle1, paddle2):
        # Meaning the base ball length has not been assigned yet
        if SplitPong.base_ball_length == 0:
            SplitPong.base_ball_length = ball.length

        SplitPong.balls = [ball]
        SplitPong.reset_ball(ball)

    def reset_ball(ball):
        ball.length = SplitPong.base_ball_length
        ball.height = SplitPong.base_ball_length
        ball.forwards_velocity = ball.base_forwards_velocity

    # The code draws multiple balls, so it doesn't need a singular ball,
    # But since it inherits the method from game_modes which has 3 parameters
    # It needs 3 parameters
    def draw_game_objects(unneeded_ball, paddle1, paddle2):
        paddle1.draw()
        paddle2.draw()
        for ball in SplitPong.balls:
            ball.draw()
