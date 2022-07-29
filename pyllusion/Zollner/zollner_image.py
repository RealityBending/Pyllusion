import numpy as np
import PIL.Image
import PIL.ImageDraw
import PIL.ImageFilter
import PIL.ImageFont
import PIL.ImageOps

from ..image import image_line
from .zollner_parameters import _zollner_parameters


def _zollner_image(parameters=None, width=800, height=600, background="white", **kwargs):

    # Create white canvas and get drawing context
    if parameters is None:
        parameters = _zollner_parameters(**kwargs)

    # Background
    image = PIL.Image.new("RGB", (width, height), color=background)

    # Distractors
    for i in range(parameters["Distractors_n"]):
        for pos in ["_Top_", "_Bottom_"]:
            image = image_line(
                image=image,
                x1=parameters["Distractors" + pos + "x1"][i],
                y1=parameters["Distractors" + pos + "y1"][i],
                x2=parameters["Distractors" + pos + "x2"][i],
                y2=parameters["Distractors" + pos + "y2"][i],
                color="black",
                adjust_height=True,
                size=20,
            )

    # Lines
    for pos in ["Top_", "Bottom_"]:
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

    return image
