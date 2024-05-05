from __future__ import annotations

from typing import List, Tuple

from actions.melee_action import MeleeAction
from actions.movement_action import MovementAction
from actions.wait_action import WaitAction
from components.ai.ai_base import AIBase
from entity import Actor


class HostileEnemyAI(AIBase):
    def __init__(self, entity: Actor):
        super().__init__(entity)
        self.path: List[Tuple[int, int]] = []

    def perform(self) -> None:
        target = self.engine.player
        dx = target.x - self.entity.x
        dy = target.y - self.entity.y
        distance = max(abs(dx), abs(dy))  # Chebyshev distance.

        if self.can_see(self.entity, target):
            if distance <= 1:
                MeleeAction(self.entity, dx, dy).perform()
                return

            self.path = self.get_path(target.x, target.y)

        if self.path:
            dest_x, dest_y = self.path.pop(0)
            MovementAction(
                self.entity,
                dest_x - self.entity.x,
                dest_y - self.entity.y,
            ).perform()
            return

        WaitAction(self.entity).perform()
