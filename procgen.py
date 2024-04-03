from __future__ import annotations

from typing import TYPE_CHECKING, Dict, Iterator, List, Tuple
import random

import tcod

from game_map import GameMap
import entity_factories
import tile_types

if TYPE_CHECKING:
    from engine import Engine
    from entity import Entity


max_items_by_floor = [
    (1, 1),
    (4, 2),
]

max_monsters_by_floor = [
    (1, 2),
    (4, 3),
    (6, 5),
]

item_chances: Dict[int, List[Tuple[Entity, int]]] = {
    0: [(entity_factories.health_potion, 35)],
    2: [(entity_factories.confusion_scroll, 10)],
    4: [(entity_factories.lightning_scroll, 25), (entity_factories.sword, 5)],
    6: [(entity_factories.fireball_scroll, 25), (entity_factories.chain_mail, 15)],
}

enemy_chances: Dict[int, List[Tuple[Entity, int]]] = {
    0: [(entity_factories.orc, 50)],
    3: [(entity_factories.ranger, 15)],
    5: [(entity_factories.ranger, 30)],
    7: [(entity_factories.ranger, 60)],
}

treasure_pool: List[Entity] = [
    entity_factories.eye_of_belial,
    entity_factories.horn_of_geddon
]


def get_max_value_for_floor(max_value_by_floor: List[Tuple[int, int]], floor: int) -> int:
    current_value = 0

    for floor_minimum, value in max_value_by_floor:
        if floor_minimum > floor:
            break
        else:
            current_value = value

    return current_value


def get_entities_at_random(
    weighted_chances_by_floor: Dict[int, List[Tuple[Entity, int]]],
    number_of_entities: int,
    floor: int,
) -> List[Entity]:
    entity_weighted_chances = {}

    for key, values in weighted_chances_by_floor.items():
        if key > floor:
            break
        else:
            for value in values:
                entity = value[0]
                weighted_chance = value[1]

                entity_weighted_chances[entity] = weighted_chance

    entities = list(entity_weighted_chances.keys())
    entity_weighted_chance_values = list(entity_weighted_chances.values())

    chosen_entities = random.choices(entities, weights=entity_weighted_chance_values, k=number_of_entities)

    return chosen_entities


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
        return slice(self.x1, self.x2+1), slice(self.y1, self.y2+1)

    def intersects(self, other: RoomBase) -> bool:
        """Return True if this room overlaps with another RectangularRoom."""
        return self.x1 <= other.x2 and self.x2 >= other.x1 and self.y1 <= other.y2 and self.y2 >= other.y1



class RegularRoom(RoomBase):
    def populate(self, dungeon: GameMap) -> None:
        number_of_monsters = random.randint(0, get_max_value_for_floor(max_monsters_by_floor, self.floor_number))
        number_of_items = random.randint(0, get_max_value_for_floor(max_items_by_floor, self.floor_number))

        monsters: List[Entity] = get_entities_at_random(enemy_chances, number_of_monsters, self.floor_number)
        items: List[Entity] = get_entities_at_random(item_chances, number_of_items, self.floor_number)

        for entity in monsters + items:
            x = random.randint(self.x1 + 1, self.x2 - 1)
            y = random.randint(self.y1 + 1, self.y2 - 1)

            if not any(entity.x == x and entity.y == y for entity in dungeon.entities):
                entity.spawn(dungeon, x, y)


class TreasureRoom(RoomBase):
    def populate(self, dungeon: GameMap) -> None:

        loot: Entity = random.choice(treasure_pool)
        treasure_pool.remove(loot)
        loot.spawn(dungeon, *self.center)

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


def generate_dungeon(
    max_rooms: int,
    room_min_size: int,
    room_max_size: int,
    map_width: int,
    map_height: int,
    engine: Engine,
) -> GameMap:
    """Generate a new dungeon map."""
    player = engine.player
    dungeon = GameMap(engine, map_width, map_height, entities=[player])

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

        # Choose room type based on whether a treasure room has been generated yet
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
