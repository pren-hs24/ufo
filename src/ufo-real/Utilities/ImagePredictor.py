from Components import Camera, RealNode, Robot, Graph, VisualNode, Obstacle, Edge
from .NodeMatcher import find_best_matching
from Basic import Colour as c
from typing import TypeVar

import numpy as np
import cv2

# enabling polymorphism
T = TypeVar('T')

# parameter for the overlay
SIZE: int = 5
SIZE_LARGE: int = SIZE * 3
ALPHA: float = 0.5

# colour pre-sets
BLACK = c.bgr("BLACK")
LIGHT_GREY = c.bgr("LIGHT_GREY")
RED = c.bgr("RED")
ORANGE = c.bgr("ORANGE")
YELLOW = c.bgr("YELLOW")
GREEN = c.bgr("GREEN")

def analyze_image(camera: Camera, robot: Robot, graph: Graph, nodes: list[VisualNode], obstacles: list[Obstacle], img) -> None:
    # renaming for clarification
    detected_obstacles = obstacles
    detected_nodes = nodes
    computed_nodes = _compute_image_nodes_from_graph(camera, robot, graph)

    # compare the mesured locations of nodes with the one the system computed and find the best matching
    node_matching: list[tuple[str, str]] = find_best_matching(detected_nodes, computed_nodes)
    # combine them and get their location in the picture as well as the names of the ones that are blocked
    matched_nodes, blocked_nodes  = render_nodes_match_overlay(node_matching, detected_nodes, computed_nodes, graph, img)
    # compute whiche areas are blocked by the obstacles
    blocked_areas = render_groundplate_obstacle(detected_obstacles, camera, img)
    # compute how it affects the edges
    render_edges(matched_nodes, blocked_areas, blocked_nodes, graph, img)

def _compute_image_nodes_from_graph(camera: Camera, robot: Robot, graph: Graph) -> list[VisualNode]:
    result: list[VisualNode] = []
    
    for i in graph.getNodes():
        r, d = robot.compute_distance_and_difference(i.get_coordinates())
        x, y = camera.compute_image_position(r, d)
        w, h = camera.compute_object_image_dimensions(d, RealNode.get_real_radius())
        result.append(VisualNode(i.getLabel(), x, y, w, h))
    
    return result

