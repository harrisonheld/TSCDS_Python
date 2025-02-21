from typing import Optional

import tcod

from components.conversation import Conversation
from engine import Engine
from handlers.action_or_handler import ActionOrHandler
from handlers.ask_user_event_handler import AskUserEventHandler
from handlers.event_handler import EventHandler
from handlers.main_game_event_handler import MainGameEventHandler
import color


class ConversationHandler(AskUserEventHandler):
    TITLE = "Conversation"

    def __init__(self, engine: Engine, conversation: Conversation) -> None:
        super().__init__(engine)
        self.conversation = conversation
        self.conversation.reset()

        self.engine.message_log.add_message(
            f"{self.conversation.parent.name}: {self.conversation.get_current_npc_text()}", color.npc_dialogue
        )

    def on_render(self, console: tcod.console.Console, delta_time: float) -> None:
        super().on_render(console, delta_time)

        width = 40
        height = 25
        sub_console = tcod.console.Console(width, height)
        sub_console.draw_frame(0, 0, width, height, bg=color.black, fg=color.white)
        sub_console.print(width // 2, 0, f"┤{self.conversation.parent.name}├", alignment=tcod.constants.CENTER)

        sub_console.print_box(1, 1, width - 2, height - 2, f"{self.conversation.get_current_npc_text()}")

        for i, (id, player_text) in enumerate(self.conversation.get_responses()):
            letter = chr(ord("a") + i)
            sub_console.print(1, height - i - 2, f"[{letter}] {player_text}")

        x = console.width // 2 - sub_console.width // 2
        y = console.height // 2 - sub_console.height // 2
        sub_console.blit(console, x, y)

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[ActionOrHandler]:
        key = event.sym
        ordinal = key - tcod.event.KeySym.a

        responses = self.conversation.get_responses()
        if 0 <= ordinal < len(responses):
            response_id, response_text = responses[ordinal]
            self.engine.message_log.add_message(f"You: {response_text}", color.player_dialogue)
            self.conversation.pick_response(response_id)

            if self.conversation.is_finished:
                return MainGameEventHandler(self.engine)
            else:
                self.engine.message_log.add_message(
                    f"{self.conversation.parent.name}: {self.conversation.get_current_npc_text()}", color.npc_dialogue
                )
                return None

        return super().ev_keydown(event)
