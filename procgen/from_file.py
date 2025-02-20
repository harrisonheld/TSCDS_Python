from __future__ import annotations

from typing import TYPE_CHECKING, Dict, List

from entity import Actor, Entity
from game_map import GameMap
import blueprints
import sizes
import tile_types

if TYPE_CHECKING:
    from engine import Engine
    from entity import Entity


def generate(engine: Engine, path: str) -> GameMap:
    player = engine.player
    dungeon = GameMap(engine, sizes.dungeon_width, sizes.dungeon_height, entities=[player])

    # Load blueprints
    bps = {}
    modules = blueprints.items, blueprints.actors
    for module in modules:
        for name, blueprint in vars(module).items():
            if isinstance(blueprint, Entity):
                bps[name] = blueprint

    # Load map
    glyphs = {}
    map_data = []
    with open(path, "r") as file:
        lines = file.readlines()

    reading_glyphs = True

    for line in lines:
        line = line.strip()
        if line == "GLYPHS:":
            continue
        elif line == "MAP:":
            reading_glyphs = False
            continue

        if reading_glyphs:
            char, item_name = line.split(": ")
            item = bps[item_name]
            glyphs[char] = item  # Store the glyph to entity mapping
        else:
            # In the MAP section, just add the map lines to the map_data list
            map_data.append(line)

    # Parse the map_data and place the entities
    lines = map_data

    # Fill map with tiles (assuming 'floor' tiles by default)
    dungeon.tiles[:] = tile_types.floor
    dungeon.explored[:] = True

    # Parse the map
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char == ".":
                continue  # Empty space, no need to place anything here
            if char in glyphs:
                entity = glyphs[char]  # Get the entity based on the glyph
                entity_instance = entity.spawn(dungeon, x, y)
                # Optionally remove AI if the entity is an Actor
                if isinstance(entity_instance, Actor):
                    entity_instance.ai = None

    # Place the player at a starting position
    player.place(0, 0, gamemap=dungeon)

    return dungeon
