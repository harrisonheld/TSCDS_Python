from typing import Optional

import tcod

from handlers.event_handler import EventHandler
from handlers.main_game_event_handler import MainGameEventHandler
import color
import keys


class DebugCP437Viewer(EventHandler):
    def __init__(self, engine):
        super().__init__(engine)

    def on_render(self, console: tcod.console.Console, delta_time: float) -> None:
        super().on_render(console, delta_time)  # Draw the main state as the background.

        width = height = 16 + 2
        sub_console = tcod.console.Console(width, height)
        sub_console.draw_frame(0, 0, width, height, bg=color.black, fg=color.white)
        sub_console.print(width // 2, 0, "┤(Debug) CP437├", alignment=tcod.constants.CENTER)

        # fmt: off
        cp437_control_map = {
            0x00: "☺", 0x01: "☻", 0x02: "♥", 0x03: "♦", 0x04: "♣", 0x05: "♠",
            0x06: "•", 0x07: "◘", 0x08: "○", 0x09: "◙", 0x0A: "♂", 0x0B: "♀",
            0x0C: "♪", 0x0D: "♫", 0x0E: "☼", 0x0F: "►", 0x10: "◄", 0x11: "↕",
            0x12: "‼", 0x13: "¶", 0x14: "§", 0x15: "▬", 0x16: "↨", 0x17: "↑",
            0x18: "↓", 0x19: "→", 0x1A: "←", 0x1B: "∟", 0x1C: "↔", 0x1D: "▲",
            0x1E: "▼", 0x1F: " "
        }
        # fmt: on

        for y in range(16):
            for x in range(16):
                cp437_char = y * 16 + x
                if cp437_char <= 0x1F:  # Control characters
                    char = cp437_control_map[cp437_char]
                else:
                    char = bytes([cp437_char]).decode("cp437")  # Decode CP437 to Unicode
                sub_console.print(x + 1, y + 1, char)

        x = console.width // 2 - sub_console.width // 2
        y = console.height // 2 - sub_console.height // 2
        sub_console.blit(console, x, y)

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[EventHandler]:
        return MainGameEventHandler(self.engine)
