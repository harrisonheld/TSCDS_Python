from __future__ import annotations

import random

from actions.action import Action
from components.ranged_weapon import RangedClass, RangedWeapon
from entity import Actor
import color
import exceptions
import strings


class RangedAttackAction(Action):
    def __init__(self, actor: Actor, target_actor: Actor):
        super().__init__(actor)
        self.target_actor = target_actor

    def perform(self) -> None:
        target = self.target_actor
        if not target:
            raise exceptions.Impossible("There is nothing there to attack.")

        attacker = self.actor

        weapon_items = [
            slot.item for slot in attacker.equipment.slots if slot.item and slot.item.get_component(RangedWeapon)
        ]
        if len(weapon_items) == 0:
            raise exceptions.Impossible("You have no ranged weapon equipped.")
        chosen_weapon_item = random.choice(weapon_items)
        assert chosen_weapon_item is not None
        weapon = chosen_weapon_item.get_component(RangedWeapon)
        assert weapon is not None
        weapon_class = weapon.ranged_class

        # log message
        attacker = self.actor
        damage = 2
        if damage > 0:
            attack_color = color.combat_good if attacker is self.engine.player else color.combat_bad
            if target is not self.engine.player and attacker is not self.engine.player:
                attack_color = color.combat_neutral
            self.engine.message_log.add_message(
                f"{attacker.name.capitalize()} shoots {target.name} for {damage} hit points.", attack_color
            )

        # attack logic
        target.fighter.take_damage(damage)
