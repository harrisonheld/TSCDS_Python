from __future__ import annotations

import random

from actions.action import Action
from entity import Actor
import exceptions


class DisplaceAction(Action):
    """Displace an entity in a random direction - usually with the intention of un-intersecting it."""

    def __init__(self, entity: Actor):
        super().__init__(entity)

    def perform(self) -> None:
        # try all 8 directions in random order
        directions = [(dx, dy) for dx in [-1, 0, 1] for dy in [-1, 0, 1] if (dx, dy) != (0, 0)]
        random.shuffle(directions)
        for dx, dy in directions:
            dest_x, dest_y = self.actor.x + dx, self.actor.y + dy
            if not self.engine.game_map.in_bounds(dest_x, dest_y):
                continue
            if not self.engine.game_map.tiles["walkable"][dest_x, dest_y]:
                continue
            if self.engine.game_map.get_blocking_entity_at_location(dest_x, dest_y):
                continue
            self.actor.move(dx, dy)
            return

        raise exceptions.Impossible("No free spaces around the entity.")
