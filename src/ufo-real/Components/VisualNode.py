# Utility base class for Nodes in order to make the code
# more understandable, better structured and easier to
# adapt and fix

import numpy as np

class VisualNode:

    pos_x: int
    pos_y: int
    width: int
    height: int
    label: str

    # [Constructor] with the values for the visual representation
    # of nodes in an image
    # - label     = (str) the label by which it is identified
    # - width     = (int) horizontal position of the node in px
    # - height    = (int) vertical position of the node in px
    # (center (0,0) is left upper corner)
    def __init__(self, label: str, pos_x: int, pos_y: int, width: int, height: int) -> "VisualNode":
        self.label = label
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.width = width
        self.height = height

    @classmethod
    def position_only(cls, label: str, pos_x: int, pos_y: int) -> "VisualNode":
        return cls(label, pos_x, pos_y, 1, 1)

    def __str__(self) -> str:
        return f"VisualNode: {self.label}({self.width}px,{self.height}px)"
    
    def __eq__(self, other) -> bool:
        if isinstance(other, str):
            return self.label == other
        elif isinstance(other, VisualNode):
            return self.label == other.label and self.width == other.width and self.height == other.height
        else:
            return False

    def getLabel(self) -> str:
        return self.label
    
    def get_pos_x(self) -> int:
        return self.pos_x
    
    def get_pos_y(self) -> int:
        return self.pos_y
    
    def get_width(self) -> int:
        return self.width
    
    def get_height(self) -> int:
        return self.height
    
    def get_coordinates(self) -> tuple[int, int]:
        return (self.pos_x, self.pos_y)
    
    def get_dimensions(self) -> tuple[int, int]:
        return (self.width, self.height)
    
    def getDistance(node1: "VisualNode", node2: "VisualNode") -> float:
        return np.sqrt(np.square(node1.get_pos_x() - node2.get_pos_x())\
                       + np.square(node1.get_pos_y() - node2.get_pos_y()))