def render_nodes_match_overlay(match: list[tuple[str, str]], nodes1: list[VisualNode], nodes2: list[VisualNode], graph: Graph, img) -> tuple[list[VisualNode], list[str]]:
    overlay = img.copy()

    result: list[VisualNode] = []
    pylons: list[str] = []

    matching: list[tuple[str, str]] = []

    computed_nodes: list[VisualNode] = []
    measured_nodes: list[VisualNode] = []

    # flip elements in tupel such that the computed labels come first
    if match[0][0].isalpha() and match[0][1].isdigit():
        matching = match
    elif match[0][0].isdigit() and match[0][1].isalpha():
        matching = [(b, a) for (a, b) in match]
    else:
        raise ValueError("Render Fail. Could not assign origin of nodes.")

    # check whiche list contains whiche type of node
    if nodes1[0].getLabel().isalpha() and nodes2[0].getLabel().isdigit():
        computed_nodes = nodes1
        measured_nodes = nodes2
    elif nodes1[0].getLabel().isdigit() and nodes2[0].getLabel().isalpha():
        computed_nodes = nodes2
        measured_nodes = nodes1
    else:
        raise ValueError("Render Fail. Could not assign origin of nodes.")
    
    cp_x: int = 0
    cp_y: int = 0
    cp_w: int = 0
    cp_h: int = 0
    cp_colour = BLACK

    ms_x: int = 0
    ms_y: int = 0
    ms_w: int = 0
    ms_h: int = 0
    ms_colour = BLACK

    offset_x, offset_y = calculate_average_offset(matching, measured_nodes, computed_nodes)

    for n, m in matching:
        if not n == "" and n in computed_nodes and not m == "" and m in measured_nodes: # classical match found
            cp_x, cp_y = _find_node_by_str(computed_nodes, n).get_coordinates()
            cp_w, cp_h = _find_node_by_str(computed_nodes, n).get_dimensions()
            cp_colour = BLACK

            ms_x, ms_y = _find_node_by_str(measured_nodes, m).get_coordinates()
            if m.__contains__("P"): # special case for pylon nodes since they are blocked
                ms_colour = RED
                pylons.append(n)
                _find_node_by_str(graph.getNodes(), n).isBlocked()
            else:
                ms_colour = GREEN
                _find_node_by_str(graph.getNodes(), n).isAvailable()

            result.append(VisualNode.position_only(n, ms_x, ms_y))
        elif not n == "" and n in computed_nodes and m == "": # missed a node that got computed but not found in the image
            cp_x, cp_y = _find_node_by_str(computed_nodes, n).get_coordinates()
            cp_w, cp_h = _find_node_by_str(computed_nodes, n).get_dimensions()
            cp_colour = BLACK

            ms_x = cp_x + offset_x
            ms_y = cp_y + offset_y
            ms_colour = YELLOW

            result.append(VisualNode.position_only(n, ms_x, ms_y))
        elif n == "" and not m == "" and m in measured_nodes: # node found in image that could not get match or is not a node
            ms_x, ms_y = _find_node_by_str(measured_nodes, m).get_coordinates()
            ms_colour = ORANGE
            
            cp_x = ms_x - offset_x
            cp_y = ms_y - offset_y
            cp_w = 0
            cp_h = 0
            cp_colour = BLACK
       
        # draw with the given specs

        # compute nodes with expected dimension and label
        cv2.ellipse(overlay, (cp_x, cp_y), (cp_w, cp_h), 0, 0, 360, LIGHT_GREY, -1)
        cv2.ellipse(overlay, (cp_x, cp_y), (cp_w, cp_h), 0, 0, 360, BLACK, 1)
        
        cv2.line(overlay, (cp_x-SIZE, cp_y-SIZE), (cp_x+SIZE, cp_y+SIZE), cp_colour, 1)
        cv2.line(overlay, (cp_x+SIZE, cp_y-SIZE), (cp_x-SIZE, cp_y+SIZE), cp_colour, 1) 
        
        cv2.putText(overlay, n, (cp_x-SIZE_LARGE, cp_y-cp_h-SIZE_LARGE), cv2.FONT_HERSHEY_SIMPLEX, 1.5, BLACK, 3)
                
        # places were the were measured
        cv2.line(overlay, (ms_x-SIZE, ms_y-SIZE), (ms_x+SIZE, ms_y+SIZE), ms_colour, 2)
        cv2.line(overlay, (ms_x+SIZE, ms_y-SIZE), (ms_x-SIZE, ms_y+SIZE), ms_colour, 2)

        # their connection
        cv2.line(overlay, (cp_x, cp_y), (ms_x, ms_y), BLACK, 1)

    cv2.addWeighted(overlay, ALPHA, img, 1 - ALPHA, 0, img)

    return (result, pylons)

def calculate_average_offset(match: list[tuple[str, str]], measuredNodes: list[VisualNode], computedNodes: list[VisualNode]) -> tuple[int, int]:
    sum_div_x: float = 0.0
    sum_div_y: float = 0.0

    num_matches: float = 1.0

    for mn in measuredNodes:
        for cp in computedNodes:
        
            if (f"{mn.getLabel()}", f"{cp.getLabel()}") in match\
                or (f"{cp.getLabel()}", f"{mn.getLabel()}") in match:

                num_matches += 1.0

                x_mn, y_mn = mn.get_coordinates()
                x_cp, y_cp = cp.get_coordinates()

                sum_div_x += float(x_mn - x_cp)
                sum_div_y += float(y_mn - y_cp)

                break

    avg_div_x = int(sum_div_x / num_matches)
    avg_div_y = int(sum_div_y/num_matches)

    return (avg_div_x, avg_div_y)

