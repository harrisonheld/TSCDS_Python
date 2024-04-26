from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional, Tuple
import random

import numpy as np
import tcod

import color
import entity_factories
from actions import Action, MeleeAction, MovementAction, WaitAction, RangedAction, BumpAction, DisplaceAction, \
    OggleAction
from entity import Item
from shape.ray import Ray

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

    def can_see(self, me: Entity, other: Entity) -> bool:
        """Return True if the other entity is within the FOV of me."""
        # as is, enemies see what players see. so if the enemy is visible, it can see you
        return self.entity.gamemap.visible[me.x, me.y]


class HostileEnemy(BaseAI):
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


class BeamerAI(BaseAI):

    def __init__(self, entity: Actor):
        super().__init__(entity)
        self.path: List[Tuple[int, int]] = []

        self.ray_cooldown = 5
        self.ray_charge = 1
        self.ray_cooldown_curr = self.ray_cooldown
        self.ray_charge_curr = 0
        self.indicators: List[Entity] = []

    def perform(self) -> None:
        target = self.engine.player
        dx = target.x - self.entity.x
        dy = target.y - self.entity.y
        distance = max(abs(dx), abs(dy))  # Chebyshev distance.

        for indicator in self.indicators:
            self.engine.game_map.entities.remove(indicator)
        self.indicators.clear()

        if self.can_see(self.entity, target):
            self.engine.message_log.add_message("The beamer focuses its gaze.", color.yellow)
            ray = Ray(self.entity.x, self.entity.y, dx, dy)
            first = True
            for (x, y) in ray:
                if first:
                    first = False
                    continue

                if self.engine.game_map.tiles["walkable"][x, y]:
                    indicator = entity_factories.beamer_ray_indicator.spawn(self.entity.gamemap, x, y)
                    self.indicators.append(indicator)
                    if self.engine.game_map.get_blocking_entity_at_location(x, y):
                        break

        if self.path:
            dest_x, dest_y = self.path.pop(0)
            return MovementAction(
                self.entity,
                dest_x - self.entity.x,
                dest_y - self.entity.y,
            ).perform()

        WaitAction(self.entity).perform()


class FlamewalkerAI(BaseAI):
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
                entity_factories.fire.spawn(self.entity.gamemap, old_x, old_y)
            return

        WaitAction(self.entity).perform()


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
        self.leap_indicator: Optional[Entity] = None

    def perform(self) -> None:
        target = self.engine.player
        dx = target.x - self.entity.x
        dy = target.y - self.entity.y
        distance = max(abs(dx), abs(dy))  # Chebyshev distance.

        # Leap towards the player if the cooldown is ready.
        if self.leap_cooldown <= 0 and distance > 1:
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
                else:
                    stuff_here = self.engine.game_map.get_entities_at_location(self.entity.x, self.entity.y)
                    # find Equippable() in stuff_here
                    for thing in stuff_here:
                        if isinstance(thing, Item) and thing.equippable and thing.equippable.power_bonus > 0:
                            damage = thing.equippable.power_bonus * 5
                            self.engine.message_log.add_message(f"Indrix hurts himself on the dropped {thing.name} for {damage} damage.")
                            self.entity.fighter.hp -= damage

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
            return

        WaitAction(self.entity).perform()


class FumeKnightAI(BaseAI):
    def __init__(self, entity: Actor):
        super().__init__(entity)
        self.path: List[Tuple[int, int]] = []
        self.phase = 1

    def perform(self) -> None:
        target = self.engine.player
        dx = target.x - self.entity.x
        dy = target.y - self.entity.y
        distance = max(abs(dx), abs(dy))  # Chebyshev distance.

        entity_factories.gas.spawn(self.engine.game_map, self.entity.x, self.entity.y)
