from __future__ import annotations

from actions.action_with_direction_base import ActionWithDirectionBase
from exceptions import Impossible
import strings


class PushAction(ActionWithDirectionBase):
    def __init__(self, entity, dx, dy, move_with_push=True):
        super().__init__(entity, dx, dy)
        self._move_with_push = move_with_push

    def perform(self) -> None:
        target = self.target_entity
        """If true, the pusher will move with the pushed object."""
        if not target:
            raise Impossible("There is nothing there to push.")

        # destination of push action
        dest_x, dest_y = self.dest_xy
        # add dxdy again to get where the pushed object will go after the push
        dest_x += self.dx
        dest_y += self.dy

        if not self.engine.game_map.in_bounds(dest_x, dest_y):
            raise Impossible(f"The {target.name} cannot be pushed off the map.")
        if self.engine.game_map.get_blocking_entity_at_location(dest_x, dest_y):
            raise Impossible(f"You can't push the {target.name}. There is something in the way.")
        if not self.engine.game_map.tiles["walkable"][dest_x, dest_y]:
            raise Impossible(f"You can't push the {target.name} into a wall.")

        target.move(self.dx, self.dy)
        if self._move_with_push:
            self.actor.move(self.dx, self.dy)
        self.engine.message_log.add_message(f"The {self.actor.name} pushes the {target.name}.")
