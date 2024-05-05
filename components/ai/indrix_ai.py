from __future__ import annotations

from typing import List, Tuple, Optional

import entity_factories
from actions.displace_action import DisplaceAction
from actions.melee_action import MeleeAction
from actions.movement_action import MovementAction
from actions.wait_action import WaitAction
from components.ai.ai_base import AIBase
from entity import Actor, Entity, Item


class IndrixAI(AIBase):
    def __init__(self, entity: Actor):
        super().__init__(entity)
        self.path: List[Tuple[int, int]] = []
        self.leap_period = 7
        self.leap_cooldown = 4
        self.leaping = 0
        self.leap_indicator: Optional[Entity] = None

    def perform(self) -> None:
        target = self.engine.player
        dx = target.x - self.entity.x
        dy = target.y - self.entity.y
        distance = max(abs(dx), abs(dy))  # Chebyshev distance.

        # Leap towards the player if the cooldown is ready.
        if self.leap_cooldown <= 0 and distance > 1:
            self.engine.message_log.add_message("Indrix leaps into the air!")
            self.leap_cooldown = self.leap_period
            self.leaping = 2
            self.entity.x, self.entity.y = (-1, -1)
            self.leap_indicator = entity_factories.indrix_leap_indicator.spawn(self.entity.gamemap, target.x, target.y)
            turns = "turns" if self.leaping > 1 else "turn"
            self.leap_indicator.description = f"Indrix will land in {self.leaping} {turns}."
            return
        # If currently in air
        if self.leaping > 0:
            assert self.leap_indicator is not None

            self.leaping -= 1
            turns = "turns" if self.leaping > 1 else "turn"
            self.leap_indicator.description = f"Indrix will land in {self.leaping} {turns}."
            if self.leaping == 0:
                # Land
                self.entity.x, self.entity.y = self.leap_indicator.xy
                self.engine.game_map.entities.remove(self.leap_indicator)
                self.leap_indicator = None
                self.engine.message_log.add_message("Indrix slams down his folded carbide hammer!")
                if self.entity.xy == target.xy:
                    DisplaceAction(target).perform()
                    dx = target.x - self.entity.x
                    dy = target.y - self.entity.y
                    self.entity.fighter.base_power += 4
                    MeleeAction(self.entity, dx, dy).perform()
                    self.entity.fighter.base_power -= 4
                else:
                    stuff_here = self.engine.game_map.get_entities_at_location(self.entity.x, self.entity.y)
                    # find Equippable() in stuff_here
                    for thing in stuff_here:
                        if isinstance(thing, Item) and thing.equippable and thing.equippable.power_bonus > 0:
                            damage = thing.equippable.power_bonus * 5
                            self.engine.message_log.add_message(f"Indrix hurts himself on the dropped {thing.name} for {damage} damage.")
                            self.entity.fighter.hp -= damage

            return

        self.leap_cooldown -= 1

        if self.engine.game_map.visible[self.entity.x, self.entity.y]:
            if distance <= 1:
                MeleeAction(self.entity, dx, dy).perform()
                return

            self.path = self.get_path(target.x, target.y)

        if self.path:
            old_x, old_y = self.entity.x, self.entity.y
            dest_x, dest_y = self.path.pop(0)
            MovementAction(
                self.entity,
                dest_x - old_x,
                dest_y - old_y,
            ).perform()
            return

        WaitAction(self.entity).perform()
