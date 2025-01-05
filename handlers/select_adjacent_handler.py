from typing import Callable, Optional, Tuple

import tcod

from actions.action import Action
from engine import Engine
from handlers.action_or_handler import ActionOrHandler
from handlers.ask_user_event_handler import AskUserEventHandler
import keys


class SelectAdjacentHandler(AskUserEventHandler):
    """Handles asking the user for one of 8 directions."""

    def __init__(self, engine: Engine, callback: Callable[[Tuple[int, int]], Optional[Action]]):
        super().__init__(engine)
        self.callback = callback

    def on_render(self, console: tcod.console.Console, delta_time: float) -> None:
        super().on_render(console, delta_time)
        console.print(0, 0, "Select a direction:")

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[ActionOrHandler]:
        """Fire callback if directional key was pressed."""
        key = event.sym
        if key in keys.MOVE_KEYS:
            dx, dy = keys.MOVE_KEYS[key]
            return self.on_index_selected(self.engine.player.x + dx, self.engine.player.y + dy)
        return super().ev_keydown(event)

    def on_index_selected(self, x: int, y: int) -> Optional[Action]:
        return self.callback((x, y))
