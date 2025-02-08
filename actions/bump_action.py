from __future__ import annotations

from actions.action_with_direction_base import ActionWithDirectionBase
from actions.melee_action import MeleeAction
from actions.movement_action import MovementAction
from actions.push_action import PushAction
from components.pushable import Pushable


class BumpAction(ActionWithDirectionBase):
    def perform(self) -> None:
        if self.target_actor:
            return MeleeAction(self.actor, self.target_actor).perform()
        elif self.blocking_entity and self.blocking_entity.has_component(Pushable):
            return PushAction(self.actor, self.blocking_entity).perform()
        else:
            return MovementAction(self.actor, self.dx, self.dy).perform()
