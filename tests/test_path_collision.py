import unittest

from base_pong.drawable_objects import GameObject, Ellipse
from base_pong.engines import CollisionsFinder
from base_pong.equations import Point, LineSegment
from base_pong.path import Path
from base_pong.utility_classes import HistoryKeeper
from base_pong.utility_functions import solve_quadratic
from base_pong.velocity_calculator import VelocityCalculator


def get_path(point1, point2, height):
    path = Path(point1)
    path.add_point(point2, height)
    return path


class CollisionsFinderTests(unittest.TestCase):
    # TODO fix is_path_collision test
    def test_is_path_collision(self):
        test_paths = [
            get_path(Point(10, 10), Point(40, 30), 2),
            get_path(Point(30, 10), Point(50, 40), 1),
            get_path(Point(60, 10), Point(80, 20), 2),
            get_path(Point(60, 40), Point(80, 50), 2)
        ]
        gotten_outputs = [
            CollisionsFinder.is_path_collision(test_paths[0], test_paths[1]),
            CollisionsFinder.is_path_collision(test_paths[2], test_paths[3])
        ]
        wanted_outputs = [
            True,
            False
        ]

        for x in range(len(gotten_outputs)):
            if gotten_outputs[x] != wanted_outputs[x]:
                self.assertEqual(wanted_outputs[x], gotten_outputs[x],
                                 f"Test Case number {x + 1} out of {len(wanted_outputs)} is Failed | want {wanted_outputs[x]} got {gotten_outputs[x]}")

    def test_is_moving_collision_ellipse(self):
        moving_object_start = GameObject(30, 30, 10, 10)
        moving_object_end = GameObject(0, 0, 10, 10)
        moving_object_path = Path.get_x_coordinate_path(moving_object_start, moving_object_end)

        gotten_outputs = [
            CollisionsFinder.is_moving_collision(moving_object_path, GameObject(0, 20, 20, 20)),
            CollisionsFinder.is_moving_collision(moving_object_path, Ellipse(0, 20, 20, 20)),
        ]
        wanted_outputs = [
            True,
            True
        ]
        for x in range(len(gotten_outputs)):
            if gotten_outputs[x] != wanted_outputs[x]:
                self.assertEqual(wanted_outputs[x], gotten_outputs[x],
                                 f"Test Case number {x + 1} out of {len(wanted_outputs)} is Failed | want {wanted_outputs[x]} got {gotten_outputs[x]}")

    def test_line_collision(self):
        line1 = LineSegment(Point(10, 20), Point(10, 40))
        line2 = LineSegment(Point(20, 40), Point(0, 10))

        gotten_outputs = [CollisionsFinder.is_line_collision(line1, line2)]
        wanted_outputs = [True]
        for x in range(len(gotten_outputs)):
            if gotten_outputs[x] != wanted_outputs[x]:
                self.assertEqual(wanted_outputs[x], gotten_outputs[x],
                                 f"Test Case number {x + 1} out of {len(wanted_outputs)} is Failed | want {wanted_outputs[x]} got {gotten_outputs[x]}")

    def test_is_line_ellipse_collision(self):
        line = LineSegment(Point(-2, 0), Point(2, 1))
        ellipse = Ellipse(-1, -1, 2, 2)
        gotten_outputs = [CollisionsFinder.is_line_ellipse_collision(ellipse, line)]
        wanted_outputs = [True]
        for x in range(len(gotten_outputs)):
            if gotten_outputs[x] != wanted_outputs[x]:
                self.assertEqual(wanted_outputs[x], gotten_outputs[x],
                                 f"Test Case number {x + 1} out of {len(wanted_outputs)} is Failed | want {wanted_outputs[x]} got {gotten_outputs[x]}")

    def test_solve_quadratic(self):
        gotten_outputs = [
            solve_quadratic(1, -30, 125),
            solve_quadratic(200, -6000, 40000)
        ]

        wanted_outputs = [
            [5, 25],
            [10, 20]
        ]
        for x in range(len(gotten_outputs)):
            if gotten_outputs[x] != wanted_outputs[x]:
                self.assertEqual(wanted_outputs[x], gotten_outputs[x],
                                 f"Test Case number {x + 1} out of {len(wanted_outputs)} is Failed | want {wanted_outputs[x]} got {gotten_outputs[x]}")

    def test_is_collision(self):
        # Stores whether the cases have passed or not
        cases = []
        # STATIONARY TESTS
        # Case 1; True
        stationary_object = GameObject(20, 20, 30, 20)
        prev_moving_object = GameObject(10, 25, 5, 5)
        current_moving_object = GameObject(30, 25, 5, 5)
        cases += self.is_collision_test_case(stationary_object, prev_moving_object, stationary_object, current_moving_object, True, 1)

        # Case 2; True
        prev_moving_object = GameObject(50, 25, 5, 5)
        current_moving_object = GameObject(33, 30, 5, 5)
        cases += self.is_collision_test_case(stationary_object, prev_moving_object, stationary_object, current_moving_object, True, 2)

        # Case 3; False
        stationary_object = GameObject(10, 60, 10, 10)
        prev_moving_object = GameObject(10, 40, 10, 10)
        current_moving_object = GameObject(40, 70, 10, 10)

        cases += self.is_collision_test_case(stationary_object, prev_moving_object, stationary_object, current_moving_object, False, 3)

        # PATH TESTS
        # Case 1 (only case; case where one object envelopes the other)
        prev_object1 = GameObject(40, 30, 10, 10)
        current_object1 = GameObject(50, 20, 10, 10)

        prev_object2 = GameObject(30, 10, 40, 30)
        current_object2 = GameObject(60, 10, 40, 30)
        cases += self.is_collision_test_case(prev_object1, prev_object2, current_object1, current_object2, True, 4)

        failed_cases = ""
        for x in range(len(cases) // 2):
            if not cases[x * 2] or not cases[x * 2 + 1]:
                failed_cases += f"{x + 1} "

        self.assertEqual(True, failed_cases == "", "These are the failed cases; " + failed_cases)

    def is_collision_test_case(self, prev_object1, prev_object2, object1, object2, want, test_case_number):
        """returns: List of boolean; [rectangle collision worked, elliptical collision worked]"""

        return_value = [True, True]
        # Case 1; rectangle
        HistoryKeeper.reset()
        VelocityCalculator.time = 0.1
        object1.name = id(object1)
        object2.name = id(object2)
        HistoryKeeper.add(prev_object1, object1.name, True)
        HistoryKeeper.add(prev_object2, object2.name, True)
        HistoryKeeper.last_time = 0.1

        got = CollisionsFinder.is_collision(object1, object2)
        if got != want:
            return_value[0] = False

        # Case 2; Ellipse
        HistoryKeeper.reset()
        HistoryKeeper.add(self.turn_into_ellipse(prev_object1), object1.name, True)
        HistoryKeeper.add(self.turn_into_ellipse(prev_object2), object2.name, True)
        HistoryKeeper.last_time = 0.1

        got = CollisionsFinder.is_collision(self.turn_into_ellipse(object1), self.turn_into_ellipse(object2))
        if got != want:
            return_value[1] = False

        return return_value

    def turn_into_ellipse(self, rectangle):
        ellipse = Ellipse(rectangle.x_coordinate, rectangle.y_coordinate, rectangle.height, rectangle.length)
        ellipse.name = rectangle.name
        return ellipse



if __name__ == '__main__':
    unittest.main()