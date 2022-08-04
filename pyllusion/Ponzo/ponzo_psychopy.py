import numpy as np

from ..psychopy.psychopy_line import psychopy_line
from .ponzo_parameters import _ponzo_parameters


def _ponzo_psychopy(window, parameters=None, target_only=False, **kwargs):

    # Create white canvas and get drawing context
    if parameters is None:
        parameters = _ponzo_parameters(**kwargs)

    # Draw distractor lines
    if target_only is True:
        for side in ["Left", "Right"]:
            psychopy_line(
                window,
                x1=parameters[side + "_x1"],
                y1=parameters[side + "_y1"],
                x2=parameters[side + "_x2"],
                y2=parameters[side + "_y2"],
                color="black",
                size=5,
            )

    # Draw target lines
    for position in ["Bottom", "Top"]:
        psychopy_line(
            window,
            x1=parameters[position + "_x1"],
            y1=parameters[position + "_y1"],
            x2=parameters[position + "_x2"],
            y2=parameters[position + "_y2"],
            color="red",
            size=5,
        )
