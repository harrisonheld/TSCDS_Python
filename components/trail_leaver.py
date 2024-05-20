from __future__ import annotations

from typing import TYPE_CHECKING

from components.base_component import BaseComponent

if TYPE_CHECKING:
    from entity import Entity


class TrailLeaver(BaseComponent):

    def __init__(self, trail_blueprint: Entity):
        self.trail_blueprint = trail_blueprint

    def before_move(self) -> None:
        self.trail_blueprint.spawn(self.gamemap, *self.parent.xy)
