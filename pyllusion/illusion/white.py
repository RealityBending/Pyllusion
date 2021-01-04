import numpy as np
import PIL.Image
import PIL.ImageDraw
import PIL.ImageFilter
import PIL.ImageFont
import PIL.ImageOps

from ..image import image_rectangle, rescale
from .contrast import _contrast_parameters


def white_image(parameters=None, width=800, height=600, **kwargs):
    """Create the white's illusion.
    White’s illusion is a brightness illusion in which rectangles of the same grey
    color are perceived of different luminance depending on their background.

    Examples
    ---------
    >>> import pyllusion as ill
    >>>
    >>> parameters = ill.white_parameters(difference=0, illusion_strength=100)
    >>> ill.white_image(parameters)  #doctest: +ELLIPSIS
    <PIL.Image.Image ...>
    """
    # Create white canvas and get drawing context
    if parameters is None:
        parameters = white_parameters(**kwargs)

    # Background1
    image = PIL.Image.new("RGB", (width, height), color=parameters["Background1_RGB"])

    # Target 1
    for y in parameters["Target1_y"]:
        image = image_rectangle(
            image=image,
            x=-0.5,
            y=y,
            size_height=parameters["Target_Height"],
            size_width=0.5,
            color=parameters["Target1_RGB"],
            antialias=False,
        )

    # Background2 and Target2
    for y in parameters["Target2_y"]:
        image = image_rectangle(
            image=image,
            y=y,
            size_height=parameters["Target_Height"],
            size_width=2,
            color=parameters["Background2_RGB"],
            antialias=False,
        )

        image = image_rectangle(
            image=image,
            x=0.5,
            y=y,
            size_height=parameters["Target_Height"],
            size_width=0.5,
            color=parameters["Target2_RGB"],
            antialias=False,
        )

    return image


def white_parameters(difference=0, illusion_strength=0, strips_n=9):

    colors, rgb = _contrast_parameters(
        difference=difference, illusion_strength=illusion_strength
    )

    y = np.linspace(-1, 1, endpoint=False, num=strips_n)  # All strips' top y
    strip_height = 2 / (strips_n)  # With of one strip
    target2_y = y[1::2] + (strip_height / 2)
    target1_y = y[0::2] + (strip_height / 2)

    parameters = {
        "Illusion": "Contrast",
        "Illusion_Strength": illusion_strength,
        "Difference": difference,
        "Illusion_Type": "Congruent" if illusion_strength > 0 else "Incongruent",
        "Target1": colors[0],
        "Target2": colors[1],
        "Background1": colors[2],
        "Background2": colors[3],
        "Target1_RGB": rgb[0],
        "Target2_RGB": rgb[1],
        "Background1_RGB": rgb[2],
        "Background2_RGB": rgb[3],
        "Target1_y": target1_y,
        "Target2_y": target2_y,
        "Target_Height": strip_height,
    }

    return parameters
