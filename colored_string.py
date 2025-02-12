from typing import List, Tuple, Union
import re

import tcod

import color


class ColoredString:
    # Matches a color in the form (r, g, b)
    COLOR_PATTERN = re.compile(r"\((\d+),\s*(\d+),\s*(\d+)\)")

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

    def __iadd__(self, other: Union["ColoredString", str]) -> "ColoredString":
        """Concatenate, preserving color. `strs` will be treated as white ColoredStrings."""
        if isinstance(other, str):
            other = ColoredString(other)

        self._characters.extend(other._characters)
        self._colors.extend(other._colors)
        return self

    def __add__(self, other: Union["ColoredString", str]) -> "ColoredString":
        """Concatenate, preserving color. `strs` will be treated as white ColoredStrings."""
        new_colored_string = ColoredString("")
        new_colored_string += self
        new_colored_string += other
        return new_colored_string

    def __str__(self):
        """Reconstructs the original input format with color markers."""
        if not self._characters:
            return ""

        reconstructed = []
        prev_color = None

        for char, color in zip(self._characters, self._colors):
            if color != prev_color:
                reconstructed.append(f"({color[0]}, {color[1]}, {color[2]})")
            reconstructed.append(char)
            prev_color = color

        return "".join(reconstructed)

    def print(self, console: tcod.console.Console, x: int, y: int) -> None:
        for char, fg_color in zip(self._characters, self._colors):
            console.print(x=x, y=y, string=char, fg=fg_color)
            x += 1
