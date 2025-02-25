from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional, Tuple, Type, TypeVar, Union
import copy
import math

from components.ai.ai_base import AIBase
from components.base_component import BaseComponent
from render_order import RenderOrder
from tables.grab_bag import GrabBag

if TYPE_CHECKING:
    from components.consumable import Consumable
    from components.equipment import Equipment
    from components.equippable import Equippable
    from components.fighter import Fighter
    from components.inventory import Inventory
    from components.level import Level
    from game_map import GameMap

T = TypeVar("T", bound="BaseComponent")
E = TypeVar("E", bound="Entity")


class Entity:
    """
    A generic object to represent players, enemies, items, etc.
    """

    parent: Union[GameMap, Inventory]

    def __init__(
        self,
        parent: Optional[GameMap] = None,
        x: int = 0,
        y: int = 0,
        char: str = "?",
        color: Tuple[int, int, int] = (255, 255, 255),
        name: str = "<Unnamed>",
        description: str = "<No Description>",
        blocks_movement: bool = False,
        render_order: RenderOrder = RenderOrder.CORPSE,
        components: List[BaseComponent] = [],
    ):
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.name = name
        self.description = description
        self.blocks_movement = blocks_movement
        self.render_order = render_order
        self.components: List[BaseComponent] = components
        if components is None:
            self.components = []
        for component in self.components:
            component.parent = self
        if parent:
            # If parent isn't provided now then it will be set later.
            self.parent = parent
            parent.entities.add(self)

    @property
    def gamemap(self) -> GameMap:
        return self.parent.gamemap

    @property
    def xy(self) -> Tuple[int, int]:
        """Return the (x, y) coordinates as a tuple."""
        return self.x, self.y

    @xy.setter
    def xy(self, value: Tuple[int, int]):
        """Set the (x, y) coordinates. WARNING: This will NOT call before_move or after_move methods of any components."""
        self.x, self.y = value

    def get_component(self, component_type: Type[T]) -> Optional[T]:
        for component in self.components:
            if isinstance(component, component_type):
                return component
        return None

    def has_component(self, component_type: Type[T]) -> bool:
        return any(isinstance(c, component_type) for c in self.components)

    def spawn(self: E, gamemap: GameMap, x: int, y: int) -> E:
        """Spawn a copy of this instance at the given location."""
        clone = copy.deepcopy(self)
        clone.x = x
        clone.y = y
        clone.parent = gamemap
        gamemap.entities.add(clone)
        return clone

    def place(self, x: int, y: int, gamemap: Optional[GameMap] = None) -> None:
        """Place this entitiy at a new location.  Handles moving across GameMaps."""
        self.x = x
        self.y = y
        if gamemap:
            if hasattr(self, "parent"):  # Possibly uninitialized.
                if self.parent is self.gamemap:
                    try:
                        self.gamemap.entities.remove(self)
                    except KeyError:
                        # probably not an issue - just means it wasn't on the map
                        pass
            self.parent = gamemap
            gamemap.entities.add(self)

    def distance(self, x: int, y: int) -> float:
        """
        Return the distance between the current entity and the given (x, y) coordinate.
        """
        return math.sqrt((x - self.x) ** 2 + (y - self.y) ** 2)

    def move(self, dx: int, dy: int) -> None:
        # Move the entity by a given amount
        for component in self.components:
            component.before_move()
        self.x += dx
        self.y += dy

    def move_to(self, x: int, y: int) -> None:
        # Move the entity to a new location
        for component in self.components:
            component.before_move()
        self.x = x
        self.y = y


class Actor(Entity):
    def __init__(
        self,
        *,
        x: int = 0,
        y: int = 0,
        char: str = "?",
        color: Tuple[int, int, int] = (255, 255, 255),
        name: str = "<Unnamed>",
        description: str = "<No Description>",
        ai_cls: Type[AIBase],
        equipment: Equipment,
        fighter: Fighter,
        inventory: Inventory,
        level: Level,
        components: List[BaseComponent] = [],
        grab_bag: GrabBag[Item] = GrabBag([]),
    ):
        super().__init__(
            x=x,
            y=y,
            char=char,
            color=color,
            name=name,
            description=description,
            blocks_movement=True,
            render_order=RenderOrder.ACTOR,
            components=components,
        )

        self.ai: Optional[AIBase] = ai_cls(self)

        self.equipment: Equipment = equipment
        self.equipment.parent = self

        self.fighter = fighter
        self.fighter.parent = self

        self.inventory = inventory
        self.inventory.parent = self

        self.level = level
        self.level.parent = self

        self.grab_bag = grab_bag

    @property
    def is_alive(self) -> bool:
        """Returns True as long as the actor has HP."""
        return self.fighter.hp > 0

    def spawn(self, gamemap: GameMap, x: int, y: int) -> Actor:
        """Spawn a copy of this instance at the given location."""
        from actions.equip_to_first_possible_slot_action import EquipToFirstPossibleSlotAction

        clone = super().spawn(gamemap, x, y)
        stuff: List[Item] = clone.grab_bag.roll_batch()
        for entry in stuff:
            item = copy.deepcopy(entry)
            if item.equippable:
                EquipToFirstPossibleSlotAction(clone, item).perform()
            else:
                clone.inventory.add(item)

        return clone


class Item(Entity):
    def __init__(
        self,
        *,
        x: int = 0,
        y: int = 0,
        char: str = "?",
        color: Tuple[int, int, int] = (255, 255, 255),
        name: str = "<Unnamed>",
        description: str = "<No Description>",
        consumable: Optional[Consumable] = None,
        equippable: Optional[Equippable] = None,
        components: List[BaseComponent] = [],
    ):
        super().__init__(
            x=x,
            y=y,
            char=char,
            color=color,
            name=name,
            description=description,
            blocks_movement=False,
            render_order=RenderOrder.ITEM,
            components=components,
        )

        self.consumable = consumable

        if self.consumable:
            self.consumable.parent = self

        self.equippable = equippable

        if self.equippable:
            self.equippable.parent = self
