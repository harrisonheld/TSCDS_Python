#!/usr/bin/env python3
import time
import traceback

import tcod

from helpers import resource_path
import color
import exceptions
import handlers.base_event_handler as input_handlers
import handlers.event_handler
import handlers.main_game_event_handler
import setup_game
import sizes


def save_game(handler: input_handlers.BaseEventHandler) -> None:
    """If the current event handler has an active Engine then save it."""
    if isinstance(handler, handlers.event_handler.EventHandler):
        handler.engine.save_as(handler.engine.save_path)
        print("Game saved.")


def main() -> None:
    font_path = resource_path("data/cheepicus12x12.png")
    tileset = tcod.tileset.load_tilesheet(font_path, 16, 16, tcod.tileset.CHARMAP_CP437)

    target_fps = 60
    target_delta_time = 1 / target_fps
    delta_time = 0.0

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
                frame_time_start = time.perf_counter()

                # rendering
                root_console.clear(bg=color.black)
                handler.on_render(console=root_console, delta_time=delta_time)
                context.present(root_console, integer_scaling=True)

                # handling input
                try:
                    for event in tcod.event.get():
                        context.convert_event(event)
                        handler = handler.handle_events(event)
                        handler.gain_focus()
                except exceptions.SaveAndQuitToMainMenu:
                    save_game(handler)
                    handler = setup_game.MainMenu()
                except exceptions.QuitToMainMenu:
                    handler = setup_game.MainMenu()
                except exceptions.StartNewGame:
                    handler = handlers.main_game_event_handler.MainGameEventHandler(setup_game.new_game())
                except Exception:  # Handle exceptions in game.
                    traceback.print_exc()  # Print error to stderr.
                    # Then print the error to the message log.
                    if isinstance(handler, handlers.event_handler.EventHandler):
                        handler.engine.message_log.add_message(traceback.format_exc(), color.error)

                frame_time_end = time.perf_counter()
                delta_time = frame_time_start - frame_time_end
                if delta_time < target_delta_time:
                    time.sleep(target_delta_time - delta_time)
                    delta_time = target_delta_time

        except exceptions.QuitWithoutSaving:  # Quit to desktop
            raise
        except SystemExit:  # Save and quit to desktop
            save_game(handler)
            raise
        except BaseException:  # Save on any other unexpected exception.
            save_game(handler)
            raise


if __name__ == "__main__":
    main()
