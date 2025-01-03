from engine import Engine
from entity import Item
from handlers.inventory_event_handler import InventoryEventHandler
from handlers.event_handler import EventHandler
from handlers.action_or_handler import ActionOrHandler
from typing import Optional

import tcod


class InspectItemHandler(EventHandler):
    def __init__(self, engine: Engine, parent_handler: InventoryEventHandler, item: Item):
        self.parent_handler = parent_handler
        self.item = item
        super().__init__(engine)

    def on_render(self, console: tcod.console.Console) -> None:
        self.parent_handler.on_render(console)
        self.engine.look_block.render_at(console, self.item, *(2, 2))

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[ActionOrHandler]:
        return self.parent_handler