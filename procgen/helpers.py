from __future__ import annotations

from typing import TYPE_CHECKING, Dict, List, Tuple
import random

import blueprints.actors as actors
import blueprints.items

if TYPE_CHECKING:
    from entity import Entity


max_items_by_floor = [
    (0, 1),
    (3, 2),
]

max_monsters_by_floor = [
    (0, 2),
    (3, 3),
    (5, 5),
]

item_chances: Dict[int, List[Tuple[Entity, int]]] = {
    0: [(blueprints.items.health_potion, 35)],
    2: [(blueprints.items.confusion_scroll, 10)],
    4: [(blueprints.items.lightning_scroll, 25), (blueprints.items.steel_sword, 5)],
    6: [(blueprints.items.fireball_scroll, 25), (blueprints.items.chain_mail, 15)],
}

enemy_chances: Dict[int, List[Tuple[Entity, int]]] = {
    0: [
        (actors.dessicated_vassal, 50),
        (actors.frog_warden, 50),
        (actors.flamewalker, 20),
        (actors.crystal_lizard, 10),
    ],
    3: [(actors.beamer, 100)],
}


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
