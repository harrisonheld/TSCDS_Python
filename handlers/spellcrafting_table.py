from typing import Optional

import tcod

from engine import Engine
from handlers.event_handler import EventHandler
from handlers.main_game_event_handler import MainGameEventHandler
import color
import exceptions
import keys


class SpellcraftingTable(EventHandler):

    def __init__(self, engine: Engine):
        super().__init__(engine)

        self.crafting_width = 10
        self.crafting_height = 5

    def on_render(self, console: tcod.console.Console, delta_time: float) -> None:
        super().on_render(console, delta_time)  # Draw the main state as the background.

        width = self.crafting_width + 2
        height = self.crafting_height + 5
        sub_console = tcod.console.Console(width, height)
        sub_console.draw_frame(0, 0, width, height, bg=color.black, fg=color.white)
        sub_console.print(width // 2, 0, "┤Spellcrafting├", alignment=tcod.constants.CENTER)
        
        for y in range(self.crafting_height):
            for x in range(self.crafting_width):
                sub_console.print(1 + x, 1 + y, ".", fg=color.white)

        x = console.width // 2 - sub_console.width // 2
        y = console.height // 2 - sub_console.height // 2
        sub_console.blit(console, x, y)

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[EventHandler]:
        key = event.sym

        if key in keys.MODIFIER_KEYS:
            return None
        else:
            return MainGameEventHandler(self.engine)

        return None
