from __future__ import annotations

from actions.action import Action
import color


class WaitAction(Action):
    def perform(self) -> None:
        if self.actor is self.engine.player:
            self.engine.message_log.add_message("You wait.")

        # literlly do nothing
        pass
