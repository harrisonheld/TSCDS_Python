from __future__ import annotations

from actions.action import Action
from actions.equip_action import EquipAction
from components.equipment import EquipmentSlot
from entity import Actor, Item
import exceptions


class EquipToFirstPossibleSlotAction(Action):
    """Equips the item to the first *empty* slot of the same type.
    If there are no such empty slots, equips to the first slot of the same type."""

    def __init__(self, entity: Actor, item: Item):
        super().__init__(entity)

        self.item = item

    def perform(self) -> None:

        assert self.item.equippable is not None

        # find the first empty slot of item.slot_type
        chosenSlot = None
        for slot in self.actor.equipment.slots:
            if slot.item is None and slot.slot_type == self.item.equippable.slot_type:
                chosenSlot = slot
                break

        # if there is no empty slot, find the first slot of the same type - we will just equip over it, uneqipping it
        if chosenSlot is None:
            for slot in self.actor.equipment.slots:
                if slot.slot_type == self.item.equippable.slot_type:
                    chosenSlot = slot
                    break

        if chosenSlot is None:
            raise exceptions.Impossible(
                f"{self.item.name} goes in the {self.item.equippable.slot_type.name} slot, but there is no such slot."
            )

        EquipAction(self.actor, self.item, chosenSlot).perform()
