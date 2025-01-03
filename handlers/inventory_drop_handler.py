from actions.drop_item_action import DropItemAction
from entity import Item
from handlers.inventory_event_handler import InventoryEventHandler
from handlers.action_or_handler import ActionOrHandler
from typing import Optional


class InventoryDropHandler(InventoryEventHandler):
    """Handle dropping an inventory item."""

    TITLE = "Select an item to drop"

    def on_item_selected(self, item: Item) -> Optional[ActionOrHandler]:
        """Drop this item."""
        return DropItemAction(self.engine.player, item)