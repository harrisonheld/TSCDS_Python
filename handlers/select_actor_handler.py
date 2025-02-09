from typing import Callable, Optional, Tuple

from actions.action import Action
from engine import Engine
from entity import Actor
from handlers.select_index_handler import SelectIndexHandler
import color


class SelectActorHandler(SelectIndexHandler):
    """Handles targeting a single enemy. Only the enemy selected will be affected."""

    def __init__(self, engine: Engine, callback: Callable[[Actor], Optional[Action]]):
        super().__init__(engine)

        self.callback = callback

        actors = list(self.engine.game_map.actors)
        # remove non-visible actors
        actors = [actor for actor in actors if self.engine.game_map.visible[actor.x, actor.y]]
        # set cursor pos to 2nd closest visible actor - the first is the player
        if len(actors) >= 2:
            actors.sort(key=lambda actor: actor.distance(*self.engine.mouse_location))
            self.engine.mouse_location = actors[1].xy


    def on_index_selected(self, x: int, y: int) -> Optional[Action]:
        actor = self.engine.game_map.get_actor_at_location(x, y)
        if not actor:
            self.engine.message_log.add_message("There is no target at that location.", color.impossible)
            return None
        return self.callback(actor)
