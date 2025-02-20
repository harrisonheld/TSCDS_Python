from color import *
from colored_string import ColoredString
from components.base_component import BaseComponent
from components.prefixes.prefix import Prefix


class Innocent(Prefix):
    def get_colored_name(self) -> ColoredString:
        return ColoredString(f"inn{yellow}o{white}cent")

    def get_description(self) -> str:
        return "This creature is unusually benevolent."