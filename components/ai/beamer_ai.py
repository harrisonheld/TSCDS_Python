from __future__ import annotations

from typing import List, Tuple
import random

from actions.bump_action import BumpAction
from actions.melee_action import MeleeAction
from actions.movement_action import MovementAction
from actions.wait_action import WaitAction
from components.ai.ai_base import AIBase
from entity import Actor, Entity
from shape.ray import Ray
import blueprints.actors as actors
import color
import tile_types


class BeamerAI(AIBase):

    def __init__(self, entity: Actor):
        super().__init__(entity)
        self.path: List[Tuple[int, int]] = []

        self.ray_cooldown = 5
        self.ray_cooldown_curr = random.randint(3, self.ray_cooldown)  # inclusive-inclusive
        self.beam_endpoint: Tuple[int, int] = (-1, -1)
        self.indicators: List[Entity] = []
        self.stored_hp = -1  # store the hp to know if we got hit while focusing beam

    def perform(self) -> None:
        target = self.engine.player
        dx = target.x - self.entity.x
        dy = target.y - self.entity.y
        distance = max(abs(dx), abs(dy))  # Chebyshev distance.

        self.ray_cooldown_curr -= 1

        # if we have taken aim, fire the beam
        if self.beam_endpoint != (-1, -1):
            # check if we got hit while focusing beam
            if self.stored_hp > self.entity.fighter.hp:
                self.engine.message_log.add_message("The beamer's focus is interrupted.", color.yellow)
                self.beam_endpoint = (-1, -1)
                for indicator in self.indicators:
                    self.engine.game_map.entities.remove(indicator)
                self.indicators.clear()
                # set cooldown to half so it'll fire another beam soonish
                self.ray_cooldown_curr = self.ray_cooldown // 2
                return

            # damage every actor in the beam and remove the indicators
            self.engine.message_log.add_message("The beamer fires a beam!", color.combat_neutral)
            for indicator in self.indicators:
                for actor in self.engine.game_map.get_actors_at_location(indicator.x, indicator.y):
                    beam_damage = self.entity.fighter.power * 2 - actor.fighter.defense
                    if beam_damage > 0:
                        atk_color = color.combat_bad if actor is self.engine.player else color.combat_neutral
                        self.engine.message_log.add_message(
                            f"The beam hits the {actor.name} for {beam_damage} damage.", atk_color
                        )
                        actor.fighter.take_damage(beam_damage)
                    else:
                        self.engine.message_log.add_message(
                            f"The beam hits the {actor.name} but does no damage.", color.combat_neutral
                        )
                self.engine.game_map.entities.remove(indicator)
            self.indicators.clear()
            self.beam_endpoint = (-1, -1)
            self.ray_cooldown_curr = self.ray_cooldown
            return

        # take aim
        if self.ray_cooldown_curr <= 0 and self.can_see(self.entity, target):
            self.engine.message_log.add_message("The beamer focuses its gaze.", color.yellow)
            ray = Ray(self.entity.x, self.entity.y, target.x, target.y)
            self.stored_hp = self.entity.fighter.hp
            first = True
            for x, y in ray:
                if first:
                    first = False
                    continue
                if self.engine.game_map.tiles[x, y] == tile_types.wall:
                    self.beam_endpoint = (x, y)
                    break

                indicator = actors.beamer_ray_indicator.spawn(self.entity.gamemap, x, y)
                self.indicators.append(indicator)
            return

        # walking
        if self.can_see(self.entity, target):
            if distance <= 1:
                MeleeAction(self.entity, dx, dy).perform()
                return
            self.path = self.get_path(target.x, target.y)
        if self.path:
            dest_x, dest_y = self.path.pop(0)
            return MovementAction(
                self.entity,
                dest_x - self.entity.x,
                dest_y - self.entity.y,
            ).perform()

        WaitAction(self.entity).perform()

    def on_die(self) -> None:
        for indicator in self.indicators:
            self.engine.game_map.entities.remove(indicator)
        self.indicators.clear()
