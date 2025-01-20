from typing import Optional

import tcod

from handlers.debug.debug_color_viewer import DebugColorViewer
from handlers.debug.debug_cp437_viewer import DebugCP437Viewer
from handlers.debug.debug_item_spawner import DebugItemSpawner
from handlers.event_handler import EventHandler
from handlers.main_game_event_handler import MainGameEventHandler
import color
import keys


class DebugMenu(EventHandler):
    def on_render(self, console: tcod.console.Console, delta_time: float) -> None:
        super().on_render(console, delta_time)  # Draw the main state as the background.

        width = 19
        height = 19
        sub_console = tcod.console.Console(width, height)
        sub_console.draw_frame(0, 0, width, height, bg=color.black, fg=color.white)
        sub_console.print(width // 2, 0, "┤Debug Menu├", alignment=tcod.constants.CENTER)
        sub_console.print(1, 1, "[a] colors")
        sub_console.print(1, 2, "[b] cp437")
        sub_console.print(1, 3, "[c] item spawner")

        x = console.width // 2 - sub_console.width // 2
        y = console.height // 2 - sub_console.height // 2
        sub_console.blit(console, x, y)

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[EventHandler]:
        key = event.sym

        if key == tcod.event.KeySym.a:
            return DebugColorViewer(self.engine)
        elif key == tcod.event.KeySym.b:
            return DebugCP437Viewer(self.engine)
        elif key == tcod.event.KeySym.c:
            return DebugItemSpawner(self.engine)

        elif key in keys.MODIFIER_KEYS:
            return None
        else:
            return MainGameEventHandler(self.engine)

        return None
