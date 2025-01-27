from typing import Generic, List, Tuple, TypeVar, Union

from tables.random_table import RandomTable

T = TypeVar("T")
GrabBagEntry = Union[T, "RandomTable[T]"]


class GrabBag(Generic[T]):
    def __init__(self, contents: List[Tuple[GrabBagEntry, int]]):
        self.contents = contents
        """List of ordered pairs, of the form (entry, count)."""

    def roll_batch(self) -> List[T]:
        result = []
        for entry, count in self.contents:
            for _ in range(count):
                if isinstance(entry, RandomTable):
                    result.append(entry.roll())
                else:
                    result.append(entry)

        return result
