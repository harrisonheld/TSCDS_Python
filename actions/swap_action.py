from __future__ import annotations

from actions.action_with_direction_base import ActionWithDirectionBase
import color
import exceptions


class SwapAction(ActionWithDirectionBase):
    """Swap positions with an entity."""

    def perform(self) -> None:
        target = self.target_entity
        if self.target_actor:
            target = self.target_actor
        if target is None:
            raise exceptions.Impossible("There is nothing there to swap with.")

        temp_xy = target.xy
        target.move_to(*self.actor.xy)
        self.actor.move_to(*temp_xy)
        self.engine.message_log.add_message(f"The {self.actor.name} swaps places with the {target.name}!", color.white)
