from __future__ import annotations

from actions.action import Action
from components.equipment import EquipmentSlot
from entity import Actor, Item


class EquipAction(Action):
    def __init__(self, entity: Actor, item: Item, slot: EquipmentSlot):
        super().__init__(entity)

        self.item = item
        self.slot = slot

    def perform(self) -> None:

        currentItem = self.slot.item
        oldItem = None

        if currentItem is not None:
            oldItem = currentItem
        self.slot.item = self.item
        self.entity.inventory.remove(self.item)
        if oldItem is not None:
            self.entity.inventory.add(oldItem)

        if oldItem is not None:
            self.engine.message_log.add_message(f"You unequip the {oldItem.name}.")
        self.engine.message_log.add_message(f"You equip the {self.item.name}.")
