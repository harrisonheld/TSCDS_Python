from __future__ import annotations

from enum import Enum, auto
from typing import TYPE_CHECKING, List, Optional

from components.base_component import BaseComponent

if TYPE_CHECKING:
    from entity import Actor, Item


class SlotType(Enum):
    HAND = auto()  # held items, like weapons
    HEAD = auto()
    BODY = auto()
    LEGS = auto()
    HANDS = auto()  # worn items, like a pair of gloves
    FEET = auto()


class Equipment(BaseComponent):

    class EquipmentSlot:
        def __init__(self, slot_type: SlotType, item: Optional[Item] = None):
            self.slot_type = slot_type
            self.item: Optional[Item] = item

    def __init__(self):
        self.parent: Actor = None
        self.slots: List[self.EquipmentSlot] = []

    def add_slot(self, slotType: SlotType) -> None:
        newSlot = self.EquipmentSlot(slotType)
        self.slots.append(newSlot)

    @property
    def defense_bonus(self) -> int:
        bonus = 0

        for slot in self.slots:
            if item := slot.item:
                bonus += item.equippable.defense_bonus

        return bonus

    @property
    def power_bonus(self) -> int:
        bonus = 0

        for slot in self.slots:
            if item := slot.item:
                bonus += item.equippable.power_bonus

        return bonus

    def item_is_equipped(self, item: Item) -> bool:
        return self.item_slot(item) is not None

    def item_slot(self, item: Item) -> Optional[EquipmentSlot]:
        return next((slot for slot in self.slots if slot.item == item), None)

    def equip_to_slot(self, slot: EquipmentSlot, item: Item, add_message: bool = True) -> None:
        currentItem = slot.item

        if currentItem is not None:
            self.unequip_from_slot(slot, add_message)

        slot.item = item

        if add_message:
            self.equip_message(item.name)

    def unequip_from_slot(self, slot: EquipmentSlot, add_message: bool = True) -> None:

        if slot.item is None:
            return

        if add_message:
            self.unequip_message(slot.item.name)

        slot.item = None

    def equip(self, equippable_item: Item, add_message: bool = True) -> None:
        """Equip the item to the first empty slot of correct type, and if there are none,
        unequip the first slot of correct type and use that one."""

        assert equippable_item.equippable

        # equip to first empty slot of correct type
        for slot in self.slots:
            if slot.item is None and slot.slot_type == equippable_item.equippable.slot_type:
                self.equip_to_slot(slot, equippable_item, add_message)
                if add_message:
                    self.equip_message(equippable_item.name)
                return

        # if there are no empty slots, unequip the first slot of correct type
        for slot in self.slots:
            if slot.item is not None and slot.slot_type == equippable_item.equippable.slot_type:
                self.unequip_from_slot(slot, add_message)
                self.equip_to_slot(slot, equippable_item, add_message)
                return

        # failed to find an empty slot
        if add_message:
            self.parent.gamemap.engine.message_log.add_message(
                f"You cannot equip the {equippable_item.name} - you don't have the right slot."
            )

    def unequip(self, equippable_item: Item, add_message: bool = True) -> None:
        if slot := self.item_slot(equippable_item):
            self.unequip_from_slot(slot, add_message)
            if add_message:
                self.unequip_message(equippable_item.name)
        else:
            if add_message:
                self.parent.gamemap.engine.message_log.add_message(
                    f"You cannot unequip the {equippable_item.name} - you aren't wearing it."
                )

    def unequip_message(self, item_name: str) -> None:
        self.parent.gamemap.engine.message_log.add_message(f"You remove the {item_name}.")

    def equip_message(self, item_name: str) -> None:
        self.parent.gamemap.engine.message_log.add_message(f"You equip the {item_name}.")
