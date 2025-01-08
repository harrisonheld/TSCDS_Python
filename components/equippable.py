from __future__ import annotations

from typing import TYPE_CHECKING

from components.base_component import BaseComponent
from components.equipment import SlotType

if TYPE_CHECKING:
    from entity import Item


class Equippable(BaseComponent):
    parent: Item

    def __init__(
        self,
        slot_type: SlotType,
        power_bonus: int = 0,
        defense_bonus: int = 0,
    ):
        self.slot_type = slot_type

        self.power_bonus = power_bonus
        self.defense_bonus = defense_bonus
