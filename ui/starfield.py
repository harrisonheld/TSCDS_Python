import math
import random

from tcod import libtcodpy

import color


class Starfield:
    def __init__(self):

        star_count = 100
        self.stars = []

        for _ in range(star_count):
            x = random.uniform(0, 1)
            y = random.uniform(0, 1)
            brightness = random.uniform(0, 1)
            star = Star(x, y, brightness)
            self.stars.append(star)

    def render(self, console, width, height):
        # draw stars
        for star in self.stars:
            hor_dist_from_center = abs(star.x-0.5)
            star.x += 0.005*(math.cos(math.pi * (hor_dist_from_center-1))+1) + 0.005
            star.x %= 1

            x = int(star.x * width)
            y = int(star.y * height)

            if 0 <= x < width and 0 <= y < height:
                t = star.apparent_brightness
                c = libtcodpy.color_lerp(color.navy, color.white, t)
                glyphs = ".,*~"
                g = int(t * (len(glyphs) - 1))
                console.print(x, y, glyphs[g], c)


class Star:
    def __init__(self, x, y, apparent_brightness):
        self.x = x
        self.y = y
        self.apparent_brightness = apparent_brightness
