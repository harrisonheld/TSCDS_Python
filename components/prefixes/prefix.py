from colored_string import ColoredString
from components.base_component import BaseComponent


class Prefix(BaseComponent):
    def get_colored_name(self) -> ColoredString:
        raise NotImplementedError()
    
    def get_uncolored_name(self) -> str:
        return self.get_colored_name().uncolored()

    def get_description(self) -> str:
        raise NotImplementedError()