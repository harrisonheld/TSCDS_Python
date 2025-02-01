from __future__ import annotations

from enum import Enum, auto
from typing import TYPE_CHECKING, List, Optional

from components.armor import Armor
from components.base_component import BaseComponent
from components.melee_weapon import MeleeWeapon

if TYPE_CHECKING:
    from entity import Actor, Item


class SlotType(Enum):
    HAND = auto()  # held items, like weapons
    HEAD = auto()
    BODY = auto()
    LEGS = auto()
    HANDS = auto()  # worn items, like a pair of gloves
    FEET = auto()
    MISSILE = auto()  # ranged weapons; guns, etc.
    THROWN = auto()


class EquipmentSlot:
    def __init__(self, slot_type: SlotType, item: Optional[Item] = None):
        self.slot_type = slot_type
        self.item: Optional[Item] = item


class Equipment(BaseComponent):
    def __init__(self) -> None:
        self.parent: Actor
        self.slots: List[EquipmentSlot] = []

    def add_slot(self, slotType: SlotType) -> None:
        newSlot = EquipmentSlot(slotType)
        self.slots.append(newSlot)

    @property
    def defense_bonus(self) -> int:
        bonus = 0

        for slot in self.slots:
            if item := slot.item:
                assert item.equippable is not None
                if armor := item.get_component(Armor):
                    bonus += armor.defense

        return bonus

    @property
    def power_bonus(self) -> int:
        bonus = 0

        for slot in self.slots:
            if item := slot.item:
                assert item.equippable is not None
                if weapon := item.get_component(MeleeWeapon):
                    bonus += weapon.damage

        return bonus
