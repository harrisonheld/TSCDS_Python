from typing import Tuple

import tcod
import color
from entity import Entity
from entity import Actor


class LookBlock:
    def __init__(self):
        self.show_full_detail = False

    def set_show_full_detail_mode(self, b: bool):
        self.show_full_detail = b

    def render(self, console: tcod.console.Console, entity: Entity) -> None:

        x = entity.x+1
        y = entity.y
        width = 15

        # draw description
        height = console.print_box(x + 1, y + 1, width-2, 1000, string=entity.description, bg=color.black)
        height += 2

        # draw frame and title
        console.draw_frame(x, y, width, height, bg=color.black, fg=color.white, clear=False)
        console.print(x + 1, y, f"{entity.name}", entity.color)

        if isinstance(entity, Actor):
            actor: Actor = entity
            hp_percent = actor.fighter.hp / actor.fighter.max_hp

            status_str: str
            status_color: Tuple[int, int, int]

            if hp_percent >= 1.0:
                status_str = "Perfect"
                status_color = color.status_perfect
            elif hp_percent >= 0.75:
                status_str = "Fine"
                status_color = color.status_fine
            elif hp_percent >= 0.3:
                status_str = "Hurt"
                status_color = color.status_hurt
            elif hp_percent >= 0.1:
                status_str = "Wounded"
                status_color = color.status_wounded
            elif hp_percent > 0:
                status_str = "!!!"
                status_color = color.status_critically_wounded
            else:
                status_str = "Dead"
                status_color = color.status_dead

            if self.show_full_detail and status_str != "Dead":
                status_str = f"{actor.fighter.hp}/{actor.fighter.max_hp}"
            if status_str != "Dead":
                status_str = "♥" + status_str

            bottom = y+height-1
            console.print(x + 1, bottom, status_str, status_color)

            if self.show_full_detail:
                right = x + width - 1

                # print defense
                defense = str(actor.fighter.defense)
                acc_x = len(defense)
                console.print(right - acc_x, bottom, defense)
                # print defense glyph
                acc_x += 1
                console.print(right - acc_x, bottom, "♦", color.defense)
                # print power
                power = str(actor.fighter.power)
                acc_x += len(power)
                # print power glyph
                console.print(right - acc_x, bottom, power)
                acc_x += 1
                console.print(right - acc_x, bottom, "♦", color.dark_red)
