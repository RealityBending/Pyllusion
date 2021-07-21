import numpy as np
import PIL.Image, PIL.ImageDraw, PIL.ImageFilter, PIL.ImageFont, PIL.ImageOps

from ..image import image_line
from .verticalhorizontal_parameters import _verticalhorizontal_parameters


def _verticalhorizontal_image(
    parameters=None, width=800, height=600, background="white", **kwargs
):

    # Create white canvas and get drawing context
    if parameters is None:
        parameters = _verticalhorizontal_parameters(**kwargs)

    # Background
    image = PIL.Image.new("RGB", (width, height), color=background)

    # Lines
    for side in ["Left", "Right"]:
        image = image_line(
            image=image,
            x1=parameters[side + "_x1"],
            y1=parameters[side + "_y1"],
            x2=parameters[side + "_x2"],
            y2=parameters[side + "_y2"],
            length=None,
            rotate=None,
            color="red",
            size=20,
            adjust_width=True,
        )

    return image
