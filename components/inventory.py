from __future__ import annotations

from typing import TYPE_CHECKING, List, Dict

import tcod.event

import exceptions
from components.base_component import BaseComponent

if TYPE_CHECKING:
    from entity import Actor, Item


class Inventory(BaseComponent):
    parent: Actor

    def __init__(self, capacity: int):
        self.capacity = capacity
        self.items: List[Item] = []
        self.binds: Dict[tcod.event.KeySym, Item] = {}

    def add(self, item: Item, add_message: bool = True) -> None:
        if len(self.items) >= self.capacity:
            raise exceptions.Impossible("Your inventory is full.")

        try:
            self.parent.gamemap.engine.game_map.entities.remove(item)
        except KeyError:
            # if not on map, dw about it
            pass

        item.parent = self
        self.items.append(item)

        if add_message:
            self.engine.message_log.add_message(f"You picked up the {item.name}!")

    def drop(self, item: Item) -> None:
        """
        Removes an item from the inventory and restores it to the game map, at the player's current location.
        """
        self.items.remove(item)
        item.place(self.parent.x, self.parent.y, self.gamemap)

        # Remove the item from key bindings if it's bound to any key
        for key, bound_item in list(self.binds.items()):
            if bound_item == item:
                del self.binds[key]

        self.engine.message_log.add_message(f"You dropped the {item.name}.")

    def bind(self, item: Item, key: tcod.event.KeySym) -> None:
        """
        Binds an item to a specific key.
        """
        self.binds[key] = item
