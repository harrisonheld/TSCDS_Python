from __future__ import annotations

from actions.action import Action
from actions.equip_action import EquipAction
from actions.unequip_action import UnequipAction
from entity import Actor, Item


class ToggleEquipAction(Action):
    def __init__(self, entity: Actor, item: Item):
        super().__init__(entity)

        self.item = item

    def perform(self) -> None:
        if self.entity.equipment.item_is_equipped(self.item):
            return UnequipAction(self.entity, self.item).perform()
        return EquipAction(self.entity, self.item).perform()
