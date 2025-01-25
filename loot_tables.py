from typing import Dict, Generic, List, Tuple, TypeVar, Union
import random

from entity import Entity, Item
import blueprints

T = TypeVar("T")
TableEntry = Union[T, "RandomTable[T]"]
GrabBagEntry = Union[T, "RandomTable[T]"]

class RandomTable(Generic[T]):
    def __init__(self, table: Dict[TableEntry, int]):
        self.table = table
        """Dictionary of entries and their weights"""

    def roll(self) -> T:

        # find the table entry
        table_entry: TableEntry
        total = sum(self.table.values())
        num = random.randint(1, total)
        for key, value in self.table.items():
            num -= value
            if num <= 0:
                table_entry = key
                break

        if isinstance(table_entry, RandomTable):
            return table_entry.roll()
        return table_entry


class GrabBag(Generic[T]):
    def __init__(self, contents: List[Tuple[GrabBagEntry, int]]):
        self.contents = contents

    def roll_batch(self) -> List[T]:
        result = []
        for entry, count in self.contents:
            for _ in range(count):
                if isinstance(entry, RandomTable):
                    result.append(entry.roll())
                else:
                    result.append(entry)

        return result


weapons = RandomTable[Item](
    {
        blueprints.sword: 10,
        blueprints.dagger: 15,
    }
)

consumables = RandomTable[Item](
    {
        blueprints.fireball_scroll: 10,
        blueprints.lightning_scroll: 10,
        blueprints.confusion_scroll: 10,
        blueprints.health_potion: 30,
    }
)

fun_bag = GrabBag[Item](
    [
        (weapons, 1),
        (consumables, 3),
    ]
)
