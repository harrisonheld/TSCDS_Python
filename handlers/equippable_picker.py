from typing import Callable, List, Optional

import tcod

from actions.action import Action
from actions.equip_to_first_possible_slot_action import EquipToFirstPossibleSlotAction
from components.equipment import SlotType
from engine import Engine
from entity import Item
from handlers.action_or_handler import ActionOrHandler
from handlers.ask_user_event_handler import AskUserEventHandler
from handlers.equipment_screen import EquipmentScreen
from handlers.event_handler import EventHandler
from handlers.item_picker import ItemPicker
import color
import keys


class EquippablePicker(ItemPicker):
    """Pick an equippable item of the given slot type."""

    TITLE = "Pick an item to equip"

    def __init__(self, engine: Engine, parent: EquipmentScreen, slot_type: SlotType):
        # super init comes after, because it uses the slot_type in its criteria method
        self.slot_type = slot_type
        super().__init__(engine)
        self.parent = parent
        self.do_render_engine = False

    def generate_items(self) -> List[Item]:
        return [
            item
            for item in self.engine.player.inventory.items
            if item.equippable is not None and item.equippable.slot_type == self.slot_type
        ]

    def on_render(self, console, delta_time):
        self.parent.on_render(console, delta_time)
        super().on_render(console, delta_time)

    def on_item_selected(self, item: Item) -> ActionOrHandler:
        action = EquipToFirstPossibleSlotAction(self.engine.player, item)
        action.next_handler = self.parent  # after performing, go back to the equipment screen
        return action

    def on_exit(self) -> Optional[ActionOrHandler]:
        return self.parent
