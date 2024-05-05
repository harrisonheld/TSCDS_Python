from __future__ import annotations

import random
from typing import List, Tuple

import color
import entity_factories
import tile_types
from actions.bump_action import BumpAction
from actions.melee_action import MeleeAction
from actions.movement_action import MovementAction
from actions.wait_action import WaitAction
from components.ai.ai_base import AIBase
from entity import Actor, Entity
from shape.ray import Ray


class BeamerAI(AIBase):

    def __init__(self, entity: Actor):
        super().__init__(entity)
        self.path: List[Tuple[int, int]] = []

        self.ray_cooldown = 5
        self.ray_cooldown_curr = random.randint(3, self.ray_cooldown)  # inclusive-inclusive
        self.beam_endpoint: Tuple[int, int] = (-1, -1)
        self.indicators: List[Entity] = []

    def perform(self) -> None:
        target = self.engine.player
        dx = target.x - self.entity.x
        dy = target.y - self.entity.y
        distance = max(abs(dx), abs(dy))  # Chebyshev distance.

        self.ray_cooldown_curr -= 1

        # if we have taken aim, fire the beam
        if self.beam_endpoint != (-1, -1):
            self.engine.message_log.add_message("The beamer fires a beam!", color.yellow)

            # clear the beam indicators
            for indicator in self.indicators:
                self.engine.game_map.entities.remove(indicator)
            self.indicators.clear()
            self.beam_endpoint = (-1, -1)

            self.ray_cooldown_curr = self.ray_cooldown
            return

        # take aim
        if self.ray_cooldown_curr <= 0 and self.can_see(self.entity, target):
            self.engine.message_log.add_message("The beamer focuses its gaze.", color.yellow)
            ray = Ray(self.entity.x, self.entity.y, target.x, target.y)
            first = True
            for (x, y) in ray:
                if first:
                    first = False
                    continue
                if self.engine.game_map.tiles[x, y] == tile_types.wall:
                    self.beam_endpoint = (x, y)
                    break

                indicator = entity_factories.beamer_ray_indicator.spawn(self.entity.gamemap, x, y)
                self.indicators.append(indicator)
            return

        # walking
        if self.can_see(self.entity, target):
            self.path = self.get_path(target.x, target.y)
        if self.path:
            dest_x, dest_y = self.path.pop(0)
            return BumpAction(
                self.entity,
                dest_x - self.entity.x,
                dest_y - self.entity.y,
            ).perform()

        WaitAction(self.entity).perform()