import unittest

from shape.line import Line
from shape.ray import Ray


class TestLine(unittest.TestCase):
    def test_horizontal_line(self):
        line = Line(0, 0, 3, 0)
        self.assertEqual([(0, 0), (1, 0), (2, 0), (3, 0)], list(line))

    def test_vertical_line(self):
        line = Line(0, 0, 0, 3)
        self.assertEqual([(0, 0), (0, 1), (0, 2), (0, 3)], list(line))

    def test_diagonal_line(self):
        line = Line(-3, -3, 2, 2)
        self.assertEqual([(-3, -3), (-2, -2), (-1, -1), (0, 0), (1, 1), (2, 2)], list(line))

    def test_negative_slope_diagonal_line(self):
        test = Line(-2, 2, 3, -3)
        self.assertEqual([(-2, 2), (-1, 1), (0, 0), (1, -1), (2, -2), (3, -3)], list(test))

    def test_backwards_diagonal_line(self):
        line = Line(2, 2, -3, -3)
        self.assertEqual([(2, 2), (1, 1), (0, 0), (-1, -1), (-2, -2), (-3, -3)], list(line))

    def test_backwards_horizontal_line(self):
        line = Line(3, 0, 0, 0)
        self.assertEqual([(3, 0), (2, 0), (1, 0), (0, 0)], list(line))

    def test_backwards_vertical_line(self):
        line = Line(0, 3, 0, 0)
        self.assertEqual([(0, 3), (0, 2), (0, 1), (0, 0)], list(line))

    def test_single_point(self):
        line = Line(0, 0, 0, 0)
        self.assertEqual([(0, 0)], list(line))


class TestRay(unittest.TestCase):
    def test_ray(self):
        ray = Ray(0, 0, 2, 2)
        self.assertIn((0, 0), ray)
        self.assertIn((1, 1), ray)
        self.assertIn((4, 4), ray)
        self.assertNotIn((1, 0), ray)
        self.assertNotIn((0, 1), ray)
