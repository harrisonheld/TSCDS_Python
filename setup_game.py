"""Handle the loading and initialization of game sessions."""
from __future__ import annotations

from datetime import datetime
from typing import Optional
import copy
import lzma
import pickle
import traceback

from PIL import Image  # type: ignore
import tcod
from tcod.event import T

import strings

from engine import Engine
from game_map import GameWorld
import color
import entity_factories
import input_handlers

from tcod import libtcodpy

import random

from ui.starfield import Starfield

# Load the background image.  Pillow returns an object convertable into a NumPy array.
background_image = Image.open("data/menu_background.png")


def new_game() -> Engine:
    """Return a brand new game session as an Engine instance."""
    player = copy.deepcopy(entity_factories.player)

    engine = Engine(player=player)

    engine.game_world = GameWorld(engine=engine)

    engine.game_world.treasure_pool = [
        entity_factories.eye_of_belial,
        entity_factories.dagashas_spur,
        entity_factories.max_health_potion,
        entity_factories.cracked_red_eye_orb,
        entity_factories.cracked_blue_eye_orb,
    ]
    engine.game_world.boss_pool = [
        entity_factories.indrix,
        entity_factories.fume_knight
    ]
    engine.game_world.generate_floor()
    engine.update_visibility()

    engine.message_log.add_message("Artow a Saad of olde Salum, and nou stonden thu at the heigh gate to Brightsheol. Fight or die.")
    engine.message_log.add_message("Press '?' for help.", color.welcome_text)

    dagger = copy.deepcopy(entity_factories.dagger)
    leather_armor = copy.deepcopy(entity_factories.leather_armor)

    player.inventory.add(dagger, add_message=False)
    player.inventory.add(leather_armor, add_message=False)

    player.equipment.toggle_equip(dagger, add_message=False)
    player.equipment.toggle_equip(leather_armor, add_message=False)

    current_time = datetime.now()
    timestamp = current_time.strftime("%Y-%m-%d_%H-%M-%S")
    save_file_name = f"save_{timestamp}.sav"
    engine.save_path = f"saves/{save_file_name}"

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
    starfield = Starfield()

    def on_render(self, console: tcod.Console) -> None:
        """Render the main menu."""
        self.starfield.render(console, console.width, console.height)

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
        for i, text in enumerate(["[n] new game", "[c] continue game", "[q] quit"]):
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
        if event.sym == tcod.event.KeySym.q:
            raise SystemExit()
        elif event.sym == tcod.event.KeySym.c:
            return SelectSaveHandler()
        elif event.sym == tcod.event.KeySym.n:
            return input_handlers.MainGameEventHandler(new_game())

        return None


class SelectSaveHandler(input_handlers.BaseEventHandler):

    def __init__(self):
        import os
        import glob

        self.save_files = glob.glob("saves/*.sav")

    def on_render(self, console: tcod.Console) -> None:
        console.print(
            console.width // 2,
            console.height // 2 - 5,
            "Select a save file to load",
            fg=color.menu_text,
            bg=color.black,
            alignment=libtcodpy.CENTER,
        )

        for i, save_file_name in enumerate(self.save_files):
            console.print(
                console.width // 2,
                console.height // 2 - 4 + i,
                f"[{chr(tcod.event.KeySym.a + i)}] {save_file_name}",
                fg=color.menu_text,
                bg=color.black,
                alignment=libtcodpy.CENTER,
                bg_blend=libtcodpy.BKGND_ALPHA(64),
            )

    def ev_keydown(self, event: tcod.event.KeyDown) -> input_handlers.BaseEventHandler | None:

        key = event.sym
        ordinal = key - tcod.event.KeySym.a

        if 0 <= ordinal < len(self.save_files):
            try:
                save_file_name = self.save_files[ordinal]
                save: Engine = load_game(save_file_name)
                return input_handlers.MainGameEventHandler(save)
            except Exception as e:
                message = f"─┤Error Loading Save File├─"
                message += "\n\n" + str(e)
                message += "\n\n" + "Contact the developer at harrydheld@gmail.com."
                return input_handlers.PopupMessage(self, message)

        return MainMenu()
