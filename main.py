#!/usr/bin/env python3
import traceback

import tcod

import color
import exceptions
import input_handlers
import setup_game
import sizes


def save_game(handler: input_handlers.BaseEventHandler, filename: str) -> None:
    """If the current event handler has an active Engine then save it."""
    if isinstance(handler, input_handlers.EventHandler):
        handler.engine.save_as(filename)
        print("Game saved.")


def main() -> None:
    tileset = tcod.tileset.load_tilesheet("data/cheepicus12x12.png", 16, 16, tcod.tileset.CHARMAP_CP437)

    handler: input_handlers.BaseEventHandler = setup_game.MainMenu()

    with tcod.context.new(
        columns=sizes.screen_width,
        rows=sizes.screen_height,
        tileset=tileset,
        title="The Stars Came Down Screaming",
        vsync=True,
    ) as context:
        root_console = tcod.console.Console(sizes.screen_width, sizes.screen_height, order="F")
        try:
            while True:
                root_console.clear()
                handler.on_render(console=root_console)
                context.present(root_console)

                try:
                    for event in tcod.event.wait():
                        context.convert_event(event)
                        handler = handler.handle_events(event)
                except exceptions.SaveAndQuitToMainMenu:
                    save_game(handler, "savegame.sav")
                    handler = setup_game.MainMenu()
                except exceptions.StartNewGame:
                    handler = input_handlers.MainGameEventHandler(setup_game.new_game())
                except Exception:  # Handle exceptions in game.
                    traceback.print_exc()  # Print error to stderr.
                    # Then print the error to the message log.
                    if isinstance(handler, input_handlers.EventHandler):
                        handler.engine.message_log.add_message(traceback.format_exc(), color.error)
        except exceptions.QuitWithoutSaving:  # Quit to desktop
            raise
        except SystemExit:  # Save and quit to desktop
            save_game(handler, "savegame.sav")
            raise
        except BaseException:  # Save on any other unexpected exception.
            save_game(handler, "savegame.sav")
            raise


if __name__ == "__main__":
    main()
