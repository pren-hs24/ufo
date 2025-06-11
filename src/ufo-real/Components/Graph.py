# Utility base class for the underlying Graph. Containes all
# the Nodes and Edges that are in a Graph. It's supposed to be
# very adaptive and allow for quick changes and adjustments
# because all the locations need to be measured first.
# 
# Since we don't know how taxing that is different definition
# for the localization of the Nodes would be helpfull.
# 
# General structure of object oriented programming in order
# to make the code more understandable, better structured and
# easier to adapt or fix in the almost certain case something
# breaks.

from Basic import NodeLabel, NodeState, EdgeState

from .RealNode import RealNode
from .Edge import Edge

import numpy as np

class Graph:

    arr_nodes: list[RealNode]
    arr_edges: list[Edge]

    # [Constructor] with the arrays for the nodes and edges
    # - arr_nodes   = (NumPy Array[RealNode]) array of nodes
    # - arr_edges   = (NumPy Array[Edge]) array of corrisponding edges
    def __init__(self, arr_nodes: list[RealNode], arr_edges: list[Edge]):

        # check if input valid
        if not self.__valid_graph(arr_nodes, arr_edges):
            raise ValueError("Graph generation failed. Inputs invalid.")
           
        self.arr_nodes = arr_nodes
        self.arr_edges = arr_edges

    def __str__(self):
        output = "\n--------------\nGraph Content\n--------------\n"
        
        for n in self.arr_nodes:
            output += f"{n}\n"
        
        output += "\n"
        for e in range(len(self.arr_edges)):
            output += f"{self.arr_edges[e]}"
            if not e == len(self.arr_edges) - 1:
                output += ";\n"

        output += ""
        return output

    def __eq__(self, value):
        if isinstance(value, RealNode):
            return self.label == value
        elif isinstance(value, RealNode):
            return self.label == value.label and\
                self.posX == value.posX and\
                self.posY == value.posY
        else:
            return False

    # A helper function that checks if the arrays provide can
    # make a valid Graph. Like both the arrays are actually arrays,
    # all the elements in those arrays are of the type RealNode or
    # Edge and all the Edges end in Nodes that are in the array of
    # Nodes.
    # - arr_nodes   = (NumPy Array[RealNode]) array of nodes
    # - arr_edges   = (NumPy Array[Edge]) array of corrisponding edges
    # - return      = True if everthing is in order.
    def __valid_graph(self, arr_nodes, arr_edges):
        # type testing
        if not isinstance(arr_nodes, list):
            raise ValueError("Graph generation failed. The nodes array was invalid.")
        if not isinstance(arr_edges, list):
            raise ValueError("Graph generation failed. The edges array was invalid.")
        
        for n in arr_nodes:
            if not isinstance(n,RealNode):
                raise ValueError("Graph generation failed. The nodes array contained an invalid node.")
        
        for e in arr_edges:
            if not isinstance(e,Edge) or\
            not np.isin(Edge.getNodes(e)[0],arr_nodes) or\
            not np.isin(Edge.getNodes(e)[1],arr_nodes):
                raise ValueError("Graph generation failed. The edges array contained an invalid edge.")
            
        return True

    
    def getNodes(self) -> list[RealNode]:
        return self.arr_nodes
    
    def getEdges(self) -> list[Edge]:
        return self.arr_edges
    
    def update(self, matching: tuple[str, str]) -> None:
        for label1, label2 in matching:
            for node in self.getNodes():
                if label1 == node.getLabel() or label2 == node.getLabel():
                    node.changeState(NodeState.FREE)
                    break
