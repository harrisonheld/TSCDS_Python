from __future__ import annotations

from actions.item_action import ItemAction
from upgrades import Upgrade


class DropItemAction(ItemAction):
    def perform(self) -> None:
        if self.entity.equipment.item_is_equipped(self.item):
            self.entity.equipment.toggle_equip(self.item)

        self.entity.inventory.drop(self.item)

        if isinstance(self.item, Upgrade):
            self.item.on_drop(self.entity)
