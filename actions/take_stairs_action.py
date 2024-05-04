from __future__ import annotations

import color
import exceptions
from actions.action import Action


class TakeStairsAction(Action):
    def perform(self) -> None:
        """
        Take the stairs, if any exist at the entity's location.
        """
        if (self.entity.x, self.entity.y) == self.engine.game_map.downstairs_location:
            self.engine.game_world.generate_floor()
            self.engine.message_log.add_message("You descend the staircase.", color.descend)
        else:
            raise exceptions.Impossible("There are no stairs here.")
