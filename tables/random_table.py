from typing import Generic, List, Tuple, TypeVar, Union
import random

T = TypeVar("T")
TableEntry = Union[T, "RandomTable[T]"]


class RandomTable(Generic[T]):
    def __init__(self, table: List[Tuple[TableEntry, int]]):
        self.table = table
        """Dictionary of entries and their weights."""

    def roll(self) -> T:

        # find the table entry
        table_entry: TableEntry
        total = sum(self.table[i][1] for i in range(len(self.table)))
        num = random.randint(1, total)
        for entry, value in self.table:
            num -= value
            if num <= 0:
                table_entry = entry
                break

        if isinstance(table_entry, RandomTable):
            return table_entry.roll()
        return table_entry
