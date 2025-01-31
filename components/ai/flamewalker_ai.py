from __future__ import annotations

from typing import List, Tuple

from actions.movement_action import MovementAction
from actions.oggle_action import OggleAction
from actions.wait_action import WaitAction
from components.ai.ai_base import AIBase
from entity import Actor


class OgglerAI(AIBase):
    """Pursue the player and oggle when near. Does not attack otherwise."""

    def __init__(self, entity: Actor):
        super().__init__(entity)
        self.path: List[Tuple[int, int]] = []

    def perform(self) -> None:
        target = self.engine.player
        dx = target.x - self.actor.x
        dy = target.y - self.actor.y
        distance = max(abs(dx), abs(dy))  # Chebyshev distance.
        if distance <= 1:
            OggleAction(self.actor, target).perform()
            return

        if self.can_see(self.actor, target):
            self.path = self.get_path(target.x, target.y)
        if self.path:
            dest_x, dest_y = self.path.pop(0)
            old_x, old_y = self.actor.x, self.actor.y
            MovementAction(
                self.actor,
                dest_x - old_x,
                dest_y - old_y,
            ).perform()
            return

        WaitAction(self.actor).perform()
