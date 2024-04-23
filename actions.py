from __future__ import annotations

import random
from typing import TYPE_CHECKING, Optional, Tuple

from tcod import tcod

import color
import exceptions
import strings
from upgrades import Upgrade

if TYPE_CHECKING:
    from engine import Engine
    from entity import Actor, Entity, Item


class Action:
    def __init__(self, entity: Actor) -> None:
        super().__init__()
        self.entity = entity

    @property
    def engine(self) -> Engine:
        """Return the engine this action belongs to."""
        return self.entity.gamemap.engine

    def perform(self) -> None:
        """Perform this action with the objects needed to determine its scope.

        `self.engine` is the scope this action is being performed in.

        `self.entity` is the object performing the action.

        This method must be overridden by Action subclasses.
        """
        raise NotImplementedError()


class DisplaceAction(Action):
    """Displace an entity in a random direction - usually with the intention of un-intersecting it."""
    def __init__(self, entity: Actor):
        super().__init__(entity)

    def perform(self) -> None:
        # try all 8 directions in random order
        directions = [(dx, dy) for dx in [-1, 0, 1] for dy in [-1, 0, 1] if (dx, dy) != (0, 0)]
        random.shuffle(directions)
        for dx, dy in directions:
            dest_x, dest_y = self.entity.x + dx, self.entity.y + dy
            if not self.engine.game_map.in_bounds(dest_x, dest_y):
                continue
            if not self.engine.game_map.tiles["walkable"][dest_x, dest_y]:
                continue
            if self.engine.game_map.get_blocking_entity_at_location(dest_x, dest_y):
                continue
            self.entity.move(dx, dy)
            return

        raise exceptions.Impossible("No free spaces around the entity.")
class PickupAction(Action):
    """Pickup an item and add it to the inventory, if there is room for it."""

    def __init__(self, entity: Actor):
        super().__init__(entity)

    def perform(self) -> None:
        x = self.entity.x
        y = self.entity.y
        item = self.engine.game_map.get_item_at_location(x, y)
        if item is None:
            raise exceptions.Impossible("There is nothing here to pick up.")

        inventory = self.entity.inventory
        inventory.add(item)

        if isinstance(item, Upgrade):
            item.on_pickup(self.entity)


class ItemAction(Action):
    def __init__(self, entity: Actor, item: Item, target_xy: Optional[Tuple[int, int]] = None):
        super().__init__(entity)
        self.item = item
        if not target_xy:
            target_xy = entity.x, entity.y
        self.target_xy = target_xy

    @property
    def target_actor(self) -> Optional[Actor]:
        """Return the actor at this actions destination."""
        return self.engine.game_map.get_actor_at_location(*self.target_xy)

    def perform(self) -> None:
        """Invoke the items ability, this action will be given to provide context."""
        if self.item.consumable:
            self.item.consumable.activate(self)


class DropItem(ItemAction):
    def perform(self) -> None:
        if self.entity.equipment.item_is_equipped(self.item):
            self.entity.equipment.toggle_equip(self.item)

        self.entity.inventory.drop(self.item)

        if isinstance(self.item, Upgrade):
            self.item.on_drop(self.entity)


class EquipAction(Action):
    def __init__(self, entity: Actor, item: Item):
        super().__init__(entity)

        self.item = item

    def perform(self) -> None:
        self.entity.equipment.toggle_equip(self.item)


class WaitAction(Action):
    def perform(self) -> None:
        if self.entity is self.engine.player:
            self.engine.message_log.add_message("You wait.", color.player_action)
        pass


class OggleAction(WaitAction):
    def __init__(self, entity: Actor, to_oggle_at: Entity):
        self.to_oggle_at = to_oggle_at
        super().__init__(entity)

    def perform(self) -> None:
        if self.entity is self.engine.player:
            self.engine.message_log.add_message(f"You oggle the {self.to_oggle_at.name} lovingly.",)
        elif self.to_oggle_at is self.engine.player:
            self.engine.message_log.add_message(f"The {self.entity.name} oggles you lovingly.")
        else:
            self.engine.message_log.add_message(f"The {self.entity.name} oggles the {self.to_oggle_at.name} lovingly.")
        pass


