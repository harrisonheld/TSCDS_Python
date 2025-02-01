from entity import Item
from tables.grab_bag import GrabBag
from tables.random_table import RandomTable
import blueprints.items

equipment3_table: RandomTable[Item] = RandomTable[Item](
    [
        (blueprints.items.mithril_sword, 1),
        (blueprints.items.mythril_plate_mail, 1),
        (blueprints.items.mithril_spear, 1),
        (blueprints.items.mithril_hammer, 1),
    ]
)
equipment2_table: RandomTable[Item] = RandomTable[Item](
    [
        (equipment3_table, 1),
        (blueprints.items.chain_mail, 1),
        (blueprints.items.steel_sword, 1),
        (blueprints.items.steel_spear, 1),
        (blueprints.items.steel_hammer, 1),
    ]
)
equipment1_table: RandomTable[Item] = RandomTable[Item](
    [
        (equipment2_table, 1),
        (blueprints.items.leather_armor, 1),
        (blueprints.items.bronze_sword, 1),
        (blueprints.items.bronze_spear, 1),
        (blueprints.items.bronze_hammer, 1),
    ]
)

treasure1_table: RandomTable[Item] = RandomTable[Item](
    [
        (blueprints.items.sunbleached_jag, 1),
        (blueprints.items.unbloodied_tear, 1),
    ]
)

consumables_table: RandomTable[Item] = RandomTable[Item](
    [
        (blueprints.items.fireball_scroll, 10),
        (blueprints.items.lightning_scroll, 10),
        (blueprints.items.confusion_scroll, 10),
        (blueprints.items.major_health_potion, 30),
    ]
)

floor_loot: RandomTable[Item] = RandomTable[Item](
    [
        (blueprints.items.minor_health_potion, 10),
        (blueprints.items.major_health_potion, 10),
    ]
)

equipment1_bag: GrabBag[Item] = GrabBag[Item](
    [
        (equipment1_table, 1, 50),
        (treasure1_table, range(1, 3), 50),
    ]
)
frog_warden_bag: GrabBag[Item] = GrabBag[Item](
    [
        (equipment1_bag, 1, 50),
        (blueprints.items.frog_leg, 1, 50),
    ]
)

crystal_lizard_bag: GrabBag[Item] = GrabBag[Item](
    [
        (consumables_table, range(2, 4), 100),
    ]
)
