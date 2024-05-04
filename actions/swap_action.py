from __future__ import annotations

import color
import exceptions
from actions.action_with_direction_base import ActionWithDirectionBase


class SwapAction(ActionWithDirectionBase):
    """Swap positions with an entity."""
    def perform(self) -> None:
        target = self.target_entity
        if target is None:
            raise exceptions.Impossible("There is nothing there to swap with.")

        temp_x = target.x
        temp_y = target.y
        target.x = self.entity.x
        target.y = self.entity.y
        self.entity.x = temp_x
        self.entity.y = temp_y
        self.engine.message_log.add_message(f"The {self.entity.name} swaps places with the {target.name}!", color.white)
