from __future__ import annotations

from typing import Union


from actions.action import Action

# base_event_handler.py imports this, so we use a string instead of the actual type here.
ActionOrHandler = Union[Action, "BaseEventHandler"] # type: ignore
"""An event handler return value which can trigger an action or switch active handlers.

If a handler is returned then it will become the active handler for future events.
If an action is returned it will be attempted and if it's valid then
MainGameEventHandler will become the active handler.
"""










