import numpy as np
import PIL.Image, PIL.ImageDraw, PIL.ImageFilter, PIL.ImageFont, PIL.ImageOps
from ..image import image_circle

def delboeuf_image(parameters=None, width=800, height=600, outline=10, background="white", **kwargs):
    """
    Examples
    ---------
    >>> import pyllusion as ill
    >>>
    >>> parameters = ill.delboeuf_parameters(difficulty=2, illusion_strength=1)
    >>> ill.delboeuf_image(parameters)  #doctest: +ELLIPSIS
    <PIL.Image.Image ...>
    """
    # Create white canvas and get drawing context
    if parameters is None:
        parameters = delboeuf_parameters(**kwargs)

    # Background
    image  = PIL.Image.new('RGB', (width, height), color=background)

    # Outer circles (outlines)
    image = image_circle(image=image,
                         x=parameters["Position_Left"],
                         size=parameters["Size_Outer_Left"],
                         color=(0, 0, 0, 0),
                         outline=outline)
    image = image_circle(image=image,
                         x=parameters["Position_Right"],
                         size=parameters["Size_Outer_Right"],
                         color=(0, 0, 0, 0),
                         outline=outline)

    # Inner circles
    image = image_circle(image=image,
                         x=parameters["Position_Left"],
                         size=parameters["Size_Inner_Left"],
                         color="red")
    image = image_circle(image=image,
                         x=parameters["Position_Right"],
                         size=parameters["Size_Inner_Right"],
                         color="red")

    return image

# ------------------------------------------
# Parameters
# ------------------------------------------

def delboeuf_parameters(difficulty=0, size_min=0.25, illusion_strength=0, distance=1, distance_auto=False):
    """Compute Parameters for Delboeuf Illusion.

    Parameters
    ----------
    difficulty : float
        Size of left inner circle as relative to the right (in percentage, e.g., if ``difficulty=1``,
        it means that the left circle will be 100% bigger, i.e., 2 times bigger than the right).
    size_min : float
        Size of smaller inner circle.
    illusion : float
        Size of outer circles.
    distance : float
        distance between circles.
    distance_auto : bool
        If true, distance is between edges (fixed spacing), if false, between centers (fixed location).

    Examples
    ---------
    >>> import pyllusion as ill
    >>>
    >>> parameters = ill.delboeuf_parameters()
    """
    # Size inner circles
    parameters = _delboeuf_parameters_sizeinner(difficulty=difficulty, size_min=size_min)
    inner_size_left = parameters["Size_Inner_Left"]
    inner_size_right = parameters["Size_Inner_Right"]

    # Base size outer circles
    outer_size_left = inner_size_left + (0.2 * size_min)
    outer_size_right = inner_size_right + (0.2 * size_min)

    # Actual outer size based on illusion
    outer_size_left, outer_size_right = _delboeuf_parameters_sizeouter(outer_size_left,
                                                                       outer_size_right,
                                                                       difficulty=difficulty,
                                                                       illusion_strength=illusion_strength)

    # Get location and distances
    if distance_auto is False:
        distance_centers = distance
        position_left, position_right = -(distance_centers / 2), (distance_centers / 2)
        distance_edges_inner = distance_centers - (inner_size_left/2 + inner_size_right/2)
        distance_edges_outer = distance_centers - (outer_size_left/2 + outer_size_right/2)
    else:
        distance_edges_outer = distance
        distance_centers = distance_edges_outer + (inner_size_left/2 + inner_size_right/2)
        distance_edges_inner = distance_centers - (outer_size_left/2 + outer_size_right/2)
        position_left, position_right = -(distance_centers / 2), (distance_centers / 2)



    parameters.update({
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
        "Position_Right": position_right
        })

    return parameters


# ------------------------------------------
# Utilities
# ------------------------------------------


def _delboeuf_parameters_sizeouter(outer_size_left, outer_size_right, illusion_strength=0, difficulty=0, both_sizes=False):
    if both_sizes is True:
        illusion_strength = illusion_strength / 2

    # Actual outer size based on illusion
    if difficulty > 0: # if right is smaller
        if illusion_strength > 0:
            outer_size_left = np.sqrt(1 + np.abs(illusion_strength)) * outer_size_left
            if both_sizes is True:
                outer_size_right = outer_size_right / np.sqrt(1 + np.abs(illusion_strength))
        else:
            outer_size_right = np.sqrt(1 + np.abs(illusion_strength)) * outer_size_right
            if both_sizes is True:
                outer_size_left = outer_size_left / np.sqrt(1 + np.abs(illusion_strength))

    else:
        if illusion_strength > 0:
            outer_size_right = np.sqrt(1 + np.abs(illusion_strength)) * outer_size_right
            if both_sizes is True:
                outer_size_left = outer_size_left / np.sqrt(1 + np.abs(illusion_strength))
        else:
            outer_size_left = np.sqrt(1 + np.abs(illusion_strength)) * outer_size_left
            if both_sizes is True:
                outer_size_right = outer_size_right / np.sqrt(1 + np.abs(illusion_strength))

    return outer_size_left, outer_size_right


def _delboeuf_parameters_sizeinner(difficulty=0, size_min=0.25):

    size_bigger = np.sqrt(1 + np.abs(difficulty)) * size_min

    if difficulty > 0: # if right is smaller
        inner_size_right = size_min
        inner_size_left = size_bigger
    else:
        inner_size_right = size_bigger
        inner_size_left = size_min

    parameters = {"Difficulty": difficulty,
                  "Size_Inner_Left": inner_size_left,
                  "Size_Inner_Right": inner_size_right,
                  "Size_Inner_Difference": np.pi * (size_bigger / 2)**2 / np.pi * (size_min / 2)**2
    }
    return parameters
