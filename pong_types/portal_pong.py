import pygame
from base_pong.important_variables import game_window
from base_pong.utility_classes import HistoryKeeper
from base_pong.utility_functions import percentage_to_number
from base_pong.engines import CollisionsFinder
from pong_types.pong_type import PongType
from pong_types.normal_pong import NormalPong
from base_pong.important_variables import *
from base_pong.drawable_objects import Ellipse
from base_pong.colors import *
from base_pong.events import Event, TimedEvent

class PortalOpening(Ellipse):
    """An opening that allows objects to teleport through it"""

    attributes = ["x_coordinate", "y_coordinate"]
    ball_exiting_direction_is_right = None
    is_enabled = True

    def __init__(self, percent_right, percent_down, percent_length, percent_height, ball_exiting_direction_is_right):
        """ summary: initializes the object

            params:
                percent_right: int; the percent it is to right (percentage of screen_length)
                percent_down: int; the percent it is down (percentage of screen_height)
                percent_length: int; the length (percentage of screen_length)
                percent_height: int; the height (percentage of screen_height)
                ball_exiting_direction_is_right: boolean; the ball exits the portal going right

            returns: None
        """

        x = percentage_to_number(percent_right, screen_length)
        y = percentage_to_number(percent_down, screen_height)
        length = percentage_to_number(percent_length, screen_length)
        height = percentage_to_number(percent_height, screen_height)
        self.ball_exiting_direction_is_right = ball_exiting_direction_is_right
        super().__init__(x, y, length, height, green)

    def disable(self, color):
        """ summary: disables the portal opening
            params: None
            returns: None
        """

        self.color = color
        self.is_enabled = False

    def enable(self, color):
        """ summary: enables the portal opening
            params: None
            returns: None
        """

        self.color = color
        self.is_enabled = True


class Portal:
    """Composed of two portal openings that allows objects to teleport through them"""

    portal_disabled_event = None
    portal_opening1 = None
    portal_opening2 = None
    is_enabled = True
    enabled_color = None

    def __init__(self, portal_opening1, portal_opening2, color):
        """ summary: initializes the object

            params:
                portal_opening1: PortalOpening; the first portal opening of the portal
                portal_opening2: PortalOpening; the second portal opening of the portal
                color: tuple; the (Red, Green, Blue) values of the portal

            returns: None
        """

        portal_opening1.name = id(self.portal_opening1)
        portal_opening2.name = id(self.portal_opening2)
        self.portal_opening1 = portal_opening1
        self.portal_opening2 = portal_opening2
        self.portal_disabled_event = TimedEvent(3, False)
        self.portal_opening2.color, self.portal_opening1.color = color, color
        self.enabled_color = color

    def teleport(self, portal_end: PortalOpening, object):
        """ summary: teleports the ball to the end of the portal provided

            params:
                portal_end: PortalOpening; the end of the portal that the object will be teleported to
                object: GameObject; the object which will be teleported

            returns: None
        """

        object.x_coordinate = portal_end.x_midpoint
        object.y_coordinate = portal_end.y_midpoint
        object.is_moving_right = portal_end.ball_exiting_direction_is_right

    def run(self, ball):
        """ summary: runs all the logic for teleporting the ball

            params:
                ball: Ball; the ball of the game

            returns: None
        """

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

    def render(self):
        """ summary: renders the portal
            params: None
            returns: None
        """

        self.portal_opening1.render()
        self.portal_opening2.render()

    def disable(self):
        """ summary: disables the portal
            params: None
            returns: None
        """

        self.portal_opening1.disable(light_gray)
        self.portal_opening2.disable(light_gray)
        self.is_enabled = False

    def enable(self):
        """ summary: enables the portal
            params: None
            returns: None
        """

        self.portal_opening1.enable(self.enabled_color)
        self.portal_opening2.enable(self.enabled_color)
        self.is_enabled = True


class PortalPong(PongType):
    """Pong where there are portals"""

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
    
    def __init__(self, player1, player2, ball):
        """ summary: Initializes the PongType with the needed objects to run its methods

            params:
                player1: Paddle; the player on the leftmost side on the screen
                player2: Paddle; the player on the rightmost side on the screen
                ball: Ball; the ball that the players hit

            returns: None
        """

        super().__init__(player1, player2, ball)
        
        self.normal_pong = NormalPong(player1, player2, ball)
        
    def run(self):
        """ summary: runs all the necessary things in order for this game mode to work
            params: None
            returns: None
        """

        self.normal_pong.run()
        for portal in self.portals:
            portal.run(self.ball)
        self.draw_game_objects()
        self.add_needed_objects()

    def reset(self):
        """ summary: resets all the necessary things (called after someone scores)
            params: None
            returns: None
        """

        self.normal_pong.reset()

    def draw_game_objects(self):
        """ summary: draws everything in this game mode
            params: None
            returns: None
        """

        for portal in self.portals:
            portal.render()
        super().draw_game_objects()
    
    def add_needed_objects(self):
        """ summary: adds all the objects to the HistoryKeeper
            params: None
            returns: None
        """

        super().add_needed_objects()
        for portal in self.portals:
            HistoryKeeper.add(portal.portal_opening1, portal.portal_opening1.name, False)
            HistoryKeeper.add(portal.portal_opening2, portal.portal_opening2.name, False)

