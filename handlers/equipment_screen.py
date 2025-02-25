from typing import Optional

import tcod

from actions.action import Action
from actions.equip_action import EquipAction
from actions.unequip_action import UnequipAction
from components.equipment import EquipmentSlot
from engine import Engine
from entity import Item
from handlers.action_or_handler import ActionOrHandler
from handlers.ask_user_event_handler import AskUserEventHandler
from handlers.main_game_event_handler import MainGameEventHandler
from ui.circular_index_selector import CircularIndexSelector
import color
import exceptions
import keys


class EquipmentScreen(AskUserEventHandler):
    """View, equip, and unequip equipment."""

    def __init__(self, engine: Engine):
        n = len(engine.player.equipment.slots)
        self.selector = CircularIndexSelector(n)
        super().__init__(engine)

    def on_render(self, console: tcod.console.Console, delta_time: float) -> None:
        super().on_render(console, delta_time)  # Draw the main state as the background.

        slot_count = len(self.engine.player.equipment.slots)
        longest_slot_name = max((len(slot.slot_type.name) for slot in self.engine.player.equipment.slots), default=0)
        longest_item_name = max(
            (len(slot.item.name) for slot in self.engine.player.equipment.slots if slot.item is not None),
            default=1,  # default is 1 because no-item is rendered as a '-'
        )

        width = longest_slot_name + longest_item_name + 8  # space for borders, item glyph, and key prompt
        height = slot_count + 2
        sub_console = tcod.console.Console(width, height)
        sub_console.draw_frame(0, 0, width, height, bg=color.black, fg=color.white)
        sub_console.print(width // 2, 0, "┤Equipment├", alignment=tcod.constants.CENTER)
        sub_console.print(1, height - 1, "[r] remove")

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
            do_highlight = idx == self.selector.get_index()
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

        # due to this code, there is no need for length==0 checks
        if len(player.equipment.slots) == 0:
            return super().ev_keydown(event)

        # movement of item selection
        if self.selector.take_input(key):
            return None
        # removal via remove key
        if key == tcod.event.KeySym.r:
            selected_slot = player.equipment.slots[self.selector.get_index()]
            player = self.engine.player
            action = UnequipAction(player, selected_slot)
            action.next_handler = self  # we do not want this action to switch handlers - let's stay in this menu
            return action
        # item selection via enter
        if key in keys.CONFIRM_KEYS:
            selected_slot = player.equipment.slots[self.selector.get_index()]
            return self.on_slot_selected(selected_slot)
        if key == tcod.event.KeySym.l:
            slot = player.equipment.slots[self.selector.get_index()]
            from handlers.inspect_item_handler import InspectItemHandler

            if slot.item is not None:
                return InspectItemHandler(self.engine, self, slot.item)

        # slot selection through a-z keys
        index = key - tcod.event.KeySym.a
        if 0 <= index < len(player.equipment.slots):
            self.selector.set_index(index)
            selected_slot = player.equipment.slots[index]
            return self.on_slot_selected(selected_slot)

        return super().ev_keydown(event)

    def on_slot_selected(self, slot: EquipmentSlot) -> Optional[ActionOrHandler]:
        """Called when the user selects a slot."""
        from handlers.equippable_picker import EquippablePicker

        return EquippablePicker(self.engine, parent=self, slot=slot)
