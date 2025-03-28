# -*- coding: utf-8 -*-
"""Base Algorithm implementation."""

__copyright__ = "Copyright (c) 2025 HSLU PREN Team 2, FS25. All rights reserved."

from abc import ABC
from uart.receiver import UARTReceiver
from uart.sender import UARTSender
from ufo.actor import Ufo
from ufo.listener import BaseUfoListener
from network.network import Network
from network.node import Node


class BaseAlgorithm(BaseUfoListener, ABC):
    """Base Algorithm"""

    def __init__(
        self,
        network: Network,
        sender: UARTSender,
        receiver: UARTReceiver,
    ) -> None:
        BaseUfoListener.__init__(self, network, receiver)

        self._sender = sender
        self._ufo = Ufo(sender, network.start)
        self._path: list[Node] = []
