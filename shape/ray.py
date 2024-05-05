from typing import Iterable, Tuple

from shape.base_shape import BaseShape
from shape.line import Line


class Ray(BaseShape):
    def __init__(self, from_x: int, from_y: int, to_x: int, to_y: int):
        self.from_x = from_x
        self.from_y = from_y
        self.to_x = to_x
        self.to_y = to_y

    def __iter__(self):
        dx = (self.to_x - self.from_x) * 100
        dy = (self.to_y - self.from_y) * 100
        return Line(self.from_x, self.from_y, self.from_x + dx, self.from_y + dy).__iter__()
