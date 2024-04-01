import tcod
import color
from entity import Actor


class InfoBlock:
    def __init__(self, actor: Actor):
        self.actor = actor

    def render(self, console: tcod.console.Console, x: int, y: int, width: int, height: int) -> None:
        console.print(x, y, string=f"{self.actor.name} {self.actor.char}", fg=self.actor.color)
        console.print(x, y+1, string=f"HP {self.actor.fighter.hp}/{self.actor.fighter.max_hp}")
        console.print(x, y+2, string=f"LVL {self.actor.level.current_level} XP {self.actor.level.current_xp} / {self.actor.level.experience_to_next_level}")
