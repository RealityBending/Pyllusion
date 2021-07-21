import numpy as np

from ..psychopy.psychopy_line import psychopy_line
from .ponzo_parameters import _ponzo_parameters


def _ponzo_psychopy(window, parameters=None, **kwargs):

    # Create white canvas and get drawing context
    if parameters is None:
        parameters = _ponzo_parameters(**kwargs)

    # Loop lines
    for side in ["Left", "Right"]:
        # Draw distractor lines
        psychopy_line(window,
                      x1=parameters[side + "_x1"],
                      y1=parameters[side + "_y1"],
                      x2=parameters[side + "_x2"],
                      y2=parameters[side + "_y2"],
                      color="black", size=5)

    for position in ["Bottom", "Top"]:
        # Draw target lines
        psychopy_line(window,
                      x1=parameters[position + "_x1"],
                      y1=parameters[position + "_y1"],
                      x2=parameters[position + "_x2"],
                      y2=parameters[position + "_y2"],
                      color="red", size=5)
