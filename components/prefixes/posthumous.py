from color import *
from colored_string import ColoredString
from components.base_component import BaseComponent
from components.prefixes.prefix import Prefix


class Posthumous(Prefix):
    def get_colored_name(self) -> ColoredString:
        return ColoredString(f"{dark_grey}posthumous")

    def get_description(self) -> str:
        return "This creature's mind has died, but the body roams."