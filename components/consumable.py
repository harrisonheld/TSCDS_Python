from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from actions.leap_action import LeapAction
from actions.swap_action import SwapAction
from components.base_component import BaseComponent
from components.inventory import Inventory
from exceptions import Impossible
from handlers.action_or_handler import ActionOrHandler
from handlers.area_ranged_attack_handler import AreaRangedAttackHandler
from handlers.select_actor_handler import SelectActorHandler
from handlers.select_adjacent_handler import SelectAdjacentHandler
import actions.item_action
import color
import components.ai.confused_ai

if TYPE_CHECKING:
    from entity import Actor, Item


class Consumable(BaseComponent):
    parent: Item

    def get_action(self, consumer: Actor) -> Optional[ActionOrHandler]:
        """Try to return the action for this item."""
        return actions.item_action.ItemAction(consumer, self.parent)

    def activate(self, action: actions.item_action.ItemAction) -> None:
        """Invoke this items ability.

        `action` is the context for this activation.
        """
        raise NotImplementedError()

    def consume(self) -> None:
        """Remove the consumed item from its containing inventory."""
        entity = self.parent
        inventory = entity.parent
        if isinstance(inventory, components.inventory.Inventory):
            inventory.remove(entity)


class ConfusionConsumable(Consumable):
    def __init__(self, number_of_turns: int):
        self.number_of_turns = number_of_turns

    def get_action(self, consumer: Actor) -> SelectActorHandler:
        self.engine.message_log.add_message("Select a target to confuse.", color.needs_target)
        return SelectActorHandler(
            self.engine,
            callback=lambda target: actions.item_action.ItemAction(consumer, self.parent, target.xy),
        )

    def activate(self, action: actions.item_action.ItemAction) -> None:
        consumer = action.actor
        target = action.target_actor

        if not self.engine.game_map.visible[action.target_xy]:
            raise Impossible("You cannot target an area that you cannot see.")
        if not target:
            raise Impossible("You must select an enemy to target.")
        if target is consumer:
            raise Impossible("You cannot confuse yourself!")

        self.engine.message_log.add_message(
            f"The eyes of the {target.name} look vacant, as it starts to stumble around!",
            color.status_effect_applied,
        )
        target.ai = components.ai.confused_ai.ConfusedAI(
            entity=target,
            previous_ai=target.ai,
            turns_remaining=self.number_of_turns,
        )
        self.consume()


class FireballDamageConsumable(Consumable):
    def __init__(self, damage: int, radius: int):
        self.damage = damage
        self.radius = radius

    def get_action(self, consumer: Actor) -> AreaRangedAttackHandler:
        self.engine.message_log.add_message("Select a target location.", color.needs_target)
        return AreaRangedAttackHandler(
            self.engine,
            radius=self.radius,
            callback=lambda xy: actions.item_action.ItemAction(consumer, self.parent, xy),
        )

    def activate(self, action: actions.item_action.ItemAction) -> None:
        target_xy = action.target_xy

        if not self.engine.game_map.visible[target_xy]:
            raise Impossible("You cannot target an area that you cannot see.")

        targets_hit = False
        for actor in self.engine.game_map.actors:
            if actor.distance(*target_xy) <= self.radius:
                self.engine.message_log.add_message(
                    f"The {actor.name} is engulfed in a fiery explosion, taking {self.damage} damage!"
                )
                actor.fighter.take_damage(self.damage)
                targets_hit = True

        if not targets_hit:
            raise Impossible("There are no targets in the radius.")
        self.consume()


class HealingConsumable(Consumable):
    def __init__(self, amount: int):
        self.amount = amount

    def activate(self, action: actions.item_action.ItemAction) -> None:
        consumer = action.actor
        amount_recovered = consumer.fighter.heal(self.amount)

        if amount_recovered > 0:
            self.engine.message_log.add_message(
                f"You consume the {self.parent.name}, and recover {amount_recovered} HP!",
                color.white,
            )
            self.consume()
        else:
            raise Impossible("Your health is already full.")


class LightningDamageConsumable(Consumable):
    def __init__(self, damage: int, maximum_range: int):
        self.damage = damage
        self.maximum_range = maximum_range

    def activate(self, action: actions.item_action.ItemAction) -> None:
        consumer = action.actor
        target = None
        closest_distance = self.maximum_range + 1.0

        for actor in self.engine.game_map.actors:
            if actor is not consumer and self.parent.gamemap.visible[actor.x, actor.y]:
                distance = consumer.distance(actor.x, actor.y)

                if distance < closest_distance:
                    target = actor
                    closest_distance = distance

        if target:
            self.engine.message_log.add_message(
                f"A lighting bolt strikes the {target.name} with a loud thunder, for {self.damage} damage!"
            )
            target.fighter.take_damage(self.damage)
            self.consume()
        else:
            raise Impossible("No enemy is close enough to strike.")


class SwapConsumable(Consumable):
    def get_action(self, consumer: Actor) -> SelectAdjacentHandler:
        self.engine.message_log.add_message("Select a target to swap with.", color.needs_target)
        return SelectAdjacentHandler(
            self.engine, callback=lambda xy: actions.item_action.ItemAction(consumer, self.parent, xy)
        )

    def activate(self, action: actions.item_action.ItemAction) -> None:
        dx = action.target_xy[0] - action.actor.x
        dy = action.target_xy[1] - action.actor.y
        swap = SwapAction(action.actor, dx, dy)
        swap.perform()


class LeapConsumable(Consumable):
    def __init__(self, distance: int):
        self.distance = distance

    def get_action(self, consumer: Actor) -> SelectAdjacentHandler:
        self.engine.message_log.add_message("Select a direction to leap.", color.needs_target)
        return SelectAdjacentHandler(
            self.engine, callback=lambda xy: actions.item_action.ItemAction(consumer, self.parent, xy)
        )

    def activate(self, action: actions.item_action.ItemAction) -> None:
        dx = action.target_xy[0] - action.actor.x
        dy = action.target_xy[1] - action.actor.y
        leap = LeapAction(action.actor, dx, dy, self.distance)
        leap.perform()
        self.consume()
