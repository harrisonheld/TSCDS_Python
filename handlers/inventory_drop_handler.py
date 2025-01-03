from typing import Optional

from actions.drop_item_action import DropItemAction
from entity import Item
from handlers.action_or_handler import ActionOrHandler
from handlers.inventory_event_handler import InventoryEventHandler


class InventoryDropHandler(InventoryEventHandler):
    """Handle dropping an inventory item."""

    TITLE = "Select an item to drop"

    def on_item_selected(self, item: Item) -> Optional[ActionOrHandler]:
        """Drop this item."""
        return DropItemAction(self.engine.player, item)
