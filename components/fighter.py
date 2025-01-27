from __future__ import annotations

from typing import TYPE_CHECKING

from actions.drop_item_action import DropItemAction
from actions.unequip_action import UnequipAction
from components.base_component import BaseComponent
from render_order import RenderOrder
import blueprints.actors as actors
import color

if TYPE_CHECKING:
    from entity import Actor


class Fighter(BaseComponent):
    parent: Actor

    def __init__(self, hp: int, base_defense: int, base_power: int):
        self.max_hp = hp
        self._hp = hp
        self.base_defense = base_defense
        self.base_power = base_power

    @property
    def hp(self) -> int:
        return self._hp

    @hp.setter
    def hp(self, value: int) -> None:
        self._hp = max(0, min(value, self.max_hp))
        if self._hp == 0 and self.parent.ai:
            self.die()

    @property
    def defense(self) -> int:
        return self.base_defense + self.defense_bonus

    @property
    def power(self) -> int:
        return self.base_power + self.power_bonus

    @property
    def defense_bonus(self) -> int:
        if self.parent.equipment:
            return self.parent.equipment.defense_bonus
        else:
            return 0

    @property
    def power_bonus(self) -> int:
        if self.parent.equipment:
            return self.parent.equipment.power_bonus
        else:
            return 0

    def die(self) -> None:

        # drop everything
        for slot in self.parent.equipment.slots:
            if slot.item is not None:
                UnequipAction(self.parent, slot, to_floor=True).perform()
        for item in self.parent.inventory.items:
            DropItemAction(self.parent, item).perform()

        assert self.parent.ai is not None
        self.parent.ai.on_die()

        if self.parent is self.engine.player:
            death_message = "Saad, thyn heres been shaken of olde lif. You are dead."
            death_message_color = color.player_die
            self.engine.message_log.add_message(death_message, death_message_color)
            # make the player itself resemble a corpse, so it will appear that way in the status bar
            self.engine.player.char = "%"
            self.engine.player.color = color.deep_red
            self.engine.player.name = f"slain {self.engine.player.name}"
        else:
            death_message = f"The {self.parent.name} dies."
            death_message_color = color.enemy_die
            self.engine.message_log.add_message(death_message, death_message_color)

            self.engine.player.level.add_xp(self.parent.level.xp_given)

        # replace killed entity with a corpse
        corpse = actors.corpse.spawn(self.gamemap, self.parent.x, self.parent.y)
        corpse.name = f"slain {self.parent.name}"
        self.gamemap.entities.remove(self.parent)

    def heal(self, amount: int) -> int:
        if self.hp == self.max_hp:
            return 0

        new_hp_value = self.hp + amount

        if new_hp_value > self.max_hp:
            new_hp_value = self.max_hp

        amount_recovered = new_hp_value - self.hp

        self.hp = new_hp_value

        return amount_recovered

    def take_damage(self, amount: int) -> None:
        self.hp -= amount
