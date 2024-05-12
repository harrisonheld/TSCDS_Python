from __future__ import annotations

from typing import TYPE_CHECKING

from components.base_component import BaseComponent
from components.fire_immune import FireImmune
from components.illumination import Illumination
import color

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

            if actor is self.engine.player:
                self.engine.message_log.add_message(
                    f"The fire beneath you burns for {self._damage} damage.", color.combat_bad
                )
            else:
                self.engine.message_log.add_message(
                    f"The fire beneath the {actor.name} burns for {self._damage} damage.", color.combat_neutral
                )

        # burn down
        self._life_remaining -= 1
        if self._life_remaining == 2:
            self.parent.description = "A dying fire."
            self.parent.color = color.orange
            if illumination := self.parent.get_component(Illumination):
                illumination.light_radius = max(0, illumination.light_radius - 1)
        if self._life_remaining <= 0:
            self.gamemap.entities.remove(self.parent)
            self.engine.message_log.add_message("The fire burns out.", color.white)
