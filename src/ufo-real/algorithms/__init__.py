# -*- coding: utf-8 -*-
"""Algorithms"""

__copyright__ = "Copyright (c) 2025 HSLU PREN Team 2, FS25. All rights reserved."


from .road_sense import RoadSenseAlgorithm

ALGORITHMS = {
    x.name: x
    for x in [
        RoadSenseAlgorithm,
    ]
}
