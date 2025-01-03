from typing import Optional
from handlers.select_index_handler import SelectIndexHandler
import keys
from engine import Engine
from handlers.main_game_event_handler import MainGameEventHandler
from handlers.input_handlers import ActionOrHandler


import tcod


class LookHandler(SelectIndexHandler):
    """Lets the player look around using the keyboard."""

    def __init__(self, engine: Engine):
        super().__init__(engine)
        self.look_index = 0
        self.entities_here = 0

    def on_index_selected(self, x: int, y: int) -> MainGameEventHandler:
        """Return to main handler."""
        return MainGameEventHandler(self.engine)

    def on_exit(self) -> Optional[ActionOrHandler]:
        self.engine.mouse_location = (-1, -1)
        return super().on_exit()

    def on_render(self, console: tcod.console.Console) -> None:
        """Draw a Look Block for the entity the cursor is on."""
        super().on_render(console)

        x, y = self.engine.mouse_location

        if not self.engine.game_map.visible[x, y]:
            return

        entities = list(self.engine.game_map.get_entities_at_location(x, y))
        self.entities_here = len(entities)

        if self.entities_here > 0:
            # render the selected entity
            console.print(x, y, entities[self.look_index].char)

            hint = self.entities_here > 1
            self.engine.look_block.render(console, entities[self.look_index], show_multi_hint=hint)

    def on_index_selection_changed(self) -> None:
        self.look_index = 0
        super().on_index_selection_changed()

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[ActionOrHandler]:

        if self.entities_here > 0 and event.sym not in keys.MOVE_KEYS:
            if event.sym in keys.MENU_NAV_UP:
                self.look_index = (self.look_index + 1) % self.entities_here
                return None
            elif event.sym in keys.MENU_NAV_DOWN:
                self.look_index = (self.look_index - 1) % self.entities_here
                return None

        return super().ev_keydown(event)