from __future__ import annotations

from actions.action_with_direction_base import ActionWithDirectionBase
from actions.movement_action import MovementAction
from entity import Actor
import exceptions


class LeapAction(ActionWithDirectionBase):
    """Leap in a direction, for the specified distance. Will stop at the first obstacle.
    Only raises an exception if NO movement is possible.
    Otherwise, will perform the leap, just not all the way.
    """

    def __init__(self, actor: Actor, dx: int, dy: int, distance: int):
        super().__init__(actor, dx, dy)
        self.distance = distance

    def perform(self) -> None:

        dist_thusfar = 0
        for _ in range(self.distance):
            try:
                MovementAction(self.actor, self.dx, self.dy).perform()
                dist_thusfar += 1
            except exceptions.Impossible:
                break

        if dist_thusfar == 0:
            raise exceptions.Impossible("You cannot leap in that direction.")
