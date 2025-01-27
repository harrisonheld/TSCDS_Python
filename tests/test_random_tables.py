import unittest
from collections import Counter
from tables.random_table import RandomTable

class TestRandomTable(unittest.TestCase):
    def test_nested(self):
        # Define the random tables
        games = RandomTable[str](
            [
                ("fortnite", 1),
                ("minecraft", 1),
                ("terraria", 1),
            ]
        )
        fruits = RandomTable[str](
            [
                ("apple", 1),
                ("banana", 1),
                ("orange", 1),
            ]
        )

        stuff = RandomTable[str](
            [
                (games, 1),
                (fruits, 1),
                ("cake", 1),
            ]
        )

        roll_count = 100_000
        results = [stuff.roll() for _ in range(roll_count)]
        counts = Counter(results)

        cake_frequency = counts["cake"] / roll_count
        expected_cake_probability = 1 / 3
        self.assertAlmostEqual(cake_frequency, expected_cake_probability, delta=0.01)

        fortnite_frequency = counts["fortnite"] / roll_count
        expected_fortnite_probability = 1 / 9
        self.assertAlmostEqual(fortnite_frequency, expected_fortnite_probability, delta=0.01)