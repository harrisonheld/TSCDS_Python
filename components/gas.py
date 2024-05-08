from __future__ import annotations

import copy
import random

import color
import entity_factories
from components.base_component import BaseComponent
from components.gas_immune import GasImmune

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from engine import Engine
    from entity import Entity
    from game_map import GameMap


class Gas(BaseComponent):
    def __init__(self, density: int, damage: int, spread_chance: float):
        self.density = density
        self.damage = damage
        self.spread_chance = spread_chance

    def do_contact_damage(self):
        for actor in self.parent.gamemap.get_actors_at_location(*self.parent.xy):

            if actor.has_component(GasImmune):
                continue

            actor.fighter.take_damage(self.damage)

            if actor is self.engine.player:
                self.engine.message_log.add_message(f"The gas scalds you for {self.damage} damage.", color.combat_bad)
            else:
                self.engine.message_log.add_message(f"The gas beneath the {actor.name} scalds for {self.damage} damage.", color.combat_neutral)

    def on_turn(self) -> None:

        self.do_contact_damage()

        self.density -= 1
        if self.density <= 0:
            self.gamemap.entities.remove(self.parent)
            self.engine.message_log.add_message("The gas dissipates.", color.white)
            return
        if self.density <= 2:
            self.parent.char = "░"
        elif self.density <= 4:
            self.parent.char = "▒"

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
                if self.spread_chance < random.random():
                    continue
                # if there's already gas there, don't spread
                if any(entity for entity in self.gamemap.get_entities_at_location(new_x, new_y) if entity.has_component(Gas)):
                    continue

                new_gas = copy.deepcopy(self.parent)
                new_gas.place(new_x, new_y, self.gamemap)
                gas_comp = new_gas.get_component(Gas)
                assert gas_comp is not None
                gas_comp.density = self.density - 1
                gas_comp.do_contact_damage()

                if random.random() < (0.1 * self.density):
                    entity_factories.fire.spawn(self.gamemap, new_x, new_y)
