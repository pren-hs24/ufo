# -*- coding: utf-8 -*-
"""Pathfinder interface module"""

__copyright__ = "Copyright (c) 2025 HSLU PREN Team 2, FS25. All rights reserved."

from abc import ABC, abstractmethod

from network.node import Node
from network.network import Network


class IPathfinder(ABC):
    """Pathfinder interface"""

    @abstractmethod
    def find_path(self, network: Network, end: Node) -> list[Node]:
        """
        Find a path in the network from (implicit) START
        to the specified end node

        :param network: The network to search in
        :param end: The end node to search for
        :return: The path from START to end
        """
