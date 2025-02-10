from typing import Optional

import tcod

from engine import Engine
from handlers.action_or_handler import ActionOrHandler
from handlers.main_game_event_handler import MainGameEventHandler
from handlers.select_index_handler import SelectIndexHandler
from ui.circular_index_selector import CircularIndexSelector
import keys


class LookHandler(SelectIndexHandler):
    """Lets the player look around using the keyboard."""

    def __init__(self, engine: Engine):
        super().__init__(engine)
        n = len(list(self.engine.game_map.get_entities_at_location(*self.engine.mouse_location)))
        self.depth_selector = CircularIndexSelector(n)
        inc_keys = keys.MENU_NAV_UP - keys.MOVE_KEYS.keys()
        dec_keys = keys.MENU_NAV_DOWN - keys.MOVE_KEYS.keys()
        self.depth_selector.set_controls(inc_keys, dec_keys)

    def on_index_selection_changed(self) -> None:
        self.depth_selector.set_index(0)
        entities_here = len(list(self.engine.game_map.get_entities_at_location(*self.engine.mouse_location)))
        self.depth_selector.set_length(entities_here)

    def on_index_selected(self, x: int, y: int) -> MainGameEventHandler:
        """Return to main handler."""
        return MainGameEventHandler(self.engine)

    def on_exit(self) -> Optional[ActionOrHandler]:
        self.engine.mouse_location = (-1, -1)
        return super().on_exit()

    def on_render(self, console: tcod.console.Console, delta_time: float) -> None:
        """Draw a Look Block for the entity the cursor is on."""
        super().on_render(console, delta_time)

        x, y = self.engine.mouse_location

        if not self.engine.game_map.visible[x, y]:
            return

        entities = list(self.engine.game_map.get_entities_at_location(x, y))
        entities_here = len(entities)

        if entities_here > 0:
            # render the selected entity
            console.print(x, y, entities[self.depth_selector.get_index()].char)

            hint = entities_here > 1
            self.engine.look_block.render(console, entities[self.depth_selector.get_index()], show_multi_hint=hint)

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[ActionOrHandler]:

        if self.depth_selector.take_input(event.sym):
            return None

        result = super().ev_keydown(event)

        return result
