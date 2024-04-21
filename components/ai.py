from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional, Tuple
import random

import numpy as np
import tcod

import entity_factories
from actions import Action, MeleeAction, MovementAction, WaitAction, RangedAction, BumpAction, DisplaceAction

if TYPE_CHECKING:
    from entity import Actor
    from entity import Entity


class BaseAI(Action):
    def perform(self) -> None:
        raise NotImplementedError()

    def get_path(self, dest_x: int, dest_y: int) -> List[Tuple[int, int]]:
        """Compute and return a path to the target position.

        If there is no valid path then returns an empty list.
        """
        # Copy the walkable array.
        cost = np.array(self.entity.gamemap.tiles["walkable"], dtype=np.int8)

        for entity in self.entity.gamemap.entities:
            # Check that an entity blocks movement and the cost isn't zero (blocking.)
            if entity.blocks_movement and cost[entity.x, entity.y]:
                # Add to the cost of a blocked position.
                # A lower number means more enemies will crowd behind each other in
                # hallways.  A higher number means enemies will take longer paths in
                # order to surround the player.
                cost[entity.x, entity.y] += 10

        # Create a graph from the cost array and pass that graph to a new pathfinder.
        graph = tcod.path.SimpleGraph(cost=cost, cardinal=2, diagonal=3)
        pathfinder = tcod.path.Pathfinder(graph)

        pathfinder.add_root((self.entity.x, self.entity.y))  # Start position.

        # Compute the path to the destination and remove the starting point.
        path: List[List[int]] = pathfinder.path_to((dest_x, dest_y))[1:].tolist()

        # Convert from List[List[int]] to List[Tuple[int, int]].
        return [(index[0], index[1]) for index in path]


class HostileEnemy(BaseAI):
    def __init__(self, entity: Actor):
        super().__init__(entity)
        self.path: List[Tuple[int, int]] = []

    def perform(self) -> None:
        target = self.engine.player
        dx = target.x - self.entity.x
        dy = target.y - self.entity.y
        distance = max(abs(dx), abs(dy))  # Chebyshev distance.

        if self.engine.game_map.visible[self.entity.x, self.entity.y]:
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


class RangedEnemy(BaseAI):
    fire_range = 5
    flee_range = 3

    def __init__(self, entity: Actor):
        super().__init__(entity)
        self.path: List[Tuple[int, int]] = []

    def perform(self) -> None:
        target = self.engine.player
        dx = target.x - self.entity.x
        dy = target.y - self.entity.y
        distance = max(abs(dx), abs(dy))  # Chebyshev distance.

        if self.engine.game_map.visible[self.entity.x, self.entity.y]:

            if distance <= 1:
                return MeleeAction(self.entity, dx, dy).perform()
            elif distance <= self.flee_range:
                self.path = self.get_path(target.x, target.y)
            elif distance <= self.fire_range:
                return RangedAction(self.entity, dx, dy).perform()
            else:
                self.path = self.get_path(target.x, target.y)

        if self.path:
            dest_x, dest_y = self.path.pop(0)
            return MovementAction(
                self.entity,
                dest_x - self.entity.x,
                dest_y - self.entity.y,
            ).perform()

        return WaitAction(self.entity).perform()


class ConfusedEnemy(BaseAI):
    """
    A confused enemy will stumble around aimlessly for a given number of turns, then revert back to its previous AI.
    If an actor occupies a tile it is randomly moving into, it will attack.
    """

    def __init__(self, entity: Actor, previous_ai: Optional[BaseAI], turns_remaining: int):
        super().__init__(entity)

        self.previous_ai = previous_ai
        self.turns_remaining = turns_remaining

    def perform(self) -> None:
        # Revert the AI back to the original state if the effect has run its course.
        if self.turns_remaining <= 0:
            self.engine.message_log.add_message(f"The {self.entity.name} is no longer confused.")
            self.entity.ai = self.previous_ai
        else:
            # Pick a random direction
            direction_x, direction_y = random.choice(
                [
                    (-1, -1),  # Northwest
                    (0, -1),  # North
                    (1, -1),  # Northeast
                    (-1, 0),  # West
                    (1, 0),  # East
                    (-1, 1),  # Southwest
                    (0, 1),  # South
                    (1, 1),  # Southeast
                ]
            )

            self.turns_remaining -= 1

            # The actor will either try to move or attack in the chosen random direction.
            # Its possible the actor will just bump into the wall, wasting a turn.
            return BumpAction(
                self.entity,
                direction_x,
                direction_y,
            ).perform()


class IndrixAI(BaseAI):
    def __init__(self, entity: Actor):
        super().__init__(entity)
        self.path: List[Tuple[int, int]] = []
        self.leap_period = 7
        self.leap_cooldown = 4
        self.leaping = 0
        self.leap_indicator: Entity = None

    def perform(self) -> None:
        target = self.engine.player
        dx = target.x - self.entity.x
        dy = target.y - self.entity.y
        distance = max(abs(dx), abs(dy))  # Chebyshev distance.

        # Leap towards the player if the cooldown is ready.
        if self.leap_cooldown <= 0 and distance > 2:
            self.engine.message_log.add_message("Indrix leaps into the air!")
            self.leap_cooldown = self.leap_period
            self.leaping = 2
            self.entity.x, self.entity.y = (-1, -1)
            self.leap_indicator = entity_factories.indrix_leap_indicator.spawn(self.entity.gamemap, target.x, target.y)
            turns = "turns" if self.leaping > 1 else "turn"
            self.leap_indicator.description = f"Indrix will land in {self.leaping} {turns}."
            return
        # If currently in air
        if self.leaping > 0:
            self.leaping -= 1
            turns = "turns" if self.leaping > 1 else "turn"
            self.leap_indicator.description = f"Indrix will land in {self.leaping} {turns}."
            if self.leaping == 0:
                # Land
                self.entity.x, self.entity.y = self.leap_indicator.xy
                self.engine.game_map.entities.remove(self.leap_indicator)
                self.leap_indicator = None
                self.engine.message_log.add_message("Indrix slams down his folded carbide hammer!")
                if self.entity.xy == target.xy:
                    DisplaceAction(target).perform()
                    dx = target.x - self.entity.x
                    dy = target.y - self.entity.y
                    self.entity.fighter.base_power += 4
                    MeleeAction(self.entity, dx, dy).perform()
                    self.entity.fighter.base_power -= 4

            return

        self.leap_cooldown -= 1

        if self.engine.game_map.visible[self.entity.x, self.entity.y]:
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
            # Leave a trail of fire if there is no fire there already.
            if not self.engine.game_map.get_entities_at_location(old_x, old_y):
                entity_factories.fire.spawn(self.entity.gamemap, old_x, old_y)
            return

        WaitAction(self.entity).perform()
