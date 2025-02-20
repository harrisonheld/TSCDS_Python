import tcod

from components.conversation import Conversation
from engine import Engine
from handlers.ask_user_event_handler import AskUserEventHandler
import color


class ConversationHandler(AskUserEventHandler):
    TITLE = "Conversation"

    def __init__(self, engine: Engine, conversation: Conversation) -> None:
        super().__init__(engine)
        self.conversation = conversation

    def on_render(self, console: tcod.console.Console, delta_time: float) -> None:
        super().on_render(console, delta_time)

        if self.engine.player.x <= 30:
            x = 40
        else:
            x = 0

        y = 0

        width = len(self.TITLE) + 4

        console.draw_frame(
            x=x, y=y, width=width, height=7, title=self.TITLE, clear=True, fg=(255, 255, 255), bg=color.black
        )

        console.print(x=x + 1, y=y + 1, string=f"Conversation Text: {self.conversation.text}")
