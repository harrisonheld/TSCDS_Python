from components import equippable
from components.ai import *
from components.ai.beamer_ai import BeamerAI
from components.ai.frog_warden_ai import FrogWardenAI
from components.ai.fumeknight_ai import FumeKnightAI
from components.ai.hostile_enemy_ai import HostileEnemyAI
from components.ai.indrix_ai import IndrixAI
from components.ai.npc_ai import NpcAI
from components.ai.oggler_ai import OgglerAI
from components.conversation import Conversation
from components.equipment import Equipment, SlotType
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
import helpers
import tables.loot_tables as loot_tables

humanoid_equipment = Equipment()
humanoid_equipment.add_slot(SlotType.HAND)
humanoid_equipment.add_slot(SlotType.HAND)
humanoid_equipment.add_slot(SlotType.HEAD)
humanoid_equipment.add_slot(SlotType.BODY)
humanoid_equipment.add_slot(SlotType.HANDS)
humanoid_equipment.add_slot(SlotType.LEGS)
humanoid_equipment.add_slot(SlotType.FEET)
humanoid_equipment.add_slot(SlotType.MISSILE)
humanoid_equipment.add_slot(SlotType.MISSILE)
humanoid_equipment.add_slot(SlotType.THROWN)

quadruped_equipment = Equipment()
quadruped_equipment.add_slot(SlotType.HEAD)
quadruped_equipment.add_slot(SlotType.BODY)
quadruped_equipment.add_slot(SlotType.LEGS)
quadruped_equipment.add_slot(SlotType.LEGS)
quadruped_equipment.add_slot(SlotType.FEET)
quadruped_equipment.add_slot(SlotType.FEET)

player = Actor(
    char="@",
    color=color.sky_blue,
    name="Harrison",
    description="It's you.",
    ai_cls=HostileEnemyAI,
    equipment=copy.deepcopy(humanoid_equipment),
    fighter=Fighter(hp=30, base_defense=0, base_power=2),
    inventory=Inventory(),
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
    equipment=copy.deepcopy(humanoid_equipment),
    fighter=Fighter(hp=8, base_defense=0, base_power=3),
    inventory=Inventory(),
    level=Level(xp_given=20),
    grab_bag=loot_tables.equipment1_bag,
)


frog_warden = Actor(
    char="f",
    color=color.green,
    name="frog warden",
    description="A creature in the shape of a man, wrought of decayed sinews and oozing ichors. Its xanthous eyes belie an animated disposition. Through the mire, its skeletal fingers grasp fervently at amphibious creatures with undisputed affection; for what ghastly purpose, no one knows.",
    ai_cls=FrogWardenAI,
    equipment=copy.deepcopy(humanoid_equipment),
    fighter=Fighter(hp=10, base_defense=1, base_power=3),
    inventory=Inventory(),
    level=Level(xp_given=35),
    grab_bag=loot_tables.frog_warden_bag,
)

# TODO: make him flee instead of fight you
crystal_lizard = Actor(
    char="l",
    color=color.sky_blue,
    name="crystal lizard",
    description="Behold, rump! Therefore, try thrusting.",
    ai_cls=HostileEnemyAI,
    equipment=Equipment(),
    fighter=Fighter(hp=1, base_defense=0, base_power=3),
    inventory=Inventory(),
    level=Level(xp_given=100),
    grab_bag=loot_tables.crystal_lizard_bag,
)

beamer = Actor(
    char="b",
    color=color.red,
    name="beamer",
    description="[TODO]",
    ai_cls=BeamerAI,
    equipment=Equipment(),
    fighter=Fighter(hp=16, base_defense=1, base_power=4),
    inventory=Inventory(),
    level=Level(xp_given=150),
)

flameling = Actor(
    char="f",
    color=color.deep_red,
    name="flameling",
    description="A little spur of fire. Locks of flame dance close behind him as he rolls and tumbles. He seems to mean no harm. Why not let him close?",
    ai_cls=OgglerAI,
    equipment=Equipment(),
    fighter=Fighter(hp=3, base_defense=0, base_power=1),
    inventory=Inventory(),
    level=Level(xp_given=20),
    components=[TrailLeaver(fire), FireImmune()],
    grab_bag=loot_tables.flameling_bag,
)
flameprowler = Actor(
    char="F",
    color=color.deep_red,
    name="flame prowler",
    description="A rolling storm of fire spawned of acridity and heat. Tendrils of wicked flame lash the air in its wake.",
    ai_cls=HostileEnemyAI,
    equipment=Equipment(),
    fighter=Fighter(hp=10, base_defense=0, base_power=3),
    inventory=Inventory(),
    level=Level(xp_given=100),
    components=[TrailLeaver(fire), FireImmune(), GasImmune()],
    grab_bag=loot_tables.flameprowler_bag,
)

indrix = Actor(
    char="G",
    color=color.sky_blue,
    name="teary-eyed Indrix",
    description="Cast from his home twice too many times, the caprine pariah wields the amaranthine prism, seeking to end his own life in a spectacular fashion. The great curling horn slung low about his hip gives him the distinction of being the only warrior to bear his own appendage as a trophy.",
    ai_cls=IndrixAI,
    equipment=copy.deepcopy(humanoid_equipment),
    fighter=Fighter(hp=30, base_defense=1, base_power=4),
    inventory=Inventory(),
    level=Level(xp_given=400),
)
fume_knight = Actor(
    char="F",
    color=color.dark_grey,
    name="Fume Knight",
    description="[TODO]",
    ai_cls=FumeKnightAI,
    equipment=copy.deepcopy(humanoid_equipment),
    fighter=Fighter(hp=50, base_defense=2, base_power=6),
    inventory=Inventory(),
    level=Level(xp_given=500),
    components=[GasImmune(), FireImmune()],
)
default_boss = Actor(
    name="Soldier of God",
    char="R",
    color=color.green,
    description="Clad in resplendent green and red armor, adorned with intricate golden filigree, Rick is the G.O.A.T. Essentially, you will have a very hard time defeating Rick.",
    ai_cls=HostileEnemyAI,
    equipment=copy.deepcopy(humanoid_equipment),
    fighter=Fighter(hp=1, base_defense=0, base_power=1),
    inventory=Inventory(),
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
bookshelf = Entity(
    char="≡",
    name="mahogany bookshelf",
    description="A bookshelf.",
    color=color.orange,
    blocks_movement=True,
    render_order=RenderOrder.ACTOR,
)
edwin_the_archivist = Actor(
    char="E",
    name="Edwin the Archivist",
    description="An elderly archivist, a keeper of endless volumes. His deep knowledge of the library is matched only by his devotion to preserving its secrets.",
    color=color.deep_red,
    ai_cls=NpcAI,
    equipment=copy.deepcopy(humanoid_equipment),
    fighter=Fighter(hp=10, base_defense=0, base_power=1),
    inventory=Inventory(),
    level=Level(xp_given=10),
    components=[Conversation(helpers.resource_path("data/conversations/edwin.yaml"))],
)


corpse = Entity(
    char="%",
    name="remains",
    description="The remains of a once living creature.",
    color=color.deep_red,
    blocks_movement=False,
    render_order=RenderOrder.CORPSE,
)
