from typing import List, Optional

import tcod

from entity import Item
from handlers.action_or_handler import ActionOrHandler
from handlers.event_handler import EventHandler
from handlers.item_picker import ItemPicker
from handlers.main_game_event_handler import MainGameEventHandler
import blueprints.items as items
import color
import keys


class DebugItemSpawner(ItemPicker):

    TITLE = "(Debug) Debug Item Spawner"

    def __init__(self, engine):
        all = [getattr(items, name) for name in dir(items) if not name.startswith("_")]
        self.all_items = [x for x in all if isinstance(x, Item)]

        super().__init__(engine)

    def on_item_selected(self, item: Item) -> Optional[ActionOrHandler]:
        item.spawn(self.engine.game_map, self.engine.player.x, self.engine.player.y)
        self.engine.message_log.add_message(f"Spawned '{item.name}'.", color.debug)
        return None

    def generate_items(self) -> List[Item]:
        # no need to do any update logic, so juts return what we already have
        return self.all_items
