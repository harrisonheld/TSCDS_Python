import sys

from components import consumable
from components.consumable import SwapConsumable
from components.equipment import SlotType
from components.equippable import Equippable
from entity import Item
from upgrades import Item, UpgradeCrackedBlueEyeOrb, UpgradeCrackedRedEyeOrb, UpgradeDagashasSpur, UpgradeEyeOfBelial
import color

confusion_scroll: Item = Item(
    char="~",
    color=color.purple,
    name="confusion scroll",
    description="[TODO]",
    consumable=consumable.ConfusionConsumable(number_of_turns=10),
)
fireball_scroll: Item = Item(
    char="~",
    color=color.red,
    name="fireball scroll",
    description="[TODO]",
    consumable=consumable.FireballDamageConsumable(damage=12, radius=3),
)
health_potion: Item = Item(
    char="&",
    color=color.green,
    name="health potion",
    description="[TODO]",
    consumable=consumable.HealingConsumable(amount=4),
)
lightning_scroll: Item = Item(
    char="~",
    color=color.orange,
    name="lightning scroll",
    description="[TODO]",
    consumable=consumable.LightningDamageConsumable(damage=20, maximum_range=5),
)
eye_of_belial = UpgradeEyeOfBelial(
    char="☼",
    color=color.red,
    name="Eye of Belial",
    description="""A perfectly smooth sphere carved of red chalcedony.

While in your inventory, allows you to see the detailed stats and health of enemies by looking at them.""",
)
dagashas_spur = UpgradeDagashasSpur(
    char="Ü",
    color=color.red,
    name="Dagasha's Spur",
    description="""This crown of thorns points outward, but its wearer's mind is pierced all the same, drawing in will.

On use, allows you to swap places with an adjacent enemy.""",
    consumable=SwapConsumable(),
)
max_health_potion = Item(
    char="&",
    color=color.red,
    name="max health potion",
    description="""Wysterwort DCXLVIII (reigned 206 - 201): Where his predecessor was known to vanquish anyone who opposed him, King Wysterwort DCXLVIII made no such distinction. For those that survived his fickle bouts of executions, they found themselves subject to strange rules of law. In the year 203, it was mandaded that human babes should be nursed with wine rather than milk. Wysterwort's eccentricities were humored amidst a backdrop of famine and disease. The mad king himself fell victim to blight, and commisioned an alchemist to brew the max health potion. Days before its completion, and for reasons undocumented, the accomplished monarch fell into a deep depression and strangled himself. He was survived by his heir Wysterwort DCXLIX, who abdicated mere minutes later.

On use, heals you to max health.""",
    consumable=consumable.HealingConsumable(amount=sys.maxsize),
)
cracked_red_eye_orb = UpgradeCrackedRedEyeOrb(
    char="Φ",
    color=color.red,
    name="Vertical-Slitted Eye",
    description="""This red gemstone whispers great strength. It would only be remiss to leave an enemy unslain.

While in your inventory, increases your attack power by 1.""",
)
cracked_blue_eye_orb = UpgradeCrackedBlueEyeOrb(
    char="Θ",
    color=color.red,
    name="Square-Pupiled Eye",
    description="""This soothing azure gemstone whispers resilience. Cast aside your doubts; they are unworthy of you.

While in your inventory, increases your defense by 1.""",
)
default_loot = Item(
    color=color.white,
    char="~",
    name="scrap of paper",
    description="A torn piece of paper with a message scrawled on it: 'Sorry adventurer, this dungeon ran out of treasure! Better luck next time!'",
)
# tier 1
bronze_sword: Item = Item(
    char="/",
    color=color.orange,
    name="bronze sword",
    equippable=Equippable(slot_type=SlotType.HAND, power_bonus=2),
)
leather_armor: Item = Item(
    char="[",
    color=color.orange,
    name="leather armor",
    equippable=Equippable(slot_type=SlotType.BODY, defense_bonus=1),
)
# tier 2
steel_sword: Item = Item(
    char="/",
    color=color.light_grey,
    name="steel sword",
    equippable=Equippable(slot_type=SlotType.HAND, power_bonus=4),
)
chain_mail: Item = Item(
    char="[",
    color=color.light_grey,
    name="chain mail",
    equippable=Equippable(slot_type=SlotType.BODY, defense_bonus=3),
)
# tier 3
mithril_sword: Item = Item(
    char="/",
    color=color.sky_blue,
    name="mythril sword",
    equippable=Equippable(slot_type=SlotType.HAND, power_bonus=6),
)
mythril_plate_mail: Item = Item(
    char="[",
    color=color.sky_blue,
    name="mythrilplate mail",
    equippable=Equippable(slot_type=SlotType.BODY, defense_bonus=5),
)
# treasure
# potential dark souls style upgrade material?
sunbleached_jag: Item = Item(char="√", color=color.white, name="sunbleached jag")
crying_jag: Item = Item(char="√", color=color.sky_blue, name="crying jag")