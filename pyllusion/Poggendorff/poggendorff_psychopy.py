import numpy as np

from ..psychopy.psychopy_line import psychopy_line
from ..psychopy.psychopy_rectangle import psychopy_rectangle
from .poggendorff_parameters import _poggendorff_parameters


def _poggendorff_psychopy(window, parameters=None, **kwargs):

    # Create white canvas and get drawing context
    if parameters is None:
        parameters = _poggendorff_parameters(**kwargs)

    # Draw lines
    for pos in ["Left_", "Right_"]:
        psychopy_line(window,
                      x1=parameters[pos + "x1"],
                      y1=parameters[pos + "y1"],
                      x2=parameters[pos + "x2"],
                      y2=parameters[pos + "y2"],
                      adjust_height=True, color="red", size=5)
    
    # Draw shaded rectangle
    psychopy_rectangle(window, x=0, y=parameters["Rectangle_y"],
                       size_width=parameters["Rectangle_Width"],
                       size_height=parameters["Rectangle_Height"], color="grey",
                       outline_color="grey")
