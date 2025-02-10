from __future__ import annotations

from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from engine import Engine
    from entity import Actor
    from handlers.base_event_handler import BaseEventHandler


class Action:
    def __init__(self, actor: Actor) -> None:
        super().__init__()
        self.actor = actor
        """The Actor which is to perform this action."""
        self.next_handler: Optional[BaseEventHandler] = None
        """If set, the game will switch to the next handler to be returned after this action is performed."""

    @property
    def engine(self) -> Engine:
        """Return the engine this action belongs to."""
        return self.actor.gamemap.engine

    def perform(self) -> None:
        """Perform this action with the objects needed to determine its scope.

        `self.engine` is the scope this action is being performed in.

        `self.entity` is the object performing the action.

        This method must be overridden by Action subclasses.
        """
        raise NotImplementedError()
