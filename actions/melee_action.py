from __future__ import annotations

from actions.action_with_direction_base import ActionWithDirectionBase
import color
import exceptions
import strings


class MeleeAction(ActionWithDirectionBase):
    def perform(self) -> None:
        target = self.target_actor
        if not target:
            raise exceptions.Impossible("There is nothing there to attack.")

        damage = self.entity.fighter.power - target.fighter.defense

        # log message
        attacker = self.entity
        if damage > 0:
            attack_color = color.combat_good if attacker is self.engine.player else color.combat_bad
            if target is not self.engine.player and attacker is not self.engine.player:
                attack_color = color.combat_neutral
            self.engine.message_log.add_message(
                f"{attacker.name.capitalize()} attacks {target.name} for {damage} hit points.", attack_color
            )
        else:
            miss_color = color.combat_bad if attacker is self.engine.player else color.combat_neutral
            self.engine.message_log.add_message(
                f"{attacker.name.capitalize()} attacks {target.name} but does no damage.", miss_color
            )

        # do attack logic
        if damage > 0:
            target.fighter.take_damage(damage)
