from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from engine import Engine
    from entity import Entity
    from game_map import GameMap


class BaseComponent:
    parent: Entity  # Owning entity instance.

    @property
    def gamemap(self) -> GameMap:
        return self.parent.gamemap

    @property
    def engine(self) -> Engine:
        return self.gamemap.engine

    def on_turn(self) -> None:
        """Called every turn by the engine."""
        pass

    def before_move(self) -> None:
        """Called when this entity moves, before the entity's xy is updated."""
        pass

    def after_move(self) -> None:
        """Called when this entity moves, after the entity's xy is updated."""
        pass
