import color
from components import consumable, equippable
from components.ai import *
from components.consumable import SwapConsumable
from components.equipment import Equipment
from components.fighter import Fighter
from components.inventory import Inventory
from components.level import Level
from entity import *
from upgrades import *

player = Actor(
    char="@",
    color=(255, 255, 255),
    name="Player",
    description="It's you.",
    ai_cls=HostileEnemy,
    equipment=Equipment(),
    fighter=Fighter(hp=30, base_defense=1, base_power=2),
    inventory=Inventory(capacity=6),
    level=Level(level_up_base=200),
)

orc = Actor(
    char="o",
    color=color.dark_green,
    name="orc",
    description="He looks like the average british person.",
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
    ai_cls=RangedEnemy,
    equipment=Equipment(),
    fighter=Fighter(hp=16, base_defense=1, base_power=4),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=100),
)

confusion_scroll = Item(
    char="~",
    color=(207, 63, 255),
    name="confusion scroll",
    consumable=consumable.ConfusionConsumable(number_of_turns=10),
)
fireball_scroll = Item(
    char="~",
    color=(255, 0, 0),
    name="fireball scroll",
    consumable=consumable.FireballDamageConsumable(damage=12, radius=3),
)
health_potion = Item(
    char="&",
    color=color.dark_green,
    name="health potion",
    consumable=consumable.HealingConsumable(amount=4),
)
lightning_scroll = Item(
    char="~",
    color=(255, 255, 0),
    name="lightning scroll",
    consumable=consumable.LightningDamageConsumable(damage=20, maximum_range=5),
)

eye_of_belial = UpgradeEyeOfBelial(
    char="☼",
    color=color.red,
    name="Eye of Belial",
    description="A perfectly smooth sphere carved of red chalcedony. Allows you to see the full stats and health of enemies."
)
dagashas_spur = UpgradeDagashasSpur(
    char="U",
    color=color.red,
    name="Dagasha's Spur",
    description="This crown of thorns points outward, but its wearer's mind is pierced all the same, drawing in will. Allows you to swap places with an adjacent enemy.",
    consumable=SwapConsumable()
)

no_loot_note = Item(
    color=color.white,
    char='~',
    name="scrap of paper",
    description="A torn piece of paper with a message scrawled on it: 'Sorry adventurer, this dungeon ran out of treasure! Better luck next time!'"
)


dagger = Item(char="/", color=(0, 191, 255), name="Dagger", equippable=equippable.Dagger())
sword = Item(char="/", color=(0, 191, 255), name="Sword", equippable=equippable.Sword())

leather_armor = Item(char="[", color=(139, 69, 19), name="Leather Armor", equippable=equippable.LeatherArmor())
chain_mail = Item(char="[", color=(139, 69, 19), name="Chain Mail", equippable=equippable.ChainMail())
