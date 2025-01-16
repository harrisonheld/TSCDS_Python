from typing import Optional

from actions.drop_item_action import DropItemAction
from actions.pickup_action import PickupAction
from entity import Item
from handlers.action_or_handler import ActionOrHandler
from handlers.base_event_handler import BaseEventHandler
from handlers.item_picker import ItemPicker
import color
import exceptions


class GetHandler(ItemPicker):
    """Handle picking up an item from a list of items on the ground."""

    TITLE = "Select an item to get"

    def generate_items(self):
        xy = self.engine.player.xy
        return self.engine.game_map.get_items_at_location(*xy)

    def on_item_selected(self, item: Item) -> Optional[ActionOrHandler]:
        """Drop this item."""
        self._dirty = True
        action = PickupAction(self.engine.player, item)
        action.next_handler = self
        return action
