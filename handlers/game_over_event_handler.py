import color
import exceptions
from engine import Engine
from handlers.event_handler import EventHandler
from typing import Optional


import tcod


import os


class GameOverEventHandler(EventHandler):
    """Handle exiting out of a finished game."""

    def __init__(self, engine: Engine):
        super().__init__(engine)
        # Deletes the active save file.
        if os.path.exists(engine.save_path):
            os.remove(engine.save_path)

    def on_render(self, console: tcod.console.Console) -> None:
        super().on_render(console)  # Draw the main state as the background.

        width = 19
        height = 19
        title = "┤You Died├" if not self.engine.player.is_alive else "┤You Won├"
        sub_console = tcod.console.Console(width, height)
        sub_console.draw_frame(0, 0, width, height, bg=color.black, fg=color.white)
        sub_console.print(width // 2, 0, title, alignment=tcod.constants.CENTER)
        sub_console.print(1, 1, "[n] new game")
        sub_console.print(width // 2, 2, "quit", alignment=tcod.constants.CENTER)
        sub_console.print(1, 3, "[q] to main menu")
        sub_console.print(1, 4, "[Q] to desktop")

        x = console.width // 2 - sub_console.width // 2
        y = console.height // 2 - sub_console.height // 2
        sub_console.blit(console, x, y)

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[EventHandler]:
        key = event.sym

        if key == tcod.event.KeySym.n:
            raise exceptions.StartNewGame()
        if key == tcod.event.KeySym.q:
            if event.mod & (tcod.event.KMOD_LSHIFT | tcod.event.KMOD_RSHIFT):
                raise exceptions.QuitWithoutSaving()  # to desktop
            raise exceptions.QuitToMainMenu()

        return None