import numpy as np
import PIL.Image
import PIL.ImageDraw
import PIL.ImageFilter
import PIL.ImageFont
import PIL.ImageOps

from ..psychopy.psychopy_circle import psychopy_circle
from .delboeuf_parameters import _delboeuf_parameters


def _delboeuf_psychopy(window, parameters=None, **kwargs):

    # Create white canvas and get drawing context
    if parameters is None:
        parameters = _delboeuf_parameters(**kwargs)

    # Loop circles
    for side in ["Left", "Right"]:
        # Draw outer circle
        size_outer = parameters["Size_Outer_" + side]
        psychopy_circle(
            window,
            x=parameters["Position_" + side],
            y=0,
            size=size_outer,
            color="white",
            outline_color="black",
            outline=3,
        )

        # Draw inner circle
        size_inner = parameters["Size_Inner_" + side]
        psychopy_circle(
            window,
            x=parameters["Position_" + side],
            y=0,
            size=size_inner,
            color="red",
            outline_color="red",
            outline=0.5,
        )
