import sys

import color
from components import consumable, equippable
from components.ai import *
from components.consumable import SwapConsumable
from components.equippable import Equippable
from components.equipment import Equipment
from components.fighter import Fighter
from components.inventory import Inventory
from components.level import Level
from entity import *
from equipment_types import EquipmentType
from upgrades import *

player = Actor(
    char="@",
    color=(255, 255, 255),
    name="Player",
    description="It's you.",
    ai_cls=HostileEnemy,
    equipment=Equipment(),
    fighter=Fighter(hp=30, base_defense=0, base_power=2),
    inventory=Inventory(capacity=4),
    level=Level(level_up_base=200),
)

frog_warden = Actor(
    char="f",
    color=color.dark_green,
    name="frog warden",
    description="A creature in the shape of a man, wrought of decayed sinews and oozing ichors. The xanthous eyes belie an animated disposition. Through the mire, its skeletal fingers grasp fervently at amphibious creatures with undisputed affection; for what ghastly purpose, no one knows.",
    ai_cls=HostileEnemy,
    equipment=Equipment(),
    fighter=Fighter(hp=10, base_defense=0, base_power=3),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=35),
)

ranger = Actor(
    char="r",
    color=color.dark_red,
    name="ranger",
    description="[TODO]",
    ai_cls=RangedEnemy,
    equipment=Equipment(),
    fighter=Fighter(hp=16, base_defense=1, base_power=4),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=100),
)

indrix = Actor(
    char="g",
    color=color.light_carbide_blue,
    name="teary-eyed Indrix",
    description="Cast from his home twice too many times, the pariah willfully wields the amaranthine prism, seeking to end his own life in a spectacular fashion. The great curling horn slung low about his hip gives him the distinction of being the only warrior to bear his own appendage as a trophy. Finally, beware: his power is most potent when he lays his hands on you.",
    ai_cls=HostileEnemy,
    equipment=Equipment(),
    fighter=Fighter(hp=35, base_defense=1, base_power=4),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=400),
)

confusion_scroll = Item(
    char="~",
    color=(207, 63, 255),
    name="confusion scroll",
    description="[TODO]",
    consumable=consumable.ConfusionConsumable(number_of_turns=10),
)
fireball_scroll = Item(
    char="~",
    color=(255, 0, 0),
    name="fireball scroll",
    description="[TODO]",
    consumable=consumable.FireballDamageConsumable(damage=12, radius=3),
)
health_potion = Item(
    char="&",
    color=color.dark_green,
    name="health potion",
    description="[TODO]",
    consumable=consumable.HealingConsumable(amount=4),
)
lightning_scroll = Item(
    char="~",
    color=(255, 255, 0),
    name="lightning scroll",
    description="[TODO]",
    consumable=consumable.LightningDamageConsumable(damage=20, maximum_range=5),
)

eye_of_belial = UpgradeEyeOfBelial(
    char="☼",
    color=color.red,
    name="Eye of Belial",
    description="""A perfectly smooth sphere carved of red chalcedony.

When in your inventory, allows you to see the detailed stats and health of enemies by looking at them."""
)
dagashas_spur = UpgradeDagashasSpur(
    char="Ü",
    color=color.red,
    name="Dagasha's Spur",
    description="""This crown of thorns points outward, but its wearer's mind is pierced all the same, drawing in will.

Allows you to swap places with an adjacent enemy.""",
    consumable=SwapConsumable()
)
max_health_potion = Item(
    char="&",
    color=color.red,
    name="max health potion",
    description="""Wysterwort DCXLVIII (reigned 206 - 201): Where his predecessor was known to vanquish anyone who opposed him, King Wysterwort DCXLVIII made no such distinction. For those that survived his fickle bouts of executions, they found themselves subject to strange rules of law. In the year 203, it was mandaded that human babes should be nursed with wine rather than milk. Wysterwort's eccentricities were humored amidst a backdrop of famine and disease. The mad king himself fell victim to blight, and commisioned an alchemist to brew the max health potion. Days before its completion, and for reasons undocumented, the accomplished monarch fell into a deep depression and strangled himself. He was survived by his heir Wysterwort DCXLIX, who abdicated mere minutes later.

Heals you to max health.""",
    consumable=consumable.HealingConsumable(amount=sys.maxsize),
)
cracked_red_eye_orb = UpgradeCrackedRedEyeOrb(
    char="Φ",
    color=color.red,
    name="Cracked Red Eye Orb",
    description="""This red gemstone lights a roaring fire in your heart, granting you a tranquil rage. It would only be remiss to leave an enemy unslain.

When in your inventory, increases your attack power by 1.""",
)
cracked_blue_eye_orb = UpgradeCrackedBlueEyeOrb(
    char="Θ",
    color=color.red,
    name="Cracked Blue Eye Orb",
    description="""This soothing azure gemstone whispers resilience. Cast aside your doubts; they are unworthy of you.

When in your inventory, increases your defense by 1.""",
)

no_loot_note = Item(
    color=color.white,
    char='~',
    name="scrap of paper",
    description="A torn piece of paper with a message scrawled on it: 'Sorry adventurer, this dungeon ran out of treasure! Better luck next time!'"
)


dagger = Item(char="/", color=color.light_grey, name="Dagger", equippable=Equippable(equipment_type=EquipmentType.WEAPON, power_bonus=2))
carbide_hammer = Item(char="/", color=color.light_carbide_blue, name="Carbide Hammer", equippable=Equippable(equipment_type=EquipmentType.WEAPON, power_bonus=5))
sword = Item(char="\\", color=color.light_grey, name="Sword", equippable=Equippable(equipment_type=EquipmentType.WEAPON, power_bonus=4))

leather_armor = Item(char="[", color=color.brown, name="Leather Armor", equippable=Equippable(equipment_type=EquipmentType.ARMOR, defense_bonus=1))
chain_mail = Item(char="[", color=color.light_grey, name="Chain Mail", equippable=Equippable(equipment_type=EquipmentType.ARMOR, defense_bonus=3))
