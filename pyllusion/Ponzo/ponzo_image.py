import numpy as np
import PIL.Image, PIL.ImageDraw, PIL.ImageFilter, PIL.ImageFont, PIL.ImageOps

from ..image import image_line
from .ponzo_parameters import _ponzo_parameters


def _ponzo_image(parameters=None, width=800, height=600, outline=20, background="white", **kwargs):

    # Create white canvas and get drawing context
    if parameters is None:
        parameters = _ponzo_parameters(**kwargs)

    # Background
    image = PIL.Image.new("RGB", (width, height), color=background)

    # Distractors lines
    for side in ["Left", "Right"]:
        image = image_line(
            image=image,
            x1=parameters[side + "_x1"],
            y1=parameters[side + "_y1"],
            x2=parameters[side + "_x2"],
            y2=parameters[side + "_y2"],
            color="black",
            size=outline,
        )

    # Target lines (horizontal)
    for position in ["Bottom", "Top"]:
        image = image_line(
            image=image,
            x1=parameters[position + "_x1"],
            y1=parameters[position + "_y1"],
            x2=parameters[position + "_x2"],
            y2=parameters[position + "_y2"],
            color="red",
            size=outline,
        )

    return image
