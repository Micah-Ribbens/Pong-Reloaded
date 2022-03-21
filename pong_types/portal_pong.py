import random

import pygame

from base_pong.equations import Point
from base_pong.important_variables import game_window
from base_pong.path import Path, VelocityPath
from base_pong.utility_classes import HistoryKeeper
from base_pong.utility_functions import percentage_to_number
from base_pong.engines import CollisionsFinder
from pong_types.pong_type import PongType
from pong_types.normal_pong import NormalPong
from base_pong.important_variables import *
from base_pong.drawable_objects import Ellipse, GameObject
from base_pong.colors import *
from base_pong.events import Event, TimedEvent
from pong_types.utility_functions import get_random_item


class PortalOpening(Ellipse):
    """An opening that allows objects to teleport through it"""

    attributes = ["x_coordinate", "y_coordinate"]
    ball_exiting_direction_is_right = None
    is_enabled = True
    was_teleported = False

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
    portal_opening1: PortalOpening = None
    portal_opening2: PortalOpening = None
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
        # object.is_moving_right = portal_end.ball_exiting_direction_is_right

    def run(self, ball):
        """ summary: runs all the logic for teleporting the ball

            params:
                ball: Ball; the ball of the game

            returns: None
        """

        # Stores value of is_enabled, which other things in this function modify
        is_enabled = self.is_enabled
        portal_opening1_collision = CollisionsFinder.is_collision(ball, self.portal_opening1)

        portal_opening2_collision = CollisionsFinder.is_collision(ball, self.portal_opening2)

        p1_x = self.portal_opening1.get_x_coordinates()
        p2_x = self.portal_opening2.get_x_coordinates()
        is_x_coll = False
        for x_coordinate in ball.get_x_coordinates():
            if p1_x.__contains__(x_coordinate) or p2_x.__contains__(x_coordinate):
                is_x_coll = True

        is_portal_collision = portal_opening1_collision or portal_opening2_collision

        # If the ball was just teleported from random portal it shouldn't disable
        was_teleported = self.portal_opening2.was_teleported or self.portal_opening1.was_teleported
        self.portal_disabled_event.run(False, is_portal_collision and not was_teleported)

        # If the ball was just teleported to it, it shouldn't be able to teleport again
        if portal_opening2_collision and is_enabled and not self.portal_opening2.was_teleported:
            self.teleport(self.portal_opening1, ball)

        if portal_opening1_collision and is_enabled and not self.portal_opening1.was_teleported:
            self.teleport(self.portal_opening2, ball)

        if self.portal_disabled_event.is_started and not self.portal_disabled_event.is_done():
            self.disable()

        # The ball shouldn't re-enable if the ball is too close to either opening
        ball_is_too_close_to_portal = is_portal_collision

        if self.portal_disabled_event.is_done() and not ball_is_too_close_to_portal:
            self.enable()
            self.portal_disabled_event.reset()

        if not CollisionsFinder.is_collision(self.portal_opening1, ball) and self.portal_opening1.was_teleported:
            self.portal_opening1.was_teleported = False

        if not CollisionsFinder.is_collision(self.portal_opening2, ball) and self.portal_opening2.was_teleported:
            self.portal_opening2.was_teleported = False

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


