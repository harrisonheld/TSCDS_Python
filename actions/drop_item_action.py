from __future__ import annotations

from actions.item_action import ItemAction
from upgrades import Upgrade


class DropItemAction(ItemAction):
    def perform(self) -> None:
        self.actor.inventory.drop(self.item)

        if isinstance(self.item, Upgrade):
            self.item.on_drop(self.actor)

        if self.actor is self.engine.player:
            self.engine.message_log.add_message(f"You drop the {self.item.name}.")
