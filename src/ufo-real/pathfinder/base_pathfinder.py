# -*- coding: utf-8 -*-
"""Pathfinder interface module"""

__copyright__ = "Copyright (c) 2025 HSLU PREN Team 2, FS25. All rights reserved."

import logging
from abc import ABC

from network.network import Network
from network.node import Node

from .ipathfinder import IPathfinder


class BasePathfinder(IPathfinder, ABC):
    """Pathfinder interface"""

    def __init__(self) -> None:
        super().__init__()
        self._logger = logging.getLogger(self.__class__.__name__)

    def _validate(self, network: Network, start: Node, end: Node) -> None:
        """Validate the network and end node"""
        if start not in network.nodes:
            raise ValueError("Start node not found")
        if end not in network.end:
            raise ValueError("End node not found")
