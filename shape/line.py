from typing import Iterable, Tuple

from shape.base_shape import BaseShape


class Line(BaseShape):
    def __init__(self, from_x: int, from_y: int, to_x: int, to_y: int):
        self.from_x = from_x
        self.from_y = from_y
        self.to_x = to_x
        self.to_y = to_y
        self.iter_last = False
        self.iter_dx = 0
        self.iter_dy = 0
        self.iter_x = 0
        self.iter_y = 0
        self.iter_D = 0
        self.step_x = 0
        self.step_y = 0

    def __iter__(self):
        self.iter_dx = abs(self.to_x - self.from_x)
        self.iter_dy = abs(self.to_y - self.from_y)
        self.iter_x = self.from_x
        self.iter_y = self.from_y
        self.iter_last = False

        if self.from_x < self.to_x:
            self.step_x = 1
        else:
            self.step_x = -1

        if self.from_y < self.to_y:
            self.step_y = 1
        else:
            self.step_y = -1

        if self.iter_dx > self.iter_dy:
            self.iter_D = 2 * self.iter_dy - self.iter_dx
        else:
            self.iter_D = 2 * self.iter_dx - self.iter_dy

        return self

    def __next__(self) -> Tuple[int, int]:
        if self.iter_last:
            raise StopIteration
        if self.iter_x == self.to_x and self.iter_y == self.to_y:
            self.last = True
        ret = (self.iter_x, self.iter_y)

        if self.iter_D > 0:
            self.iter_x += self.step_x
            self.iter_y += self.step_y
            self.iter_D -= 2 * (self.iter_dx if self.iter_dx > self.iter_dy else self.iter_dy)
        else:
            if self.iter_dx > self.iter_dy:
                self.iter_x += self.step_x
                self.iter_D += 2 * self.iter_dy
            else:
                self.iter_y += self.step_y
                self.iter_D += 2 * self.iter_dx

        return ret
