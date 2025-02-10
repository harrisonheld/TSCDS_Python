from __future__ import annotations

from actions.action import Action
from entity import Actor, Item
from upgrades import Upgrade
import exceptions


class PickupAction(Action):
    """Pickup an item and add it to the inventory, if there is room for it."""

    def __init__(self, entity: Actor, item: Item):
        super().__init__(entity)
        self.item = item

    def perform(self) -> None:

        if self.item.x != self.actor.x or self.item.y != self.actor.y:
            raise exceptions.Impossible("You can't pick that up - it is too far away.")

        inventory = self.actor.inventory
        inventory.add(self.item)

        if isinstance(self.item, Upgrade):
            self.item.on_pickup(self.actor)

        if self.actor is self.engine.player:
            self.engine.message_log.add_message(f"You pick up the {self.item.name}.")
