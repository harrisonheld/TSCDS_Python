from typing import Optional

import tcod

from actions.bump_action import BumpAction
from actions.pickup_action import PickupAction
from actions.wait_action import WaitAction
from handlers.action_or_handler import ActionOrHandler
from handlers.event_handler import EventHandler
import actions.take_stairs_action
import color
import keys


class MainGameEventHandler(EventHandler):
    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[ActionOrHandler]:
        key = event.sym
        modifier = event.mod

        player = self.engine.player

        if key == tcod.event.KeySym.PERIOD and modifier & (tcod.event.KMOD_LSHIFT | tcod.event.KMOD_RSHIFT):
            # TODO: remove this cheat lol
            player.x, player.y = self.engine.game_map.downstairs_location
            return actions.take_stairs_action.TakeStairsAction(player)

        if key in keys.MOVE_KEYS:
            dx, dy = keys.MOVE_KEYS[key]
            return BumpAction(player, dx, dy)
        elif key in keys.WAIT_KEYS:
            return WaitAction(player)
        elif key in keys.BINDABLE_KEYS:
            if key not in player.inventory.binds:
                self.engine.message_log.add_message(f"{key.name} is unbound.", color.impossible)
                return None

            # Retrieve the item bound to the key
            item = player.inventory.binds[key]
            assert item.consumable is not None
            return item.consumable.get_action(player)

        elif key == tcod.event.KeySym.ESCAPE:
            from handlers.pause_viewer import PauseViewer

            return PauseViewer(self.engine)
        elif key == tcod.event.KeySym.m:
            from handlers.history_viewer import HistoryViewer

            return HistoryViewer(self.engine)
        elif key == tcod.event.KeySym.SLASH:
            from handlers.help_viewer import HelpViewer

            return HelpViewer(self.engine)

        elif key == tcod.event.KeySym.g:
            return PickupAction(player)
        elif key == tcod.event.KeySym.i:
            from handlers.inventory_activate_handler import InventoryActivateHandler

            return InventoryActivateHandler(self.engine)
        elif key == tcod.event.KeySym.b:
            from handlers.inventory_binds_handler import InventoryBindsHandler

            return InventoryBindsHandler(self.engine)
        elif key == tcod.event.KeySym.d:
            from handlers.inventory_drop_handler import InventoryDropHandler

            return InventoryDropHandler(self.engine)
        elif key == tcod.event.KeySym.c:
            from handlers.character_screen_event_handler import CharacterScreenEventHandler

            return CharacterScreenEventHandler(self.engine)
        elif key == tcod.event.KeySym.l:
            from handlers.look_handler import LookHandler

            return LookHandler(self.engine)
        elif key == tcod.event.KeySym.e:
            from handlers.equipment_screen import EquipmentScreen

            return EquipmentScreen(self.engine)

        # No valid key was pressed
        return None
