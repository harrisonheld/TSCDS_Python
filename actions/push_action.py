from __future__ import annotations

from actions.action import Action
from entity import Actor, Entity
from exceptions import Impossible
import helpers
import strings


class PushAction(Action):
    def __init__(self, actor: Actor, target: Entity, move_with_push=True):
        super().__init__(actor)
        self._target_entity = target
        self._move_with_push = move_with_push

    def perform(self) -> None:
        target = self._target_entity
        """If true, the pusher will move with the pushed object."""
        if not target:
            raise Impossible("There is nothing there to push.")
        if helpers.distance_chess(*target.xy, *self.actor.xy) > 1:
            raise Impossible("You can't reach that.")

        dx = target.x - self.actor.x
        dy = target.y - self.actor.y
        # add dxdy to get where the pushed object will go after the push
        dest_x = target.x + dx
        dest_y = target.y + dy

        if not self.engine.game_map.in_bounds(dest_x, dest_y):
            raise Impossible(f"The {target.name} cannot be pushed off the map.")
        if self.engine.game_map.get_blocking_entity_at_location(dest_x, dest_y):
            raise Impossible(f"You can't push the {target.name}. There is something in the way.")
        if not self.engine.game_map.tiles["walkable"][dest_x, dest_y]:
            raise Impossible(f"You can't push the {target.name} into a wall.")

        target.move(dx, dy)
        if self._move_with_push:
            self.actor.move(dx, dy)
        self.engine.message_log.add_message(f"The {self.actor.name} pushes the {target.name}.")
