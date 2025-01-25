from typing import Dict, Generic, TypeVar, Union
import random

from entity import Entity, Item
import blueprints

T = TypeVar("T")
TableEntry = Union[T, "RandomTable[T]"]

class RandomTable(Generic[T]):
    def __init__(self, table: Dict[TableEntry, int]):
        self.table = table
        """Dictionary of entries and their weights"""

    def roll(self) -> T:

        # find the table entry
        # if this gets inefficient, can make a cumulative_sum_table and binary search
        table_entry: TableEntry
        total = sum(self.table.values())
        num = random.randint(1, total)
        for key, value in self.table.items():
            num -= value
            if num <= 0:
                table_entry = key
                break

        # check if table_entry is a RandomTable
        if isinstance(table_entry, RandomTable):
            return table_entry.roll()
        return table_entry

        # unreachable
        raise RuntimeError("Something went wrong in the random table generator")


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

treasure = RandomTable[Item]({weapons: 50, consumables: 50})
