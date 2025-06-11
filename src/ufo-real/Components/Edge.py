# Utility base class for Edges. It is supposed to make
# the code more understandable, well organized and easier to
# adapt in case something changes

from Basic import EdgeState
from .RealNode import RealNode

class Edge:

    start: RealNode # start-node
    end: RealNode # end-node
    status: EdgeState # state of the edge

    # [Constructor] with the values for physical nodes
    # - start     = (RealNode) one of the two connected nodes
    # - end       = (RealNode) second of the two connected nodes
    # (edges are treated als bidirectional)
    # - status    = (EdgeState) reflects the current amount
    #               of knowledge we have of this edge
    def __init__(self, start: RealNode, end: RealNode, status: EdgeState):
        if isinstance(start,RealNode) and isinstance(end,RealNode) and isinstance(status,EdgeState):
            self.start = start
            self.end = end
            self.status = status
        else:
            raise ValueError("Edge generation failed. Invalid types where provided.")
    
    def __str__(self) -> str:
        return f"Edge: ({self.start.getLabel()},{self.end.getLabel()}) {self.status.name}"
    
    def __eq__(self, value) -> bool:
        if not isinstance(value, Edge):
            return False
        
        return (self.start == value.start and self.end == value.end) or\
                (self.start == value.end and self.end == value.start)

    def getNodes(self) -> tuple[RealNode, RealNode]:
        return (self.start,self.end)
    
    def getStatus(self) -> str:
        return self.status.name
    
    def changeStatus(self, newStatus: EdgeState) -> None:
        self.status = newStatus