class TakeStairsAction(Action):
    def perform(self) -> None:
        """
        Take the stairs, if any exist at the entity's location.
        """
        if (self.entity.x, self.entity.y) == self.engine.game_map.downstairs_location:
            self.engine.game_world.generate_floor()
            self.engine.message_log.add_message("You descend the staircase.", color.descend)
        else:
            raise exceptions.Impossible("There are no stairs here.")


class ActionWithDirection(Action):
    def __init__(self, entity: Actor, dx: int, dy: int):
        super().__init__(entity)

        self.dx = dx
        self.dy = dy

    @property
    def dest_xy(self) -> Tuple[int, int]:
        """Returns this actions destination."""
        return self.entity.x + self.dx, self.entity.y + self.dy

    @property
    def blocking_entity(self) -> Optional[Entity]:
        """Return the blocking entity at this actions destination.."""
        return self.engine.game_map.get_blocking_entity_at_location(*self.dest_xy)

    @property
    def target_actor(self) -> Optional[Actor]:
        """Return the actor at this actions destination."""
        return self.engine.game_map.get_actor_at_location(*self.dest_xy)

    @property
    def target_entity(self) -> Optional[Entity]:
        """Return the entity at this actions destination."""
        return self.engine.game_map.get_entity_at_location(*self.dest_xy)

    def perform(self) -> None:
        raise NotImplementedError()


class MeleeAction(ActionWithDirection):
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
            target.fighter.hp -= damage
        else:
            self.engine.message_log.add_message(f"{attack_desc} but does no damage.", attack_color)


class MovementAction(ActionWithDirection):
    def perform(self) -> None:
        dest_x, dest_y = self.dest_xy

        if not self.engine.game_map.in_bounds(dest_x, dest_y):
            # Destination is out of bounds.
            raise exceptions.Impossible("That way is blocked.")
        if not self.engine.game_map.tiles["walkable"][dest_x, dest_y]:
            # Destination is blocked by a tile.
            raise exceptions.Impossible("That way is blocked.")
        if self.engine.game_map.get_blocking_entity_at_location(dest_x, dest_y):
            # Destination is blocked by an entity.
            raise exceptions.Impossible("That way is blocked.")

        self.entity.move(self.dx, self.dy)


class BumpAction(ActionWithDirection):
    def perform(self) -> None:
        if self.target_actor:
            return MeleeAction(self.entity, self.dx, self.dy).perform()

        else:
            return MovementAction(self.entity, self.dx, self.dy).perform()


class SwapAction(ActionWithDirection):
    """Swap positions with an entity."""
    def perform(self) -> None:
        target = self.target_entity
        if target is None:
            raise exceptions.Impossible("There is nothing there to swap with.")

        temp_x = target.x
        temp_y = target.y
        target.x = self.entity.x
        target.y = self.entity.y
        self.entity.x = temp_x
        self.entity.y = temp_y
        self.engine.message_log.add_message(f"The {self.entity.name} swaps places with the {target.name}!", color.white)


class RangedAction(ActionWithDirection):
    def perform(self) -> None:
        target = self.target_actor
        if not target:
            raise exceptions.Impossible("Nothing to fire at.")

        damage = self.entity.fighter.power - target.fighter.defense

        attack_desc = f"{strings.preserve_capitalize(self.entity.name)} fires a bolt at {target.name}"
        if self.entity is self.engine.player:
            attack_color = color.player_atk
        else:
            attack_color = color.enemy_atk

        if damage > 0:
            self.engine.message_log.add_message(f"{attack_desc} for {damage} hit points.", attack_color)
            target.fighter.hp -= damage
        else:
            self.engine.message_log.add_message(f"{attack_desc} but does no damage.", attack_color)
