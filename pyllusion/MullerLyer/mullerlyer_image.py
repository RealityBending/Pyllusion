import numpy as np
import PIL.Image
import PIL.ImageDraw
import PIL.ImageFilter
import PIL.ImageFont
import PIL.ImageOps

from ..image import image_line
from .mullerlyer_parameters import _mullerlyer_parameters


def _mullerlyer_image(parameters=None, width=800, height=600, outline=20, background="white", **kwargs):

    # Create white canvas and get drawing context
    if parameters is None:
        parameters = mullerlyer_parameters(**kwargs)

    # Background
    image  = PIL.Image.new('RGB', (width, height), color=background)

    # Distractors lines
    for which in ["TopLeft", "TopRight", "BottomLeft", "BottomRight"]:  #
        for side in ["1", "2"]:
            image = image_line(
                image=image,
                x1=parameters["Distractor_" + which + side + "_x1"],
                y1=parameters["Distractor_" + which + side + "_y1"],
                x2=parameters["Distractor_" + which + side + "_x2"],
                y2=parameters["Distractor_" + which + side + "_y2"],
                color="black",
                size=outline)

    # Target lines (horizontal)
    for position in ["Bottom", "Top"]:
        image = image_line(image=image,
                           x1=parameters[position + "_x1"],
                           y1=parameters[position + "_y1"],
                           x2=parameters[position + "_x2"],
                           y2=parameters[position + "_y2"],
                           color="red",
                           size=outline)

    return image
