import PIL.Image, PIL.ImageDraw, PIL.ImageFilter, PIL.ImageFont, PIL.ImageOps
from ..image import image_circle

def delboeuf_image(parameters=None, width=800, height=600, background="white", **kwargs):
    """
    Examples
    ---------
    >>> import pyllusion as ill
    >>>
    >>> parameters = ill.delboeuf_parameters(difficulty=1, illusion_strength=1)
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
                         outline=5)
    image = image_circle(image=image,
                         x=parameters["Position_Right"],
                         size=parameters["Size_Outer_Right"],
                         color=(0, 0, 0, 0),
                         outline=5)

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



def delboeuf_parameters(difficulty=0, illusion_strength=0, minimum_size=0.25, distance=0.5, distance_auto=True):
    """Compute Parameters for Delboeuf Illusion.

    Parameters
    ----------
    difficulty : float
        Size of right inner circle.
    illusion : float
        Size of outer circles.
    minimum_size : float
        Size of smaller inner circle.
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
    if difficulty > 0: # if right is smaller
        inner_size_right = minimum_size
        inner_size_left = inner_size_right + inner_size_right * abs(difficulty)
        outer_size_left = inner_size_left + (inner_size_left/10)
        outer_size_right = inner_size_right + (inner_size_right/10)

        if illusion_strength > 0:
            illusion_type = "Incongruent"
            outer_size_left = outer_size_left + outer_size_left * abs(illusion_strength)
        else:
            illusion_type = "Congruent"
            outer_size_right = outer_size_right + outer_size_right * abs(illusion_strength)

    else:
        inner_size_left = minimum_size
        inner_size_right = inner_size_left +  inner_size_left * abs(difficulty)
        outer_size_left = inner_size_left + (inner_size_left/10)
        outer_size_right = inner_size_right + (inner_size_right/10)

        if illusion_strength > 0:
            illusion_type = "Incongruent"
            outer_size_right = outer_size_right + outer_size_right * abs(illusion_strength)
        else:
            illusion_type = "Congruent"
            outer_size_left = outer_size_left + outer_size_left * abs(illusion_strength)


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



    parameters = {"Illusion": "Delboeuf",
                  "Illusion_Strength": illusion_strength,
                  "Illusion_Type": illusion_type,
                  "Difficulty": difficulty,

                  "Size_Inner_Left": inner_size_left,
                  "Size_Inner_Right": inner_size_right,
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
                  }

    return(parameters)