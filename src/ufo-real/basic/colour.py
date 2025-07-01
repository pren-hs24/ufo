# -*- coding: utf-8 -*-
"""Colour module"""

__copyright__ = "Copyright (c) 2025 HSLU PREN Team 2, FS25. All rights reserved."

from enum import Enum
from typing import NamedTuple


class RGB(NamedTuple):
    """clear addressable RGB-Tuple"""

    r: int
    g: int
    b: int


class ColourTypes(Enum):
    """pre-defined colours to chose from"""

    BLACK = RGB(0, 0, 0)
    DARK_GREY = RGB(100, 100, 100)
    LIGHT_GREY = RGB(200, 200, 200)
    LIGHT = RGB(255, 255, 255)
    RED = RGB(255, 0, 0)
    GREEN = RGB(0, 255, 0)
    BLUE = RGB(0, 0, 255)
    YELLOW = RGB(255, 255, 0)
    ORANGE = RGB(255, 165, 0)
    DUSTY_STEEL_BLUE = RGB(87, 120, 164)
    WARM_ORANGE = RGB(228, 148, 68)
    SOFT_CORAL_RED = RGB(209, 97, 93)
    MINTY_TEAL = RGB(133, 182, 178)
    OLIVE_GREEN = RGB(106, 159, 88)
    GOLDEN_SAND = RGB(231, 202, 96)
    DUSTY_MAUVE = RGB(168, 124, 159)
    SOFT_PINK_LAVENDER = RGB(241, 162, 169)
    WARM_TAUPE = RGB(150, 118, 98)
    LIGHT_WARM_GRAY = RGB(184, 176, 172)

    def __eq__(self, value: object) -> bool:
        if isinstance(value, str):
            return self.name == value

        return super().__eq__(value)


class Colour:
    """Colours in various needed formats"""

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
