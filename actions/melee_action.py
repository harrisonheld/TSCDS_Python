from __future__ import annotations

import color
import exceptions
import strings
from actions.action_with_direction_base import ActionWithDirectionBase


class MeleeAction(ActionWithDirectionBase):
    def perform(self) -> None:
        target = self.target_actor
        if not target:
            raise exceptions.Impossible("Nothing to attack.")

        damage = self.entity.fighter.power - target.fighter.defense

        attack_desc = f"{strings.preserve_capitalize(self.entity.name)} attacks {target.name}"
        if self.entity is self.engine.player:
            attack_desc = f"You attack {target.name}"
            attack_color = color.player_action
        else:
            attack_color = color.enemy_atk

        if damage > 0:
            self.engine.message_log.add_message(f"{attack_desc} for {damage} hit points.", attack_color)
            target.fighter.take_damage(damage)
        else:
            self.engine.message_log.add_message(f"{attack_desc} but does no damage.", attack_color)
