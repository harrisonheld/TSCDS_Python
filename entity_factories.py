import sys

from components import consumable, equippable
from components.ai import *
from components.ai.beamer_ai import BeamerAI
from components.ai.flamewalker_ai import OgglerAI
from components.ai.frog_warden_ai import FrogWardenAI
from components.ai.fumeknight_ai import FumeKnightAI
from components.ai.hostile_enemy_ai import HostileEnemyAI
from components.ai.indrix_ai import IndrixAI
from components.consumable import SwapConsumable
from components.equipment import Equipment, SlotType
from components.equippable import Equippable
from components.fighter import Fighter
from components.fire import Fire
from components.fire_immune import FireImmune
from components.gas import Gas
from components.gas_immune import GasImmune
from components.illumination import Illumination
from components.inventory import Inventory
from components.level import Level
from components.pushable import Pushable
from components.trail_leaver import TrailLeaver
from entity import *
from upgrades import *
import color

humanoid_equipment = Equipment()
humanoid_equipment.add_slot(SlotType.HAND)
humanoid_equipment.add_slot(SlotType.HAND)
humanoid_equipment.add_slot(SlotType.HEAD)
humanoid_equipment.add_slot(SlotType.BODY)
humanoid_equipment.add_slot(SlotType.HANDS)
humanoid_equipment.add_slot(SlotType.LEGS)
humanoid_equipment.add_slot(SlotType.FEET)

player = Actor(
    char="@",
    color=color.sky_blue,
    name="Player",
    description="It's you.",
    ai_cls=HostileEnemyAI,
    equipment=copy.deepcopy(humanoid_equipment),
    fighter=Fighter(hp=30, base_defense=0, base_power=2),
    inventory=Inventory(capacity=4),
    level=Level(level_up_base=200),
)

fire = Entity(
    char="‼",
    name="fire",
    description="A roaring fire.",
    color=color.red,
    blocks_movement=False,
    components=[Fire(lifetime=6, damage=1), Illumination(light_radius=4)],
)
gas = Entity(
    char="▓",
    name="scalding gas",
    description="A cloud of scalding gas, drawn from deep within the earth. It burns the skin and lungs.",
    color=color.red,
    blocks_movement=False,
    components=[Gas(density=7, damage=1, spread_chance=0.2)],
)

dessicated_vassal = Actor(
    char="v",
    color=color.dark_grey,
    name="dessicated vassal",  # dessicated means dry, but it also means "lacking vitality or interest"
    description="His body crumbles with every step. Dry, cracked skin hangs from his bones. A testament to time's cruelty.",
    ai_cls=HostileEnemyAI,
    equipment=Equipment(),
    fighter=Fighter(hp=12, base_defense=1, base_power=3),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=20),
)


frog_warden = Actor(
    char="f",
    color=color.green,
    name="frog warden",
    description="A creature in the shape of a man, wrought of decayed sinews and oozing ichors. Its xanthous eyes belie an animated disposition. Through the mire, its skeletal fingers grasp fervently at amphibious creatures with undisputed affection; for what ghastly purpose, no one knows.",
    ai_cls=FrogWardenAI,
    equipment=Equipment(),
    fighter=Fighter(hp=10, base_defense=0, base_power=3),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=35),
)

beamer = Actor(
    char="b",
    color=color.red,
    name="beamer",
    description="[TODO]",
    ai_cls=BeamerAI,
    equipment=Equipment(),
    fighter=Fighter(hp=16, base_defense=1, base_power=4),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=150),
)

flamewalker = Actor(
    char="f",
    color=color.deep_red,
    name="flamewalker",
    description="A little spur of fire. Locks of flame dance close behind him as he rolls and tumbles. He seems to mean no harm. Why not let him close?",
    ai_cls=OgglerAI,
    equipment=Equipment(),
    fighter=Fighter(hp=3, base_defense=0, base_power=1),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=20),
    components=[TrailLeaver(fire), FireImmune()],
)
flameprowler = Actor(
    char="F",
    color=color.deep_red,
    name="flame prowler",
    description="A rolling storm of fire spawned of acridity and heat. Tendrils of wicked flame lash the air in its wake.",
    ai_cls=HostileEnemyAI,
    equipment=Equipment(),
    fighter=Fighter(hp=10, base_defense=0, base_power=3),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=100),
    components=[TrailLeaver(fire), FireImmune(), GasImmune()],
)

