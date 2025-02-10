import tcod
import color

class ColoredString:

    DELIMITER="#"

    def __init__(self, string):
        self._characters = string
        self._colors = [color.white] * len(string)

    def print(self, console: tcod.console.Console, x: int, y: int):
        for char, color in zip(self._characters, self._colors):
            console.print(x=x, y=y, string=char, fg=color)
            x += 1