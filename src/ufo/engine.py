# -*- coding: utf-8 -*-
"""UFO Engine"""

__copyright__ = "Copyright (c) 2025 HSLU PREN Team 2, FS25. All rights reserved."

from typing import Callable

from algorithms.base_algorithm import BaseAlgorithm
from algorithms.road_sense import RoadSenseAlgorithm
from uart.sender import UARTSender
from uart.receiver import UARTReceiver
from network.network import Network


class Engine:
    """UFO Engine"""

    def __init__(
        self,
        sender: UARTSender,
        receiver: UARTReceiver,
        network_provider: Callable[[], Network],
    ) -> None:
        self._sender = sender
        self._receiver = receiver
        self._network_provider = network_provider
        self._algorithm = self._create_algorithm(RoadSenseAlgorithm)

    def _create_algorithm[T: type[BaseAlgorithm]](self, of_type: T) -> BaseAlgorithm:
        return of_type(self._network_provider(), self._sender, self._receiver)
