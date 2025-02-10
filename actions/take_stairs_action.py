from __future__ import annotations

from actions.action import Action
import color
import exceptions


class TakeStairsAction(Action):
    def perform(self) -> None:
        """
        Take the stairs, if any exist at the entity's location.
        """
        if (self.actor.x, self.actor.y) == self.engine.game_map.downstairs_location:
            self.engine.game_world.generate_floor()
        else:
            raise exceptions.Impossible("There are no stairs here to descend.")
