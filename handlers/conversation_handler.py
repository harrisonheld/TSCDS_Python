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

        width = 40
        height = 25
        sub_console = tcod.console.Console(width, height)
        sub_console.draw_frame(0, 0, width, height, bg=color.black, fg=color.white)
        sub_console.print(width // 2, 0, f"┤{self.conversation.parent.name}├", alignment=tcod.constants.CENTER)

        sub_console.print_box(1, 1, width - 2, height - 2, f"{self.conversation.text}")

        x = console.width // 2 - sub_console.width // 2
        y = console.height // 2 - sub_console.height // 2
        sub_console.blit(console, x, y)
