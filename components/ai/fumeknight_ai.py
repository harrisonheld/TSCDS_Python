from __future__ import annotations

from typing import List, Tuple

from actions.bump_action import BumpAction
from actions.melee_action import MeleeAction
from actions.movement_action import MovementAction
from actions.wait_action import WaitAction
from components.ai.ai_base import AIBase
from entity import Actor
import blueprints.actors as actors
import color


class FumeKnightAI(AIBase):
    def __init__(self, entity: Actor):
        super().__init__(entity)
        self.path: List[Tuple[int, int]] = []
        self.gas_period = 10
        self.gas_cooldown = 7
        self.gas_duration = 3  # for how many turns to emit gas

    def perform(self) -> None:
        target = self.engine.player
        dx = target.x - self.actor.x
        dy = target.y - self.actor.y
        distance = max(abs(dx), abs(dy))

        self.gas_cooldown -= 1
        if self.gas_duration == self.gas_cooldown:
            self.engine.message_log.add_message(
                "The Fume Knight impales his ventilated sword into the ground.", color.yellow
            )
            WaitAction(self.actor).perform()
            return
        if self.gas_cooldown < self.gas_duration:
            if self.gas_cooldown == self.gas_duration - 1:
                self.engine.message_log.add_message(
                    "The Fume Knight's sword begins to release toxic gas from the earth.", color.yellow
                )
            # else:
            #     self.engine.message_log.add_message("The Fume Knight's sword continues to release residual vapor.", color.yellow)
            if self.gas_cooldown == 0:
                self.gas_cooldown = self.gas_period
            actors.gas.spawn(self.actor.gamemap, *self.actor.xy)

        if self.can_see(self.actor, target):
            if distance <= 1:
                MeleeAction(self.actor, dx, dy).perform()
                return
            self.path = self.get_path(target.x, target.y)

        if self.path:
            old_x, old_y = self.actor.x, self.actor.y
            dest_x, dest_y = self.path.pop(0)
            MovementAction(
                self.actor,
                dest_x - old_x,
                dest_y - old_y,
            ).perform()
            return

        WaitAction(self.actor).perform()
