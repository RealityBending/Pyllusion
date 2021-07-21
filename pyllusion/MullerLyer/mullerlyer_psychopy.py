import numpy as np

from ..psychopy.psychopy_line import psychopy_line
from .mullerlyer_parameters import _mullerlyer_parameters


def _mullerlyer_psychopy(window, parameters=None, **kwargs):

    # Create white canvas and get drawing context
    if parameters is None:
        parameters = mullerlyer_parameters(**kwargs)

    # Loop lines
    for which in ["TopLeft", "TopRight", "BottomLeft", "BottomRight"]:
        # Draw distractor lines
        for side in ["1", "2"]:
            psychopy_line(window,
                          x1=parameters["Distractor_" + which + side + "_x1"],
                          y1=parameters["Distractor_" + which + side + "_y1"],
                          x2=parameters["Distractor_" + which + side + "_x2"],
                          y2=parameters["Distractor_" + which + side + "_y2"],
                          color="black", size=5)
    
    for position in ["Bottom", "Top"]:
        # Draw target lines
        psychopy_line(window,
                      x1=parameters[position + "_x1"],
                      y1=parameters[position + "_y1"],
                      x2=parameters[position + "_x2"],
                      y2=parameters[position + "_y2"],
                      color="red", size=5)
