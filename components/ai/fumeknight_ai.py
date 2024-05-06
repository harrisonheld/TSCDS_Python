from __future__ import annotations

from typing import List, Tuple

import color
import entity_factories
from actions.bump_action import BumpAction
from actions.spawn_action import SpawnAction
from actions.wait_action import WaitAction
from components.ai.ai_base import AIBase
from entity import Actor


class FumeKnightAI(AIBase):
    def __init__(self, entity: Actor):
        super().__init__(entity)
        self.path: List[Tuple[int, int]] = []
        self.gas_period = 10
        self.gas_cooldown = 7
        self.gas_duration = 3  # for how many turns to emit gas

    def perform(self) -> None:
        target = self.engine.player
        dx = target.x - self.entity.x
        dy = target.y - self.entity.y
        distance = max(abs(dx), abs(dy))

        self.gas_cooldown -= 1
        if self.gas_duration == self.gas_cooldown:
            self.engine.message_log.add_message("The Fume Knight impales his ventilated sword into the ground.", color.yellow)
            WaitAction(self.entity).perform()
            return
        if self.gas_cooldown < self.gas_duration:
            if self.gas_cooldown == self.gas_duration - 1:
                self.engine.message_log.add_message("The Fume Knight's sword begins to release toxic gas from the earth.", color.pink)
            # else:
            #     self.engine.message_log.add_message("The Fume Knight's sword continues to release residual vapor.", color.yellow)
            if self.gas_cooldown == 0:
                self.gas_cooldown = self.gas_period
            SpawnAction(self.entity, entity_factories.gas, self.entity.x, self.entity.y).perform()

        if self.engine.game_map.visible[self.entity.x, self.entity.y]:
            self.path = self.get_path(target.x, target.y)

        if self.path:
            old_x, old_y = self.entity.x, self.entity.y
            dest_x, dest_y = self.path.pop(0)
            BumpAction(
                self.entity,
                dest_x - old_x,
                dest_y - old_y,
            ).perform()
            return

        WaitAction(self.entity).perform()
