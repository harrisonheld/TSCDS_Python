import color
from handlers.input_handlers import AskUserEventHandler
from handlers.input_handlers import ActionOrHandler
from typing import Optional


import tcod
from tcod import libtcodpy


class LevelUpEventHandler(AskUserEventHandler):
    def on_render(self, console: tcod.console.Console) -> None:
        super().on_render(console)

        width = 42
        height = 8
        x = console.width // 2 - width // 2
        y = console.height // 2 - height // 2

        sub_console = tcod.console.Console(width, height)
        sub_console.draw_frame(0, 0, width, height, bg=color.black, fg=color.white)
        sub_console.print(x=width // 2, y=0, string="┤Level Up├", alignment=libtcodpy.CENTER)

        sub_console.print(x=1, y=1, string="Select an attribute to increase.")

        sub_console.print(x=1, y=3, string=f"a) Vitality (+10 HP, from {self.engine.player.fighter.max_hp})")
        sub_console.print(x=1, y=4, string=f"b) Strength (+1 attack, from {self.engine.player.fighter.power})")
        sub_console.print(x=1, y=5, string=f"c) Endurance (+1 defense, from {self.engine.player.fighter.defense})")
        sub_console.print(
            x=1, y=6, string=f"d) Inventory Space (+2 items, from {self.engine.player.inventory.capacity})"
        )

        sub_console.blit(console, x, y)

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[ActionOrHandler]:
        player = self.engine.player
        key = event.sym
        index = key - tcod.event.KeySym.a

        if 0 <= index <= 3:
            if index == 0:
                player.level.increase_max_hp()
            elif index == 1:
                player.level.increase_power()
            elif index == 2:
                player.level.increase_defense()
            elif index == 3:
                player.level.increase_inventory()
        else:
            self.engine.message_log.add_message("Invalid entry.", color.impossible)

            return None

        return super().ev_keydown(event)

    def ev_mousebuttondown(self, event: tcod.event.MouseButtonDown) -> Optional[ActionOrHandler]:
        """
        Don't allow the player to click to exit the menu, like normal.
        """
        return None