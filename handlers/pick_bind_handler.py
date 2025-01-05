from typing import Optional

import tcod

from engine import Engine
from entity import Item
from handlers.action_or_handler import ActionOrHandler
from handlers.ask_user_event_handler import AskUserEventHandler
from handlers.inventory_binds_handler import InventoryBindsHandler
from handlers.main_game_event_handler import MainGameEventHandler
import keys


class PickBindHandler(AskUserEventHandler):
    def __init__(self, engine: Engine, parent_handler: InventoryBindsHandler, consumable_to_bind: Item):
        super().__init__(engine)
        self.parent_handler: InventoryBindsHandler = parent_handler
        self.consumable_to_bind: Item = consumable_to_bind

    def on_render(self, console: tcod.console.Console, delta_time: float) -> None:
        super().on_render(console, delta_time)
        # render the inventory too
        # self.parent_handler.on_render(console)
        console.print(0, 0, f"Pick a key to bind {self.consumable_to_bind.name} to (1-9):")

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[ActionOrHandler]:
        key = event.sym
        if key in keys.BINDABLE_KEYS:
            self.engine.player.inventory.bind(self.consumable_to_bind, key)
            return MainGameEventHandler(self.engine)
        else:
            return self.parent_handler
