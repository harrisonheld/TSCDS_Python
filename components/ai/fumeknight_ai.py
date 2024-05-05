from __future__ import annotations

from typing import List, Tuple

import color
import entity_factories
from actions.spawn_action import SpawnAction
from components.ai.ai_base import AIBase
from entity import Actor


class FumeKnightAI(AIBase):
    def __init__(self, entity: Actor):
        super().__init__(entity)
        self.path: List[Tuple[int, int]] = []

    def perform(self) -> None:
        target = self.engine.player
        dx = target.x - self.entity.x
        dy = target.y - self.entity.y

        SpawnAction(self.entity, entity_factories.gas, self.entity.x, self.entity.y).perform()
        self.engine.message_log.add_message("The Fume Knight releases a cloud of toxic gas!", color.yellow)
