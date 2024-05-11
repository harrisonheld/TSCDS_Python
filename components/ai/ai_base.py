from __future__ import annotations

from typing import TYPE_CHECKING, List, Tuple

import numpy as np
import tcod

from actions.action import Action

if TYPE_CHECKING:
    from entity import Entity


class AIBase(Action):
    def perform(self) -> None:
        raise NotImplementedError()

    def on_die(self) -> None:
        pass

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
