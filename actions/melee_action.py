from __future__ import annotations

import random

from actions.action_with_direction_base import ActionWithDirectionBase
import color
import exceptions
import strings


class MeleeAction(ActionWithDirectionBase):
    def perform(self) -> None:
        target = self.target_actor
        if not target:
            raise exceptions.Impossible("There is nothing there to attack.")

        attacker = self.actor
        power = attacker.fighter.power
        defense = target.fighter.defense

        total_penetrations = 0
        while True:
            # roll three d20s
            dice = [random.randint(1, 20) for _ in range(3)]

            penetrations = 0
            for die in dice:
                # 20's penetrate twice, and always succeed
                if die == 20:
                    penetrations += 2
                    continue
                # 1's always fail
                elif die == 1:
                    break
                elif die + power > defense:
                    penetrations += 1
                    continue
                else:
                    break
            total_penetrations += penetrations

            if penetrations < 3:
                break
            # reduce power for next round
            power -= 6

        damage = total_penetrations

        # log message
        attacker = self.actor
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
