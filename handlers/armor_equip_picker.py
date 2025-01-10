from typing import Callable, Optional

import tcod

from actions.action import Action
from actions.equip_to_first_possible_slot_action import EquipToFirstPossibleSlotAction
from components.equipment import SlotType
from engine import Engine
from entity import Item
from handlers.action_or_handler import ActionOrHandler
from handlers.ask_user_event_handler import AskUserEventHandler
from handlers.event_handler import EventHandler
from handlers.item_picker import ItemPicker
import color
import keys


class ArmorEquipPicker(ItemPicker):
    """Pick an armor of the given slot type."""

    TITLE = "Pick an armor"

    def __init__(self, engine: Engine, slot_type: SlotType):
        # super init comes after, because it uses the slot_type in its criteria method
        self.slot_type = slot_type
        super().__init__(engine)

    def criteria(self, item: Item) -> bool:
        if item.equippable is None:
            return False
        if item.equippable.slot_type != self.slot_type:
            return False
        return True

    def on_item_selected(self, item: Item) -> ActionOrHandler:
        return EquipToFirstPossibleSlotAction(self.engine.player, item)
