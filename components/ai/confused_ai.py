from __future__ import annotations

from typing import Optional
import random

from actions.bump_action import BumpAction
from components.ai.ai_base import AIBase
from entity import Actor
import color


class ConfusedAI(AIBase):
    """
    A confused enemy will stumble around aimlessly for a given number of turns, then revert back to its previous AI.
    If an actor occupies a tile it is randomly moving into, it will attack.
    """

    def __init__(self, entity: Actor, previous_ai: Optional[AIBase], turns_remaining: int, silent: bool = False):
        super().__init__(entity)

        self._previous_ai = previous_ai
        self._turns_remaining = turns_remaining
        self._silent = silent

        if not silent:
            self.engine.message_log.add_message(f"The {self.actor.name} is confused!", color.combat_good)

    def add_turns_remaining(self, turns: int):
        self._turns_remaining += turns

    def get_turns_remaining(self):
        return self._turns_remaining

    def set_turns_remaining(self, turns: int):
        self._turns_remaining = turns

    def perform(self) -> None:
        # Revert the AI back to the original state if the effect has run its course.
        if self._turns_remaining <= 0:
            if not self._silent:
                self.engine.message_log.add_message(
                    f"The {self.actor.name} is no longer confused.", color.combat_neutral
                )
            self.actor.ai = self._previous_ai
        else:
            # Pick a random direction
            direction_x, direction_y = random.choice(
                [
                    (-1, -1),  # Northwest
                    (0, -1),  # North
                    (1, -1),  # Northeast
                    (-1, 0),  # West
                    (1, 0),  # East
                    (-1, 1),  # Southwest
                    (0, 1),  # South
                    (1, 1),  # Southeast
                ]
            )

            self._turns_remaining -= 1

            # The actor will either try to move or attack in the chosen random direction.
            # Its possible the actor will just bump into the wall, wasting a turn.
            return BumpAction(
                self.actor,
                direction_x,
                direction_y,
            ).perform()
