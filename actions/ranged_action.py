from __future__ import annotations

import random

from actions.action import Action
from entity import Actor
import color
import exceptions
import strings


class RangedAction(Action):
    def __init__(self, actor: Actor, x: int, y: int) -> None:
        super().__init__(actor)
        self.x = x
        self.y = y

    def perform(self) -> None:
        print(str(self.x) + " " + str(self.y))
