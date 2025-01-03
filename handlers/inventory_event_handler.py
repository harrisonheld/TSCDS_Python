import color
import keys
from engine import Engine
from entity import Item
from handlers.ask_user_event_handler import AskUserEventHandler
from handlers.input_handlers import ActionOrHandler
from typing import Optional

import tcod


class InventoryEventHandler(AskUserEventHandler):
    """This handler lets the user select an item.

    What happens then depends on the subclass.
    """

    TITLE = "<missing title>"

    def __init__(self, engine: Engine):
        self.curr_selected_idx = 0
        super().__init__(engine)

    def on_render(self, console: tcod.console.Console) -> None:
        """Render an inventory menu, which displays the items in the inventory, and the letter to select them.
        Will move to a different position based on where the player is located, so the player can always see where
        they are.
        """
        super().on_render(console)
        inventory = self.engine.player.inventory
        number_of_items_in_inventory = len(inventory.items)

        height = number_of_items_in_inventory + 4

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
        console.print(x + 1, y, f"┤{self.TITLE} ({number_of_items_in_inventory}/{inventory.capacity} items)├")
        hint = "┤[l]ook├"
        console.print(x + width - 1 - len(hint), y + height - 1, hint)

        if number_of_items_in_inventory > 0:
            for i, item in enumerate(self.engine.player.inventory.items):
                item_key = chr(ord("a") + i)

                # add keybind marker
                bound_to_key: Optional[tcod.event.KeySym] = None
                for key, bound_item in self.engine.player.inventory.binds.items():
                    if bound_item == item:
                        bound_to_key = key
                        break

                item_string = item.name
                is_equipped = self.engine.player.equipment.item_is_equipped(item)
                if is_equipped:
                    item_string = f"{item_string} (equipped)"
                if bound_to_key is not None:
                    item_string = f"{item_string} (bound to {bound_to_key.name})"

                ordinal_fg, ordinal_bg = color.white, color.black
                if i == self.curr_selected_idx:
                    ordinal_fg, ordinal_bg = color.black, color.white
                console.print(x + 1, y + i + 1, f"[{item_key}]", ordinal_fg, ordinal_bg)
                console.print(x + 4, y + i + 1, item.char, item.color)
                console.print(x + 5, y + i + 1, item_string)

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[ActionOrHandler]:
        player = self.engine.player
        key = event.sym

        # movement of item selection
        if key in keys.MENU_NAV_UP:
            self.curr_selected_idx = (self.curr_selected_idx - 1) % len(player.inventory.items)
            return None
        elif key in keys.MENU_NAV_DOWN:
            self.curr_selected_idx = (self.curr_selected_idx + 1) % len(player.inventory.items)
            return None
        # item selection via enter
        if key in keys.CONFIRM_KEYS:
            selected_item = player.inventory.items[self.curr_selected_idx]
            return self.on_item_selected(selected_item)
        if key == tcod.event.KeySym.l:
            item = self.engine.player.inventory.items[self.curr_selected_idx]
            from handlers.inspect_item_handler import InspectItemHandler
            return InspectItemHandler(self.engine, self, item)

        # item selection through A-Z keys
        index = key - tcod.event.KeySym.a
        if 0 <= index <= 26:
            try:
                selected_item = player.inventory.items[index]
            except IndexError:
                self.engine.message_log.add_message("Invalid entry.", color.impossible)
                return None
            return self.on_item_selected(selected_item)
        return super().ev_keydown(event)

    def on_item_selected(self, item: Item) -> Optional[ActionOrHandler]:
        """Called when the user selects a valid item."""
        raise NotImplementedError()