def render_edges(nodes: list[VisualNode], obstacles: list[VisualNode], pylons: list[str], graph: Graph, img) -> None:
    overlay = img.copy()

    for e in graph.getEdges():
        n, m = e.getNodes()
        label1 = n.getLabel()
        label2 = m.getLabel()
        if label1 in nodes and label2 in nodes:
            x_1, y_1 = _find_node_by_str(nodes, label1).get_coordinates()
            x_2, y_2 = _find_node_by_str(nodes, label2).get_coordinates()

            if label1 in pylons or label2 in pylons:
                colour = RED
                graph.getEdges()[graph.getEdges().index(e)].isMissing()
            elif _does_line_cross_any_obstacle((x_1, y_1), (x_2, y_2), obstacles):
                colour = YELLOW
                graph.getEdges()[graph.getEdges().index(e)].isBlocked()
            else:
                colour = GREEN
                graph.getEdges()[graph.getEdges().index(e)].isAvailable()

            cv2.line(overlay, (x_1, y_1), (x_2, y_2), colour, 1)

    cv2.addWeighted(overlay, ALPHA, img, 1 - ALPHA, 0, img)

def render_groundplate_obstacle(obstacles: list[Obstacle], camera: Camera, img) -> list[VisualNode]:
    overlay = img.copy()

    obstacles_images: list[VisualNode] = []

    for o in obstacles:
        temp = camera.compute_groundplate(o)
        x, y = temp.get_coordinates()
        w, h = temp.get_dimensions()
        
        cv2.ellipse(overlay,(x, y), (w, h), 0, 0, 360, RED, -1)
        cv2.ellipse(overlay,(x, y), (w, h), 0, 0, 360, BLACK, 1)

        cv2.line(overlay, (x-SIZE, y-SIZE), (x+SIZE, y+SIZE), BLACK, 1)
        cv2.line(overlay, (x+SIZE, y-SIZE), (x-SIZE, y+SIZE), BLACK, 1)

        obstacles_images.append(VisualNode(f"O{o.get_id()}", x, y, w, h))

    cv2.addWeighted(overlay, ALPHA, img, 1 - ALPHA, 0, img)

    return obstacles_images

def _does_line_intersect_ellipse(point_a: tuple[int, int], point_b: tuple[int, int], obstacle: VisualNode) -> bool:
    # code by ChatGPT 4.0 <3
    x1, y1 = point_a
    x2, y2 = point_b

    x3, y3 = obstacle.get_coordinates()
    w, h = obstacle.get_dimensions()

    # Transformiere Koordinaten, damit Ellipse um Ursprung liegt
    dx = x2 - x1
    dy = y2 - y1

    # Parametrische Linie: (x, y) = (x1, y1) + t*(dx, dy), 0 <= t <= 1
    # Ellipsengleichung: ((x - x3)^2 / (w/2)^2) + ((y - y3)^2 / (h/2)^2) = 1

    if h == 0:
        h = 1

    a = (dx**2) / (w/2)**2 + (dy**2) / (h/2)**2
    b = 2 * ((x1 - x3) * dx / (w/2)**2 + (y1 - y3) * dy / (h/2)**2)
    c = ((x1 - x3)**2) / (w/2)**2 + ((y1 - y3)**2) / (h/2)**2 - 1

    # Löse quadratische Gleichung: at^2 + bt + c = 0
    discriminant = b**2 - 4*a*c

    if discriminant < 0:
        return False  # Kein Schnittpunkt

    # Schnittpunkte berechnen
    sqrt_disc = np.sqrt(discriminant)
    t1 = (-b - sqrt_disc) / (2*a)
    t2 = (-b + sqrt_disc) / (2*a)

    # Prüfen, ob ein Schnittpunkt auf der Linie liegt (0 <= t <= 1)
    return (0 <= t1 <= 1) or (0 <= t2 <= 1)

def _does_line_cross_any_obstacle(point_a: tuple[int, int], point_b: tuple[int, int], obstacles: list[VisualNode]) -> bool:
    result = False

    for o in obstacles:
        if _does_line_intersect_ellipse(point_a, point_b, o):
            result = True
            break

    return result

def _find_index_by_str(nodes: list[T], name: str) -> int:
    for i, node in enumerate(nodes):
        if node == name:
            return i
    raise ValueError(f"{name} not found")

def _find_node_by_str(nodes: list[T], name: str) -> T:
    value: int = _find_index_by_str(nodes, name)
    return nodes[value]