from enum import Enum
from typing import NamedTuple

class RGB(NamedTuple):
    r: int
    g: int
    b: int
    
class ColourTypes(Enum):
    BLACK = RGB(0, 0, 0)
    DARK_GREY = RGB(100, 100, 100)
    LIGHT_GREY = RGB(200, 200, 200)
    LIGHT = RGB(255, 255, 255)
    RED = RGB(255, 0, 0)
    GREEN = RGB(0, 255, 0)
    BLUE = RGB(0, 0, 255)
    YELLOW = RGB(255, 255, 0)
    ORANGE = RGB(255, 165, 0)

    def __eq__(self, value: object) -> bool:
        if isinstance(value, str):
            return ColourTypes.name == value
        else:
            return super().__eq__(value)

class Colour():

    @classmethod
    def rgb(cls, name: str) -> tuple[int, int, int]:
        """
        Get the corresponding ``RGB-Values`` as\n
        ``(R: int, G: int, B: int)`` for the named colour.
        """
        colour: ColourTypes = ColourTypes[name.upper()]
        r: int = colour.value.r
        g: int = colour.value.g
        b: int = colour.value.b
        return (r, g, b)

    @classmethod
    def bgr(cls, name: str) -> tuple[int, int, int]:
        """
        Get the corresponding ``BGR-Values`` as\n
        ``(B: int, G: int, R: int)`` for the named colour.
        """
        r, g, b = cls.rgb(name)
        return (b, g, r)
    
    @classmethod
    def hex(cls, name: str) -> str:
        """
        Get the corresponding ``Hex-Code`` as\n
        16-Bit ``#XXXXXX`` for the named colour.
        """
        r, g, b = cls.rgb(name)
        return f"#{r:02X}{g:02X}{b:02X}"