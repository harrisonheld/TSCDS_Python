from __future__ import annotations

from typing import TYPE_CHECKING, List

from entity import Actor, Entity
from game_map import GameMap
from procgen.helpers import *
import blueprints
import sizes
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

    blueprints: List[Entity] = [value for value in vars(blueprints).values() if isinstance(value, Entity)]
    idx = 0
    for blueprint in blueprints:
        idx += 1
        instance: Entity = blueprint.spawn(dungeon, idx, 0)
        # remove AI
        if isinstance(instance, Actor):
            instance.ai = None

    return dungeon
