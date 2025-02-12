from typing import Optional

import tcod

from colored_string import ColoredString
from handlers.event_handler import EventHandler
from handlers.main_game_event_handler import MainGameEventHandler
import color
import keys


class ColoredStringsTest(EventHandler):
    def on_render(self, console: tcod.console.Console, delta_time: float) -> None:
        super().on_render(console, delta_time)  # Draw the main state as the background.

        width = height = 40
        sub_console = tcod.console.Console(width, height)
        sub_console.draw_frame(0, 0, width, height, bg=color.black, fg=color.white)
        sub_console.print(width // 2, 0, "┤(Debug) Colored Strings Test├", alignment=tcod.constants.CENTER)

        strs = [
            ColoredString(f"This is a white string, hopefully."),
            ColoredString(f"This is a {color.red}red{color.white} string, hopefully."),
            ColoredString(f"Inn{color.yellow}o{color.white}cent"),
        ]

        for i, string in enumerate(strs):
            string.print(sub_console, 1, i + 1)

        x = console.width // 2 - sub_console.width // 2
        y = console.height // 2 - sub_console.height // 2
        sub_console.blit(console, x, y)

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[EventHandler]:
        return MainGameEventHandler(self.engine)
