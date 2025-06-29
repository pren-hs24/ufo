# Core class the takes care of the matching between the computed
# Node-Locations and the actual Node-Locations in the picture. Expands
# upon the base class of Nodes.

# TODO: Expand this class into a strategy pattern in order to
# test different matching strategies in order to improve results.

from Components import VisualNode

import itertools
import numpy as np

# Pubicliy accessable function that clients can use to find a matching. Gives access
# to all the other functions and simplifys access by hiding all the conditional
# statemates and adaptations. On its own only checks whether the two given lists as
# parameters have the same length and decides which recursive method needs to be
# invoked. Returns the best matching regardless with the nodes that could not be
# asigned as an empty tuple.
# - image   = (list[VisualNodes]) list of nodes extracted from the image
# - calc    = (list[VisualNodes]) list of nodes that were calculated
# - returns = (list[(str,str)]) list of tuples that create the minimal Matching
def find_best_matching(image: list[VisualNode], calc: list[VisualNode]) -> list[tuple[str, str]]:
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
def _calculate_best_matching(image: tuple[VisualNode, ...], calc: list[VisualNode]) -> tuple[float, list[tuple[str, str]]]:
    if len(image) != len(calc):
        raise ValueError("Calculation Failed. The arrays don't have the same length.")
    
    perms = list(itertools.permutations(image))
    currentBest = float('inf')
    result: list[tuple[str, str]] = []

    for p in perms:
        temp = _calculate_distance(p,calc)
        if temp < currentBest:
            currentBest = temp
            result = _calculate_matching(p,calc)

    return (currentBest, result)

# Private function that is needed in cases the list do not have the same length.
# Generates subsets on all the possible subsets and recursively checks them all.
# TODO: exceptionally slow since it makes the algorithm O(N!*N!) Alternatives
# desperately needed.
# - image   = (list[VisualNodes]) list of nodes extracted from the image
# - calc    = (list[VisualNodes]) list of nodes that were calculated
# - returns = (list[str,str]) list of tuples that create the minimal Matching
def _create_subset_for_matching(image: list[VisualNode], calc: list[VisualNode]) -> list[tuple[str, str]]:
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
        raise ValueError("Calculation went wrong. The arrays were already the same length"\
                         +" and did not need to be turned into subsets.")
    
    currentBest = float('inf')
    result: list[tuple[str, str]] = []

    # try every subset
    for c in comb:
        tempDis, tempRes = _calculate_best_matching(c, fix)
        if tempDis < currentBest:
            currentBest = tempDis
            result = tempRes

    # add all nodes as empty tuples that could not get a match
    for of in overflow:
        if not any(of.getLabel() in tuple for tuple in result): 
            result.append((of.getLabel(),""))

    return result

# Calculates the distance between each node in both arrays
# - image   = Array of VisualNodes
# - calc    = Array of VisualNodes
# - returns = (float) total distance
def _calculate_distance(image: tuple[VisualNode, ...], calc: list[VisualNode]) -> float:
    if len(image) != len(calc):
        raise ValueError("Calculation Failed. The arrays don't have the same length.")
    
    sum = 0.0
    for i in range(len(image)):
        sum += np.square(VisualNode.getDistance(image[i],calc[i]))
    
    return sum

# Generates a list (matching) of tuples for two arrays of nodes
# - image   = Array of Nodes
# - calc    = Array of Nodes
# - returns = Array of Tuples
def _calculate_matching(image: tuple[VisualNode, ...], calc: list[VisualNode]) -> list[tuple[str, str]]:
    if len(image) != len(calc):
        raise ValueError("Calculation Failed. The arrays don't have the same length.")
    
    result: list[tuple[str, str]] = []
    for i in range(len(image)):
        result.append((f"{image[i].getLabel()}", f"{calc[i].getLabel()}"))

    return result