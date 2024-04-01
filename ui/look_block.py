import textwrap
import tcod
import color
from entity import Entity


class LookBlock:
    def __init__(self, entity: Entity):
        self.entity = entity

    def render(self, console: tcod.console.Console, x: int, y: int, width: int, height: int) -> None:
        console.draw_frame(x, y, width, height, bg=color.black, fg=color.white)
        acc_y = 1
        acc_y += console.print_box(x + 1, y+acc_y, width-2, height-acc_y-1, string=self.entity.name)
        acc_y += console.print_box(x + 1, y+acc_y, width-2, height-acc_y-1, string=self.entity.description)

        if acc_y > height-2:
            console.print(x+width-4, y+height-1, "...")
