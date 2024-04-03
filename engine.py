from __future__ import annotations

from typing import TYPE_CHECKING
import lzma
import pickle

from tcod import tcod
from tcod.console import Console
from tcod.map import compute_fov

import color
from ui.look_block import LookBlock
from ui.message_log import MessageLog
from ui.info_block import InfoBlock
import exceptions
import render_functions

if TYPE_CHECKING:
    from entity import Actor
    from game_map import GameMap, GameWorld


class Engine:
    game_map: GameMap
    game_world: GameWorld

    def __init__(self, player: Actor):
        self.message_log = MessageLog()
        self.info_block = InfoBlock(player)
        self.look_block = LookBlock()
        self.mouse_location = (0, 0)
        self.player = player

    def handle_enemy_turns(self) -> None:
        for entity in set(self.game_map.actors) - {self.player}:
            if entity.ai:
                try:
                    entity.ai.perform()
                except exceptions.Impossible:
                    pass  # Ignore impossible action exceptions from AI.

    def update_fov(self) -> None:
        """Recompute the visible area based on the players point of view."""
        self.game_map.visible[:] = compute_fov(
            self.game_map.tiles["transparent"],
            (self.player.x, self.player.y),
            radius=8,
        )
        # If a tile is "visible" it should be added to "explored".
        self.game_map.explored |= self.game_map.visible

    def render(self, console: Console) -> None:
        self.game_map.render(console)
        self.info_block.render(console, self.game_map.width+1, 0, width=19, height=10)
        self.message_log.render(console=console, x=self.game_map.width+1, y=11, width=19, height=self.game_map.height-11)
        console.draw_frame(self.game_map.width, 0, 1, self.game_map.height, decoration="│││││││││")
        console.draw_frame(self.game_map.width, 10, 20, 1, decoration="──────├──")
        console.print_box(self.game_map.width+1, 10, 19, 1, "┤Message Log├", fg=color.white, alignment=tcod.constants.CENTER)
        render_functions.render_names_at_mouse_location(console=console, x=0, y=self.game_map.height-1, engine=self)

    def save_as(self, filename: str) -> None:
        """Save this Engine instance as a compressed file."""
        save_data = lzma.compress(pickle.dumps(self))
        with open(filename, "wb") as f:
            f.write(save_data)
