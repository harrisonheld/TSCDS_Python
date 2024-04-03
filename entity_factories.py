import color
from components import consumable, equippable
from components.ai import *
from components.equipment import Equipment
from components.fighter import Fighter
from components.inventory import Inventory
from components.level import Level
from entity import Actor, Item

player = Actor(
    char="@",
    color=(255, 255, 255),
    name="Player",
    ai_cls=HostileEnemy,
    equipment=Equipment(),
    fighter=Fighter(hp=30, base_defense=1, base_power=2),
    inventory=Inventory(capacity=26),
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
    char="!",
    color=(127, 0, 255),
    name="health potion",
    consumable=consumable.HealingConsumable(amount=4),
)
lightning_scroll = Item(
    char="~",
    color=(255, 255, 0),
    name="lightning scroll",
    consumable=consumable.LightningDamageConsumable(damage=20, maximum_range=5),
)

eye_of_belial = Item(
    char="☼",
    color=color.dark_red,
    name="Eye of Belial",
    description="A perfectly smooth sphere carved of red chalcedony. Allows you to see the full stats and health of enemies."
)
horn_of_gelb = Item(
    char="φ",
    color=color.yellow,
    name="Horn of Geddon",
    description="[flavor text here]. Confuses all enemies within a radius."
)


dagger = Item(char="/", color=(0, 191, 255), name="Dagger", equippable=equippable.Dagger())
sword = Item(char="/", color=(0, 191, 255), name="Sword", equippable=equippable.Sword())

leather_armor = Item(char="[", color=(139, 69, 19), name="Leather Armor", equippable=equippable.LeatherArmor())
chain_mail = Item(char="[", color=(139, 69, 19), name="Chain Mail", equippable=equippable.ChainMail())
