from typing import Tuple

from engine import Engine
from entity import Item, Actor
from ui.look_block import LookBlock


class Upgrade(Item):
    def on_pickup(self, actor: Actor) -> None:
        pass

    def on_drop(self, actor: Actor) -> None:
        pass


class UpgradeEyeOfBelial(Upgrade):
    def on_pickup(self, actor: Actor) -> None:
        self.gamemap.engine.look_block.set_show_full_detail_mode(True)

    def on_drop(self, actor: Actor) -> None:
        self.gamemap.engine.look_block.set_show_full_detail_mode(False)


class UpgradeCrackedRedEyeOrb(Upgrade):
    def on_pickup(self, actor: Actor) -> None:
        actor.fighter.base_power += 1

    def on_drop(self, actor: Actor) -> None:
        actor.fighter.base_power -= 1


class UpgradeCrackedBlueEyeOrb(Upgrade):
    def on_pickup(self, actor: Actor) -> None:
        actor.fighter.base_defense += 1

    def on_drop(self, actor: Actor) -> None:
        actor.fighter.base_defense -= 1


class UpgradeDagashasSpur(Upgrade):
    pass
