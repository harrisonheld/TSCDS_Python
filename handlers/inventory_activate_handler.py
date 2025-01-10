from typing import Optional

from actions.equip_to_first_possible_slot_action import EquipToFirstPossibleSlotAction
from entity import Item
from handlers.action_or_handler import ActionOrHandler
from handlers.item_picker import ItemPicker
import color


class InventoryActivateHandler(ItemPicker):
    """Handle using an inventory item."""

    TITLE = "Select an item to use"

    def on_item_selected(self, item: Item) -> Optional[ActionOrHandler]:
        if item.consumable:
            return item.consumable.get_action(self.engine.player)
        elif item.equippable:
            return EquipToFirstPossibleSlotAction(self.engine.player, item)
        else:
            self.engine.message_log.add_message("That item has no uses.", color.impossible)
            return None
