from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional, Tuple
import lzma
import pickle

from tcod import libtcodpy
from tcod.console import Console
from tcod.map import compute_fov

from components.illumination import Illumination
from ui.info_block import InfoBlock
from ui.look_block import LookBlock
from ui.message_log import MessageLog
import color
import exceptions
import render_functions
import sizes

if TYPE_CHECKING:
    from entity import Actor, Entity
    from game_map import GameMap, GameWorld


class Engine:
    game_map: GameMap
    game_world: GameWorld

    def __init__(self, player: Actor):
        self.message_log = MessageLog()
        self.info_block = InfoBlock(player)
        self.look_block = LookBlock()
        self.mouse_location = (-1, -1)  # off-screen
        self.player = player
        self.save_path = ""

    def handle_enemy_turns(self) -> None:
        for actor in set(self.game_map.actors) - {self.player}:
            if actor.ai:
                try:
                    actor.ai.perform()
                except exceptions.Impossible:
                    pass  # Ignore impossible action exceptions from AI.

        entities_copy = list(self.game_map.entities)
        for entity in entities_copy:
            for component in entity.components:
                component.on_turn()

    def update_visibility(self) -> None:
        """Computer what is visible to the player"""
        self.game_map.visible[:] = compute_fov(
            self.game_map.tiles["transparent"],
            (self.player.x, self.player.y),
            radius=8,
            algorithm=libtcodpy.FOV_SYMMETRIC_SHADOWCAST,
        )

        # for every entity that has an Illumination component
        for entity in self.game_map.entities:
            if illumination := entity.get_component(Illumination):
                self.game_map.visible |= compute_fov(
                    self.game_map.tiles["transparent"],
                    (entity.x, entity.y),
                    radius=illumination.light_radius,
                    algorithm=libtcodpy.FOV_SYMMETRIC_SHADOWCAST,
                )
        # If a tile is "visible" it should be added to "explored".
        self.game_map.explored |= self.game_map.visible

    def render(self, console: Console) -> None:
        self.game_map.render(console)
        self.info_block.render(
            console,
            self.game_map.width + 1,
            0,
            width=sizes.sidebar_width_including_border,
            height=sizes.info_block_height,
        )
        self.message_log.render(
            console=console,
            x=self.game_map.width + 1,
            y=sizes.info_block_height,
            width=sizes.sidebar_width_including_border,
            height=sizes.screen_height - sizes.info_block_height,
        )
        console.draw_frame(self.game_map.width, 0, 1, self.game_map.height, decoration="│││││││││")
        console.draw_frame(self.game_map.width, 10, sizes.sidebar_width_including_border, 1, decoration="──────├──")
        console.print_box(
            self.game_map.width + 1,
            10,
            sizes.sidebar_width_including_border - 1,
            1,
            "┤Message Log├",
            fg=color.white,
            alignment=libtcodpy.CENTER,
        )
        render_functions.render_names_at_mouse_location(console=console, x=0, y=self.game_map.height - 1, engine=self)

    def save_as(self, filename: str) -> None:
        """Save this Engine instance as a compressed file."""
        save_data = lzma.compress(pickle.dumps(self))
        with open(filename, "wb") as f:
            f.write(save_data)
