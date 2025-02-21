from __future__ import annotations

import random

from actions.action import Action
from components.conversation import Conversation
from components.melee_weapon import MeleeClass, MeleeWeapon
from entity import Actor
import color
import exceptions
import strings


class ConverseAction(Action):
    def __init__(self, actor: Actor, target: Actor) -> None:

        from handlers.conversation_handler import ConversationHandler

        conversation = target.get_component(Conversation)
        assert conversation is not None

        super().__init__(actor)
        self.target_actor = target
        self.next_handler = ConversationHandler(self.engine, conversation)

    def perform(self) -> None:
        self.engine.message_log.add_message(f"You converse with the {self.target_actor.name}.", color.white)
