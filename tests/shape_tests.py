import unittest

from shape.line import Line


class TestLine(unittest.TestCase):
    def test_horizontal_line(self):
        line = Line(0, 0, 3, 0)
        self.assertEqual([(0, 0), (1, 0), (2, 0), (3, 0)], list(line))

    def test_vertical_line(self):
        line = Line(0, 0, 0, 3)
        self.assertEqual([(0, 0), (0, 1), (0, 2), (0, 3)], list(line))
