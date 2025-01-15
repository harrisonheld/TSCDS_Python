from typing import Optional

import tcod

from actions.action import Action
from actions.equip_action import EquipAction
from actions.unequip_action import UnequipAction
from components.equipment import EquipmentSlot
from engine import Engine
from entity import Item
from handlers.action_or_handler import ActionOrHandler
from handlers.event_handler import EventHandler
from handlers.main_game_event_handler import MainGameEventHandler
import color
import exceptions
import keys


class EquipmentScreen(EventHandler):
    """View, equip, and unequip equipment."""

    def __init__(self, engine: Engine):
        self.curr_selected_idx = 0
        super().__init__(engine)

    def on_render(self, console: tcod.console.Console, delta_time: float) -> None:
        super().on_render(console, delta_time)  # Draw the main state as the background.

        slot_count = len(self.engine.player.equipment.slots)
        longest_slot_name = max((len(slot.slot_type.name) for slot in self.engine.player.equipment.slots), default=0)
        longest_item_name = max(
            (len(slot.item.name) for slot in self.engine.player.equipment.slots if slot.item is not None),
            default=1,  # default is 1 because no-item is rendered as a '-'
        )

        width = longest_slot_name + longest_item_name + 7  # space for borders, item glyph, and key prompt
        height = slot_count + 2
        sub_console = tcod.console.Console(width, height)
        sub_console.draw_frame(0, 0, width, height, bg=color.black, fg=color.white)
        sub_console.print(width // 2, 0, "┤Equipment├", alignment=tcod.constants.CENTER)

        idx = 0
        for slot in self.engine.player.equipment.slots:
            y = 1 + idx

            slot_name = slot.slot_type.name.lower()
            item_name = slot.item.name if slot.item is not None else "-"
            item_char = slot.item.char if slot.item is not None else " "
            item_color = slot.item.color if slot.item is not None else color.white
            ordinal = "(" + chr(ord("a") - 1 + y) + ")"
            ordinal_fg = color.white
            ordinal_bg = color.black
            do_highlight = idx == self.curr_selected_idx
            if do_highlight:
                ordinal_fg, ordinal_bg = ordinal_bg, ordinal_fg  # swap colors

            sub_console.print(1, y, slot_name)  # slot name
            sub_console.print(longest_slot_name + 2, y, ordinal, fg=ordinal_fg, bg=ordinal_bg)  # key prompt
            sub_console.print(longest_slot_name + 5, y, item_char, fg=item_color)
            sub_console.print(longest_slot_name + 6, y, item_name)

            idx += 1

        x = console.width // 2 - sub_console.width // 2
        y = console.height // 2 - sub_console.height // 2
        sub_console.blit(console, x, y)

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[ActionOrHandler]:
        player = self.engine.player
        key = event.sym

        # movement of item selection
        if key in keys.MENU_NAV_UP:
            self.curr_selected_idx = (self.curr_selected_idx - 1) % len(player.equipment.slots)
            return None
        elif key in keys.MENU_NAV_DOWN:
            self.curr_selected_idx = (self.curr_selected_idx + 1) % len(player.equipment.slots)
            return None
        # item selection via enter
        if key in keys.CONFIRM_KEYS:
            selected_slot = player.equipment.slots[self.curr_selected_idx]
            return self.on_slot_selected(selected_slot)
        if key == tcod.event.KeySym.l:
            slot = player.equipment.slots[self.curr_selected_idx]
            from handlers.inspect_item_handler import InspectItemHandler

            if slot.item is not None:
                return InspectItemHandler(self.engine, self, slot.item)
        if key == tcod.event.KeySym.ESCAPE:
            return MainGameEventHandler(self.engine)

        # slot selection through a-z keys
        index = key - tcod.event.KeySym.a
        if 0 <= index < len(player.equipment.slots):
            self.curr_selected_idx = index
            selected_slot = player.equipment.slots[index]
            return self.on_slot_selected(selected_slot)

        return None

    def on_slot_selected(self, slot: EquipmentSlot) -> Optional[ActionOrHandler]:
        """Called when the user selects a slot."""
        if slot.item is None:
            from handlers.equippable_picker import EquippablePicker

            return EquippablePicker(self.engine, self, slot_type=slot.slot_type)

        assert slot.item is not None
        player = self.engine.player
        action = UnequipAction(player, slot.item)
        action.next_handler = self  # we do not want thing action to switch handlers - let's stay in this menu
        return action
