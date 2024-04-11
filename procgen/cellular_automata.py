from __future__ import annotations

from procgen.helpers import *

import sizes
from game_map import GameMap
import tile_types

if TYPE_CHECKING:
    from engine import Engine
    from entity import Entity


def generate_dungeon(engine: Engine) -> GameMap:
    floor_percent = 0.5
    iterations = 4

    player = engine.player
    dungeon = GameMap(engine, sizes.dungeon_width, sizes.dungeon_height, entities=[player])

    # Randomly place floor
    for x in range(sizes.dungeon_width):
        for y in range(sizes.dungeon_height):
            dungeon.tiles[x, y] = tile_types.floor if (random.random() < floor_percent) else tile_types.wall

    # Cellular Automata
    for _ in range(iterations):
        neighbor_counts = [[0 for _ in range(sizes.dungeon_height)] for _ in range(sizes.dungeon_width)]
        for x in range(1, sizes.dungeon_width-1):
            for y in range(1, sizes.dungeon_height-1):
                for dx in range(x - 1, x + 2):
                    for dy in range(y - 1, y + 2):
                        if (dx != x or dy != y) and 0 < dx < sizes.dungeon_width-1 and 0 < dy < sizes.dungeon_height-1 and dungeon.tiles[dx, dy] == tile_types.floor:
                            neighbor_counts[x][y] += 1

        for x in range(0, sizes.dungeon_width - 1):
            for y in range(0, sizes.dungeon_height - 1):
                if neighbor_counts[x][y] > 4:
                    dungeon.tiles[x, y] = tile_types.floor
                elif neighbor_counts[x][y] < 4:
                    dungeon.tiles[x, y] = tile_types.wall

    # Place stairs
    dungeon.tiles[sizes.dungeon_width // 2, sizes.dungeon_height // 2] = tile_types.down_stairs
    dungeon.downstairs_location = (sizes.dungeon_width // 2, sizes.dungeon_height // 2)
    # Place player
    player.place(*dungeon.downstairs_location, gamemap=dungeon)

    return dungeon
