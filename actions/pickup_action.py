from __future__ import annotations

from actions.action import Action
from entity import Actor
from upgrades import Upgrade
import exceptions


class PickupAction(Action):
    """Pickup an item and add it to the inventory, if there is room for it."""

    def __init__(self, entity: Actor):
        super().__init__(entity)

    def perform(self) -> None:
        x = self.entity.x
        y = self.entity.y
        item = self.engine.game_map.get_item_at_location(x, y)
        if item is None:
            raise exceptions.Impossible("There is nothing here to pick up.")

        inventory = self.entity.inventory
        inventory.add(item)

        if isinstance(item, Upgrade):
            item.on_pickup(self.entity)
