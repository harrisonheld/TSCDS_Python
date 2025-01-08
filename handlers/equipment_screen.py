from typing import Optional

import tcod

from components.equipment import Equipment, EquipmentSlot, SlotType
from handlers.event_handler import EventHandler
from handlers.main_game_event_handler import MainGameEventHandler
import color
import exceptions
import keys


class EquipmentScreen(EventHandler):
    """View, equip, and unequip equipment."""

    def on_render(self, console: tcod.console.Console, delta_time: float) -> None:
        super().on_render(console, delta_time)  # Draw the main state as the background.

        slot_count = len(self.engine.player.equipment.slots)
        longest_slot_name = max(
            (len(slot.slot_type.name) for slot in self.engine.player.equipment.slots), 
            default=0
        )
        longest_item_name = max(
            (len(slot.item.name) for slot in self.engine.player.equipment.slots if slot.item is not None),
            default=1  # default is 1 because no-item is rendered as a '-'
        )


        width = longest_slot_name + longest_item_name + 7  # space for borders, item glyph, and key prompt
        height = slot_count + 2
        sub_console = tcod.console.Console(width, height)
        sub_console.draw_frame(0, 0, width, height, bg=color.black, fg=color.white)
        sub_console.print(width // 2, 0, "┤Equipment├", alignment=tcod.constants.CENTER)

        y = 1
        for slot in self.engine.player.equipment.slots:
            slot_name = slot.slot_type.name.lower()
            item_name = slot.item.name if slot.item is not None else "-"
            item_char = slot.item.char if slot.item is not None else " "
            item_color = slot.item.color if slot.item is not None else color.white
            ordinal = '(' + chr(ord('a') - 1 + y) + ')'

            sub_console.print(1,                     y, slot_name)  # slot name
            sub_console.print(longest_slot_name + 2, y, ordinal)  # key prompt
            sub_console.print(longest_slot_name + 5, y, item_char, fg=item_color)
            sub_console.print(longest_slot_name + 6, y, item_name)

            y += 1

        x = console.width // 2 - sub_console.width // 2
        y = console.height // 2 - sub_console.height // 2
        sub_console.blit(console, x, y)

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[EventHandler]:
        key = event.sym

        if key == tcod.event.KeySym.ESCAPE:
            return MainGameEventHandler(self.engine)

        return None
