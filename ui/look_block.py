from typing import Tuple

import tcod
import color
import sizes
from entity import Entity
from entity import Actor


class LookBlock:
    def __init__(self):
        self.show_full_detail = False

    def set_show_full_detail_mode(self, b: bool):
        self.show_full_detail = b

    def calculate_bounds(self, console: tcod.console.Console, entity: Entity, min_height: int):
        name = entity.name
        description = entity.description

        x = entity.x + 1
        y = entity.y

        # width based on entity name
        width = len(name)
        width = max(13, width)
        width += len(description) // 20  # gives super long descriptions a more squarish frame
        width += 2  # for border

        if x + width >= console.width:
            width = console.width - x

        # height based on entity description
        height = console.get_height_rect(0, 0, width - 2, 1000, description)
        height += 2  # for border
        height += 1  # for extra line beneath description
        height = max(height, min_height)  # minimal height so 1-line descriptions aren't tiny

        if y + height > console.height:
            y -= height
            y += 1
        y = max(0, y)

        return x, y, width, height

    def render(self, console: tcod.console.Console, entity: Entity, show_multi_hint: bool = False) -> None:
        min_height = 9 if show_multi_hint else 4
        x, y, width, height = self.calculate_bounds(console, entity, min_height)

        # draw frame
        console.draw_frame(x, y, width, height, bg=color.black, fg=color.white)
        # draw title
        console.print(x + 1, y, f"{entity.name}", entity.color)
        # draw description
        console.print_box(x + 1, y + 1, width - 2, height, string=entity.description, bg=color.black)
        if show_multi_hint:
            for idx, char in enumerate("┴^+ -v┬"):
                console.print(x, y + idx + 1, char)

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
