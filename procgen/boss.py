from __future__ import annotations

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

    dungeon.tiles[:] = tile_types.wall

    room_width = random.randint(17, sizes.dungeon_height - 6)
    room_height = random.randint(17, sizes.dungeon_height - 6)
    room_x = (sizes.dungeon_width - room_width) // 2
    room_y = (sizes.dungeon_height - room_height) // 2
    dungeon.tiles[room_x : room_x + room_width, room_y : room_y + room_height] = tile_types.floor

    # Place stairs
    dungeon.tiles[sizes.dungeon_width // 2, sizes.dungeon_height // 2] = tile_types.down_stairs
    dungeon.downstairs_location = (sizes.dungeon_width // 2, sizes.dungeon_height // 2)
    # Place player
    player.place(sizes.dungeon_width // 2, sizes.dungeon_height // 2 + 6, gamemap=dungeon)
    # Place boss
    boss_pos = (sizes.dungeon_width // 2, sizes.dungeon_height // 2)
    if engine.game_world.boss_pool == []:
        blueprints.default_boss.spawn(dungeon, *boss_pos)
    else:
        chosen = random.choice(engine.game_world.boss_pool)
        engine.game_world.boss_pool.remove(chosen)
        chosen.spawn(dungeon, sizes.dungeon_width // 2, sizes.dungeon_height // 2)
    # place braziers in corners
    blueprints.brazier.spawn(dungeon, room_x + 1, room_y + 1)
    blueprints.brazier.spawn(dungeon, room_x + room_width - 2, room_y + 1)
    blueprints.brazier.spawn(dungeon, room_x + 1, room_y + room_height - 2)
    blueprints.brazier.spawn(dungeon, room_x + room_width - 2, room_y + room_height - 2)
    # place statues orthogonally
    blueprints.statue.spawn(dungeon, sizes.dungeon_width // 2, room_y + 1)
    blueprints.statue.spawn(dungeon, sizes.dungeon_width // 2, room_y + room_height - 2)
    blueprints.statue.spawn(dungeon, room_x + 1, sizes.dungeon_height // 2)
    blueprints.statue.spawn(dungeon, room_x + room_width - 2, sizes.dungeon_height // 2)

    # make room visible
    dungeon.explored[room_x - 1 : room_x + room_width + 1, room_y - 1 : room_y + room_height + 1] = True

    return dungeon
