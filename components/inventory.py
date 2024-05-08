from __future__ import annotations

from typing import TYPE_CHECKING, List, Dict, Optional

import tcod.event

import color
import exceptions
from components.base_component import BaseComponent
from keys import BINDABLE_KEYS

if TYPE_CHECKING:
    from entity import Actor, Item


class Inventory(BaseComponent):
    parent: Actor

    def __init__(self, capacity: int):
        self.capacity = capacity
        self.items: List[Item] = []
        self.binds: Dict[tcod.event.KeySym, Item] = {}

    def add(self, item: Item, add_message: bool = True) -> None:
        """
        Add or pickup (from the game map) an item to the inventory, and attempt to auto-bind it to a key.
        """
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

        # try auto-binding
        if item.consumable is not None:
            for key in BINDABLE_KEYS:
                if key not in self.binds:
                    self.bind(item, key, add_message=False)
                    break

    def remove(self, item: Item):
        """Remove an item from the inventory."""
        # Remove the item from key bindings if it's bound to any key
        for key, bound_item in list(self.binds.items()):
            if bound_item == item:
                del self.binds[key]

        # removal
        self.items.remove(item)

    def drop(self, item: Item) -> None:
        """
        Removes an item from the inventory and restores it to the game map, at the holder's current location.
        """
        self.remove(item)
        item.place(self.parent.x, self.parent.y, self.gamemap)

        self.engine.message_log.add_message(f"You dropped the {item.name}.")

    def bind(self, item: Item, key: tcod.event.KeySym, add_message: bool = True) -> None:
        """
        Binds an item to a specific key.
        """
        self.unbind(item, add_message=False)
        self.binds[key] = item
        if add_message:
            self.engine.message_log.add_message(f"Bound {item.name} to [{key.name}].")

    def unbind(self, item: Item, add_message: bool = True) -> Optional[tcod.event.KeySym]:
            """
            Unbinds an item from its current key, if any, and returns the key it was bound to.
            Returns None if the item was not bound to any key.
            """
            for key, bound_item in list(self.binds.items()):
                if bound_item == item:
                    del self.binds[key]
                    if add_message:
                        self.engine.message_log.add_message(f"Unbound {item.name} from [{key.name}].")
                    return key

            if add_message:
                self.engine.message_log.add_message(f"Cannot unbind {item.name}, it isn't bound.", color.impossible)
            return None
