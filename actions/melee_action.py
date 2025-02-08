from __future__ import annotations

import random

from actions.action import Action
from components.melee_weapon import MeleeClass, MeleeWeapon
from entity import Actor
import color
import exceptions
import strings


class MeleeAction(Action):
    def __init__(self, actor: Actor, target: Actor) -> None:
        super().__init__(actor)
        self.target_actor = target

    def perform(self) -> None:
        target = self.target_actor
        if not target:
            raise exceptions.Impossible("There is nothing there to attack.")

        attacker = self.actor

        # Pick a random weapon. If none, use fists
        weapon_items = [
            slot.item for slot in attacker.equipment.slots if slot.item and slot.item.get_component(MeleeWeapon)
        ]
        weapon: MeleeWeapon
        if not weapon_items:
            weapon = MeleeWeapon(MeleeClass.FIST, 1)
        else:
            chosen_weapon_item = random.choice(weapon_items)
            weapon_component = chosen_weapon_item.get_component(MeleeWeapon)

            if weapon_component is None:
                weapon = MeleeWeapon(MeleeClass.FIST, 1)
            else:
                weapon = weapon_component

        weapon_class = weapon.melee_class

        if weapon_class == MeleeClass.SPEAR:
            try:
                from actions.push_action import PushAction
                from components.ai.stunned_ai import StunnedAI

                PushAction(self.actor, target, move_with_push=False).perform()
                target.ai = StunnedAI(
                    entity=target,
                    previous_ai=target.ai,
                    turns_remaining=0,
                    silent=True,
                )
            except exceptions.Impossible as e:
                # if the push fails, print it, but continue on and do the attack.
                self.engine.message_log.add_message(e.args[0], color.impossible)
        elif weapon_class == MeleeClass.HAMMER:
            from components.ai.confused_ai import ConfusedAI
            from components.ai.stunned_ai import StunnedAI

            # first, confuse the target
            if not isinstance(target.ai, ConfusedAI) and not isinstance(target.ai, StunnedAI):
                target.ai = ConfusedAI(entity=target, previous_ai=target.ai, turns_remaining=2, silent=False)
            # if already confused, add stun
            elif isinstance(target.ai, ConfusedAI):
                target.ai = StunnedAI(
                    entity=target,
                    previous_ai=target.ai,
                    turns_remaining=3,
                    silent=False,
                )
            # finally, inflict mental retardation
            elif isinstance(target.ai, StunnedAI):
                self.engine.message_log.add_message(
                    f"The {target.name} has become mentally retarded!", color.combat_good
                )
                target.ai.add_turns_remaining(2)

        power = attacker.fighter.power + weapon.damage
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
