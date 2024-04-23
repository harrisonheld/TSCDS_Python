from components.base_component import BaseComponent


class Illumination(BaseComponent):
    """The actor with this component is immune to fire damage."""
    def __init__(self, light_radius: int):
        self.light_radius = light_radius
