from typing import Iterable, Tuple

from shape.base_shape import BaseShape


class Ray(BaseShape):
    def __init__(self, origin_x: int, origin_y: int, direction_x: int, direction_y: int):
        self.origin = (origin_x, origin_y)
        self.direction = (direction_x, direction_y)

    def __iter__(self) -> Iterable[Tuple[int, int]]:
        x, y = self.origin
        dx, dy = self.direction
        # move end point super far away
        dx *= 100
        dy *= 100

        # Determine the signs of dx and dy for the direction
        sx = 1 if dx > 0 else -1
        sy = 1 if dy > 0 else -1

        # Make dx and dy positive for simplicity
        dx = abs(dx)
        dy = abs(dy)

        # Bresenham's line algorithm
        if dx > dy:
            p_inc = 2 * dy - dx
            p = 2 * dy - dx
            for _ in range(dx):
                yield x, y
                x += sx
                if p < 0:
                    p += 2 * dy
                else:
                    y += sy
                    p += 2 * (dy - dx)
        else:
            p_inc = 2 * dx - dy
            p = 2 * dx - dy
            for _ in range(dy):
                yield x, y
                y += sy
                if p < 0:
                    p += 2 * dx
                else:
                    x += sx
                    p += 2 * (dx - dy)
