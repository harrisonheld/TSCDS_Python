import color
from handlers.ask_user_event_handler import AskUserEventHandler


import tcod


class CharacterScreenEventHandler(AskUserEventHandler):
    TITLE = "Character Information"

    def on_render(self, console: tcod.console.Console) -> None:
        super().on_render(console)

        if self.engine.player.x <= 30:
            x = 40
        else:
            x = 0

        y = 0

        width = len(self.TITLE) + 4

        console.draw_frame(
            x=x, y=y, width=width, height=7, title=self.TITLE, clear=True, fg=(255, 255, 255), bg=color.black
        )

        console.print(x=x + 1, y=y + 1, string=f"Level: {self.engine.player.level.current_level}")
        console.print(x=x + 1, y=y + 2, string=f"XP: {self.engine.player.level.current_xp}")
        console.print(
            x=x + 1,
            y=y + 3,
            string=f"XP for next Level: {self.engine.player.level.experience_to_next_level}",
        )

        console.print(x=x + 1, y=y + 4, string=f"Attack: {self.engine.player.fighter.power}")
        console.print(x=x + 1, y=y + 5, string=f"Defense: {self.engine.player.fighter.defense}")