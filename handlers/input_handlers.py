from __future__ import annotations

from typing import TYPE_CHECKING, Callable, Optional, Tuple, Type, Union

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


class SelectAdjacentHandler(AskUserEventHandler):
    """Handles asking the user for one of 8 directions."""

    def __init__(self, engine: Engine, callback: Callable[[Tuple[int, int]], Optional[Action]]):
        super().__init__(engine)
        self.callback = callback

    def on_render(self, console: tcod.console.Console) -> None:
        super().on_render(console)
        console.print(0, 0, "Select a direction:")

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[ActionOrHandler]:
        """Fire callback if directional key was pressed."""
        key = event.sym
        if key in keys.MOVE_KEYS:
            dx, dy = keys.MOVE_KEYS[key]
            return self.on_index_selected(self.engine.player.x + dx, self.engine.player.y + dy)
        return super().ev_keydown(event)

    def on_index_selected(self, x: int, y: int) -> Optional[Action]:
        return self.callback((x, y))


class SelectIndexHandler(AskUserEventHandler):
    """Handles asking the user for an index on the map."""

    def __init__(self, engine: Engine):
        """Sets the cursor to the player when this handler is constructed."""
        super().__init__(engine)
        player = self.engine.player
        engine.mouse_location = player.x, player.y

    def on_render(self, console: tcod.console.Console) -> None:
        """Highlight the tile under the cursor."""
        super().on_render(console)

        x, y = self.engine.mouse_location
        console.rgb["bg"][x, y] = color.white
        console.rgb["fg"][x, y] = color.black

    def on_index_selection_changed(self) -> None:
        pass

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[ActionOrHandler]:
        """Check for key movement or confirmation keys."""
        key = event.sym
        if key in keys.MOVE_KEYS:
            modifier = 1  # Holding modifier keys will speed up key movement.
            if event.mod & (tcod.event.KMOD_LSHIFT | tcod.event.KMOD_RSHIFT):
                modifier *= 5
            if event.mod & (tcod.event.KMOD_LCTRL | tcod.event.KMOD_RCTRL):
                modifier *= 10
            if event.mod & (tcod.event.KMOD_LALT | tcod.event.KMOD_RALT):
                modifier *= 20

            x, y = self.engine.mouse_location
            dx, dy = keys.MOVE_KEYS[key]
            x += dx * modifier
            y += dy * modifier
            # Clamp the cursor index to the map size.
            x = max(0, min(x, self.engine.game_map.width - 1))
            y = max(0, min(y, self.engine.game_map.height - 1))
            self.engine.mouse_location = x, y
            self.on_index_selection_changed()
            return None
        elif key in keys.CONFIRM_KEYS:
            return self.on_index_selected(*self.engine.mouse_location)
        return super().ev_keydown(event)

    def ev_mousebuttondown(self, event: tcod.event.MouseButtonDown) -> Optional[ActionOrHandler]:
        """Left click confirms a selection."""
        if self.engine.game_map.in_bounds(*event.tile):
            if event.button == 1:
                return self.on_index_selected(*event.tile)
        return super().ev_mousebuttondown(event)

    def on_index_selected(self, x: int, y: int) -> Optional[ActionOrHandler]:
        """Called when an index is selected."""
        raise NotImplementedError()


class SingleRangedAttackHandler(SelectIndexHandler):
    """Handles targeting a single enemy. Only the enemy selected will be affected."""

    def __init__(self, engine: Engine, callback: Callable[[Tuple[int, int]], Optional[Action]]):
        super().__init__(engine)

        self.callback = callback

    def on_index_selected(self, x: int, y: int) -> Optional[Action]:
        return self.callback((x, y))


class AreaRangedAttackHandler(SelectIndexHandler):
    """Handles targeting an area within a given radius. Any entity within the area will be affected."""

    def __init__(
        self,
        engine: Engine,
        radius: int,
        callback: Callable[[Tuple[int, int]], Optional[Action]],
    ):
        super().__init__(engine)

        self.radius = radius
        self.callback = callback

    def on_render(self, console: tcod.console.Console) -> None:
        """Highlight the tile under the cursor."""
        super().on_render(console)

        x, y = self.engine.mouse_location

        # Draw a rectangle around the targeted area, so the player can see the affected tiles.
        console.draw_frame(
            x=x - self.radius - 1,
            y=y - self.radius - 1,
            width=self.radius**2,
            height=self.radius**2,
            fg=color.red,
            clear=False,
        )

    def on_index_selected(self, x: int, y: int) -> Optional[Action]:
        return self.callback((x, y))


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


class PauseViewer(EventHandler):
    def on_render(self, console: tcod.console.Console) -> None:
        super().on_render(console)  # Draw the main state as the background.

        width = 19
        height = 19
        sub_console = tcod.console.Console(width, height)
        sub_console.draw_frame(0, 0, width, height, bg=color.black, fg=color.white)
        sub_console.print(width // 2, 0, "┤Paused├", alignment=tcod.constants.CENTER)
        sub_console.print(width // 2, 1, "save and quit", alignment=tcod.constants.CENTER)
        sub_console.print(1, 2, "[q] to main menu")
        sub_console.print(1, 3, "[Q] to desktop")

        x = console.width // 2 - sub_console.width // 2
        y = console.height // 2 - sub_console.height // 2
        sub_console.blit(console, x, y)

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[EventHandler]:
        key = event.sym

        if key == tcod.event.KeySym.q:
            if event.mod & (tcod.event.KMOD_LSHIFT | tcod.event.KMOD_RSHIFT):
                raise SystemExit()
            raise exceptions.SaveAndQuitToMainMenu()

        elif key in keys.MODIFIER_KEYS:
            return None
        else:
            return MainGameEventHandler(self.engine)

        return None
