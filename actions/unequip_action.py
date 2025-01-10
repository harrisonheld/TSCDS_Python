from __future__ import annotations

from actions.action import Action
from components.equipment import EquipmentSlot
from entity import Actor, Item
import exceptions


class UnequipAction(Action):
    def __init__(self, entity: Actor, item: Item):
        super().__init__(entity)

        self.item = item

    def perform(self) -> None:

        if self.entity.inventory.is_full:
            raise exceptions.Impossible("Nowhere to put that - your inventory is full.")

        slot: EquipmentSlot
        for s in self.entity.equipment.slots:
            if s.item is self.item:
                slot = s
                break

        if slot is None:
            raise exceptions.Impossible(f"You cannot unequip the {self.item.name} - you aren't wearing it.")

        slot.item = None
        self.entity.inventory.add(self.item)
        self.engine.message_log.add_message(f"You unequip the {self.item.name}.")
