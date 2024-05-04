from __future__ import annotations

import color
import exceptions
import strings
from actions.action_with_direction_base import ActionWithDirectionBase


class RangedAttackAction(ActionWithDirectionBase):
    def perform(self) -> None:
        target = self.target_actor
        if not target:
            raise exceptions.Impossible("Nothing to fire at.")

        damage = self.entity.fighter.power - target.fighter.defense

        attack_desc = f"{strings.preserve_capitalize(self.entity.name)} fires a bolt at {target.name}"
        if self.entity is self.engine.player:
            attack_color = color.player_action
        else:
            attack_color = color.enemy_atk

        if damage > 0:
            self.engine.message_log.add_message(f"{attack_desc} for {damage} hit points.", attack_color)
            target.fighter.hp -= damage
        else:
            self.engine.message_log.add_message(f"{attack_desc} but does no damage.", attack_color)
