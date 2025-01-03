import color
from handlers.main_game_event_handler import MainGameEventHandler
import keys
import strings
from engine import Engine
from handlers.event_handler import EventHandler
from typing import Optional


import tcod


class HelpViewer(EventHandler):
    """Print the controls."""

    titles = ["Controls", "General Info", "About"]
    texts = [strings.controls, strings.general_info, strings.about]

    def __init__(self, engine: Engine):
        super().__init__(engine)
        self.curr_page = 0

    def on_render(self, console: tcod.console.Console) -> None:
        super().on_render(console)  # Draw the main state as the background.

        width = console.width - 6
        height = console.height - 6
        this_here_console = tcod.console.Console(width, height)

        # draw this page
        text = HelpViewer.texts[self.curr_page]

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
        for i, title in enumerate(HelpViewer.titles):
            col = color.white
            if i == self.curr_page:
                col = color.welcome_text

            if i == self.curr_page:
                this_here_console.print(acc_x - 1, 0, "┤")
            this_here_console.print(acc_x, 0, title, col)
            if i == self.curr_page:
                this_here_console.print(acc_x + len(title), 0, "├")
            acc_x += len(title) + 3

        this_here_console.blit(console, 3, 3)

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[EventHandler]:
        if event.sym in keys.MENU_NAV_RIGHT:
            self.curr_page = (self.curr_page + 1) % len(HelpViewer.titles)
        elif event.sym in keys.MENU_NAV_LEFT:
            self.curr_page = (self.curr_page - 1) % len(HelpViewer.titles)
        else:
            return MainGameEventHandler(self.engine)
        return None