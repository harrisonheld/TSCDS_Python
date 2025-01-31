from typing import Generic, List, Tuple, TypeVar, Union
import random

from tables.random_table import RandomTable

T = TypeVar("T")
GrabBagEntry = Union[T, "RandomTable[T]", "GrabBag[T]"]
Count = Union[int, range]


class GrabBag(Generic[T]):
    def __init__(self, contents: List[Tuple[GrabBagEntry, Count, float]]):
        """Initialize a GrabBag with contents. Each entry in `contents` can be:
        - A tuple of (entry, count, chance): `(entry, 5, 100)`
        - A tuple of (entry, range, chance): `(entry, range(8, 11), 100)`

        Remarks:
        - Remember that range is [inclusive, exclusive)
        """
        self.contents = contents

    def roll_batch(self) -> List[T]:
        result = []
        for entry, count, chance in self.contents:
            if random.random() > chance / 100.0:
                continue
            num = self._resolve_count(count)
            for _ in range(num):
                result.extend(self._resolve_grab_bag_entry(entry))

        return result

    def _resolve_count(self, spec: Union[int, range]) -> int:
        """Resolve a count from an integer or a range."""
        if isinstance(spec, int):
            return spec
        elif isinstance(spec, range):
            return random.choice(spec)
        raise ValueError(f"Invalid count spec: {spec}")

    def _resolve_grab_bag_entry(self, entry: GrabBagEntry) -> List[T]:
        if isinstance(entry, GrabBag):
            return entry.roll_batch()
        if isinstance(entry, RandomTable):
            return [entry.roll()]
        return [entry]
