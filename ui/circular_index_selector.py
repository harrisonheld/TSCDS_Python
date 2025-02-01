import tcod

import keys


class CircularIndexSelector:
    def __init__(self, length: int, vertical: bool = True):
        self._length = length
        self._vertical = vertical
        self._index = 0

        if vertical:
            # backwards, because higher indexes are at the bottom of the screen
            self._increment_keys = keys.MENU_NAV_DOWN
            self._decrement_keys = keys.MENU_NAV_UP
        else:
            self._increment_keys = keys.MENU_NAV_RIGHT
            self._decrement_keys = keys.MENU_NAV_LEFT

    def set_controls(self, increment_keys: set[tcod.event.KeySym], decrement_keys: set[tcod.event.KeySym]):
        self._increment_keys = increment_keys
        self._decrement_keys = decrement_keys

    def increment(self):
        if self._length <= 0:
            return
        self._index = (self._index + 1) % self._length

    def decrement(self):
        if self._length <= 0:
            return
        self._index = (self._index - 1) % self._length

    def set_length(self, length: int):
        print("setting length to " + str(length))
        self._length = length
        if self._index >= length:
            self._index = length - 1

    def get_index(self) -> int:
        return self._index

    def set_index(self, index: int):
        # note: we allow 0 index, even if length is 0

        if index < 0:
            raise ValueError(f"Invalid index: {index}. Must be non negative.")
        if index >= self._length and index != 0:
            raise ValueError(f"Invalid index: {index}. Must be between 0 and {self._length - 1}.")
        self._index = index

    def take_input(self, key: tcod.event.KeySym) -> bool:
        """
        Takes input and moves the index accordingly.
        Returns True if the input moved the index, False otherwise.
        """
        if key in self._increment_keys:
            self.increment()
            return True
        elif key in self._decrement_keys:
            self.decrement()
            return True

        return False
