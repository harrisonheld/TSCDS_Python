from typing import Optional

import tcod

from actions.action import Action
from handlers.action_or_handler import ActionOrHandler


class BaseEventHandler(tcod.event.EventDispatch[ActionOrHandler]):
    def handle_events(self, event: tcod.event.Event) -> "BaseEventHandler":
        """Handle an event and return the next active event handler."""
        state = self.dispatch(event)
        if isinstance(state, BaseEventHandler):
            return state
        assert not isinstance(state, Action), f"{self!r} can not handle actions."
        return self

    def on_render(self, console: tcod.console.Console, delta_time: float) -> None:
        raise NotImplementedError()

    def ev_quit(self, event: tcod.event.Quit) -> Optional[Action]:
        raise SystemExit()

    def gain_focus(self) -> None:
        """Called when this handler gains focus, such as when the game starts
        or when the player closes a menu and this handler becomes the active one.
        """
        pass
