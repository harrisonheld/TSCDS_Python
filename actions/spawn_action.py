from __future__ import annotations

from actions.action import Action
from entity import Actor, Entity
import color
import exceptions


class SpawnAction(Action):
    def __init__(self, entity: Actor, blueprint: Entity, spawn_x: int, spawn_y: int):
        """
        Spawn an entity at the given location by calling the supplied blueprint entity's spawn method.
        """
        super().__init__(entity)
        self.blueprint = blueprint
        self.spawn_x = spawn_x
        self.spawn_y = spawn_y

    def perform(self) -> None:
        self.blueprint.spawn(self.engine.game_map, self.spawn_x, self.spawn_y)
