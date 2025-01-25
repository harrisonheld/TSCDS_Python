from __future__ import annotations

from typing import TYPE_CHECKING, Dict, Iterator, List, Tuple
import random

import tcod

from game_map import GameMap
from procgen.helpers import *
import blueprints
import sizes
import tile_types

if TYPE_CHECKING:
    from engine import Engine
    from entity import Entity


class RoomBase:
    def __init__(self, x: int, y: int, width: int, height: int, floor_number: int):
        self.x1 = x
        self.y1 = y
        self.x2 = x + width
        self.y2 = y + height
        self.floor_number = floor_number

    @property
    def center(self) -> Tuple[int, int]:
        center_x = int((self.x1 + self.x2) / 2)
        center_y = int((self.y1 + self.y2) / 2)

        return center_x, center_y

    @property
    def inner(self) -> Tuple[slice, slice]:
        """Return the inner area of this room as a 2D array index."""
        return slice(self.x1 + 1, self.x2), slice(self.y1 + 1, self.y2)

    @property
    def inner_with_rind(self) -> Tuple[slice, slice]:
        """Return the area of this room, including the walls, as a 2D array index."""
        return slice(self.x1, self.x2 + 1), slice(self.y1, self.y2 + 1)

    def intersects(self, other: RoomBase) -> bool:
        """Return True if this room overlaps with another RectangularRoom."""
        return self.x1 <= other.x2 and self.x2 >= other.x1 and self.y1 <= other.y2 and self.y2 >= other.y1

    def populate(self, dungeon: GameMap) -> None:
        pass


class RegularRoom(RoomBase):
    def populate(self, dungeon: GameMap) -> None:
        number_of_monsters = random.randint(0, get_max_value_for_floor(max_monsters_by_floor, self.floor_number))
        number_of_items = random.randint(0, get_max_value_for_floor(max_items_by_floor, self.floor_number))

        monsters: List[Entity] = get_entities_at_random(enemy_chances, number_of_monsters, self.floor_number)
        items: List[Entity] = get_entities_at_random(item_chances, number_of_items, self.floor_number)

        for entity in monsters + items:
            x = random.randint(self.x1 + 1, self.x2 - 1)
            y = random.randint(self.y1 + 1, self.y2 - 1)

            if len(dungeon.get_entities_at_location(x, y)) == 0 and not dungeon.tiles[x, y] == tile_types.down_stairs:
                entity.spawn(dungeon, x, y)


class TreasureRoom(RoomBase):
    def populate(self, dungeon: GameMap) -> None:

        # spawn loot
        loot: Entity
        pool: List[Entity] = dungeon.engine.game_world.treasure_pool
        if len(pool) > 0:
            loot = random.choice(pool)
            pool.remove(loot)
        else:
            loot = blueprints.default_loot
        loot.spawn(dungeon, *self.center)

        # spawn a few barrels
        barrels = random.randint(1, 3)
        for _ in range(barrels):
            x = random.randint(self.x1 + 1, self.x2 - 1)
            y = random.randint(self.y1 + 1, self.y2 - 1)

            if len(dungeon.get_entities_at_location(x, y)) == 0 and not dungeon.tiles[x, y] == tile_types.down_stairs:
                blueprints.barrel.spawn(dungeon, x, y)

        # TODO: remove this, it makes it so you can see the treasure room from the start
        dungeon.explored[self.inner_with_rind] = True


def tunnel_between(start: Tuple[int, int], end: Tuple[int, int]) -> Iterator[Tuple[int, int]]:
    """Return an L-shaped tunnel between these two points."""
    x1, y1 = start
    x2, y2 = end
    if random.random() < 0.5:  # 50% chance.
        # Move horizontally, then vertically.
        corner_x, corner_y = x2, y1
    else:
        # Move vertically, then horizontally.
        corner_x, corner_y = x1, y2

    # Generate the coordinates for this tunnel.
    for x, y in tcod.los.bresenham((x1, y1), (corner_x, corner_y)).tolist():
        yield x, y
    for x, y in tcod.los.bresenham((corner_x, corner_y), (x2, y2)).tolist():
        yield x, y


def generate(engine: Engine) -> GameMap:
    """Generate a new dungeon map."""
    room_max_size = 10
    room_min_size = 6
    max_rooms = 30

    player = engine.player
    dungeon = GameMap(engine, sizes.dungeon_width, sizes.dungeon_height, entities=[player])

    treasure_room_generated = False
    rooms: List[RoomBase] = []

    center_of_last_room = (0, 0)

    treasure_room_generated = False
    player_placed = False

    for i in range(max_rooms):
        room_width = random.randint(room_min_size, room_max_size)
        room_height = random.randint(room_min_size, room_max_size)

        x = random.randint(0, dungeon.width - room_width - 1)
        y = random.randint(0, dungeon.height - room_height - 1)

        new_room: RoomBase
        if not treasure_room_generated:
            new_room = TreasureRoom(x, y, room_width, room_height, engine.game_world.current_floor)
        else:
            new_room = RegularRoom(x, y, room_width, room_height, engine.game_world.current_floor)

        # Run through the other rooms and see if they intersect with this one.
        if any(new_room.intersects(other_room) for other_room in rooms):
            continue  # This room intersects, so go to the next attempt.
        # If there are no intersections then the room is valid.

        # Dig out this room's inner area.
        dungeon.tiles[new_room.inner] = tile_types.floor

        if not player_placed and isinstance(new_room, RegularRoom):
            # The first room, where the player starts.
            player.place(*new_room.center, gamemap=dungeon)
            player_placed = True

        if i > 0:  # All rooms after the first.
            # Dig out a tunnel between this room and the previous one.
            for x, y in tunnel_between(rooms[-1].center, new_room.center):
                dungeon.tiles[x, y] = tile_types.floor

            center_of_last_room = new_room.center

        new_room.populate(dungeon)

        dungeon.tiles[center_of_last_room] = tile_types.down_stairs
        dungeon.downstairs_location = center_of_last_room

        # Set the flag to True after generating the first treasure room
        if isinstance(new_room, TreasureRoom):
            treasure_room_generated = True

        # Finally, append the new room to the list.
        rooms.append(new_room)

    return dungeon
