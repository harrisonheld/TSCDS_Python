from color import *
from colored_string import ColoredString
from components.base_component import BaseComponent
from components.prefixes.prefix import Prefix


class Cruciformed(Prefix):
    def get_colored_name(self) -> ColoredString:
        return ColoredString(f"{pink}cruciformed")
    
    def get_description(self) -> str:
        return "A living worm, twisted into the shape of a cross, writhes beneath this creature's flesh."