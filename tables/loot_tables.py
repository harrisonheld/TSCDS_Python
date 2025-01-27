from entity import Item
from tables.grab_bag import GrabBag
from tables.random_table import RandomTable
import blueprints.items

equipment1_table: RandomTable[Item] = RandomTable[Item](
    [
        (blueprints.items.sword, 1),
        (blueprints.items.dagger, 1),
        (blueprints.items.chain_mail, 1),
        (blueprints.items.leather_armor, 1),
    ]
)

consumables_table: RandomTable[Item] = RandomTable[Item](
    [
        (blueprints.items.fireball_scroll, 10),
        (blueprints.items.lightning_scroll, 10),
        (blueprints.items.confusion_scroll, 10),
        (blueprints.items.health_potion, 30),
    ]
)

equipment1_bag: GrabBag[Item] = GrabBag[Item](
    [
        (equipment1_table, 1),
    ]
)

crystal_lizard_bag: GrabBag[Item] = GrabBag[Item](
    [
        (consumables_table, 5),
    ]
)
