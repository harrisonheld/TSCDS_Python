from __future__ import annotations

import color
from components.base_component import BaseComponent

from typing import TYPE_CHECKING

from components.fire_immune import FireImmune

if TYPE_CHECKING:
    from engine import Engine
    from entity import Entity
    from game_map import GameMap

class Fire(BaseComponent):
    def __init__(self, lifetime: int, damage: int):
        self._life_remaining = lifetime
        self._damage = damage

    def on_turn(self) -> None:
        # damage actors here
        for actor in self.parent.gamemap.get_actors_at_location(*self.parent.xy):
            # don't hurt FireImmune actors
            if actor.has_component(FireImmune):
                continue

            actor.fighter.take_damage(self._damage)

        # burn down
        self._life_remaining -= 1
        if self._life_remaining == 2:
            self.parent.description = "A modest fire."
            self.parent.color = color.orange
        elif self._life_remaining == 1:
            self.parent.description = "A dying fire."
            self.parent.color = color.yellow
        elif self._life_remaining <= 0:
            self.parent.gamemap.entities.remove(self.parent)

