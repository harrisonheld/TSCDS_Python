from __future__ import annotations

from actions.action_with_direction_base import ActionWithDirectionBase
import color
import exceptions


class SwapAction(ActionWithDirectionBase):
    """Swap positions with an entity."""

    def perform(self) -> None:
        target = self.target_entity
        if target is None:
            raise exceptions.Impossible("There is nothing there to swap with.")

        temp_xy = target.xy
        target.move_to(*self.entity.xy)
        self.entity.move_to(*temp_xy)
        self.engine.message_log.add_message(f"The {self.entity.name} swaps places with the {target.name}!", color.white)
