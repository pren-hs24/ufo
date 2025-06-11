# -*- coding: utf-8 -*-
"""UFO Engine"""

__copyright__ = "Copyright (c) 2025 HSLU PREN Team 2, FS25. All rights reserved."

import logging

from algorithms.base_algorithm import BaseAlgorithm
from algorithms.road_sense import RoadSenseAlgorithm
from uart.protocol import UARTProtocol
from uart.sender import UARTSender
from uart.receiver import UARTReceiver
from uart.mock.log_bus import LogUARTBus
from network.network import Network, NetworkProvider


class Engine:
    """UFO Engine"""

    def __init__(
        self,
        network_provider: NetworkProvider,
    ) -> None:
        self._network_provider = network_provider
        self._logger = logging.getLogger("engine")
        self._sender = UARTSender(LogUARTBus())
        self._receiver = UARTReceiver(LogUARTBus())
        self._algorithm: BaseAlgorithm | None = None

    def init(
        self,
        bus: UARTProtocol,
        manual: bool = False,
    ) -> None:
        """init"""
        self._sender.bus = bus
        self._receiver.bus = bus
        if not manual:
            self._logger.info("Starting algorithm")
            self._algorithm = self._create_algorithm(RoadSenseAlgorithm)
        self._logger.info("Engine initialised")

    def change_algorithm(self, to_type: type[BaseAlgorithm] | None) -> None:
        """change algorithm"""
        if self._algorithm is not None:
            self._logger.info("Stopping current algorithm")
            del self._algorithm
        if to_type is None:
            self._logger.info("No algorithm specified, manual control enabled")
            self._algorithm = None
            return
        self._logger.info("Changing algorithm to %s", to_type.__name__)
        self._algorithm = self._create_algorithm(to_type)

    def _create_algorithm[T: type[BaseAlgorithm]](self, of_type: T) -> BaseAlgorithm:
        return of_type(self._network_provider, self.sender, self.receiver)

    @property
    def algorithm(self) -> BaseAlgorithm | None:
        """algorithm"""
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

    def reset(self) -> None:
        """reset engine"""
        self._logger.info("Resetting engine")
        if self._algorithm is not None:
            self._algorithm.reset()
        self._logger.info("Engine reset complete")
