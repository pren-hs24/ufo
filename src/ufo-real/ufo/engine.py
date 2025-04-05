# -*- coding: utf-8 -*-
"""UFO Engine"""

__copyright__ = "Copyright (c) 2025 HSLU PREN Team 2, FS25. All rights reserved."

from typing import Callable
import logging

from algorithms.base_algorithm import BaseAlgorithm
from algorithms.road_sense import RoadSenseAlgorithm
from uart.protocol import UARTProtocol
from uart.sender import UARTSender
from uart.receiver import UARTReceiver
from uart.mock.log_bus import LogUARTBus
from network.network import Network


class Engine:
    """UFO Engine"""

    def __init__(
        self,
        network_provider: Callable[[], Network],
    ) -> None:
        self._network_provider = network_provider
        self._logger = logging.getLogger("engine")
        self._sender = UARTSender(LogUARTBus())
        self._receiver = UARTReceiver(LogUARTBus())
        self._algorithm: BaseAlgorithm | None = None

    def init(self, bus: UARTProtocol) -> None:
        """init"""
        self._sender.bus = bus
        self._receiver.bus = bus
        self._algorithm = self._create_algorithm(RoadSenseAlgorithm)
        self._logger.info("Engine initialised")

    def _create_algorithm[T: type[BaseAlgorithm]](self, of_type: T) -> BaseAlgorithm:
        return of_type(self._network_provider(), self.sender, self.receiver)

    @property
    def algorithm(self) -> BaseAlgorithm:
        """algorithm"""
        assert self._algorithm is not None
        return self._algorithm

    def create_network(self) -> Network:
        """network"""
        return self._network_provider()

    @property
    def sender(self) -> UARTSender:
        """sender"""
        assert self._sender is not None
        return self._sender

    @property
    def receiver(self) -> UARTReceiver:
        """receiver"""
        assert self._receiver is not None
        return self._receiver
