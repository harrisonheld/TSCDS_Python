from typing import Optional

from entity import Item
from handlers.action_or_handler import ActionOrHandler
from handlers.item_picker import ItemPicker
import color


class InventoryBindsHandler(ItemPicker):
    """Handle binding an inventory item."""

    TITLE = "Select an item to bind"

    def __init__(self, engine):
        super().__init__(engine)
        self.show_inventory_count = True

    def on_item_selected(self, item: Item) -> Optional[ActionOrHandler]:
        if item.consumable:
            from handlers.pick_bind_handler import PickBindHandler

            return PickBindHandler(self.engine, self, item)
        else:
            self.engine.message_log.add_message("That item is not bindable.", color.impossible)
            return None
