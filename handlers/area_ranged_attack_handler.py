from typing import Callable, Optional, Tuple

import tcod

from actions.action import Action
from engine import Engine
from handlers.select_index_handler import SelectIndexHandler
import color


class AreaRangedAttackHandler(SelectIndexHandler):
    """Handles targeting an area within a given radius. Any entity within the area will be affected."""

    def __init__(
        self,
        engine: Engine,
        radius: int,
        callback: Callable[[Tuple[int, int]], Optional[Action]],
    ):
        super().__init__(engine)

        self.radius = radius
        self.callback = callback

    def on_render(self, console: tcod.console.Console) -> None:
        """Highlight the tile under the cursor."""
        super().on_render(console)

        x, y = self.engine.mouse_location

        # Draw a rectangle around the targeted area, so the player can see the affected tiles.
        console.draw_frame(
            x=x - self.radius,
            y=y - self.radius,
            width=self.radius * 2 + 1,
            height=self.radius * 2 + 1,
            fg=color.red,
            clear=False,
        )
        print(self.radius)

    def on_index_selected(self, x: int, y: int) -> Optional[Action]:
        return self.callback((x, y))
