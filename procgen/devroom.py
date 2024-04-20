from __future__ import annotations

import entity_factories
from procgen.helpers import *
from typing import List, TYPE_CHECKING
from entity import Entity, Actor

import sizes
from game_map import GameMap
import tile_types

if TYPE_CHECKING:
    from engine import Engine
    from entity import Entity


def generate(engine: Engine) -> GameMap:
    player = engine.player
    dungeon = GameMap(engine, sizes.dungeon_width, sizes.dungeon_height, entities=[player])

    dungeon.tiles[:] = tile_types.floor
    dungeon.explored[:] = True

    # Place stairs
    dungeon.tiles[0, 0] = tile_types.down_stairs
    dungeon.downstairs_location = (0, 0)
    # Place player
    player.place(0, 0, gamemap=dungeon)

    blueprints: List[Entity] = [value for value in vars(entity_factories).values() if isinstance(value, Entity)]
    idx = 0
    for blueprint in blueprints:
        idx += 1
        instance: Entity = blueprint.spawn(dungeon, idx, 0)
        # remove AI
        if isinstance(instance, Actor):
            instance.ai = None

    return dungeon
