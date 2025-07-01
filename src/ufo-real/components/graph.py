# -*- coding: utf-8 -*-
"""Graph class"""

__copyright__ = "Copyright (c) 2025 HSLU PREN Team 2, FS25. All rights reserved."

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

from .edge import Edge
from .real_node import RealNode


class Graph:
    """visual representation of a graph"""

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

    def __str__(self) -> str:
        output: str = "\n--------------\nGraph Content\n--------------\n"

        for n in self.arr_nodes:
            output += f"{n}\n"

        output += "\n"
        for e in self.arr_edges:
            output += f"{e}"
            if not e == self.arr_edges[-1]:
                output += ";\n"

        output += ""
        return output

    def __eq__(self, value: object) -> bool:
        if isinstance(value, list):
            if not value:
                return not self.arr_nodes or not self.arr_edges
            if isinstance(value[0], RealNode):
                return self.arr_nodes == value
            if isinstance(value[0], Edge):
                return self.arr_edges == value
        elif isinstance(value, Graph):
            return (
                self.arr_nodes == value.arr_nodes and self.arr_edges == value.arr_edges
            )
        return False

    # A helper function that checks if the arrays provide can
    # make a valid Graph. Like both the arrays are actually arrays,
    # all the elements in those arrays are of the type RealNode or
    # Edge and all the Edges end in Nodes that are in the array of
    # Nodes.
    # - arr_nodes   = (list[RealNode]) array of nodes
    # - arr_edges   = (list[Edge]) array of corresponding edges
    # - return      = True if everthing is in order.
    def __valid_graph(self, arr_nodes: list[RealNode], arr_edges: list[Edge]) -> bool:
        for e in arr_edges:
            if e.get_nodes[0] not in arr_nodes or e.get_nodes[1] not in arr_nodes:
                raise ValueError(
                    "Graph generation failed. The edges array contained an invalid edge."
                )

        return True

    @property
    def get_nodes(self) -> list[RealNode]:
        """returns a list of the nodes"""
        return self.arr_nodes

    def get_node_by_str(self, name: str) -> RealNode:
        """
        Looks at all the nodes in the graph and returns the first\n
        ``RealNode`` matching with the given ``String``. Will raise\n
        ``ValueError`` if there is no matching node.
        """
        nodes: list[RealNode] = self.arr_nodes
        for node in nodes:
            if node == name:
                return node
        raise ValueError(f"{name} not found")

    @property
    def get_edges(self) -> list[Edge]:
        """returns a list of the edges"""
        return self.arr_edges

    def update(self, matching: tuple[str, str]) -> None:
        """sets all the edges from the matching to available"""
        for match in matching:
            for node in self.arr_nodes:
                if node.get_label in match:
                    node.is_available()
                    break
