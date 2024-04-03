from typing import Tuple

from entity import Item
from ui.look_block import LookBlock


class Upgrade(Item):
    def on_pickup(self) -> None:
        pass

    def on_drop(self) -> None:
        pass


class UpgradeEyeOfBelial(Upgrade):
    def on_pickup(self) -> None:
        LookBlock.set_show_full_detail_mode(True)

    def on_drop(self) -> None:
        LookBlock.set_show_full_detail_mode(False)


class UpgradeHornOfGeddon(Upgrade):
    pass
