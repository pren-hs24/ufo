# Utility base class for Nodes in order to make the code
# more understandable, better structured and easier to
# adapt and fix

from Basic import NodeLabel, NodeState

class RealNode:

    REAL_RADIUS: int = 30 # expected radius of a Node on the Graph in mm

    posX: int
    posY: int
    label: NodeLabel
    state: NodeState

    # [Constructor] with the values for physical nodes
    # - label     = (str) the label by which it is identified
    # - posX      = (int) horizontal position of the node in mm
    # - posY      = (int) vertical position of the node in mm
    # (center (0,0) is left upper corner)
    def __init__(self, label: NodeLabel, posX: int, posY: int):
        if not isinstance(label, NodeLabel):
            raise ValueError("Node generation failed. Label invalid.")
        
        self.label = label
        self.state = NodeState.UNKNOWN
        self.posX = posX
        self.posY = posY

    def __str__(self) -> str:
        return f"Node: {self.label.name}({self.posX}mm,{self.posY}mm) -> {self.state.name}"
    
    def __eq__(self, other) -> bool:
        if isinstance(other, RealNode):
            return self.label == other.label and\
                self.posX == other.posX and\
                self.posY == other.posY
        elif isinstance(other, str):
            return self.label.name == other
        else:
            return False

    def getLabel(self) -> str:
        return self.label.name
    
    def setLabel(self, label: NodeLabel) -> None:
        self.label = label
    
    def getPosX(self) -> int:
        return self.posX
    
    def setPosX(self, posX: int) -> None:
        self.posX = posX
    
    def getPosY(self) -> int:
        return self.posY
    
    def setPosY(self, posY: int) -> None:
        self.posY = posY

    def get_coordinates(self) -> tuple[int, int]:
        return (self.posX, self.posY)

    def get_real_radius() -> int:
        return RealNode.REAL_RADIUS
    
    def changePosition(self, posX: int, posY: int) -> None:
        self.__setPosX(posX)
        self.__setPosY(posY)

    def changeState(self, new_state: NodeState) -> None:
        self.state = new_state