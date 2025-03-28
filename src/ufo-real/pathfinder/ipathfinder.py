# -*- coding: utf-8 -*-
"""Pathfinder interface module"""

__copyright__ = "Copyright (c) 2025 HSLU PREN Team 2, FS25. All rights reserved."

from abc import ABC, abstractmethod

from network.node import Node
from network.network import Network


class IPathfinder(ABC):
    """Pathfinder interface"""

    @abstractmethod
    def find_path(self, network: Network, start: Node, end: Node) -> list[Node]:
        """
        Find a path in the network from the specified start node
        to the specified end node

        :param network: The network to search in
        :param start: The start node to search from
        :param end: The end node to search for
        :return: The path from start to end
        """
