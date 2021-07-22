import numpy as np

from ..Delboeuf.delboeuf_parameters import _delboeuf_parameters_sizeinner, _delboeuf_parameters_sizeouter


def _ebbinghaus_parameters(illusion_strength=0, difference=0, size_min=0.25, distance=1, distance_auto=False):

    # Size inner circles
    parameters = _delboeuf_parameters_sizeinner(difference=difference, size_min=size_min)
    inner_size_left = parameters["Size_Inner_Left"]
    inner_size_right = parameters["Size_Inner_Right"]

    # Position
    position_left = -0.5
    position_right = 0.5

    # Base size outer circles
    outer_size_left = size_min
    outer_size_right = size_min

    # Actual outer size based on illusion
    outer_size_left, outer_size_right = _delboeuf_parameters_sizeouter(outer_size_left,
                                                                       outer_size_right,
                                                                       difference=difference,
                                                                       illusion_strength=illusion_strength,
                                                                       both_sizes=True)

    # Location outer circles
    l_outer_x, l_outer_y, l_distance_edges = _ebbinghaus_parameters_outercircles(x=position_left,
                                                            y=0,
                                                            size_inner=inner_size_left,
                                                            size_outer=outer_size_left,
                                                            n="auto")
    r_outer_x, r_outer_y, r_distance_edges = _ebbinghaus_parameters_outercircles(x=position_right,
                                                            y=0,
                                                            size_inner=inner_size_right,
                                                            size_outer=outer_size_right,
                                                            n="auto")

    # Get location and distances
    if distance_auto is False:
        distance_reference = 'Between Centers'
        distance_centers = distance
        position_left, position_right = -(distance_centers / 2), (distance_centers / 2)
        distance_edges_inner = distance_centers - (inner_size_left/2 + inner_size_right/2)
        distance_edges_outer = distance_centers - l_distance_edges - (outer_size_left/2) - r_distance_edges - (outer_size_right/2)

    else:
        distance_reference = 'Between Edges'
        distance_edges_outer = distance
        distance_centers = distance_edges_outer + l_distance_edges + (outer_size_left/2) + r_distance_edges + (outer_size_right/2)
        distance_edges_inner = distance_centers - (outer_size_left/2 + outer_size_right/2)
        position_left, position_right = -(distance_centers / 2), (distance_centers / 2)

    parameters.update({
        "Illusion": "Ebbinghaus",
        "Illusion_Strength": illusion_strength,
        "Illusion_Type": "Incongruent" if illusion_strength > 0 else "Congruent",

        "Size_Outer_Left": outer_size_left,
        "Size_Outer_Right": outer_size_right,

        "Distance": distance_centers,
        "Distance_Reference": distance_reference,
        "Distance_Edges_Inner": distance_edges_inner,
        "Distance_Edges_Outer": distance_edges_outer,

        "Size_Inner_Smaller": np.min([inner_size_left, inner_size_right]),
        "Size_Inner_Larger": np.max([inner_size_left, inner_size_right]),
        "Size_Outer_Smaller": np.min([outer_size_left, outer_size_right]),
        "Size_Outer_Larger": np.max([outer_size_left, outer_size_right]),

        "Position_Outer_x_Left": l_outer_x,
        "Position_Outer_y_Left": l_outer_y,
        "Position_Outer_x_Right": r_outer_x,
        "Position_Outer_y_Right": r_outer_y,

        "Position_Left": position_left,
        "Position_Right": position_right
        })

    return parameters



def _ebbinghaus_parameters_outercircles(x=0, y=0, size_inner=0.25, size_outer=0.3, n="auto"):
    # Find distance between center of inner circle and centers of outer circles
    distance = (size_inner / 2) + (size_outer / 2) + 0.01

    # Find n
    if n == "auto":
        perimeter = 2 * np.pi * distance
        n = int(perimeter / size_outer)

    # Get position of outer circles
    angle = np.deg2rad(np.linspace(0, 360, num=n, endpoint=False))
    circle_x = x + (np.cos(angle) * distance)
    circle_y = y + (np.sin(angle) * distance)

    return circle_x, circle_y, distance
