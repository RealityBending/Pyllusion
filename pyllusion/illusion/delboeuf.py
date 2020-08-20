import numpy as np
import PIL.Image, PIL.ImageDraw, PIL.ImageFilter, PIL.ImageFont, PIL.ImageOps
from ..image import image_circle

def delboeuf_image(parameters=None, width=800, height=600, outline=10, background="white", **kwargs):
    """
    Examples
    ---------
    >>> import pyllusion as ill
    >>>
    >>> parameters = ill.delboeuf_parameters(difference=2, illusion_strength=0)
    >>> ill.delboeuf_image(parameters)
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

def delboeuf_parameters(difference=0, size_min=0.25, illusion_strength=0, distance=0.5, distance_auto=True):
    """Compute Parameters for Delboeuf Illusion.

    Parameters
    ----------
    difference : float
        Size of left inner circle as relative to the right (in percentage, e.g., if ``difference=1``,
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
    parameters = _delboeuf_parameters_sizeinner(difference=difference, size_min=size_min)
    inner_size_left = parameters["Size_Inner_Left"]
    inner_size_right = parameters["Size_Inner_Right"]

    outer_size_left = inner_size_left + (0.2 * size_min)
    outer_size_right = inner_size_right + (0.2 * size_min)


    if difference > 0: # if right is smaller
        if illusion_strength > 0:
            illusion_type = "Incongruent"
            outer_size_left = outer_size_left + outer_size_left * np.abs(illusion_strength)
        else:
            illusion_type = "Congruent"
            outer_size_right = outer_size_right + outer_size_right * np.abs(illusion_strength)

    else:
        if illusion_strength > 0:
            illusion_type = "Incongruent"
            outer_size_right = outer_size_right + outer_size_right * np.abs(illusion_strength)
        else:
            illusion_type = "Congruent"
            outer_size_left = outer_size_left + outer_size_left * np.abs(illusion_strength)


    inner_size_smaller = min([inner_size_left, inner_size_right])
    inner_size_larger = max([inner_size_left, inner_size_right])
    outer_size_smaller = min([outer_size_left, outer_size_right])
    outer_size_larger = max([outer_size_left, outer_size_right])

    if distance_auto is False:
        distance_centers = distance
        position_left = 0 - distance_centers/2
        position_right = 0 + distance_centers/2
        distance_edges_inner = distance_centers - (inner_size_left/2 + inner_size_right/2)
        distance_edges_outer = distance_centers - (outer_size_left/2 + outer_size_right/2)
    else:
        distance_edges_outer = distance
        distance_centers = distance_edges_outer + (inner_size_left/2 + inner_size_right/2)
        distance_edges_inner = distance_centers - (outer_size_left/2 + outer_size_right/2)
        position_left = 0-distance_centers/2
        position_right = 0+distance_centers/2



    parameters.update({
        "Illusion": "Delboeuf",
        "Illusion_Strength": illusion_strength,
        "Illusion_Type": illusion_type,

        "Size_Outer_Left": outer_size_left,
        "Size_Outer_Right": outer_size_right,

        "Distance_Centers": distance_centers,
        "Distance_Edges_Inner": distance_edges_inner,
        "Distance_Edges_Outer": distance_edges_outer,

        "Size_Inner_Smaller": inner_size_smaller,
        "Size_Inner_Larger": inner_size_larger,
        "Size_Outer_Smaller": outer_size_smaller,
        "Size_Outer_Larger": outer_size_larger,

        "Position_Left": position_left,
        "Position_Right": position_right,
        })

    return parameters


# ------------------------------------------
# Utilities
# ------------------------------------------


def _delboeuf_parameters_sizeinner(difference=0, size_min=0.25):

    size_bigger = np.sqrt(1 + np.abs(difference)) * size_min

    if difference > 0: # if right is smaller
        inner_size_right = size_min
        inner_size_left = size_bigger
    else:
        inner_size_right = size_bigger
        inner_size_left = size_min

    parameters = {"Difference": difference,
                  "Size_Inner_Left": inner_size_left,
                  "Size_Inner_Right": inner_size_right,
                  "Size_Inner_Difference": np.pi * (size_bigger / 2)**2 / np.pi * (size_min / 2)**2
    }
    return parameters
