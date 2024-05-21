import tcod

from entity import Actor
from keys import BINDABLE_KEYS
import color


class InfoBlock:
    def __init__(self, actor: Actor):
        self.actor = actor

    def render(self, console: tcod.console.Console, x: int, y: int, width: int, height: int) -> None:
        console.print(x, y, string=f"{self.actor.name} {self.actor.char}", fg=self.actor.color)
        console.print(x, y + 1, string=f"HP {self.actor.fighter.hp}/{self.actor.fighter.max_hp}")
        console.print(x, y + 2, string=f"LVL {self.actor.level.current_level}")
        console.print(
            x, y + 3, string=f"XP {self.actor.level.current_xp} / {self.actor.level.experience_to_next_level}"
        )
        console.print(x, y + 4, string=f"FLOOR {self.actor.gamemap.engine.game_world.current_floor}")

        # print bound items
        if len(self.actor.inventory.binds) > 0:
            console.print(x, y + height - 3, "keybinds:")

        for i, key in enumerate(BINDABLE_KEYS):
            # check for bind
            bound_item = self.actor.inventory.binds.get(key, None)
            if bound_item is None:
                continue

            # convert names like N1 to 1
            key_name = key.name
            if len(key_name) >= 2 and key_name[0] == "N" and key_name[1].isdigit():
                key_name = key_name[1:]

            col = x + i
            row = y + height - 1
            console.print(col, row - 1, bound_item.char, bound_item.color)
            console.print(col, row, key_name)
