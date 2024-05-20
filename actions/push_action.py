from __future__ import annotations

from actions.action_with_direction_base import ActionWithDirectionBase
from exceptions import Impossible
import strings


class PushAction(ActionWithDirectionBase):
    def perform(self) -> None:
        target = self.target_entity
        if not target:
            raise Impossible("There is nothing there to push.")

        # destination of push action
        dest_x, dest_y = self.dest_xy
        # add dxdy again to get where the pushed object will go after the push
        dest_x += self.dx
        dest_y += self.dy

        if not self.engine.game_map.in_bounds(dest_x, dest_y):
            raise Impossible("The object cannot be pushed off the map.")
        if self.engine.game_map.get_blocking_entity_at_location(dest_x, dest_y):
            raise Impossible("You can't push that. There is something in the way.")
        if not self.engine.game_map.tiles["walkable"][dest_x, dest_y]:
            raise Impossible("You can't push that into a wall.")

        target.move(self.dx, self.dy)
        self.entity.move(self.dx, self.dy)
        self.engine.message_log.add_message(
            f"The {self.entity.name} pushes the {target.name}."
        )
