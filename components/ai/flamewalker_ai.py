from __future__ import annotations

from typing import List, Tuple

import entity_factories
from actions.movement_action import MovementAction
from actions.oggle_action import OggleAction
from actions.spawn_action import SpawnAction
from actions.wait_action import WaitAction
from components.ai.ai_base import AIBase
from entity import Actor


class FlamewalkerAI(AIBase):
    """Pursue the player and leave a trail of fire. Does not attack otherwise."""
    def __init__(self, entity: Actor):
        super().__init__(entity)
        self.path: List[Tuple[int, int]] = []

    def perform(self) -> None:
        target = self.engine.player
        dx = target.x - self.entity.x
        dy = target.y - self.entity.y
        distance = max(abs(dx), abs(dy))  # Chebyshev distance.
        if distance <= 1:
            OggleAction(self.entity, target).perform()
            return

        if self.can_see(self.entity, target):
            self.path = self.get_path(target.x, target.y)
        if self.path:
            dest_x, dest_y = self.path.pop(0)
            old_x, old_y = self.entity.x, self.entity.y
            MovementAction(
                self.entity,
                dest_x - old_x,
                dest_y - old_y,
            ).perform()
            # Leave a trail of fire if there is no fire there already.
            if not self.engine.game_map.get_entities_at_location(old_x, old_y):
                SpawnAction(self.entity, entity_factories.fire, old_x, old_y).perform()
            return

        WaitAction(self.entity).perform()