indrix = Actor(
    char="G",
    color=color.sky_blue,
    name="teary-eyed Indrix",
    description="Cast from his home twice too many times, the caprine pariah wields the amaranthine prism, seeking to end his own life in a spectacular fashion. The great curling horn slung low about his hip gives him the distinction of being the only warrior to bear his own appendage as a trophy.",
    ai_cls=IndrixAI,
    equipment=Equipment(),
    fighter=Fighter(hp=30, base_defense=1, base_power=4),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=400),
)
fume_knight = Actor(
    char="F",
    color=color.dark_grey,
    name="Fume Knight",
    description="[TODO]",
    ai_cls=FumeKnightAI,
    equipment=Equipment(),
    fighter=Fighter(hp=50, base_defense=2, base_power=6),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=500),
    components=[GasImmune(), FireImmune()],
)
default_boss = Actor(
    name="Soldier of God",
    char="R",
    color=color.green,
    description="Clad in resplendent green and red armor, adorned with intricate golden filigree, Rick is the G.O.A.T. Essentially, you will have a very hard time defeating Rick.",
    ai_cls=HostileEnemyAI,
    equipment=Equipment(),
    fighter=Fighter(hp=1, base_defense=0, base_power=1),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=10),
)

indrix_leap_indicator = Entity(
    char="▼",
    name="indicator",
    description="Indrix is about to land!",
    color=color.deep_red,
    render_order=RenderOrder.EFFECT_TOP,
)
beamer_ray_indicator = Entity(
    char=".",
    color=color.deep_red,
    name="indicator",
    description="If you're standing here, you shouldn't be.",
    render_order=RenderOrder.EFFECT_BOTTOM,
)

confusion_scroll = Item(
    char="~",
    color=color.purple,
    name="confusion scroll",
    description="[TODO]",
    consumable=consumable.ConfusionConsumable(number_of_turns=10),
)
fireball_scroll = Item(
    char="~",
    color=color.red,
    name="fireball scroll",
    description="[TODO]",
    consumable=consumable.FireballDamageConsumable(damage=12, radius=3),
)
health_potion = Item(
    char="&",
    color=color.green,
    name="health potion",
    description="[TODO]",
    consumable=consumable.HealingConsumable(amount=4),
)
lightning_scroll = Item(
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


dagger = Item(
    char="/",
    color=color.light_grey,
    name="dagger",
    equippable=Equippable(slot_type=SlotType.HAND, power_bonus=2),
)
sword = Item(
    char="\\",
    color=color.light_grey,
    name="sword",
    equippable=Equippable(slot_type=SlotType.HAND, power_bonus=4),
)

leather_armor = Item(
    char="[",
    color=color.orange,
    name="leather armor",
    equippable=Equippable(slot_type=SlotType.BODY, defense_bonus=1),
)
chain_mail = Item(
    char="[",
    color=color.light_grey,
    name="chain mail",
    equippable=Equippable(slot_type=SlotType.BODY, defense_bonus=3),
)

brazier = Entity(
    char="O",
    name="brazier",
    description="A large copper basin of flaming coals.",
    color=color.orange,
    blocks_movement=True,
    render_order=RenderOrder.ACTOR,
    components=[Illumination(light_radius=10)],
)
statue = Entity(
    char="Ω",
    name="statue of Indrix",
    description=r"""A black ivory statue depicting the goatman-turned-shaman Indrix. A curling horn from the statue's head is broken off, while the other winds and pierces sharply the air above.

It is a heavy, solid thing, but it could be moved if you used your whole bodyweight.""",
    color=color.dark_grey,
    blocks_movement=True,
    render_order=RenderOrder.ACTOR,
    components=[Pushable()],
)
barrel = Entity(
    char="O",
    name="barrel",
    description="A wooden barrel.",
    color=color.orange,
    blocks_movement=True,
    render_order=RenderOrder.ACTOR,
    components=[Pushable()],
)
corpse = Entity(
    char="%",
    name="remains",
    description="The remains of a once living creature.",
    color=color.deep_red,
    blocks_movement=False,
    render_order=RenderOrder.CORPSE,
)
