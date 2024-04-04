"""Handle the loading and initialization of game sessions."""
from __future__ import annotations

from typing import Optional
import copy
import lzma
import pickle
import traceback

from PIL import Image  # type: ignore
import tcod
import strings

from engine import Engine
from game_map import GameWorld
import color
import entity_factories
import input_handlers

from tcod import libtcodpy

import random

# Load the background image.  Pillow returns an object convertable into a NumPy array.
background_image = Image.open("data/menu_background.png")


def new_game() -> Engine:
    """Return a brand new game session as an Engine instance."""
    map_width = 80
    map_height = 43

    room_max_size = 10
    room_min_size = 6
    max_rooms = 30

    player = copy.deepcopy(entity_factories.player)

    engine = Engine(player=player)

    engine.game_world = GameWorld(
        engine=engine,
        max_rooms=max_rooms,
        room_min_size=room_min_size,
        room_max_size=room_max_size,
        map_width=map_width,
        map_height=map_height,
    )

    engine.game_world.treasure_pool = [
        entity_factories.eye_of_belial,
        entity_factories.dagashas_spur,
    ]
    engine.game_world.generate_floor()
    engine.update_fov()

    engine.message_log.add_message("Artow a Saad of olde Salum, and nou stonden thu at the heigh gate to Brightsheol. Fight or die.")
    engine.message_log.add_message("Press '?' for help.", color.welcome_text)

    dagger = copy.deepcopy(entity_factories.dagger)
    leather_armor = copy.deepcopy(entity_factories.leather_armor)

    player.inventory.add(dagger, add_message=False)
    player.inventory.add(leather_armor, add_message=False)

    player.equipment.toggle_equip(dagger, add_message=False)
    player.equipment.toggle_equip(leather_armor, add_message=False)

    return engine


def load_game(filename: str) -> Engine:
    """Load an Engine instance from a file."""
    with open(filename, "rb") as f:
        engine = pickle.loads(lzma.decompress(f.read()))
    assert isinstance(engine, Engine)
    return engine


class MainMenu(input_handlers.BaseEventHandler):
    """Handle the main menu rendering and input."""
    musing = random.choice(strings.musings)

    def on_render(self, console: tcod.Console) -> None:
        """Render the main menu."""

        # console.draw_semigraphics(background_image, 0, 0)
        console.print(0, 0, strings.eye_art, color.main_menu_background)

        console.print(
            console.width // 2,
            console.height // 2 - 5,
            "The Stars Came Down Screaming",
            fg=color.main_menu_title,
            bg=color.black,
            alignment=libtcodpy.CENTER,
        )
        console.print(
            console.width // 2,
            console.height // 2 - 4,
            self.musing,
            fg=color.main_menu_subtitle,
            bg=color.black,
            alignment=libtcodpy.CENTER,
        )
        console.print(
            console.width // 2,
            console.height - 2,
            "By Harrison Held",
            fg=color.main_menu_title,
            bg=color.black,
            alignment=libtcodpy.CENTER,
        )

        menu_width = 24
        for i, text in enumerate(["[n] New game", "[c] Continue last game", "[q] Quit"]):
            console.print(
                console.width // 2,
                console.height // 2 - 2 + i,
                text.ljust(menu_width),
                fg=color.menu_text,
                bg=color.black,
                alignment=libtcodpy.CENTER,
                bg_blend=libtcodpy.BKGND_ALPHA(64),
            )

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[input_handlers.BaseEventHandler]:
        if event.sym in (tcod.event.KeySym.q, tcod.event.KeySym.ESCAPE):
            raise SystemExit()
        elif event.sym == tcod.event.KeySym.c:
            try:
                return input_handlers.MainGameEventHandler(load_game("savegame.sav"))
            except FileNotFoundError:
                return input_handlers.PopupMessage(self, "No saved game to load.")
            except Exception as exc:
                traceback.print_exc()  # Print to stderr.
                return input_handlers.PopupMessage(self, f"Failed to load save:\n{exc}")
        elif event.sym == tcod.event.KeySym.n:
            return input_handlers.MainGameEventHandler(new_game())

        return None
