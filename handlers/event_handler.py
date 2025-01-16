from typing import Optional

import tcod

from actions.action import Action
from engine import Engine
from handlers.base_event_handler import BaseEventHandler
import color
import exceptions


class EventHandler(BaseEventHandler):
    def __init__(self, engine: Engine):
        self.engine = engine
        self.do_render_engine = True
        """If true, will render the gamescreen: the playable area and message log."""

    def handle_events(self, event: tcod.event.Event) -> BaseEventHandler:
        """Handle events for input handlers with an engine."""
        action_or_handler = self.dispatch(event)
        if action_or_handler is None:
            return self
        if isinstance(action_or_handler, BaseEventHandler):
            return action_or_handler
        assert isinstance(action_or_handler, Action)
        action: Action = action_or_handler
        if self.handle_action(action):
            # A valid action was performed.
            if not self.engine.player.is_alive:
                # The player was killed sometime due to the action.
                from handlers.game_over_event_handler import GameOverEventHandler

                return GameOverEventHandler(self.engine)
            elif self.engine.player.level.requires_level_up:
                from handlers.level_up_event_handler import LevelUpEventHandler

                return LevelUpEventHandler(self.engine)
            elif action.next_handler:
                return action.next_handler
            else:
                from handlers.main_game_event_handler import MainGameEventHandler

                return MainGameEventHandler(self.engine)  # Return to the main handler.

        raise RuntimeError("Control should not reach this point.")

    def handle_action(self, action: Optional[Action]) -> bool:
        """Handle actions returned from event methods.

        Returns True if the action will advance a turn.
        """
        if action is None:
            return False

        try:
            action.perform()
        except exceptions.Impossible as exc:
            self.engine.message_log.add_message(exc.args[0], color.impossible)
            return False  # Skip enemy turn on failures.

        # TODO: enemies use visibility to know if they can see player.
        # if we change this, this first update visibility will no longer be necessary
        self.engine.update_visibility()
        self.engine.handle_enemy_turns()
        self.engine.update_visibility()

        return True

    def ev_mousemotion(self, event: tcod.event.MouseMotion) -> None:
        if self.engine.game_map.in_bounds(event.tile.x, event.tile.y):
            self.engine.mouse_location = event.tile.x, event.tile.y

    def on_render(self, console: tcod.console.Console, delta_time: float) -> None:
        if self.do_render_engine:
            self.engine.render(console)
