from __future__ import annotations

import color
from actions.action import Action


class WaitAction(Action):
    def perform(self) -> None:
        if self.entity is self.engine.player:
            self.engine.message_log.add_message("You wait.", color.player_action)
        pass
