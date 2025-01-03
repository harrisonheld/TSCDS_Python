from __future__ import annotations

from typing import List, Tuple
import random

from actions.bump_action import BumpAction
from actions.melee_action import MeleeAction
from actions.movement_action import MovementAction
from actions.wait_action import WaitAction
from components.ai.ai_base import AIBase
from entity import Actor


class FrogWardenAI(AIBase):
    def __init__(self, entity: Actor):
        super().__init__(entity)
        self.path: List[Tuple[int, int]] = []
        self.hop_chance = 0.25

    def perform(self) -> None:
        target = self.engine.player
        dx = target.x - self.entity.x
        dy = target.y - self.entity.y
        distance = max(abs(dx), abs(dy))  # Chebyshev distance.

        if self.can_see(self.entity, target):
            # if next to target
            if distance <= 1:
                # try for hop over the target
                opposite_x = self.entity.x + 2 * dx
                opposite_y = self.entity.y + 2 * dy
                if (
                    random.random() < self.hop_chance
                    and self.engine.game_map.in_bounds(opposite_x, opposite_y)
                    and not self.engine.game_map.get_blocking_entity_at_location(opposite_x, opposite_y)
                ):
                    MovementAction(self.entity, 2 * dx, 2 * dy).perform()
                    self.engine.message_log.add_message(f"The {self.entity.name} hops over you!")
                    return
                # if no hop, melee
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