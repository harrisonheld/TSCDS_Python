from enum import Enum, auto


class RenderOrder(Enum):
    EFFECT_BOTTOM = auto()
    CORPSE = auto()
    ITEM = auto()
    ACTOR = auto()
    EFFECT_TOP = auto()
