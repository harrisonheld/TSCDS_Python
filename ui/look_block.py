from typing import Tuple

import tcod
import color
from entity import Entity
from entity import Actor


class LookBlock:
    def __init__(self, entity: Entity):
        self.entity = entity

    def render(self, console: tcod.console.Console, x: int, y: int, width: int, height: int) -> None:
        console.draw_frame(x, y, width, height, bg=color.black, fg=color.white)
        acc_y = 1
        acc_y += console.print_box(x + 1, y+acc_y, width-2, height-acc_y-1, string=self.entity.name)
        acc_y += console.print_box(x + 1, y+acc_y, width-2, height-acc_y-1, string=self.entity.description)

        if isinstance(self.entity, Actor):
            actor: Actor = self.entity
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
                status_str = "Critically Wounded"
                status_color = color.status_critically_wounded
            else:
                status_str = "Dead"
                status_color = color.status_dead

            console.print(x + 1, y+height-1, status_str, status_color)

        if acc_y > height-2:
            console.print(x+width-4, y+height-1, "...")
