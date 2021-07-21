import numpy as np
import PIL.Image, PIL.ImageDraw, PIL.ImageFilter, PIL.ImageFont, PIL.ImageOps

from ..image import image_rectangle
from .white_parameters import _white_parameters


def _white_image(parameters=None, width=800, height=600, **kwargs):

    # Create white canvas and get drawing context
    if parameters is None:
        parameters = _white_parameters(**kwargs)

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
