from typing import Optional

import tcod

from handlers.event_handler import EventHandler
from handlers.main_game_event_handler import MainGameEventHandler
from tables.grab_bag import GrabBag
from tables.random_table import RandomTable
import color
import keys
import tables.loot_tables


class DebugTableViewer(EventHandler):
    def __init__(self, engine):
        super().__init__(engine)
        all_tables_and_grab_bags = {
            name: getattr(tables.loot_tables, name) for name in dir(tables.loot_tables) if not name.startswith("_")
        }

        # Store names along with instances
        self.all_tables = [
            (name, obj) for name, obj in all_tables_and_grab_bags.items() if isinstance(obj, RandomTable)
        ]
        self.all_grab_bags = [(name, obj) for name, obj in all_tables_and_grab_bags.items() if isinstance(obj, GrabBag)]

    def on_render(self, console: tcod.console.Console, delta_time: float) -> None:
        super().on_render(console, delta_time)  # Draw the main state as the background.

        width = 40
        height = len(self.all_tables) + len(self.all_grab_bags) + 6
        sub_console = tcod.console.Console(width, height)
        sub_console.draw_frame(0, 0, width, height, bg=color.black, fg=color.white)
        sub_console.print(width // 2, 0, "┤(Debug) Tables├", alignment=tcod.constants.CENTER)

        sub_console.print(1, 1, "[Random Tables]", color.orange)
        for i, (name, table) in enumerate(self.all_tables):
            sub_console.print(1, i + 2, name)

        sub_console.print(1, len(self.all_tables) + 3, "[Grab Bags]", color.orange)
        for i, (name, table) in enumerate(self.all_grab_bags):
            sub_console.print(1, i + len(self.all_tables) + 4, name)

        x = console.width // 2 - sub_console.width // 2
        y = console.height // 2 - sub_console.height // 2
        sub_console.blit(console, x, y)

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[EventHandler]:
        return MainGameEventHandler(self.engine)
