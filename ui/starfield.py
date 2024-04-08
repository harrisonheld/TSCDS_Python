import math
import random

from tcod import libtcodpy

import color


class Starfield:
    def __init__(self):

        self.fov = math.radians(90)
        self.cam_theta = 0
        self.cam_phi = 0

        star_count = 1000
        self.min_star_distance = 5
        self.max_star_distance = 10
        self.min_star_brightness = 7
        self.max_star_brightness = 10
        self.stars = []

        for _ in range(star_count):
            star = self.generate_star()
            self.stars.append(star)

    def generate_star(self):
        x = random.uniform(-1, 1)
        y = random.uniform(-1, 1)
        z = random.uniform(-1, 1)
        magnitude = math.sqrt(x ** 2 + y ** 2 + z ** 2)
        x /= magnitude
        y /= magnitude
        z /= magnitude

        theta = math.atan2(y, x)
        phi = math.acos(z)
        distance = random.uniform(self.min_star_distance, self.max_star_distance)
        brightness = random.uniform(self.min_star_brightness, self.max_star_brightness)

        return Star(theta, phi, distance, brightness)

    def render(self, console, width, height):
        # animate
        self.cam_theta = (self.cam_theta + 0.001)

        # draw stars
        for star in self.stars:
            x, y = self.get_star_position(star, width, height)
            if 0 <= x < width and 0 <= y < height:
                max_brightness = self.max_star_brightness / (self.min_star_distance ** 2)
                brightness = star.apparent_brightness
                t = brightness / max_brightness
                c = libtcodpy.color_lerp(color.black, color.white, t)
                glyphs = ".,*~"
                g = int(t * (len(glyphs) - 1))
                console.print(x, y, glyphs[g], c)


    def get_star_position(self, star, width, height):
        aspect = width / height
        fov_x = self.fov
        fov_y = self.fov / aspect

        # assume the sensor is a screen 1 unit away
        sensor_width = math.tan(fov_x / 2) * 2
        sensor_height = math.tan(fov_y / 2) * 2

        # Rotate stars around the camera
        rel_theta = star.theta - self.cam_theta
        rel_phi = star.phi - self.cam_phi

        # project onto the sensor
        off_x = math.tan(rel_theta) * (sensor_width / 2)
        off_y = math.tan(rel_phi) * (sensor_height / 2)

        # center
        x_proj = width/2 + off_x
        y_proj = height/2 + off_y

        return int(x_proj), int(y_proj)


class Star:
    def __init__(self, theta, phi, distance, brightness):
        self.theta = theta
        self.phi = phi
        self.distance = distance
        self.brightness = brightness

    @property
    def apparent_brightness(self):
        return self.brightness / self.distance ** 2
