from enum import Enum, auto

from components.base_component import BaseComponent


class RangedClass(Enum):
    PISTOL = auto()
    RIFLE = auto()
    BOW = auto()


class RangedWeapon(BaseComponent):
    def __init__(self, ranged_class: RangedClass, damage: int):
        super().__init__()
        self.ranged_class = ranged_class
        self.damage = damage
