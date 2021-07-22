import numpy as np
import PIL.Image, PIL.ImageDraw, PIL.ImageFilter, PIL.ImageFont, PIL.ImageOps

from ..image import image_line, image_rectangle
from .poggendorff_parameters import _poggendorff_parameters


def _poggendorff_image(
    parameters=None, width=800, height=600, background="white", **kwargs
):

    # Create white canvas and get drawing context
    if parameters is None:
        parameters = poggendorff_parameters(**kwargs)

    # Background
    image = PIL.Image.new("RGB", (width, height), color=background)

    # Lines
    for pos in ["Left_", "Right_"]:
        image = image_line(
            image=image,
            x1=parameters[pos + "x1"],
            y1=parameters[pos + "y1"],
            x2=parameters[pos + "x2"],
            y2=parameters[pos + "y2"],
            color="red",
            adjust_height=True,
            size=20,
        )

    image = image_rectangle(
        image=image,
        y=0,
        size_width=parameters["Rectangle_Width"],
        size_height=parameters["Rectangle_Height"],
        color="grey",
        adjust_height=False
    )

    return image
