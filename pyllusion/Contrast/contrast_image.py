import numpy as np
import PIL.Image, PIL.ImageDraw, PIL.ImageFilter, PIL.ImageFont, PIL.ImageOps

from ..image import image_rectangle
from .contrast_parameters import _contrast_parameters


def _contrast_image(parameters=None, width=800, height=600, **kwargs):

    # Create white canvas and get drawing context
    if parameters is None:
        parameters = _contrast_parameters(**kwargs)

    # Background upper
    image = PIL.Image.new(
        "RGB", (width, height), color=parameters["Background_Top_RGB"]
    )
    # Background lower
    image = image_rectangle(
        image=image,
        y=-0.5,
        size_height=1,
        size_width=2,
        color=parameters["Background_Bottom_RGB"],
        antialias=False,
    )

    image = image_rectangle(
        image=image,
        y=0.5,
        size_height=0.5,
        size_width=1,
        color=parameters["Rectangle_Top_RGB"],
        antialias=False,
    )
    image = image_rectangle(
        image=image,
        y=-0.5,
        size_height=0.5,
        size_width=1,
        color=parameters["Rectangle_Bottom_RGB"],
        antialias=False,
    )

    return image
