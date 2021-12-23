from base_pong.velocity_calculator import VelocityCalculator
from base_pong.important_variables import *
from base_pong.engines import CollisionsEngine, CollisionsFinder
from game_modes.game_mode import PongType
from game_modes.normal_pong import NormalPong


class PhysicsEngine:
    def find_a(vertex, time_to_reach_vertex):
        return vertex/(-1*(time_to_reach_vertex ** 2))

    def distance_change(vertex, time_to_reach_vertex, current_time):
        a = PhysicsEngine.find_a(vertex, time_to_reach_vertex)
        return a * (current_time)*(current_time - time_to_reach_vertex * 2)

# TODO make it so GravityPong has tip and middle hits
class GravityPong(PongType):
    def ball_collisions(ball, paddle1, paddle2):
        CollisionsEngine.ball_collisions(ball, paddle1, paddle2)
        vertex_increase = 1.05
        max_vertex = screen_height - ball.height

        ball_has_collided = CollisionsFinder.is_collision(
            ball, paddle1) or CollisionsFinder.is_collision(ball, paddle2)

        if ball_has_collided:
            GravityPong.vertex *= vertex_increase

        vertex_is_too_big = GravityPong.vertex > max_vertex
        if vertex_is_too_big:
            GravityPong.vertex = max_vertex

    def ball_gravity(ball):
        if ball.bottom >= screen_height:
            ball.last_y_unmoving = screen_height - ball.height
            GravityPong.time_since_ground = VelocityCalculator.time
        GravityPong.time_since_ground += VelocityCalculator.time
        y_change = PhysicsEngine.distance_change(
            GravityPong.vertex, .8, GravityPong.time_since_ground)
        bottom_of_screen = screen_height - ball.height
        ball.y_coordinate = bottom_of_screen - y_change

    def run(ball, paddle1, paddle2):
        GravityPong.ball_gravity(ball)
        GravityPong.ball_collisions(ball, paddle1, paddle2)
        NormalPong.run(ball, paddle1, paddle2)

    def reset(ball, paddle1, paddle2):
        GravityPong.time_since_ground = 0
        GravityPong.vertex = screen_height // 2
