from __future__ import annotations

from actions.wait_action import WaitAction
from entity import Actor, Entity


class OggleAction(WaitAction):
    def __init__(self, entity: Actor, to_oggle_at: Entity):
        self.to_oggle_at = to_oggle_at
        super().__init__(entity)

    def perform(self) -> None:
        if self.actor is self.engine.player:
            self.engine.message_log.add_message(
                f"You oggle the {self.to_oggle_at.name} lovingly.",
            )
        elif self.to_oggle_at is self.engine.player:
            self.engine.message_log.add_message(f"The {self.actor.name} oggles you lovingly.")
        else:
            self.engine.message_log.add_message(f"The {self.actor.name} oggles the {self.to_oggle_at.name} lovingly.")
        pass
