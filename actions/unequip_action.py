from __future__ import annotations

from actions.action import Action
from actions.drop_item_action import DropItemAction
from components.equipment import EquipmentSlot
from entity import Actor, Item
import exceptions


class UnequipAction(Action):
    def __init__(self, entity: Actor, slot: EquipmentSlot, to_floor: bool = False):
        super().__init__(entity)

        self.slot = slot
        self.to_floor = to_floor

    def perform(self) -> None:

        item = self.slot.item
        if item is None:
            raise exceptions.Impossible("There's nothing to unequip here.")

        if not self.to_floor:
            self.actor.inventory.add(item)

        self.slot.item = None
        self.engine.message_log.add_message(f"You unequip the {item.name}.")

        if self.to_floor:
            item.place(self.actor.x, self.actor.y, self.actor.gamemap)
