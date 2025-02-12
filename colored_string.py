from typing import List, Tuple
import re

import tcod

import color


class ColoredString:
    # Matches a color in the form (r, g, b)
    COLOR_PATTERN = re.compile(r"\((\d+),\s*(\d+),\s*(\d+)\)")

    "Inno(20, 30, 40)o(255,255,255)cent".

    def __init__(self, string: str) -> None:
        self._characters: List[str] = []
        self._colors: List[Tuple[int, int, int]] = []

        current_color = color.white
        position = 0

        while position < len(string):
            match = self.COLOR_PATTERN.search(string, position)
            if match:
                # Add text before the color change
                text_segment = string[position : match.start()]
                self._characters.extend(text_segment)
                self._colors.extend([current_color] * len(text_segment))

                # Parse the new color
                r, g, b = map(int, match.groups())
                current_color = (r, g, b)

                # Move position past the match
                position = match.end()
            else:
                # No more colors, add the rest of the string
                self._characters.extend(string[position:])
                self._colors.extend([current_color] * (len(string) - position))
                break

    def print(self, console: tcod.console.Console, x: int, y: int) -> None:
        for char, fg_color in zip(self._characters, self._colors):
            console.print(x=x, y=y, string=char, fg=fg_color)
            x += 1
