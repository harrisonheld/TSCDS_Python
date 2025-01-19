from typing import Callable, List, Optional

import tcod

from actions.action import Action
from actions.equip_action import EquipAction
from components.equipment import EquipmentSlot, SlotType
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
    """Pick an equippable item to put in a given slot."""

    TITLE = "Pick an item to equip"

    def __init__(self, engine: Engine, parent: EquipmentScreen, slot: EquipmentSlot):
        # super init comes after, because it uses the slot_type in its criteria method
        self.slot = slot
        super().__init__(engine)
        self.parent = parent
        self.do_render_engine = False
        self.show_on_ground_hint = True

    def generate_items(self) -> List[Item]:
        # all inventory items, plus items at player location
        candidates = self.engine.player.inventory.items + self.engine.game_map.get_items_at_location(
            *self.engine.player.xy
        )

        return [item for item in candidates if item.equippable and item.equippable.slot_type == self.slot.slot_type]

    def on_render(self, console, delta_time):
        self.parent.on_render(console, delta_time)
        super().on_render(console, delta_time)

    def on_item_selected(self, item: Item) -> ActionOrHandler:
        action = EquipAction(self.engine.player, item, self.slot)
        action.next_handler = self.parent  # after performing, go back to the equipment screen
        return action

    def on_exit(self) -> Optional[ActionOrHandler]:
        return self.parent
