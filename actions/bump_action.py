from __future__ import annotations

from actions.action import Action
from actions.action_with_direction_base import ActionWithDirectionBase
from actions.converse_action import ConverseAction
from actions.melee_action import MeleeAction
from actions.movement_action import MovementAction
from actions.push_action import PushAction
from components.conversation import Conversation
from components.pushable import Pushable


class BumpAction(ActionWithDirectionBase):
    def perform(self) -> None:

        true_action: Action

        if self.target_actor:
            if self.target_actor.has_component(Conversation):
                true_action = ConverseAction(self.actor, self.target_actor)
            else:
                true_action = MeleeAction(self.actor, self.target_actor)
        elif self.blocking_entity and self.blocking_entity.has_component(Pushable):
            true_action = PushAction(self.actor, self.blocking_entity)
        else:
            true_action = MovementAction(self.actor, self.dx, self.dy)

        true_action.perform()
        self.next_handler = true_action.next_handler
