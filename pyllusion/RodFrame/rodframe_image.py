import numpy as np
import PIL.Image, PIL.ImageDraw, PIL.ImageFilter, PIL.ImageFont, PIL.ImageOps

from ..image import image_line, image_rectangle
from ..image.utilities import _coord_line
from .rodframe_parameters import _rodframe_parameters


def _rodframe_image(
    parameters=None, width=800, height=600, outline=20, background="white", **kwargs
):

    # Create white canvas and get drawing context
    if parameters is None:
        parameters = _rodframe_parameters(**kwargs)

    # Background
    image = PIL.Image.new("RGB", (width, height), color=background)

    # Frame
    image = image_rectangle(
        image=image,
        size_width=1,
        size_height=1,
        rotate=parameters["Frame_Angle"],
        color=(0, 0, 0, 0),
        outline=outline,
        adjust_width=True,
    )

    # Rod
    coord, _, _ = _coord_line(x=0, y=0, length=0.8, angle=parameters["Rod_Angle"])
    x1, y1, x2, y2 = coord

    image = image_line(
        image=image,
        x1=x1,
        y1=y1,
        x2=x2,
        y2=y2,
        length=None,
        rotate=None,
        color="red",
        size=outline,
        adjust_width=True,
    )

    return image
