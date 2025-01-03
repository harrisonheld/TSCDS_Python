import color
import exceptions
from handlers.main_game_event_handler import MainGameEventHandler
import keys
from handlers.event_handler import EventHandler
from typing import Optional


import tcod


class PauseViewer(EventHandler):
    def on_render(self, console: tcod.console.Console) -> None:
        super().on_render(console)  # Draw the main state as the background.

        width = 19
        height = 19
        sub_console = tcod.console.Console(width, height)
        sub_console.draw_frame(0, 0, width, height, bg=color.black, fg=color.white)
        sub_console.print(width // 2, 0, "┤Paused├", alignment=tcod.constants.CENTER)
        sub_console.print(width // 2, 1, "save and quit", alignment=tcod.constants.CENTER)
        sub_console.print(1, 2, "[q] to main menu")
        sub_console.print(1, 3, "[Q] to desktop")

        x = console.width // 2 - sub_console.width // 2
        y = console.height // 2 - sub_console.height // 2
        sub_console.blit(console, x, y)

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[EventHandler]:
        key = event.sym

        if key == tcod.event.KeySym.q:
            if event.mod & (tcod.event.KMOD_LSHIFT | tcod.event.KMOD_RSHIFT):
                raise SystemExit()
            raise exceptions.SaveAndQuitToMainMenu()

        elif key in keys.MODIFIER_KEYS:
            return None
        else:
            return MainGameEventHandler(self.engine)

        return None