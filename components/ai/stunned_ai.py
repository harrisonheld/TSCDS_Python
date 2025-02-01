from __future__ import annotations

from typing import Optional

from components.ai.ai_base import AIBase
from entity import Actor
import color


class StunnedAI(AIBase):
    """
    A stunned enemy will do nothing for a number of turns, then revert back to its previous AI.
    """

    def __init__(self, entity: Actor, previous_ai: Optional[AIBase], turns_remaining: int, silent: bool = False):
        super().__init__(entity)
        self._previous_ai = previous_ai
        self._turns_remaining = turns_remaining
        self._silent = silent

        if not self._silent:
            self.engine.message_log.add_message(f"The {self.actor.name} is stunned!", color.combat_good)

    def add_turns_remaining(self, turns: int) -> None:
        self._turns_remaining += turns

    def get_turns_remaining(self) -> int:
        return self._turns_remaining

    def set_turns_remaining(self, turns: int) -> None:
        self._turns_remaining = turns

    def perform(self) -> None:
        # Revert the AI back to the original state if the effect has run its course.
        if self._turns_remaining <= 0:
            if not self._silent:
                self.engine.message_log.add_message(
                    f"The {self.actor.name} is no longer stunned.", color.combat_neutral
                )
            self.actor.ai = self._previous_ai

        self._turns_remaining -= 1
