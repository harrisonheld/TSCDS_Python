from tcod.event import KeySym

MOVE_KEYS = {
    # Arrow keys.
    KeySym.UP: (0, -1),
    KeySym.DOWN: (0, 1),
    KeySym.LEFT: (-1, 0),
    KeySym.RIGHT: (1, 0),
    KeySym.HOME: (-1, -1),
    KeySym.END: (-1, 1),
    KeySym.PAGEUP: (1, -1),
    KeySym.PAGEDOWN: (1, 1),
    # Numpad keys
    KeySym.KP_1: (-1, 1),
    KeySym.KP_2: (0, 1),
    KeySym.KP_3: (1, 1),
    KeySym.KP_4: (-1, 0),
    KeySym.KP_6: (1, 0),
    KeySym.KP_7: (-1, -1),
    KeySym.KP_8: (0, -1),
    KeySym.KP_9: (1, -1)
}

WAIT_KEYS = {
    KeySym.PERIOD,
    KeySym.KP_5,
    KeySym.CLEAR,
}

CONFIRM_KEYS = {
    KeySym.RETURN,
    KeySym.KP_ENTER,
}

BINDABLE_KEYS = [
    KeySym.N1,
    KeySym.N2,
    KeySym.N3,
    KeySym.N4,
    KeySym.N5,
    KeySym.N6,
    KeySym.N7,
    KeySym.N8,
    KeySym.N9
]