class RandomPortal(Portal):
    """A portal where it can teleport to multiple openings"""

    possible_outputs = []
    portal_end = None

    def __init__(self, color, portal_opening, possible_outputs):
        """ summary: initializes the object

            params:
                color: tuple; the (Red, Green, Blue) values of the portal's color
                portal_opening: PortalOpening; the opening of the portal
                possible_outputs: List of PortalOpening; the possible portal openings that the ball could be teleported to

            returns: None
        """

        self.enabled_color = color
        self.portal_opening1 = portal_opening
        self.portal_opening1.color = color
        self.possible_outputs = possible_outputs
        portal_opening.name = id(self.portal_opening1)
        self.portal_disabled_event = TimedEvent(3, False)
        # It extends a regular portal and that uses portal_opening2, so this prevents a NoneType Exception
        self.portal_opening2 = PortalOpening(0, 0, 0, 0, False)
        self.portal_end = self.get_portal_end()

    def run(self, ball):
        # Stores value of is_enabled, which other things in this function modify
        is_enabled = self.is_enabled
        is_portal_collision = CollisionsFinder.is_collision(ball, self.portal_opening1)

        self.portal_disabled_event.run(False, is_portal_collision)

        if is_portal_collision and is_enabled:
            self.teleport(self.portal_end, ball)
            self.portal_end.was_teleported = True
            self.portal_end = self.get_portal_end()

        if self.portal_disabled_event.is_started and not self.portal_disabled_event.is_done():
            self.disable()

        # The ball shouldn't re-enable if the ball is too close to either opening
        ball_is_too_close_to_portal = is_portal_collision

        if self.portal_disabled_event.is_done() and not ball_is_too_close_to_portal:
            self.enable()
            self.portal_disabled_event.reset()

    def get_portal_end(self):
        """ summary: finds a random portal output and returns it
            params: None
            returns: The place where the object should be teleported to (the portal end)
        """

        return get_random_item(self.possible_outputs)


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

        # The possible places that a random portal can travel to
        possible_outputs = []
        for portal in self.portals:
            possible_outputs += [portal.portal_opening1, portal.portal_opening2]

        self.portals.append(RandomPortal(purple, PortalOpening(50, 50, 25, 25, False), possible_outputs))
        self.player2.set_action(self.run_ai)
        
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

    # AI CODE
    def run_ai(self):
        if self.ball.right_edge >= self.player2.x_coordinate:
            print("YESSIR")
        prev_ball = HistoryKeeper.get_last(self.ball.name)
        if prev_ball is not None and self.ball_is_going_towards_ai():
            self.set_player_path()

        if self.player2.path is not None:
            self.player2.x_coordinate, self.player2.y_coordinate = self.player2.path.get_coordinates()
            # print(self.player2.path)
            # print(self.player2)

    def set_player_path(self):
        """Sets the player's path; NOTE must only be called if the ball is going towards the player"""

        ball_x_coordinate, ball_y_coordinate = self.ball.x_coordinate, self.ball.y_coordinate
        ball_is_moving_down = self.ball.is_moving_down

        next_portal = "placeholder instead of None"
        ball_path = None
        last_portal = None
        print("\n\nI WAS CALLED")

        while True:
            print("=====CYCLE=======\n")
            ball_path = self.get_ball_path_from(ball_y_coordinate, ball_x_coordinate, self.player2.x_coordinate,
                                                ball_is_moving_down)

            next_portal = self.get_next_portal_collision(ball_path)

            if last_portal is not None and self.get_next_portal(ball_path) == last_portal:
                next_portal = None

            if next_portal is None:
                break

            ball_is_moving_down = self.ball_direction_is_down(ball_y_coordinate, ball_x_coordinate, self.player2.x_coordinate, ball_is_moving_down)

            ball_x_coordinate, ball_y_coordinate = next_portal.x_midpoint, next_portal.y_midpoint
            last_portal = self.get_next_portal(ball_path)
            print(ball_path, next_portal, Point(ball_x_coordinate, ball_y_coordinate))

        ball_end_point = ball_path.get_end_points()[0]
        print(ball_path)
        self.player2.add_path(VelocityPath(Point(self.player2.x_coordinate, self.player2.y_coordinate),
                                           [Point(ball_end_point.x_coordinate, ball_end_point.y_coordinate)], self.player2.velocity))
    def ball_is_going_towards_ai(self):
        """returns: boolean; if the ball is going towards the ai"""

        return not HistoryKeeper.get_last(self.ball.name).is_moving_right and self.ball.is_moving_right

    def get_next_portal_collision(self, ball_path: Path):
        """returns: PortalOpening; the next portal opening that the ball will hit; None if it doesn't hit a portal"""

        for line in ball_path.get_lines():
            for portal in self.portals:
                is_random_portal = type(portal) == RandomPortal

                if CollisionsFinder.is_line_ellipse_equation(line, portal.portal_opening1):
                    return portal.portal_end if is_random_portal else portal.portal_opening2

                if not is_random_portal and CollisionsFinder.is_line_ellipse_equation(line, portal.portal_opening2):
                    return portal.portal_opening1
        return None

    def get_next_portal(self, ball_path: Path):
        """returns: Portal; the next portal the ball will hit"""
        for line in ball_path.get_lines():
            for portal in self.portals:
                is_random_portal = type(portal) == RandomPortal
                if CollisionsFinder.is_line_ellipse_equation(line, portal.portal_opening1):
                    return portal

                if not is_random_portal and CollisionsFinder.is_line_ellipse_equation(line, portal.portal_opening2):
                    return portal
        return None



