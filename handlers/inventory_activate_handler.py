from typing import Optional

from actions.equip_action import EquipAction
from entity import Item
from handlers.action_or_handler import ActionOrHandler
from handlers.inventory_event_handler import InventoryEventHandler
import color


class InventoryActivateHandler(InventoryEventHandler):
    """Handle using an inventory item."""

    TITLE = "Select an item to use"

    def on_item_selected(self, item: Item) -> Optional[ActionOrHandler]:
        if item.consumable:
            return item.consumable.get_action(self.engine.player)
        elif item.equippable:
            return EquipAction(self.engine.player, item)
        else:
            self.engine.message_log.add_message("That item has no uses.", color.impossible)
            return None
