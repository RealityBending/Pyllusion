import numpy as np
import PIL.Image
import PIL.ImageDraw
import PIL.ImageFilter
import PIL.ImageFont
import PIL.ImageOps

from ..image import image_circle
from .delboeuf_parameters import _delboeuf_parameters


def _delboeuf_image(
    parameters=None, width=800, height=600, outline=10, background="white", **kwargs
):

    # Create white canvas and get drawing context
    if parameters is None:
        parameters = _delboeuf_parameters(**kwargs)

    # Background
    image = PIL.Image.new("RGB", (width, height), color=background)

    # Loop circles
    for side in ["Left", "Right"]:
        # Draw outer circle
        size_outer = parameters["Size_Outer_" + side]
        image = image_circle(
            image=image,
            x=parameters["Position_" + side],
            y=0,
            size=size_outer,
            color=(0, 0, 0, 0),
            outline=outline,
        )

        # Draw inner circle
        size_inner = parameters["Size_Inner_" + side]
        image = image_circle(
            image=image, x=parameters["Position_" + side], y=0, size=size_inner, color="red"
        )

    return image
