from typing import List, Tuple

import tcod


class PaletteViewer:
    def __init__(self, colors: List[Tuple[int, int, int]]):
        self.colors = colors

    def render(self, console: tcod.console.Console, x: int, y: int) -> None:
        for x_off in range(0, len(self.colors)):
            for y_off in range(0, len(self.colors)):
                primary = self.colors[x_off]
                secondary = self.colors[y_off]
                console.print(x + x_off, y + y_off, "Ω", bg=primary, fg=secondary)
