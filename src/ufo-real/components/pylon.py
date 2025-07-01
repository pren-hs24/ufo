# -*- coding: utf-8 -*-
"""
# Pylon module:
Utility base class for Pylons. It is supposed to make\n
the code more understandable, well organized and easier to\n
adapt in case something changes. In this case it stores the\n
information of the Pylon in the image to make it more\n
accessable in calculations.
"""

__copyright__ = "Copyright (c) 2025 HSLU PREN Team 2, FS25. All rights reserved."


class Pylon:
    """Pylon repersentation in an image and reallife"""

    REAL_HEIGHT: int = 220  # real height of Pylons messured in mm
    PYLON_COUNTER: int = 1  # unique id for each detected pylon

    xmin: int
    ymin: int
    xmax: int
    ymax: int
    id: int

    # [Constructor] with the values for physical nodes
    # - start     = (RealNode) one of the two connected nodes
    # - end       = (RealNode) second of the two connected nodes
    # (edges are treated als bidirectional)
    # - status    = (EdgeState) reflects the current amount
    #               of knowledge we have of this edge
    def __init__(self, xmin: int, ymin: int, xmax: int, ymax: int):
        self.xmin = xmin
        self.ymin = ymin
        self.xmax = xmax
        self.ymax = ymax
        self.id = Pylon.PYLON_COUNTER

        Pylon.PYLON_COUNTER += 1

    def __str__(self) -> str:
        return (
            f"Pylon Image: {self.id} [({self.xmin},{self.ymin}), "
            + f"({self.xmax},{self.ymax})]"
        )

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, Pylon):
            return False

        return (
            self.xmin == value.xmin
            and self.ymin == value.ymin
            and self.xmax == value.xmax
            and self.ymax == value.ymax
        )

    @property
    def get_xmin(self) -> int:
        """of the visual rectangle get the point fardest to the left"""
        return self.xmin

    @property
    def get_ymin(self) -> int:
        """... of the visual rectangle get the highest point"""
        return self.ymin

    @property
    def get_xmax(self) -> int:
        """... of the visual rectangle get the point fardest to the right"""
        return self.xmax

    @property
    def get_ymax(self) -> int:
        """... of the visual rectangle get the lost lowest point"""
        return self.ymax

    @property
    def get_id(self) -> str:
        """... get the unique name of this pylon"""
        return f"P{str(self.id)}"

    @property
    def get_width(self) -> int:
        """... get the width of the visual rectangle"""
        return self.xmax - self.xmin

    @property
    def get_height(self) -> int:
        """... get the height of the visual rectangle"""
        return self.ymax - self.ymin

    @classmethod
    def get_real_height(cls) -> int:
        """get the actual height of a pylon in mm"""
        return Pylon.REAL_HEIGHT
