from typing import List, Optional
import cProfile

import tcod

from engine import Engine
from entity import Item
from handlers.action_or_handler import ActionOrHandler
from handlers.ask_user_event_handler import AskUserEventHandler
from handlers.base_event_handler import BaseEventHandler
import color
import keys


class ItemPicker(AskUserEventHandler):
    """This handler lets the user select an item.

    What happens then depends on the subclass.
    """

    TITLE = "<missing title>"

    def __init__(self, engine: Engine):
        super().__init__(engine)
        self.curr_selected_idx = 0
        self.items = self.generate_items()
        self._dirty = False
        """This dirty flag will be set to True when the items have changed (or MAY have changed)."""
        self.show_inventory_count = False
        """This will show the inventory count at the bottom of the menu."""
        self.show_on_ground_hint = False
        """This will show the "on ground" hint for items that are not in the player's inventory."""

    def gain_focus(self) -> None:
        if self._dirty:
            self.items = self.generate_items()
            if self.curr_selected_idx >= len(self.items):
                self.curr_selected_idx = len(self.items) - 1
            self._dirty = False

    def on_render(self, console: tcod.console.Console, delta_time: float) -> None:
        """Render an inventory menu, which displays the items in the inventory, and the letter to select them.
        Will move to a different position based on where the player is located, so the player can always see where
        they are.
        """
        super().on_render(console, delta_time)
        num_items = len(self.items)

        height = num_items + 4

        if height <= 4:
            height = 4

        if self.engine.player.x <= 30:
            x = 40
        else:
            x = 0

        y = 0

        width = 40

        console.draw_frame(
            x=x,
            y=y,
            width=width,
            height=height,
            clear=True,
            fg=(255, 255, 255),
            bg=color.black,
        )
        console.print(x + 1, y, f"┤{self.TITLE}├")
        if self.show_inventory_count:
            console.print(x + 2, y + height - 1, f"{self.engine.player.inventory.capacity_string}")
        hint = "┤[l]ook├"
        console.print(x + width - 1 - len(hint), y + height - 1, hint)

        if num_items > 0:
            for i, item in enumerate(self.items):
                item_key = chr(ord("a") + i)

                item_string = item.name
                if self.show_on_ground_hint and item not in self.engine.player.inventory.items:
                    item_string += f" (on ground)"

                ordinal_fg, ordinal_bg = color.white, color.black
                if i == self.curr_selected_idx:
                    ordinal_fg, ordinal_bg = color.black, color.white
                console.print(x + 1, y + i + 1, f"[{item_key}]", ordinal_fg, ordinal_bg)
                console.print(x + 4, y + i + 1, item.char, item.color)
                console.print(x + 5, y + i + 1, item_string)
        else:
            console.print(x + 1, y + 1, "-- Nothing here! --", fg=color.light_grey)

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[ActionOrHandler]:
        self.items = self.generate_items()
        key = event.sym

        # due to this code, there is no need for length==0 checks
        if len(self.items) == 0:
            return super().ev_keydown(event)

        # movement of item selection
        if key in keys.MENU_NAV_UP:
            self.curr_selected_idx = (self.curr_selected_idx - 1) % len(self.items)
            return None
        elif key in keys.MENU_NAV_DOWN:
            self.curr_selected_idx = (self.curr_selected_idx + 1) % len(self.items)
            return None
        # item selection via enter
        if key in keys.CONFIRM_KEYS:
            selected_item = self.items[self.curr_selected_idx]
            return self.on_item_selected(selected_item)
        if key == tcod.event.KeySym.l:
            item = self.items[self.curr_selected_idx]
            from handlers.inspect_item_handler import InspectItemHandler

            return InspectItemHandler(self.engine, self, item)

        # item selection through A-Z keys
        index = key - tcod.event.KeySym.a
        if 0 <= index < len(self.items):
            selected_item = self.items[index]
            return self.on_item_selected(selected_item)

        return super().ev_keydown(event)

    def on_item_selected(self, item: Item) -> Optional[ActionOrHandler]:
        """Called when the user selects a valid item."""
        raise NotImplementedError()

    def generate_items(self) -> List[Item]:
        """Get the items that can be selected."""
        # This returns a REFERENCE to the items in the player's inventory
        # (notably NOT a copy, in case you're not catching on here, Harrison in 6 months)
        # This is the intended behavior - modifications to inventory will be reflected in the item picker
        return self.engine.player.inventory.items
