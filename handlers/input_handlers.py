from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Type, Union

import tcod

from actions.action import Action
from actions.bump_action import BumpAction
from actions.pickup_action import PickupAction
from actions.wait_action import WaitAction
import actions.take_stairs_action
import color
import exceptions
import keys

if TYPE_CHECKING:
    from engine import Engine


ActionOrHandler = Union[Action, "BaseEventHandler"]
"""An event handler return value which can trigger an action or switch active handlers.

If a handler is returned then it will become the active handler for future events.
If an action is returned it will be attempted and if it's valid then
MainGameEventHandler will become the active handler.
"""


class BaseEventHandler(tcod.event.EventDispatch[ActionOrHandler]):
    def handle_events(self, event: tcod.event.Event) -> BaseEventHandler:
        """Handle an event and return the next active event handler."""
        state = self.dispatch(event)
        if isinstance(state, BaseEventHandler):
            return state
        assert not isinstance(state, Action), f"{self!r} can not handle actions."
        return self

    def on_render(self, console: tcod.console.Console) -> None:
        raise NotImplementedError()

    def ev_quit(self, event: tcod.event.Quit) -> Optional[Action]:
        raise SystemExit()


class EventHandler(BaseEventHandler):
    def __init__(self, engine: Engine):
        self.engine = engine

    def handle_events(self, event: tcod.event.Event) -> BaseEventHandler:
        """Handle events for input handlers with an engine."""
        action_or_state = self.dispatch(event)
        if isinstance(action_or_state, BaseEventHandler):
            return action_or_state
        if self.handle_action(action_or_state):
            # A valid action was performed.
            if not self.engine.player.is_alive:
                # The player was killed sometime during or after the action.
                from handlers.game_over_event_handler import GameOverEventHandler
                return GameOverEventHandler(self.engine)
            elif self.engine.player.level.requires_level_up:
                from handlers.level_up_event_handler import LevelUpEventHandler
                return LevelUpEventHandler(self.engine)
            return MainGameEventHandler(self.engine)  # Return to the main handler.
        return self

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
            return False  # Skip enemy turn on exceptions.

        # TODO: enemies use visibility to know if they can see player.
        # if we change this, this first update visibility will no longer be necessary
        self.engine.update_visibility()
        self.engine.handle_enemy_turns()

        self.engine.update_visibility()

        return True

    def ev_mousemotion(self, event: tcod.event.MouseMotion) -> None:
        if self.engine.game_map.in_bounds(event.tile.x, event.tile.y):
            self.engine.mouse_location = event.tile.x, event.tile.y

    def on_render(self, console: tcod.console.Console) -> None:
        self.engine.render(console)


class AskUserEventHandler(EventHandler):
    """Handles user input for actions which require special input."""

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[ActionOrHandler]:
        """By default any key exits this input handler."""
        if event.sym in keys.MODIFIER_KEYS:
            return None
        return self.on_exit()

    def ev_mousebuttondown(self, event: tcod.event.MouseButtonDown) -> Optional[ActionOrHandler]:
        """By default any mouse click exits this input handler."""
        return self.on_exit()

    def on_exit(self) -> Optional[ActionOrHandler]:
        """Called when the user is trying to exit or cancel an action.

        By default this returns to the main event handler.
        """
        return MainGameEventHandler(self.engine)


class MainGameEventHandler(EventHandler):
    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[ActionOrHandler]:
        key = event.sym
        modifier = event.mod

        player = self.engine.player

        if key == tcod.event.KeySym.PERIOD and modifier & (tcod.event.KMOD_LSHIFT | tcod.event.KMOD_RSHIFT):
            # TODO: remove this cheat lol
            player.x, player.y = self.engine.game_map.downstairs_location
            return actions.take_stairs_action.TakeStairsAction(player)

        if key in keys.MOVE_KEYS:
            dx, dy = keys.MOVE_KEYS[key]
            return BumpAction(player, dx, dy)
        elif key in keys.WAIT_KEYS:
            return WaitAction(player)
        elif key in keys.BINDABLE_KEYS:
            if key not in player.inventory.binds:
                self.engine.message_log.add_message(f"{key.name} is unbound.", color.impossible)
                return None

            # Retrieve the item bound to the key
            item = player.inventory.binds[key]
            assert item.consumable is not None
            return item.consumable.get_action(player)

        elif key == tcod.event.KeySym.ESCAPE:
            from handlers.pause_viewer import PauseViewer
            return PauseViewer(self.engine)
        elif key == tcod.event.KeySym.m:
            from handlers.history_viewer import HistoryViewer
            return HistoryViewer(self.engine)
        elif key == tcod.event.KeySym.SLASH:
            from handlers.help_viewer import HelpViewer
            return HelpViewer(self.engine)

        elif key == tcod.event.KeySym.g:
            return PickupAction(player)
        elif key == tcod.event.KeySym.i:
            from handlers.inventory_activate_handler import InventoryActivateHandler
            return InventoryActivateHandler(self.engine)
        elif key == tcod.event.KeySym.b:
            from handlers.inventory_binds_handler import InventoryBindsHandler
            return InventoryBindsHandler(self.engine)
        elif key == tcod.event.KeySym.d:
            from handlers.inventory_drop_handler import InventoryDropHandler
            return InventoryDropHandler(self.engine)
        elif key == tcod.event.KeySym.c:
            from handlers.character_screen_event_handler import CharacterScreenEventHandler
            return CharacterScreenEventHandler(self.engine)
        elif key == tcod.event.KeySym.l:
            from handlers.look_handler import LookHandler
            return LookHandler(self.engine)

        # No valid key was pressed
        return None


