from enum import Enum, auto

from components.base_component import BaseComponent


class MeleeClass(Enum):
    NONE = auto()  # still a melee weapon, just doesn't have any special qualities
    FIST = auto()  # bare hands, hand wraps, brass knuckles, etc
    SPEAR = auto()
    HAMMER = auto()
    SWORD = auto()


class MeleeWeapon(BaseComponent):
    def __init__(self, melee_class: MeleeClass, damage: int):
        super().__init__()
        self.melee_class = melee_class
        self.damage = damage
