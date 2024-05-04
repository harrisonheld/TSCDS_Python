from __future__ import annotations

from typing import Tuple, Optional

from actions.action import Action
from entity import Actor, Entity


class ActionWithDirectionBase(Action):
    def __init__(self, entity: Actor, dx: int, dy: int):
        super().__init__(entity)

        self.dx = dx
        self.dy = dy

    @property
    def dest_xy(self) -> Tuple[int, int]:
        """Returns this actions destination."""
        return self.entity.x + self.dx, self.entity.y + self.dy

    @property
    def blocking_entity(self) -> Optional[Entity]:
        """Return the blocking entity at this actions destination.."""
        return self.engine.game_map.get_blocking_entity_at_location(*self.dest_xy)

    @property
    def target_actor(self) -> Optional[Actor]:
        """Return the actor at this actions destination."""
        return self.engine.game_map.get_actor_at_location(*self.dest_xy)

    @property
    def target_entity(self) -> Optional[Entity]:
        """Return the entity at this actions destination."""
        return self.engine.game_map.get_entity_at_location(*self.dest_xy)

    def perform(self) -> None:
        raise NotImplementedError()
