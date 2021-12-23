import pygame
from base_pong.important_variables import game_window
from base_pong.utility_classes import HistoryKeeper
from base_pong.utility_functions import percentage_to_number
from base_pong.engines import CollisionsFinder
from game_modes.game_mode import PongType
from game_modes.normal_pong import NormalPong
from base_pong.important_variables import *
from base_pong.drawable_objects import Ellipse
from base_pong.colors import *
from base_pong.events import Event, TimedEvent

class PortalOpening(Ellipse):
    attributes = ["x_coordinate", "y_coordinate"]
    ball_exiting_direction_is_right = None
    is_enabled = True

    def __init__(self, percent_right=0, percent_down=0, percent_length=0, percent_height=0, ball_exiting_direction_is_right=False):
        x = percentage_to_number(percent_right, screen_length)
        y = percentage_to_number(percent_down, screen_height)
        length = percentage_to_number(percent_length, screen_length)
        height = percentage_to_number(percent_height, screen_height)
        self.ball_exiting_direction_is_right = ball_exiting_direction_is_right
        super().__init__(x, y, length, height, green)

    def disable(self, color):
        self.color = color
        self.is_enabled = False

    def enable(self, color):
        self.color = color
        self.is_enabled = True


class Portal:
    portal_disabled_event = None
    portal_opening1 = None
    portal_opening2 = None
    is_enabled = True
    enabled_color = None

    def __init__(self, portal_opening1, portal_opening2, color):
        portal_opening1.name = id(self.portal_opening1)
        portal_opening2.name = id(self.portal_opening2)
        self.portal_opening1 = portal_opening1
        self.portal_opening2 = portal_opening2
        self.portal_disabled_event = TimedEvent(3, False)
        self.portal_opening2.color, self.portal_opening1.color = color, color
        self.enabled_color = color

    def teleport(self, portal_end, object):
        object.x_coordinate = portal_end.x_midpoint
        object.y_coordinate = portal_end.y_midpoint
        # Could make it so ball direction is based on exiting_direction_is_right, but not doing that now

    def run(self, ball):
        # Needed for collisions; the CollisionsFinder needs to know what the object was previously
        HistoryKeeper.add(self.portal_opening1, self.portal_opening1.name, False)
        HistoryKeeper.add(self.portal_opening2, self.portal_opening2.name, False)

        # Stores value of is_enabled, which other things in this function modify
        is_enabled = self.is_enabled
        portal_opening1_collision = CollisionsFinder.is_collision(
            ball, self.portal_opening1)

        portal_opening2_collision = CollisionsFinder.is_collision(
            ball, self.portal_opening2)
        
        is_portal_collision = portal_opening1_collision or portal_opening2_collision
        self.portal_disabled_event.run(False, is_portal_collision)

        if portal_opening2_collision and is_enabled:
            self.teleport(self.portal_opening1, ball)

        if portal_opening1_collision and is_enabled:
            self.teleport(self.portal_opening2, ball)

        if self.portal_disabled_event.is_started and not self.portal_disabled_event.is_done():
            self.disable()

        # The ball shouldn't re-enable if the ball is too close to either opening
        ball_is_too_close_to_portal = is_portal_collision

        if self.portal_disabled_event.is_done() and not ball_is_too_close_to_portal:
            self.enable()
            self.portal_disabled_event.reset()

    def draw(self):
        self.portal_opening1.draw()
        self.portal_opening2.draw()

    def disable(self):
        self.portal_opening1.disable(light_gray)
        self.portal_opening2.disable(light_gray)
        self.is_enabled = False

    def enable(self):
        self.portal_opening1.enable(self.enabled_color)
        self.portal_opening2.enable(self.enabled_color)
        self.is_enabled = True


class PortalPong(PongType):
    portal_length_percent = 15
    portal_height_percent = 15
    portals = [
        Portal(
            PortalOpening(20, 20, portal_length_percent,
                          portal_height_percent, False),
            PortalOpening(80, 80, portal_length_percent,
                          portal_height_percent, True), blue
        ),
        Portal(
            PortalOpening(80, 10, portal_length_percent,
                          portal_height_percent, True),
            PortalOpening(15, 80, portal_length_percent,
                          portal_height_percent, False), green
        )

    ]

    def run(ball, paddle1, paddle2):
        NormalPong.run(ball, paddle1, paddle2)
        for portal in PortalPong.portals:
            portal.run(ball)

    def reset(ball, paddle1, paddle2):
        NormalPong.reset(ball, paddle1, paddle2)

    def ball_collisions(ball, paddle1, paddle2):
        NormalPong.ball_collisions(ball, paddle1, paddle2)

    def draw_game_objects(ball, paddle1, paddle2):
        for portal in PortalPong.portals:
            portal.draw()
        PongType.draw_game_objects(ball, paddle1, paddle2)
