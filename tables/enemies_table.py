from entity import Actor
from tables.random_table import RandomTable
import blueprints.actors

dungeon_table: RandomTable[Actor] = RandomTable[Actor](
    [
        (blueprints.actors.dessicated_vassal, 50),
        (blueprints.actors.frog_warden, 50),
        (blueprints.actors.flameling, 20),
        (blueprints.actors.crystal_lizard, 10),
        (blueprints.actors.beamer, 50),
    ]
)
