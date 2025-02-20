from __future__ import annotations

from typing import List, Tuple

from actions.bump_action import BumpAction
from actions.melee_action import MeleeAction
from actions.movement_action import MovementAction
from actions.wait_action import WaitAction
from components.ai.ai_base import AIBase
from entity import Actor


class NpcAI(AIBase):
    def perform(self) -> None:
        WaitAction(self.actor).perform()
