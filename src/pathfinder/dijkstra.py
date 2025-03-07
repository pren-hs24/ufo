# -*- coding: utf-8 -*-
"""Pathfinder interface module"""

__copyright__ = "Copyright (c) 2025 HSLU PREN Team 2, FS25. All rights reserved."

from scipy.sparse import csr_array  # type: ignore
from scipy.sparse.csgraph import dijkstra  # type: ignore

from common.constants import NODE_PENALTY_WEIGHT
from network.node import Node
from network.network import Network
from .base_pathfinder import BasePathfinder


class DijkstraPathfinder(BasePathfinder):
    """Pathfinder: Dijkstra+ Pro Max Ultra"""

    def _create_adjacency_matrix(
        self, network: Network, start_end: tuple[Node, Node]
    ) -> list[list[float]]:
        nodes = list(network.nodes)
        matrix = [[0.0 for _ in range(len(nodes))] for _ in range(len(nodes))]

        for edge in network.edges:
            i = nodes.index(edge.nodes[0])
            j = nodes.index(edge.nodes[1])

            weight = edge.weight

            if not any(node in start_end for node in edge.nodes):
                weight += NODE_PENALTY_WEIGHT

            matrix[i][j] = weight
            matrix[j][i] = weight

        return matrix

    def find_path(self, network: Network, end: Node) -> list[Node]:
        self._validate(network, end)

        nodes = list(network.nodes)
        istart = nodes.index(network.start)
        iend = nodes.index(end)

        adj_matrix = self._create_adjacency_matrix(network, (network.start, end))
        dist_matrix, predecessors = dijkstra(
            csr_array(adj_matrix), directed=False, return_predecessors=True
        )
        path = [iend]
        while path[-1] != istart:
            path.append(predecessors[istart][path[-1]])

        node_path = [nodes[i] for i in reversed(path)]
        self._logger.debug("path to %s (%s): %s", end, dist_matrix[istart][iend], node_path)

        return node_path
