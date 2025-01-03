from typing import Optional
import color
from handlers.input_handlers import BaseEventHandler


import tcod
from tcod import libtcodpy


class PopupMessage(BaseEventHandler):
    """Display a popup text window."""

    def __init__(self, parent_handler: BaseEventHandler, text: str):
        self.parent = parent_handler
        self.text = text

    def on_render(self, console: tcod.console.Console) -> None:
        """Render the parent and dim the result, then print the message on top."""
        self.parent.on_render(console)
        console.rgb["fg"] //= 8
        console.rgb["bg"] //= 8

        console.print_box(
            x=console.width // 4,
            y=console.height // 4,
            width=console.width // 2,
            height=console.height // 2,
            string=self.text,
            fg=color.white,
            bg=None,
            alignment=libtcodpy.CENTER,
        )

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[BaseEventHandler]:
        """Any key returns to the parent handler."""
        return self.parent