from __future__ import annotations

from typing import List, Optional, Tuple

from actions.bump_action import BumpAction
from actions.displace_action import DisplaceAction
from actions.melee_action import MeleeAction
from actions.movement_action import MovementAction
from actions.wait_action import WaitAction
from components.ai.ai_base import AIBase
from components.pushable import Pushable
from entity import Actor, Entity, Item
import blueprints.actors as actors
import color


class IndrixAI(AIBase):
    def __init__(self, entity: Actor):
        super().__init__(entity)
        self.path: List[Tuple[int, int]] = []
        self.leap_period = 7
        self.air_time = 3  # how many turns after leaping before landing
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
            self.engine.message_log.add_message("Indrix leaps into the air!", color.yellow)
            self.leap_cooldown = self.leap_period
            self.leaping = self.air_time
            self.entity.x, self.entity.y = (-1, -1)
            self.leap_indicator = actors.indrix_leap_indicator.spawn(self.entity.gamemap, target.x, target.y)
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
                self.engine.message_log.add_message("Indrix slams down his folded carbide hammer!", color.yellow)
                if self.entity.xy == target.xy:
                    DisplaceAction(target).perform()
                    dx = target.x - self.entity.x
                    dy = target.y - self.entity.y
                    self.entity.fighter.base_power += 4
                    MeleeAction(self.entity, dx, dy).perform()
                    self.entity.fighter.base_power -= 4

                stuff_here = self.engine.game_map.get_entities_at_location(self.entity.x, self.entity.y)
                # find Equippable() in stuff_here
                for thing in stuff_here:
                    if isinstance(thing, Item) and thing.equippable and thing.equippable.power_bonus > 0:
                        damage = thing.equippable.power_bonus * 2
                        self.engine.message_log.add_message(
                            f"Indrix hurts himself on the dropped {thing.name} for {damage} damage.",
                            color.combat_good,
                        )
                        self.entity.fighter.take_damage(damage)
                    if thing.has_component(Pushable):
                        #  indrix hurts himself on the statue's horns
                        self.engine.message_log.add_message(
                            f"Indrix breaks the {thing.name} on landing! He takes 5 damage.", color.combat_good
                        )
                        self.entity.fighter.take_damage(5)
                        self.engine.game_map.entities.remove(thing)

            return

        self.leap_cooldown -= 1

        if self.can_see(self.entity, target):
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

    def on_die(self) -> None:
        if self.leap_indicator is not None:
            self.engine.game_map.entities.remove(self.leap_indicator)
