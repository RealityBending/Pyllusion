import numpy as np
import PIL.Image, PIL.ImageDraw, PIL.ImageFilter, PIL.ImageFont, PIL.ImageOps
from ..image import image_circle
from ..psychopy.psychopy_circle import psychopy_circle




def _delboeuf_parameters(
    illusion_strength=0, difference=0, size_min=0.25, distance=1, distance_auto=False
):
    """Compute Parameters for Delboeuf Illusion.

    Parameters
    ----------
    illusion_strength : float
        The strength of the surrounding context, i.e. outer circles, in biasing perception of unequally sized inner circles.
        Specifically, the size of left outer circle relative to its inner circle (in percentage, e.g, if ``difference=1``,
        it means that the left outer circle will be 100% bigger, i.e., 2 times bigger than the left
        inner circle). A negative sign reflects the size difference of the right circles, i.e.,
        i.e., ``difference=-1`` means the right outer circle will be 100% bigger than the inner right circle.
    difference : float
        The objective size difference of the inner circles.
        Specifically, the size of left inner circle relative to the right inner circle (in percentage, e.g., if ``difference=1``,
        it means that the left circle will be 100% bigger, i.e., 2 times bigger than the right).
        A negative sign reflects the size difference of the right inner circle relative to the left,
        i.e., ``difference=-1`` means the right inner circle will be 100% bigger than the left inner circle.
    size_min : float
        Size of smaller inner circle.
    distance : float
        Distance between circles.
    distance_auto : bool
        If true, distance is between edges (fixed spacing), if false, between centers (fixed location).

    Returns
    -------
    dict
        Dictionary of parameters of the delboeuf illusion.

    Examples
    ---------
    >>> import pyllusion
    >>>
    >>> parameters = pyllusion.delboeuf_parameters()
    """
    # Size inner circles
    parameters = _delboeuf_parameters_sizeinner(
        difference=difference, size_min=size_min
    )
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
        distance_centers = distance
        position_left, position_right = -(distance_centers / 2), (distance_centers / 2)
        distance_edges_inner = distance_centers - (
            inner_size_left / 2 + inner_size_right / 2
        )
        distance_edges_outer = distance_centers - (
            outer_size_left / 2 + outer_size_right / 2
        )
    else:
        distance_edges_outer = distance
        distance_centers = distance_edges_outer + (
            inner_size_left / 2 + inner_size_right / 2
        )
        distance_edges_inner = distance_centers - (
            outer_size_left / 2 + outer_size_right / 2
        )
        position_left, position_right = -(distance_centers / 2), (distance_centers / 2)

    parameters.update(
        {
            "Illusion": "Delboeuf",
            "Illusion_Strength": illusion_strength,
            "Illusion_Type": "Congruent" if illusion_strength > 0 else "Incongruent",
            "Size_Outer_Left": outer_size_left,
            "Size_Outer_Right": outer_size_right,
            "Distance_Centers": distance_centers,
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
            outer_size_left = np.sqrt(1 + np.abs(illusion_strength)) * outer_size_left
            if both_sizes is True:
                outer_size_right = outer_size_right / np.sqrt(
                    1 + np.abs(illusion_strength)
                )
        else:
            outer_size_right = np.sqrt(1 + np.abs(illusion_strength)) * outer_size_right
            if both_sizes is True:
                outer_size_left = outer_size_left / np.sqrt(
                    1 + np.abs(illusion_strength)
                )

    else:
        if illusion_strength > 0:
            outer_size_right = np.sqrt(1 + np.abs(illusion_strength)) * outer_size_right
            if both_sizes is True:
                outer_size_left = outer_size_left / np.sqrt(
                    1 + np.abs(illusion_strength)
                )
        else:
            outer_size_left = np.sqrt(1 + np.abs(illusion_strength)) * outer_size_left
            if both_sizes is True:
                outer_size_right = outer_size_right / np.sqrt(
                    1 + np.abs(illusion_strength)
                )

    return outer_size_left, outer_size_right


def _delboeuf_parameters_sizeinner(difference=0, size_min=0.25):

    size_bigger = np.sqrt(1 + np.abs(difference)) * size_min

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
        "Size_Inner_Difference": np.pi
        * (size_bigger / 2) ** 2
        / np.pi
        * (size_min / 2) ** 2,
    }
    return parameters
