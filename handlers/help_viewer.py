from typing import Optional

import tcod

from engine import Engine
from handlers.event_handler import EventHandler
from handlers.main_game_event_handler import MainGameEventHandler
from ui.circular_index_selector import CircularIndexSelector
import color
import keys
import strings


class HelpViewer(EventHandler):
    """Print the controls."""

    def __init__(self, engine: Engine):
        super().__init__(engine)
        self.titles = ["Controls", "General Info", "About"]
        self.texts = [strings.controls, strings.general_info, strings.about]
        n = len(self.titles)
        self.selector = CircularIndexSelector(n, vertical=False)

    def on_render(self, console: tcod.console.Console, delta_time: float) -> None:
        super().on_render(console, delta_time)  # Draw the main state as the background.

        width = console.width - 6
        height = console.height - 6
        this_here_console = tcod.console.Console(width, height)

        # draw this page
        idx = self.selector.get_index()
        text = self.texts[idx]

        # frame
        this_here_console.draw_frame(
            0, 0, this_here_console.width, this_here_console.height, bg=color.black, fg=color.white
        )
        # contents
        this_here_console.print_box(1, 1, width - 2, height - 2, text)
        # controls in bottom right
        controls = "┤«[NumPad4]/[NumPad6]»├"
        this_here_console.print(width - len(controls) - 4, height - 1, controls)
        # tabs on top
        acc_x = 3
        for i, title in enumerate(self.titles):
            col = color.white
            if i == self.selector.get_index():
                col = color.welcome_text

            if i == self.selector.get_index():
                this_here_console.print(acc_x - 1, 0, "┤")
            this_here_console.print(acc_x, 0, title, col)
            if i == self.selector.get_index():
                this_here_console.print(acc_x + len(title), 0, "├")
            acc_x += len(title) + 3

        this_here_console.blit(console, 3, 3)

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[EventHandler]:
        if self.selector.take_input(event.sym):
            return None

        return MainGameEventHandler(self.engine)
