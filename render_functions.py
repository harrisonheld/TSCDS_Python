from __future__ import annotations

from typing import TYPE_CHECKING, Tuple

from tcod.console import Console

import color

if TYPE_CHECKING:
    from engine import Engine
    from game_map import GameMap


def render_names_at_mouse_location(console: Console, x: int, y: int, engine: Engine) -> None:

    mouse = engine.mouse_location
    if not engine.game_map.in_bounds(*mouse) or not engine.game_map.visible[*mouse]:
        return

    acc_x = 0
    entities = list(engine.game_map.get_entities_at_location(*mouse))

    for i, entity in enumerate(entities):
        console.print(x=x + acc_x, y=y, string=entity.char, fg=entity.color)
        acc_x += 1
        console.print(x=x + acc_x, y=y, string=entity.name, fg=color.white)
        acc_x += len(entity.name)

        if i < len(entities) - 1:
            console.print(x=x + acc_x, y=y, string=", ", fg=color.light_grey)
            acc_x += 2  # Account for comma and space


def render_names_at_player_location(console: Console, x: int, y: int, max_height: int, engine: Engine) -> None:
    player = engine.player
    mouse = player.xy

    here = engine.game_map.get_entities_at_location(*mouse)
    here.remove(engine.player)
    more = len(here) > max_height

    for i, entity in enumerate(here):
        if more and i == max_height - 1:
            remaining = len(here) - max_height + 1
            console.print(x=x, y=y + i, string=f"...and {remaining} more.", fg=color.light_grey)
            break

        console.print(x=x, y=y + i, string=entity.char, fg=entity.color)
        console.print(x=x + 1, y=y + i, string=entity.name, fg=color.white)
