from __future__ import annotations

from actions.action import Action
from actions.pickup_action import PickupAction
from components.equipment import EquipmentSlot
from entity import Actor, Item
import exceptions


class EquipAction(Action):
    def __init__(self, entity: Actor, item: Item, slot: EquipmentSlot):
        super().__init__(entity)

        self.item = item
        self.slot = slot

    def perform(self) -> None:
        if self.item.equippable is None:
            raise exceptions.Impossible("{self.item.name} is not equippable.")

        if self.slot.slot_type != self.item.equippable.slot_type:
            raise exceptions.Impossible(
                f"{self.item.name} goes in the {self.item.equippable.slot_type.name} slot, not the {self.slot.slot_type.name} slot."
            )

        if self.item not in self.entity.inventory.items:
            PickupAction(self.entity, self.item).perform()

        currentItem = self.slot.item
        oldItem = None

        if currentItem is not None:
            oldItem = currentItem
        self.slot.item = self.item
        if self.item in self.entity.inventory.items:
            self.entity.inventory.remove(self.item)
        if oldItem is not None:
            self.entity.inventory.add(oldItem)

        if oldItem is not None:
            self.engine.message_log.add_message(f"You unequip the {oldItem.name}.")
        self.engine.message_log.add_message(f"You equip the {self.item.name}.")
