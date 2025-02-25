from typing import Optional

import tcod

from actions.bump_action import BumpAction
from actions.pickup_action import PickupAction
from actions.wait_action import WaitAction
from handlers.action_or_handler import ActionOrHandler
from handlers.event_handler import EventHandler
from handlers.get_handler import GetHandler
import actions.ranged_attack_action
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
            items = self.engine.game_map.get_items_at_location(*self.engine.player.xy)
            if len(items) == 0:
                self.engine.message_log.add_message("There is nothing here to pick up.", color.impossible)
                return None
            elif len(items) == 1:
                return PickupAction(player, items[0])
            return GetHandler(self.engine)
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
            from handlers.character_sheet_screen import CharacterSheetScreen

            return CharacterSheetScreen(self.engine)
        elif key == tcod.event.KeySym.l:
            from handlers.look_handler import LookHandler

            return LookHandler(self.engine)
        elif key == tcod.event.KeySym.e:
            from handlers.equipment_screen import EquipmentScreen

            return EquipmentScreen(self.engine)
        elif key == tcod.event.KeySym.z:
            from handlers.debug.debug_menu import DebugMenu

            return DebugMenu(self.engine)
        elif key == tcod.event.KeySym.f:
            from actions.ranged_attack_action import RangedAttackAction
            from handlers.select_actor_handler import SelectActorHandler

            return SelectActorHandler(self.engine, lambda chosen_target: RangedAttackAction(player, chosen_target))

        # No valid key was pressed
        return None
