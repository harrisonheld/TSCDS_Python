from __future__ import annotations

from actions.action_with_direction_base import ActionWithDirectionBase
from actions.melee_action import MeleeAction
from actions.movement_action import MovementAction
from actions.push_action import PushAction
from components.pushable import Pushable


class BumpAction(ActionWithDirectionBase):
    def perform(self) -> None:
        if self.target_entity and self.target_entity.has_component(Pushable):
            return PushAction(self.entity, self.dx, self.dy).perform()
        if self.target_actor:
            return MeleeAction(self.entity, self.dx, self.dy).perform()
        else:
            return MovementAction(self.entity, self.dx, self.dy).perform()
