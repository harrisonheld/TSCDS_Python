"""Handle the loading and initialization of game sessions."""

from __future__ import annotations

from datetime import datetime
from typing import Optional
import copy
import lzma
import pickle
import random

from tcod import libtcodpy
import tcod

from engine import Engine
from game_map import GameWorld
from helpers import resource_path
from ui.starfield import Starfield
import color
import entity_factories
import input_handlers
import keys
import strings


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
    engine.game_world.boss_pool = [entity_factories.indrix, entity_factories.fume_knight]
    engine.game_world.generate_floor()
    engine.update_visibility()

    engine.message_log.add_message(
        "Artow a Saad of olde Salum, and nou stonden thu at the heigh gate to Brightsheol. Fight or die."
    )
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
    engine.save_path = resource_path(f"saves/{save_file_name}")

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

    def on_render(self, console: tcod.console.Console) -> None:
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
        import glob

        path = resource_path("saves")
        self.save_files = glob.glob(f"{path}/*.sav")

    def on_render(self, console: tcod.console.Console) -> None:

        text = "Select a save file to load."
        if not self.save_files:
            text = "You don't have any saves."

        console.print(
            x=console.width // 2,
            y=console.height // 2 - 5,
            string=text,
            fg=color.menu_text,
            bg=color.black,
            alignment=libtcodpy.CENTER,
        )

        for i, save_file_path in enumerate(self.save_files):

            save_file_name = save_file_path.split("/")[-1]  # extract just the file name
            save_file_name = save_file_name[:-4]  # remove the .sav extension
            letter = chr(ord("a") + i)
            console.print(
                x=console.width // 2,
                y=console.height // 2 - 3 + i,
                string=f"[{letter}] {save_file_name}",
                alignment=libtcodpy.CENTER,
            )

        console.print(
            x=console.width // 2,
            y=console.height - 2,
            string=f"Saves are stored at {resource_path('saves') + '/'}.",
            fg=color.light_grey,
            bg=color.black,
            alignment=libtcodpy.CENTER,
        )

    def ev_keydown(self, event: tcod.event.KeyDown) -> input_handlers.BaseEventHandler | None:

        key = event.sym
        ordinal = key - tcod.event.KeySym.a

        if 0 <= ordinal < len(self.save_files):
            return SaveOptionsHandler(self.save_files[ordinal])

        return MainMenu()


class SaveOptionsHandler(input_handlers.BaseEventHandler):

    def __init__(self, save_path: str):
        self.save_path = save_path

    def on_render(self, console: tcod.console.Console) -> None:
        # options are:
        # load the save or delete the save
        console.print(
            console.width // 2,
            console.height // 2 - 5,
            "Save Options",
            fg=color.menu_text,
            bg=color.black,
            alignment=libtcodpy.CENTER,
        )
        console.print(
            console.width // 2,
            console.height // 2 - 3,
            "[enter] load",
            fg=color.menu_text,
            bg=color.black,
            alignment=libtcodpy.CENTER,
        )
        console.print(
            console.width // 2,
            console.height // 2 - 2,
            "[shift+D] delete",
            fg=color.menu_text,
            bg=color.black,
            alignment=libtcodpy.CENTER,
        )

    def ev_keydown(self, event: tcod.event.KeyDown) -> input_handlers.BaseEventHandler | None:
        key = event.sym
        # load the save
        if key in keys.CONFIRM_KEYS:
            try:
                save_file_name = self.save_path
                save: Engine = load_game(save_file_name)
                return input_handlers.MainGameEventHandler(save)
            except Exception as e:
                message = f"─┤Error Loading Save File├─"
                message += "\n\n" + str(e)
                message += "\n\n" + "Contact the developer at harrydheld@gmail.com."
                return input_handlers.PopupMessage(self, message)
        # delete the save
        elif key == tcod.event.KeySym.d and event.mod & (tcod.event.KMOD_RSHIFT | tcod.event.KMOD_LSHIFT):
            import os

            os.remove(self.save_path)
            return SelectSaveHandler()
        # cancel
        elif key not in keys.MODIFIER_KEYS:
            return SelectSaveHandler()

        return None
