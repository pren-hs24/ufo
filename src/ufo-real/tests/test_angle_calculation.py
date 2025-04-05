# -*- coding: utf-8 -*-
"""angle calculation tests"""

__copyright__ = "Copyright (c) 2025 HSLU PREN Team 2, FS25. All rights reserved."


from common.helper import Math
from network.node import Node


def test_straight_up() -> None:
    """
    test straight up (0°)
    """
    a = Node(x=0, y=0)
    b = Node(x=0, y=1)
    assert Math.calculate_angle_deg(a, b) == 0


def test_straight_down() -> None:
    """
    test straight down (180° / -180°)
    """
    a = Node(x=0, y=0)
    b = Node(x=0, y=-1)
    assert Math.calculate_angle_deg(a, b) in (180, -180)


def test_straight_right() -> None:
    """
    test straight right (90°)
    """
    a = Node(x=0, y=0)
    b = Node(x=1, y=0)
    assert Math.calculate_angle_deg(a, b) == 90


def test_straight_left() -> None:
    """
    test straight left (-90°)
    """
    a = Node(x=0, y=0)
    b = Node(x=-1, y=0)
    assert Math.calculate_angle_deg(a, b) == -90


def test_optimise_nothing() -> None:
    """
    test don't optimise if already at optimum
    """
    assert Math.optimise_for_next_angle(180, 180) == 180
    assert Math.optimise_for_next_angle(270, 270) == 270


def test_optimise_360() -> None:
    """optimise 360 <-> 0"""
    assert Math.optimise_for_next_angle(0, 350) == 360
    assert Math.optimise_for_next_angle(360, 10) == 0
    assert Math.optimise_for_next_angle(360, -10) == 0


def test_optimise_some_more() -> None:
    """optimise some random angles"""
    assert Math.optimise_for_next_angle(0, 190) == 360
    assert Math.optimise_for_next_angle(90, -100) == -270
    assert Math.optimise_for_next_angle(-80, 270) == 280
