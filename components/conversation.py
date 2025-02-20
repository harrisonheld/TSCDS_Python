from enum import Enum, auto

from components.base_component import BaseComponent


class Conversation(BaseComponent):
    def __init__(self, text: str):
        super().__init__()
        self.text = text
