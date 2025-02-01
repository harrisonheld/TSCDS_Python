from enum import Enum, auto

from components.base_component import BaseComponent


class Armor(BaseComponent):
    def __init__(self, defense: int):
        super().__init__()
        self.defense = defense
