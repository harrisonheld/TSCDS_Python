from __future__ import annotations

from actions.action_with_direction_base import ActionWithDirectionBase
from actions.melee_action import MeleeAction
from actions.movement_action import MovementAction


class BumpAction(ActionWithDirectionBase):
    def perform(self) -> None:
        if self.target_actor:
            return MeleeAction(self.entity, self.dx, self.dy).perform()

        else:
            return MovementAction(self.entity, self.dx, self.dy).perform()
