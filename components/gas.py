from __future__ import annotations

import copy
import random

import color
from components.base_component import BaseComponent

from typing import TYPE_CHECKING

from components.fire_immune import FireImmune
from components.illumination import Illumination

if TYPE_CHECKING:
    from engine import Engine
    from entity import Entity
    from game_map import GameMap

class Gas(BaseComponent):
    def __init__(self, density: int, damage: int, spread_chance: float):
        self._density = density
        self._damage = damage
        self._spread_chance = spread_chance

    def on_turn(self) -> None:
        self._density -= 1
        if self._density == 3:
            self.parent.char = "▒"
        elif self._density == 2:
            self.parent.char = "░"
        elif self._density == 1:
            self.parent.char = "#"
        elif self._density <= 0:
            self.gamemap.entities.remove(self.parent)
            self.engine.message_log.add_message("The gas dissipates.", color.white)
            return

        # spread gas via deepclone
        for x in range(-1, 2):
            for y in range(-1, 2):
                if x == 0 and y == 0:
                    continue
                new_x, new_y = self.parent.x + x, self.parent.y + y
                if not self.gamemap.in_bounds(new_x, new_y):
                    continue
                if not self.gamemap.tiles["walkable"][new_x, new_y]:
                    continue
                if self.gamemap.get_blocking_entity_at_location(new_x, new_y):
                    continue
                if self._spread_chance < random.random():
                    continue
                # if there's already gas there, don't spread
                if any(entity for entity in self.gamemap.get_entities_at_location(new_x, new_y) if entity.has_component(Gas)):
                    continue
                new_gas = copy.deepcopy(self.parent)
                new_gas.place(new_x, new_y, self.gamemap)
                new_gas.get_component(Gas).density = self._density - 1

