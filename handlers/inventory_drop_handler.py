from typing import Optional

from actions.drop_item_action import DropItemAction
from entity import Item
from handlers.action_or_handler import ActionOrHandler
from handlers.item_picker import ItemPicker


class InventoryDropHandler(ItemPicker):
    """Handle dropping an inventory item."""

    TITLE = "Select an item to drop"

    def __init__(self, engine):
        super().__init__(engine)

    def on_item_selected(self, item: Item) -> Optional[ActionOrHandler]:
        """Drop this item."""
        action = DropItemAction(self.engine.player, item)
        action.next_handler = self
        return action
