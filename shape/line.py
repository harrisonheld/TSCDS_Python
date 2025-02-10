from typing import Iterable, Tuple


class Line:
    def __init__(self, from_x: int, from_y: int, to_x: int, to_y: int):
        self.from_x = from_x
        self.from_y = from_y
        self.to_x = to_x
        self.to_y = to_y
        self.dx = abs(to_x - from_x)
        self.dy = abs(to_y - from_y)
        self.step_x = 1 if from_x < to_x else -1
        self.step_y = 1 if from_y < to_y else -1
        self.error = self.dx - self.dy
        self.current_x = from_x
        self.current_y = from_y
        self.finished = False

    def __iter__(self):
        return self

    def __next__(self) -> Tuple[int, int]:
        if self.finished:
            raise StopIteration

        current_point = (self.current_x, self.current_y)

        if (self.current_x, self.current_y) == (self.to_x, self.to_y):
            self.finished = True
            return current_point

        error2 = 2 * self.error
        if error2 > -self.dy:
            self.error -= self.dy
            self.current_x += self.step_x
        if error2 < self.dx:
            self.error += self.dx
            self.current_y += self.step_y

        return current_point
