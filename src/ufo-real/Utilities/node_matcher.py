# -*- coding: utf-8 -*-
"""
# Matching Module:
Core class the takes care of the matching between the computed\n
Node-Locations and the actual Node-Locations in the picture.\n
Expands upon the base class of Nodes.\n
"""

__copyright__ = "Copyright (c) 2025 HSLU PREN Team 2, FS25. All rights reserved."


# TODO: Expand this class into a strategy pattern in order to
# test different matching strategies in order to improve results.

import itertools

import numpy as np
from components import VisualNode


# Pubicliy accessable function that clients can use to find a matching. Gives access
# to all the other functions and simplifys access by hiding all the conditional
# statemates and adaptations. On its own only checks whether the two given lists as
# parameters have the same length and decides which recursive method needs to be
# invoked. Returns the best matching regardless with the nodes that could not be
# asigned as an empty tuple.
# - image   = (list[VisualNodes]) list of nodes extracted from the image
# - calc    = (list[VisualNodes]) list of nodes that were calculated
# - returns = (list[(str,str)]) list of tuples that create the minimal Matching
def find_best_matching(
    image: list[VisualNode], calc: list[VisualNode]
) -> list[tuple[str, str]]:
    """give it two list of VisualNodes, lean back and enjoy so magic happening"""
    result: list[tuple[str, str]] = []

    if len(image) != len(calc):
        result = _create_subset_for_matching(image, calc)
    else:
        eval, result = _calculate_best_matching(tuple(image), calc)

    return result


# Private function that does all the heavy lifting. Generates all possible
# permutations between the two sets and returns the minimal matching. Does
# however need the lists to be of equal length. Because of that it might be
# necessary use the method repeatedly. For that case it can return in addition
# to the matching the corresponding distance so the caller can compare results
# of different sublists.
# TODO: Exceptionally slow since this part alone takes O(N!). Alternatives
# desperately needed.
# - image    = (list[VisualNodes]) list of nodes extracted from the image
# - calc     = (list[VisualNodes]) list of nodes that were calculated
# - needEval = (bool) caller can say if they want the distance as well
# - returns  = (list[(str,str)]) list of tuples that create the minimal Matching
# alternative:
# - returns  = (float, list[str,str]) same as above but with the distance
def _calculate_best_matching(
    image: tuple[VisualNode, ...], calc: list[VisualNode]
) -> tuple[float, list[tuple[str, str]]]:
    if len(image) != len(calc):
        raise ValueError("Calculation Failed. The arrays don't have the same length.")

    perms = list(itertools.permutations(image))
    current_best = float("inf")
    result: list[tuple[str, str]] = []

    for p in perms:
        temp = _calculate_distance(p, calc)
        if temp < current_best:
            current_best = temp
            result = _calculate_matching(p, calc)

    return (current_best, result)


# Private function that is needed in cases the list do not have the same length.
# Generates subsets on all the possible subsets and recursively checks them all.
# TODO: exceptionally slow since it makes the algorithm O(N!*N!) Alternatives
# desperately needed.
# - image   = (list[VisualNodes]) list of nodes extracted from the image
# - calc    = (list[VisualNodes]) list of nodes that were calculated
# - returns = (list[str,str]) list of tuples that create the minimal Matching
def _create_subset_for_matching(
    image: list[VisualNode], calc: list[VisualNode]
) -> list[tuple[str, str]]:
    len_image: int = len(image)
    len_calc: int = len(calc)

    comb: list[tuple[VisualNode, ...]] = []
    fix: list[VisualNode] = []
    overflow: list[VisualNode] = []

    if len_image > len_calc:
        comb = list(itertools.combinations(image, len_calc))
        fix = calc
        overflow = image
    elif len_calc > len_image:
        comb = list(itertools.combinations(calc, len_image))
        fix = image
        overflow = calc
    else:
        raise ValueError(
            "Calculation went wrong. The arrays were already the same length"
            + " and did not need to be turned into subsets."
        )

    current_best = float("inf")
    result: list[tuple[str, str]] = []

    # try every subset
    for c in comb:
        temp_dis, temp_res = _calculate_best_matching(c, fix)
        if temp_dis < current_best:
            current_best = temp_dis
            result = temp_res

    # add all nodes as empty tuples that could not get a match
    for of in overflow:
        if not any(of.get_label in tuple for tuple in result):
            result.append((of.get_label, ""))

    return result


# Calculates the distance between each node in both arrays
# - image   = Array of VisualNodes
# - calc    = Array of VisualNodes
# - returns = (float) total distance
def _calculate_distance(image: tuple[VisualNode, ...], calc: list[VisualNode]) -> float:
    if len(image) != len(calc):
        raise ValueError("Calculation Failed. The arrays don't have the same length.")

    value: float = 0.0
    match: list[tuple[VisualNode, VisualNode]] = list(zip(image, calc))
    for i, c in match:
        value += np.square(i.get_distance(c))

    return value


# Generates a list (matching) of tuples for two arrays of nodes
# - image   = Array of Nodes
# - calc    = Array of Nodes
# - returns = Array of Tuples
def _calculate_matching(
    image: tuple[VisualNode, ...], calc: list[VisualNode]
) -> list[tuple[str, str]]:
    if len(image) != len(calc):
        raise ValueError("Calculation Failed. The arrays don't have the same length.")

    result: list[tuple[str, str]] = []
    match: list[tuple[VisualNode, VisualNode]] = list(zip(image, calc))
    for i, c in match:
        result.append((f"{i.get_label}", f"{c.get_label}"))

    return result
