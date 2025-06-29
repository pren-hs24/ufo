# -*- coding: utf-8 -*-
"""
Utility base class for Edges. It is supposed to make\n
the code more understandable, well organized and easier to\n
adapt in case something changes.
"""

__copyright__ = "Copyright (c) 2025 HSLU PREN Team 2, FS25. All rights reserved."


from enum import Enum

from .real_node import RealNode


class EdgeState(Enum):
    """state of information we have about an edge"""

    FREE = 0
    MISSING = 1
    BLOCKED = 2
    UNKNOWN = 3


class Edge:
    """Edge in the Graph"""

    start: RealNode  # start-node
    end: RealNode  # end-node
    status: EdgeState  # state of the edge

    # [Constructor] with the values for physical nodes
    # - start     = (RealNode) one of the two connected nodes
    # - end       = (RealNode) second of the two connected nodes
    # (edges are treated als bidirectional)
    # - status    = (EdgeState) reflects the current amount
    #               of knowledge we have of this edge
    def __init__(self, start: RealNode, end: RealNode):
        if isinstance(start, RealNode) and isinstance(end, RealNode):
            self.start = start
            self.end = end
            self.status = EdgeState.UNKNOWN
        else:
            raise ValueError("Edge generation failed. Invalid types where provided.")

    def __str__(self) -> str:
        return f"Edge: ({self.start.get_label},{self.end.get_label}) {self.status.name}"

    def __eq__(self, value) -> bool:
        if not isinstance(value, Edge):
            return False

        return (self.start == value.start and self.end == value.end) or (
            self.start == value.end and self.end == value.start
        )

    @property
    def get_nodes(self) -> tuple[RealNode, RealNode]:
        """get both of the ``RealNode``'s that are connected to the edge"""
        return (self.start, self.end)

    @property
    def get_status(self) -> str:
        """get a ``String`` representing what we know about this edge"""
        return self.status.name

    def is_available(self) -> None:
        """let the system know this edge can be used"""
        self._change_status_if_different(EdgeState.FREE)

    def is_blocked(self) -> None:
        """let the system know this edge is present but slower to use"""
        self._change_status_if_different(EdgeState.BLOCKED)

    def is_missing(self) -> None:
        """let the system know this edge can **not** be used"""
        self._change_status_if_different(EdgeState.MISSING)

    def _change_status_if_different(self, new_status: EdgeState) -> None:
        if not self.status == new_status:
            self.status = new_status
