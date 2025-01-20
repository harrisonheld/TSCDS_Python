from typing import Optional

import tcod

from handlers.event_handler import EventHandler
from handlers.main_game_event_handler import MainGameEventHandler
import color
import keys


class DebugColorViewer(EventHandler):
    def __init__(self, engine):
        super().__init__(engine)
        all_colors = [getattr(color, name) for name in dir(color) if not name.startswith("_")]
        self.unique_colors = set(all_colors)

    def on_render(self, console: tcod.console.Console, delta_time: float) -> None:
        super().on_render(console, delta_time)  # Draw the main state as the background.

        width = height = len(self.unique_colors) + 2
        sub_console = tcod.console.Console(width, height)
        sub_console.draw_frame(0, 0, width, height, bg=color.black, fg=color.white)
        sub_console.print(width // 2, 0, "┤(Debug) Colors├", alignment=tcod.constants.CENTER)

        for y, col1 in enumerate(self.unique_colors):
            for x, col2 in enumerate(self.unique_colors):
                sub_console.print(x + 1, y + 1, "h", bg=col1, fg=col2)

        x = console.width // 2 - sub_console.width // 2
        y = console.height // 2 - sub_console.height // 2
        sub_console.blit(console, x, y)

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[EventHandler]:
        return MainGameEventHandler(self.engine)
