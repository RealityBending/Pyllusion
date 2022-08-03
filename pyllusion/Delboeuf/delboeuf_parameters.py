import numpy as np


def _delboeuf_parameters(
    illusion_strength=0, difference=0, size_min=0.25, distance=1, distance_auto=False
):

    # Size inner circles
    parameters = _delboeuf_parameters_sizeinner(difference=difference, size_min=size_min)
    inner_size_left = parameters["Size_Inner_Left"]
    inner_size_right = parameters["Size_Inner_Right"]

    # Base size outer circles
    outer_size_left = inner_size_left + (0.2 * size_min)
    outer_size_right = inner_size_right + (0.2 * size_min)

    # Actual outer size based on illusion
    outer_size_left, outer_size_right = _delboeuf_parameters_sizeouter(
        outer_size_left,
        outer_size_right,
        difference=difference,
        illusion_strength=illusion_strength,
    )

    # Get location and distances
    if distance_auto is False:
        distance_reference = "Between Centers"
        distance_centers = distance
        position_left, position_right = -(distance_centers / 2), (distance_centers / 2)
        distance_edges_inner = distance_centers - (inner_size_left / 2 + inner_size_right / 2)
        distance_edges_outer = distance_centers - (outer_size_left / 2 + outer_size_right / 2)
    else:
        distance_reference = "Between Edges"
        distance_edges_outer = distance
        distance_centers = distance_edges_outer + (inner_size_left / 2 + inner_size_right / 2)
        distance_edges_inner = distance_centers - (outer_size_left / 2 + outer_size_right / 2)
        position_left, position_right = -(distance_centers / 2), (distance_centers / 2)

    parameters.update(
        {
            "Illusion": "Delboeuf",
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
            "Position_Left": position_left,
            "Position_Right": position_right,
        }
    )

    return parameters


# ------------------------------------------
# Utilities
# ------------------------------------------


def _delboeuf_parameters_sizeouter(
    outer_size_left,
    outer_size_right,
    illusion_strength=0,
    difference=0,
    both_sizes=False,
):
    if both_sizes is True:
        illusion_strength = illusion_strength / 2

    # Actual outer size based on illusion
    if difference > 0:  # if right is smaller
        if illusion_strength > 0:
            outer_size_left = (1 + np.abs(illusion_strength)) * outer_size_left
            if both_sizes is True:
                outer_size_right = outer_size_right / (1 + np.abs(illusion_strength))
        else:
            outer_size_right = (1 + np.abs(illusion_strength)) * outer_size_right
            if both_sizes is True:
                outer_size_left = outer_size_left / (1 + np.abs(illusion_strength))

    else:
        if illusion_strength > 0:
            outer_size_right = (1 + np.abs(illusion_strength)) * outer_size_right
            if both_sizes is True:
                outer_size_left = outer_size_left / (1 + np.abs(illusion_strength))
        else:
            outer_size_left = (1 + np.abs(illusion_strength)) * outer_size_left
            if both_sizes is True:
                outer_size_right = outer_size_right / (1 + np.abs(illusion_strength))

    return outer_size_left, outer_size_right


def _delboeuf_parameters_sizeinner(difference=0, size_min=0.25):

    size_bigger = (1 + np.abs(difference)) * size_min

    if difference > 0:  # if right is smaller
        inner_size_right = size_min
        inner_size_left = size_bigger
    else:
        inner_size_right = size_bigger
        inner_size_left = size_min

    parameters = {
        "Difference": difference,
        "Size_Inner_Left": inner_size_left,
        "Size_Inner_Right": inner_size_right,
        "Size_Inner_Difference": np.pi * (size_bigger / 2) ** 2 / np.pi * (size_min / 2) ** 2,
    }
    return parameters
